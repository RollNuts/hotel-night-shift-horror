"""Quality gate for ReturnRoute trailer-beat PNG evidence.

This validates a short internal proof sequence from the production hotel map.
It is not a public trailer approval gate; it catches blank, static, dark, or
misbound MRQ output before a PR is considered ready.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import os
import re

from check_hotel_mrq_capture_pngs import is_too_dark, metrics_for


MIN_EXPECTED_FRAME_COUNT = 28
MAX_EXPECTED_FRAME_COUNT = 31
MIN_UNIQUE_HASHES = 20
MIN_FRAME_SPAN = 300
MIN_AVERAGE_LUMA_RANGE = 2.0
MIN_AVERAGE_RGB_ENERGY_RANGE = 5.0


def fail(message: str) -> None:
    raise RuntimeError(f"[ReturnRouteTrailerProofGate] {message}")


def frame_number_from_path(path: str) -> int | None:
    match = re.search(r"return_route_trailer_proof_(\d+)\.png$", os.path.basename(path))
    if not match:
        return None
    return int(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capture-dir",
        default=os.path.join("Saved", "MovieRenders", "ReturnRouteTrailerBeat"),
        help="Directory containing ReturnRoute trailer-proof PNGs.",
    )
    args = parser.parse_args()

    paths = sorted(glob.glob(os.path.join(args.capture_dir, "return_route_trailer_proof_*.png")))
    if not (MIN_EXPECTED_FRAME_COUNT <= len(paths) <= MAX_EXPECTED_FRAME_COUNT):
        fail(
            f"Expected {MIN_EXPECTED_FRAME_COUNT}-{MAX_EXPECTED_FRAME_COUNT} ReturnRoute trailer PNGs "
            f"in {args.capture_dir}, found {len(paths)}."
        )

    hashes = []
    all_metrics = []
    frame_numbers = []
    for path in paths:
        with open(path, "rb") as f:
            hashes.append(hashlib.sha256(f.read()).hexdigest())
        frame_number = frame_number_from_path(path)
        if frame_number is not None:
            frame_numbers.append(frame_number)

        metrics = metrics_for(path)
        all_metrics.append(metrics)
        if metrics["width"] != 1280 or metrics["height"] != 720:
            fail(f"{path} has wrong resolution: {metrics['width']}x{metrics['height']}")
        if is_too_dark(metrics):
            fail(
                f"{path} is too dark: average luma {metrics['average_luma']:.1f}, "
                f"average RGB energy {metrics['average_rgb_energy']:.1f}, "
                f"peak RGB energy {metrics['peak_rgb_energy']}, "
                f"visible pixels {metrics['visible_sample_count']}."
            )
        print(
            f"[ReturnRouteTrailerProofGate] {path}: average luma {metrics['average_luma']:.1f}, "
            f"average RGB energy {metrics['average_rgb_energy']:.1f}, peak RGB energy {metrics['peak_rgb_energy']}, "
            f"visible pixels {metrics['visible_sample_count']}/{metrics['sample_count']}"
        )

    unique_hash_count = len(set(hashes))
    if unique_hash_count < MIN_UNIQUE_HASHES:
        fail(
            f"ReturnRoute trailer PNGs are too static: {unique_hash_count}/{len(paths)} unique hashes, "
            f"minimum {MIN_UNIQUE_HASHES}."
        )

    first_hash = hashes[0]
    mid_hash = hashes[len(hashes) // 2]
    last_hash = hashes[-1]
    if len({first_hash, mid_hash, last_hash}) < 3:
        fail("First, middle, and final ReturnRoute trailer frames are not distinct.")

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
            "ReturnRoute trailer PNGs have too little exposure/color variation; "
            f"average luma range {luma_range:.1f}/{MIN_AVERAGE_LUMA_RANGE:.1f}, "
            f"average RGB energy range {rgb_energy_range:.1f}/{MIN_AVERAGE_RGB_ENERGY_RANGE:.1f}."
        )

    print(
        f"[ReturnRouteTrailerProofGate] Passed {len(paths)} ReturnRoute trailer proof PNGs "
        f"with {unique_hash_count} unique frames."
    )


if __name__ == "__main__":
    main()
