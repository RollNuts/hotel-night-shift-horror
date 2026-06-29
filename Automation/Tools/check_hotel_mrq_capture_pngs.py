"""Quality gate for MRQ hotel spine PNG evidence.

This deliberately uses only the Python standard library so the check can run on
a clean machine without paid tools or package installs.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import os
import struct
import zlib


EXPECTED_CAPTURE_COUNT = 8
MIN_AVERAGE_LUMA = 12.0
MIN_AVERAGE_LUMA_RANGE = 8.0
MIN_AVERAGE_RGB_ENERGY = 36.0
MIN_AVERAGE_RGB_ENERGY_RANGE = 24.0
MIN_PEAK_RGB_ENERGY = 60
VISIBLE_SAMPLE_MIN_LUMA = 12.0
MIN_VISIBLE_SAMPLE_COUNT = 5


def fail(message: str) -> None:
    raise RuntimeError(f"[HotelMRQCaptureGate] {message}")


def paeth_predictor(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_png_pixels(path: str) -> tuple[int, int, list[tuple[int, int, int]]]:
    with open(path, "rb") as f:
        data = f.read()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        fail(f"Not a PNG file: {path}")

    offset = 8
    width = height = bit_depth = color_type = None
    compressed = bytearray()
    while offset < len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_data = data[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack(
                ">IIBBBBB", chunk_data
            )
            if bit_depth != 8 or color_type not in (2, 6) or compression != 0 or filter_method != 0 or interlace != 0:
                fail(f"Unsupported PNG format for {path}: bit_depth={bit_depth} color_type={color_type} interlace={interlace}")
        elif chunk_type == b"IDAT":
            compressed.extend(chunk_data)
        elif chunk_type == b"IEND":
            break

    if width is None or height is None:
        fail(f"Missing IHDR in {path}")

    channels = 4 if color_type == 6 else 3
    stride = width * channels
    raw = zlib.decompress(bytes(compressed))
    pixels: list[tuple[int, int, int]] = []
    previous = [0] * stride
    cursor = 0
    for _ in range(height):
        filter_type = raw[cursor]
        cursor += 1
        scanline = list(raw[cursor : cursor + stride])
        cursor += stride
        recon = [0] * stride
        for index, value in enumerate(scanline):
            left = recon[index - channels] if index >= channels else 0
            up = previous[index]
            up_left = previous[index - channels] if index >= channels else 0
            if filter_type == 0:
                recon[index] = value
            elif filter_type == 1:
                recon[index] = (value + left) & 0xFF
            elif filter_type == 2:
                recon[index] = (value + up) & 0xFF
            elif filter_type == 3:
                recon[index] = (value + ((left + up) // 2)) & 0xFF
            elif filter_type == 4:
                recon[index] = (value + paeth_predictor(left, up, up_left)) & 0xFF
            else:
                fail(f"Unsupported PNG filter {filter_type} in {path}")
        previous = recon
        for x in range(width):
            base = x * channels
            pixels.append((recon[base], recon[base + 1], recon[base + 2]))
    return width, height, pixels


def color_luma(pixel: tuple[int, int, int]) -> float:
    r, g, b = pixel
    return (0.2126 * r) + (0.7152 * g) + (0.0722 * b)


def metrics_for(path: str) -> dict[str, float | int]:
    width, height, pixels = read_png_pixels(path)
    energies = [r + g + b for r, g, b in pixels]
    lumas = [color_luma(pixel) for pixel in pixels]
    return {
        "width": width,
        "height": height,
        "average_luma": sum(lumas) / len(lumas),
        "average_rgb_energy": sum(energies) / len(energies),
        "peak_rgb_energy": max(energies),
        "visible_sample_count": sum(1 for luma in lumas if luma >= VISIBLE_SAMPLE_MIN_LUMA),
        "sample_count": len(pixels),
    }


def is_too_dark(metrics: dict[str, float | int]) -> bool:
    return (
        metrics["average_luma"] < MIN_AVERAGE_LUMA
        or metrics["average_rgb_energy"] < MIN_AVERAGE_RGB_ENERGY
        or metrics["peak_rgb_energy"] < MIN_PEAK_RGB_ENERGY
        or metrics["visible_sample_count"] < MIN_VISIBLE_SAMPLE_COUNT
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capture-dir",
        default=os.path.join("Saved", "MovieRenders", "HotelSpineSlice"),
        help="Directory containing MRQ hotel evidence PNGs.",
    )
    args = parser.parse_args()

    paths = sorted(glob.glob(os.path.join(args.capture_dir, "hotel_spine_evidence_*.png")))
    if len(paths) != EXPECTED_CAPTURE_COUNT:
        fail(f"Expected exactly {EXPECTED_CAPTURE_COUNT} MRQ evidence PNGs in {args.capture_dir}, found {len(paths)}.")

    hashes = []
    all_metrics = []
    for path in paths:
        with open(path, "rb") as f:
            hashes.append(hashlib.sha256(f.read()).hexdigest())
        metrics = metrics_for(path)
        all_metrics.append(metrics)
        if metrics["width"] != 1280 or metrics["height"] != 720:
            fail(f"{path} has wrong resolution: {metrics['width']}x{metrics['height']}")
        if is_too_dark(metrics):
            fail(
                f"{path} is too dark: average luma {metrics['average_luma']:.1f}/{MIN_AVERAGE_LUMA:.1f}, "
                f"average RGB energy {metrics['average_rgb_energy']:.1f}/{MIN_AVERAGE_RGB_ENERGY:.1f}, "
                f"peak RGB energy {metrics['peak_rgb_energy']}/{MIN_PEAK_RGB_ENERGY}, "
                f"visible pixels {metrics['visible_sample_count']}/{MIN_VISIBLE_SAMPLE_COUNT}."
            )
        print(
            f"[HotelMRQCaptureGate] {path}: average luma {metrics['average_luma']:.1f}, "
            f"average RGB energy {metrics['average_rgb_energy']:.1f}, peak RGB energy {metrics['peak_rgb_energy']}, "
            f"visible pixels {metrics['visible_sample_count']}/{metrics['sample_count']}"
        )

    if len(set(hashes)) < len(paths):
        fail("MRQ evidence PNGs are not unique; this usually means the capture path ignored the camera cuts.")

    luma_values = [float(metrics["average_luma"]) for metrics in all_metrics]
    rgb_energy_values = [float(metrics["average_rgb_energy"]) for metrics in all_metrics]
    luma_range = max(luma_values) - min(luma_values)
    rgb_energy_range = max(rgb_energy_values) - min(rgb_energy_values)
    if luma_range < MIN_AVERAGE_LUMA_RANGE or rgb_energy_range < MIN_AVERAGE_RGB_ENERGY_RANGE:
        fail(
            "MRQ evidence PNGs have too little shot-to-shot exposure variation; "
            f"average luma range {luma_range:.1f}/{MIN_AVERAGE_LUMA_RANGE:.1f}, "
            f"average RGB energy range {rgb_energy_range:.1f}/{MIN_AVERAGE_RGB_ENERGY_RANGE:.1f}. "
            "This usually means the camera cuts did not bind to the expected capture actors."
        )

    print(f"[HotelMRQCaptureGate] Passed {len(paths)} hotel MRQ evidence PNGs.")


if __name__ == "__main__":
    main()
