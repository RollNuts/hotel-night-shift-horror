"""Quality gate for security-monitor readability proof PNGs."""

from __future__ import annotations

import argparse
import glob
import hashlib
import os
import re

from check_hotel_mrq_capture_pngs import color_luma, is_too_dark, metrics_for, read_png_pixels


MIN_EXPECTED_FRAME_COUNT = 19
MAX_EXPECTED_FRAME_COUNT = 22
MIN_UNIQUE_HASHES = 13
MIN_FRAME_SPAN = 114
MIN_AVERAGE_LUMA_RANGE = 0.5
MIN_AVERAGE_RGB_ENERGY_RANGE = 1.2
SCREEN_ROI = (120, 70, 1240, 690)
MIN_SCREEN_ROI_LUMA_RANGE = 34.0
MIN_SCREEN_ROI_EDGE_SCORE = 1.35
MIN_GREEN_FEED_PIXELS = 850
MIN_WARM_WARNING_PIXELS_ANY_FRAME = 8


def screen_roi_metrics(path: str) -> dict[str, float | int]:
    width, height, pixels = read_png_pixels(path)
    left, top, right, bottom = SCREEN_ROI
    left = max(0, min(width - 1, left))
    right = max(left + 1, min(width, right))
    top = max(0, min(height - 1, top))
    bottom = max(top + 1, min(height, bottom))

    roi_pixels: list[tuple[int, int, int]] = []
    luma_rows: list[list[float]] = []
    for y in range(top, bottom):
        row_lumas: list[float] = []
        row_start = y * width
        for x in range(left, right):
            pixel = pixels[row_start + x]
            roi_pixels.append(pixel)
            row_lumas.append(color_luma(pixel))
        luma_rows.append(row_lumas)

    lumas = [luma for row in luma_rows for luma in row]
    edge_total = 0.0
    edge_samples = 0
    sample_step = 3
    for row_index in range(0, len(luma_rows), sample_step):
        row = luma_rows[row_index]
        previous_row = luma_rows[row_index - sample_step] if row_index >= sample_step else None
        for column_index in range(sample_step, len(row), sample_step):
            edge_total += abs(row[column_index] - row[column_index - sample_step])
            edge_samples += 1
            if previous_row is not None:
                edge_total += abs(row[column_index] - previous_row[column_index])
                edge_samples += 1

    green_feed_pixels = 0
    warm_warning_pixels = 0
    for red, green, blue in roi_pixels:
        if green >= 58 and green > red * 1.18 and green > blue * 1.10:
            green_feed_pixels += 1
        if red >= 118 and green >= 38 and blue <= 96 and red > green * 1.12:
            warm_warning_pixels += 1

    return {
        "width": width,
        "height": height,
        "luma_range": max(lumas) - min(lumas),
        "edge_score": edge_total / max(1, edge_samples),
        "green_feed_pixels": green_feed_pixels,
        "warm_warning_pixels": warm_warning_pixels,
    }


def fail(message: str) -> None:
    raise RuntimeError(f"[SecurityMonitorFeedProofGate] {message}")


def frame_number_from_path(path: str) -> int | None:
    match = re.search(r"security_monitor_feed_readability_proof_(\d+)\.png$", os.path.basename(path))
    if not match:
        return None
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capture-dir",
        default=os.path.join("Saved", "MovieRenders", "SecurityMonitorFeedReadability"),
        help="Directory containing security-monitor proof PNGs.",
    )
    args = parser.parse_args()

    paths = sorted(glob.glob(os.path.join(args.capture_dir, "security_monitor_feed_readability_proof_*.png")))
    if not (MIN_EXPECTED_FRAME_COUNT <= len(paths) <= MAX_EXPECTED_FRAME_COUNT):
        fail(
            f"Expected {MIN_EXPECTED_FRAME_COUNT}-{MAX_EXPECTED_FRAME_COUNT} security-monitor proof PNGs "
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
        roi_metrics = screen_roi_metrics(path)
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
        if roi_metrics["luma_range"] < MIN_SCREEN_ROI_LUMA_RANGE:
            fail(
                f"{path} monitor ROI has too little internal contrast: "
                f"{roi_metrics['luma_range']:.1f}/{MIN_SCREEN_ROI_LUMA_RANGE:.1f}."
            )
        if roi_metrics["edge_score"] < MIN_SCREEN_ROI_EDGE_SCORE:
            fail(
                f"{path} monitor ROI has too little detail edge energy: "
                f"{roi_metrics['edge_score']:.2f}/{MIN_SCREEN_ROI_EDGE_SCORE:.2f}."
            )
        if roi_metrics["green_feed_pixels"] < MIN_GREEN_FEED_PIXELS:
            fail(
                f"{path} monitor ROI has too few green CCTV-feed pixels: "
                f"{roi_metrics['green_feed_pixels']}/{MIN_GREEN_FEED_PIXELS}."
            )
        print(
            f"[SecurityMonitorFeedProofGate] {path}: average luma {metrics['average_luma']:.1f}, "
            f"average RGB energy {metrics['average_rgb_energy']:.1f}, peak RGB energy {metrics['peak_rgb_energy']}, "
            f"visible pixels {metrics['visible_sample_count']}/{metrics['sample_count']}, "
            f"monitor ROI luma range {roi_metrics['luma_range']:.1f}, "
            f"edge score {roi_metrics['edge_score']:.2f}, "
            f"green pixels {roi_metrics['green_feed_pixels']}, "
            f"warm warning pixels {roi_metrics['warm_warning_pixels']}"
        )

    unique_hash_count = len(set(hashes))
    if unique_hash_count < MIN_UNIQUE_HASHES:
        fail(
            f"Security-monitor proof PNGs are too static: {unique_hash_count}/{len(paths)} unique hashes, "
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
            "Security-monitor proof PNGs have too little exposure/color variation; "
            f"average luma range {luma_range:.1f}/{MIN_AVERAGE_LUMA_RANGE:.1f}, "
            f"average RGB energy range {rgb_energy_range:.1f}/{MIN_AVERAGE_RGB_ENERGY_RANGE:.1f}."
        )

    max_warm_warning_pixels = max(int(metrics["warm_warning_pixels"]) for metrics in all_roi_metrics)
    if max_warm_warning_pixels < MIN_WARM_WARNING_PIXELS_ANY_FRAME:
        fail(
            "Security-monitor proof PNGs do not show enough warm contradiction/warning pixels in any frame; "
            f"max {max_warm_warning_pixels}/{MIN_WARM_WARNING_PIXELS_ANY_FRAME}."
        )

    print(
        f"[SecurityMonitorFeedProofGate] Passed {len(paths)} security-monitor proof PNGs "
        f"with {unique_hash_count} unique frames."
    )


if __name__ == "__main__":
    main()
