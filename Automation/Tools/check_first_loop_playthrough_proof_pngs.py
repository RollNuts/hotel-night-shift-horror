"""Quality gate for first-loop playthrough proof PNGs."""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from check_hotel_mrq_capture_pngs import color_luma, is_too_dark, metrics_for, read_png_pixels


MIN_EXPECTED_FRAME_COUNT = 47
MAX_EXPECTED_FRAME_COUNT = 50
MIN_UNIQUE_HASHES = 40
MIN_FRAME_SPAN = 564
MIN_AVERAGE_LUMA_RANGE = 8.0
MIN_AVERAGE_RGB_ENERGY_RANGE = 24.0
MIN_FRONT_DESK_WARM_PIXELS = 5200
MIN_FRONT_DESK_GREEN_PIXELS = 1600
MAX_FRONT_DESK_BLOWN_PIXELS = 85000
MIN_MONITOR_GREEN_PIXELS = 38000
MIN_MONITOR_WARM_PIXELS = 18
MIN_MONITOR_EDGE_SCORE = 2.0
MIN_ROOM203_EDGE_SCORE = 1.35
MIN_ROOM203_WARM_PIXELS = 950
MIN_REPORT_TEXT_PIXELS = 1300
MIN_VIDEO_DURATION_SECONDS = 23.8
MAX_VIDEO_DURATION_SECONDS = 24.2
MIN_VIDEO_OUTPUT_FRAMES = 500


SHOT_RANGES = {
    "front_desk": (0, 96),
    "monitor": (96, 144),
    "room203": (248, 316),
    "report": (384, 448),
    "post_report_monitor": (448, 512),
    "post_report_log": (512, 576),
}


def fail(message: str) -> None:
    raise RuntimeError(f"[FirstLoopPlaythroughProofGate] {message}")


def require_tool(tool_name: str) -> str:
    tool_path = shutil.which(tool_name)
    if not tool_path:
        fail(f"Missing required tool `{tool_name}` on PATH.")
    return tool_path


def frame_number_from_path(path: str) -> int | None:
    match = re.search(r"first_loop_playthrough_proof_(\d+)\.png$", os.path.basename(path))
    if not match:
        return None
    return int(match.group(1))


def shot_for_frame(frame_number: int | None) -> str | None:
    if frame_number is None:
        return None
    for shot_name, (start, end) in SHOT_RANGES.items():
        if start <= frame_number < end:
            return shot_name
    return None


def content_metrics_for(path: str) -> dict[str, float | int]:
    width, height, pixels = read_png_pixels(path)
    luma_rows: list[list[float]] = []
    green_pixels = 0
    warm_pixels = 0
    report_text_pixels = 0
    blown_pixels = 0
    for y in range(height):
        row: list[float] = []
        row_start = y * width
        for x in range(width):
            red, green, blue = pixels[row_start + x]
            row.append(color_luma((red, green, blue)))
            if green >= 58 and green > red * 1.16 and green > blue * 1.08:
                green_pixels += 1
            if red >= 112 and green >= 45 and blue <= 105 and red > green * 1.08:
                warm_pixels += 1
            if red >= 128 and green >= 118 and blue >= 62 and red + green > blue * 2.8:
                report_text_pixels += 1
            if red >= 235 and green >= 235 and blue >= 235:
                blown_pixels += 1
        luma_rows.append(row)

    edge_total = 0.0
    edge_samples = 0
    sample_step = 4
    for row_index in range(0, len(luma_rows), sample_step):
        row = luma_rows[row_index]
        previous_row = luma_rows[row_index - sample_step] if row_index >= sample_step else None
        for column_index in range(sample_step, len(row), sample_step):
            edge_total += abs(row[column_index] - row[column_index - sample_step])
            edge_samples += 1
            if previous_row is not None:
                edge_total += abs(row[column_index] - previous_row[column_index])
                edge_samples += 1

    return {
        "green_pixels": green_pixels,
        "warm_pixels": warm_pixels,
        "report_text_pixels": report_text_pixels,
        "blown_pixels": blown_pixels,
        "edge_score": edge_total / max(1, edge_samples),
    }


def escaped_concat_path(path: str) -> str:
    return str(Path(path).resolve()).replace("'", "'\\''")


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, capture_output=True)


def write_video_concat_list(paths: list[str], source_fps: float) -> Path:
    frame_duration = 1.0 / source_fps
    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix="first_loop_playthrough_",
        suffix=".ffconcat",
        delete=False,
    )
    with temp_file:
        for path in paths:
            temp_file.write(f"file '{escaped_concat_path(path)}'\n")
            temp_file.write(f"duration {frame_duration:.6f}\n")
        temp_file.write(f"file '{escaped_concat_path(paths[-1])}'\n")
    return Path(temp_file.name)


