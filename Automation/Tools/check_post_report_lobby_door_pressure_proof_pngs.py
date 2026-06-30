"""Quality gate for post-report lobby-door pressure proof PNGs."""

from __future__ import annotations

import argparse
import glob
import hashlib
import os
import re

from check_hotel_mrq_capture_pngs import color_luma, is_too_dark, metrics_for, read_png_pixels


MIN_EXPECTED_FRAME_COUNT = 23
MAX_EXPECTED_FRAME_COUNT = 26
MIN_UNIQUE_HASHES = 17
MIN_FRAME_SPAN = 138
MIN_AVERAGE_LUMA_RANGE = 1.0
MIN_AVERAGE_RGB_ENERGY_RANGE = 2.4
MIN_DOOR_ROI_LUMA_RANGE = 64.0
MIN_DOOR_ROI_EDGE_AVERAGE = 0.75
MAX_DOOR_ROI_DARK_RATIO = 0.86


def fail(message: str) -> None:
    raise RuntimeError(f"[PostReportLobbyDoorPressureProofGate] {message}")


def frame_number_from_path(path: str) -> int | None:
    match = re.search(r"post_report_lobby_door_pressure_proof_(\d+)\.png$", os.path.basename(path))
    if not match:
        return None
    return int(match.group(1))


def door_roi_metrics(path: str) -> dict[str, float | int]:
    width, height, pixels = read_png_pixels(path)
    # Track the framed lobby door surface, not the right-side hallway context.
    x0 = int(width * 0.08)
    x1 = int(width * 0.76)
    y0 = int(height * 0.12)
    y1 = int(height * 0.92)
    lumas: list[float] = []
    edge_total = 0.0
    edge_count = 0
    dark_count = 0

    for y in range(y0, y1):
        for x in range(x0, x1):
            luma = color_luma(pixels[y * width + x])
            lumas.append(luma)
            if luma < 9.0:
                dark_count += 1
            if x + 1 < x1:
                edge_total += abs(luma - color_luma(pixels[y * width + x + 1]))
                edge_count += 1
            if y + 1 < y1:
                edge_total += abs(luma - color_luma(pixels[(y + 1) * width + x]))
                edge_count += 1

    return {
        "luma_range": max(lumas) - min(lumas),
        "edge_average": edge_total / max(1, edge_count),
        "dark_ratio": dark_count / max(1, len(lumas)),
        "sample_count": len(lumas),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capture-dir",
        default=os.path.join("Saved", "MovieRenders", "PostReportLobbyDoorPressure"),
        help="Directory containing post-report lobby-door pressure proof PNGs.",
    )
    args = parser.parse_args()

    paths = sorted(glob.glob(os.path.join(args.capture_dir, "post_report_lobby_door_pressure_proof_*.png")))
    if not (MIN_EXPECTED_FRAME_COUNT <= len(paths) <= MAX_EXPECTED_FRAME_COUNT):
        fail(
            f"Expected {MIN_EXPECTED_FRAME_COUNT}-{MAX_EXPECTED_FRAME_COUNT} lobby-door proof PNGs "
            f"in {args.capture_dir}, found {len(paths)}."
        )

    hashes = []
    all_metrics = []
    all_roi_metrics = []
    frame_numbers = []
    for path in paths:
        with open(path, "rb") as f:
            hashes.append(hashlib.sha256(f.read()).hexdigest())
        frame_number = frame_number_from_path(path)
        if frame_number is not None:
            frame_numbers.append(frame_number)

        metrics = metrics_for(path)
        roi_metrics = door_roi_metrics(path)
        all_metrics.append(metrics)
        all_roi_metrics.append(roi_metrics)
        if metrics["width"] != 1280 or metrics["height"] != 720:
            fail(f"{path} has wrong resolution: {metrics['width']}x{metrics['height']}")
        if is_too_dark(metrics):
            fail(
                f"{path} is too dark: average luma {metrics['average_luma']:.1f}, "
                f"average RGB energy {metrics['average_rgb_energy']:.1f}, "
                f"peak RGB energy {metrics['peak_rgb_energy']}, "
                f"visible pixels {metrics['visible_sample_count']}."
            )
        if roi_metrics["dark_ratio"] > MAX_DOOR_ROI_DARK_RATIO:
            fail(f"{path} lobby-door ROI is mostly black: dark ratio {roi_metrics['dark_ratio']:.2f}.")
        print(
            f"[PostReportLobbyDoorPressureProofGate] {path}: average luma {metrics['average_luma']:.1f}, "
            f"average RGB energy {metrics['average_rgb_energy']:.1f}, "
            f"door ROI luma range {roi_metrics['luma_range']:.1f}, "
            f"edge {roi_metrics['edge_average']:.2f}, dark ratio {roi_metrics['dark_ratio']:.2f}"
        )

    unique_hash_count = len(set(hashes))
    if unique_hash_count < MIN_UNIQUE_HASHES:
        fail(
            f"Post-report lobby-door proof PNGs are too static: {unique_hash_count}/{len(paths)} unique hashes, "
            f"minimum {MIN_UNIQUE_HASHES}."
        )

    if frame_numbers:
        if min(frame_numbers) != 0:
            fail(f"First rendered frame should be 0, got {min(frame_numbers)}.")
        frame_span = max(frame_numbers) - min(frame_numbers)
        if frame_span < MIN_FRAME_SPAN:
            fail(f"Rendered frame span is too short: {frame_span}/{MIN_FRAME_SPAN}.")

    luma_values = [float(metrics["average_luma"]) for metrics in all_metrics]
    rgb_energy_values = [float(metrics["average_rgb_energy"]) for metrics in all_metrics]
    luma_range = max(luma_values) - min(luma_values)
    rgb_energy_range = max(rgb_energy_values) - min(rgb_energy_values)
    if luma_range < MIN_AVERAGE_LUMA_RANGE or rgb_energy_range < MIN_AVERAGE_RGB_ENERGY_RANGE:
        fail(
            "Post-report lobby-door proof PNGs have too little exposure/color variation; "
            f"average luma range {luma_range:.1f}/{MIN_AVERAGE_LUMA_RANGE:.1f}, "
            f"average RGB energy range {rgb_energy_range:.1f}/{MIN_AVERAGE_RGB_ENERGY_RANGE:.1f}."
        )

    roi_luma_range = max(float(metrics["luma_range"]) for metrics in all_roi_metrics)
    roi_edge_average = max(float(metrics["edge_average"]) for metrics in all_roi_metrics)
    if roi_luma_range < MIN_DOOR_ROI_LUMA_RANGE or roi_edge_average < MIN_DOOR_ROI_EDGE_AVERAGE:
        fail(
            "Lobby-door ROI lacks enough visible surface detail; "
            f"luma range {roi_luma_range:.1f}/{MIN_DOOR_ROI_LUMA_RANGE:.1f}, "
            f"edge average {roi_edge_average:.2f}/{MIN_DOOR_ROI_EDGE_AVERAGE:.2f}."
        )

    print(
        f"[PostReportLobbyDoorPressureProofGate] Passed {len(paths)} post-report lobby-door pressure proof PNGs "
        f"with {unique_hash_count} unique frames."
    )


if __name__ == "__main__":
    main()