def video_probe(ffprobe_path: str, output_path: str) -> dict:
    result = run_command(
        [
            ffprobe_path,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,nb_frames,avg_frame_rate:format=duration",
            "-of",
            "json",
            output_path,
        ]
    )
    return json.loads(result.stdout)


def video_duration(probe: dict) -> float:
    try:
        return float(probe["format"]["duration"])
    except (KeyError, TypeError, ValueError):
        fail("ffprobe did not report a valid video duration.")


def verify_video_probe(probe: dict) -> None:
    streams = probe.get("streams") or []
    if not streams:
        fail("ffprobe found no video stream.")
    stream = streams[0]
    width = int(stream.get("width") or 0)
    height = int(stream.get("height") or 0)
    if width != 1280 or height != 720:
        fail(f"Encoded video has wrong resolution: {width}x{height}.")

    duration = video_duration(probe)
    if not (MIN_VIDEO_DURATION_SECONDS <= duration <= MAX_VIDEO_DURATION_SECONDS):
        fail(
            f"Encoded video duration is outside the proof window: "
            f"{duration:.2f}s, expected {MIN_VIDEO_DURATION_SECONDS:.1f}-{MAX_VIDEO_DURATION_SECONDS:.1f}s."
        )

    frame_count = stream.get("nb_frames")
    if frame_count is not None and str(frame_count).isdigit() and int(frame_count) < MIN_VIDEO_OUTPUT_FRAMES:
        fail(f"Encoded video has too few output frames: {frame_count}.")


def encode_review_video(paths: list[str], output_path: str, source_fps: float, output_fps: float, crf: int) -> None:
    if source_fps <= 0.0:
        fail("--video-source-fps must be positive.")
    if output_fps <= 0.0:
        fail("--video-output-fps must be positive.")
    if not (0 <= crf <= 51):
        fail("--video-crf must be between 0 and 51.")

    ffmpeg_path = require_tool("ffmpeg")
    ffprobe_path = require_tool("ffprobe")
    output_parent = os.path.dirname(output_path)
    if output_parent:
        os.makedirs(output_parent, exist_ok=True)

    concat_list = write_video_concat_list(paths, source_fps)
    duration_seconds = len(paths) / source_fps
    try:
        run_command(
            [
                ffmpeg_path,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list),
                "-t",
                f"{duration_seconds:.6f}",
                "-vf",
                f"fps={output_fps:g},scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p",
                "-c:v",
                "libx264",
                "-preset",
                "slow",
                "-crf",
                str(crf),
                "-movflags",
                "+faststart",
                "-an",
                output_path,
            ]
        )
    finally:
        try:
            concat_list.unlink()
        except OSError:
            pass

    probe = video_probe(ffprobe_path, output_path)
    verify_video_probe(probe)
    print(
        f"[FirstLoopPlaythroughProofGate] Encoded review video {output_path} "
        f"from {len(paths)} PNGs, duration {video_duration(probe):.2f}s."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--capture-dir",
        default=os.path.join("Saved", "MovieRenders", "FirstLoopPlaythrough"),
        help="Directory containing first-loop playthrough proof PNGs.",
    )
    parser.add_argument(
        "--encode-video",
        action="store_true",
        help="Also encode a local ignored MP4 from the validated PNGs using ffmpeg/ffprobe.",
    )
    parser.add_argument(
        "--video-output",
        default=os.path.join("Saved", "MovieRenders", "FirstLoopPlaythrough", "first_loop_playthrough_proof.mp4"),
        help="Output MP4 path used with --encode-video.",
    )
    parser.add_argument("--video-source-fps", type=float, default=2.0)
    parser.add_argument("--video-output-fps", type=float, default=24.0)
    parser.add_argument("--video-crf", type=int, default=18)
    args = parser.parse_args()

    paths = sorted(glob.glob(os.path.join(args.capture_dir, "first_loop_playthrough_proof_*.png")))
    if not (MIN_EXPECTED_FRAME_COUNT <= len(paths) <= MAX_EXPECTED_FRAME_COUNT):
        fail(
            f"Expected {MIN_EXPECTED_FRAME_COUNT}-{MAX_EXPECTED_FRAME_COUNT} first-loop proof PNGs "
            f"in {args.capture_dir}, found {len(paths)}."
        )

    hashes = []
    all_metrics = []
    shot_content_metrics: dict[str, list[dict[str, float | int]]] = {shot_name: [] for shot_name in SHOT_RANGES}
    frame_numbers = []
    for path in paths:
        with open(path, "rb") as f:
            hashes.append(hashlib.sha256(f.read()).hexdigest())
        frame_number = frame_number_from_path(path)
        if frame_number is not None:
            frame_numbers.append(frame_number)
        shot_name = shot_for_frame(frame_number)

        metrics = metrics_for(path)
        content_metrics = content_metrics_for(path)
        all_metrics.append(metrics)
        if shot_name:
            shot_content_metrics[shot_name].append(content_metrics)
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
            f"[FirstLoopPlaythroughProofGate] {path}: average luma {metrics['average_luma']:.1f}, "
            f"average RGB energy {metrics['average_rgb_energy']:.1f}, peak RGB energy {metrics['peak_rgb_energy']}, "
            f"visible pixels {metrics['visible_sample_count']}/{metrics['sample_count']}, "
            f"green pixels {content_metrics['green_pixels']}, warm pixels {content_metrics['warm_pixels']}, "
            f"report text pixels {content_metrics['report_text_pixels']}, blown pixels {content_metrics['blown_pixels']}, "
            f"edge score {content_metrics['edge_score']:.2f}"
        )

    unique_hash_count = len(set(hashes))
    if unique_hash_count < MIN_UNIQUE_HASHES:
        fail(
            f"First-loop proof PNGs are too static: {unique_hash_count}/{len(paths)} unique hashes, "
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
            "First-loop proof PNGs have too little shot-to-shot exposure/color variation; "
            f"average luma range {luma_range:.1f}/{MIN_AVERAGE_LUMA_RANGE:.1f}, "
            f"average RGB energy range {rgb_energy_range:.1f}/{MIN_AVERAGE_RGB_ENERGY_RANGE:.1f}."
        )

    front_desk_metrics = shot_content_metrics["front_desk"]
    if not front_desk_metrics:
        fail("Missing first-loop front desk proof frames.")
    if max(int(metrics["warm_pixels"]) for metrics in front_desk_metrics) < MIN_FRONT_DESK_WARM_PIXELS:
        fail("Front desk opener has too few warm hotel-work pixels to read as a night reception desk.")
    if max(int(metrics["green_pixels"]) for metrics in front_desk_metrics) < MIN_FRONT_DESK_GREEN_PIXELS:
        fail("Front desk opener has too few monitor/CCTV green pixels to connect phone work to surveillance.")
    if min(int(metrics["blown_pixels"]) for metrics in front_desk_metrics) > MAX_FRONT_DESK_BLOWN_PIXELS:
        fail("Front desk opener is overexposed in every sampled frame; lamp/desk glare is overpowering the work scene.")

    monitor_metrics = shot_content_metrics["monitor"] + shot_content_metrics["post_report_monitor"]
    if not monitor_metrics:
        fail("Missing first-loop monitor proof frames.")
    if max(int(metrics["green_pixels"]) for metrics in monitor_metrics) < MIN_MONITOR_GREEN_PIXELS:
        fail("Monitor proof shots have too few green CCTV pixels to read as surveillance work.")
    if max(int(metrics["warm_pixels"]) for metrics in monitor_metrics) < MIN_MONITOR_WARM_PIXELS:
        fail("Monitor proof shots never expose the warm Room 203 warning content.")
    if max(float(metrics["edge_score"]) for metrics in monitor_metrics) < MIN_MONITOR_EDGE_SCORE:
        fail("Monitor proof shots have too little edge detail and read as abstract glow.")

    room203_metrics = shot_content_metrics["room203"]
    if not room203_metrics:
        fail("Missing first-loop Room 203 proof frames.")
    if max(float(metrics["edge_score"]) for metrics in room203_metrics) < MIN_ROOM203_EDGE_SCORE:
        fail("Room 203 proof shot has too little visible door/wall detail.")
    if max(int(metrics["warm_pixels"]) for metrics in room203_metrics) < MIN_ROOM203_WARM_PIXELS:
        fail("Room 203 proof shot has too few warm notice/door/light pixels to read as a refusal beat.")

    report_metrics = shot_content_metrics["report"] + shot_content_metrics["post_report_log"]
    if not report_metrics:
        fail("Missing first-loop report proof frames.")
    if max(int(metrics["report_text_pixels"]) for metrics in report_metrics) < MIN_REPORT_TEXT_PIXELS:
        fail("Report/log proof shots have too few readable paper/text pixels.")

    print(
        f"[FirstLoopPlaythroughProofGate] Passed {len(paths)} first-loop proof PNGs "
        f"with {unique_hash_count} unique frames."
    )
    if args.encode_video:
        encode_review_video(paths, args.video_output, args.video_source_fps, args.video_output_fps, args.video_crf)


if __name__ == "__main__":
    main()
