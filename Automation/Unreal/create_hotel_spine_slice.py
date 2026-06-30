"""Create the first production-intent hotel spine level.

This script uses only project-authored/generated assets and Unreal Engine
stock primitives. It is intentionally a production-context slice, not a
small-room test map.
"""

from __future__ import annotations

import math
import pathlib
import struct
import wave
import zlib

import unreal


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE_AUDIO_DIR = PROJECT_ROOT / "SourceAssets" / "AudioGenerated"
SOURCE_MESH_DIR = PROJECT_ROOT / "SourceAssets" / "GeometryGenerated"
SOURCE_TEXTURE_DIR = PROJECT_ROOT / "SourceAssets" / "TextureGenerated"
MAP_PATH = "/Game/Hotel/Maps/L_HotelNightShift_Slice"
UPDATED_SOURCE_MESHES: set[str] = set()
UPDATED_SOURCE_TEXTURES: set[str] = set()
ALWAYS_REIMPORT_TEXTURES = {
    "TX_Hotel_ReportLogFiledPaper_v0",
    "TX_Hotel_ReturnRouteSlipPaper_v0",
    "TX_Hotel_RoomDoorPaint_v0",
    "TX_Hotel_SecurityMonitorFeed_v0",
    "TX_Hotel_LobbyDoorSmudgedGlass_v0",
    "TX_Hotel_FrontDeskHeroBoard_v0",
}


def log(message: str) -> None:
    unreal.log(f"[HotelSpineSlice] {message}")


def ensure_dirs() -> None:
    for path in [
        "/Game/Hotel",
        "/Game/Hotel/Maps",
        "/Game/Hotel/Materials",
        "/Game/Hotel/Meshes",
        "/Game/Hotel/Audio",
        "/Game/Hotel/Textures",
        "/Game/Hotel/Blueprints",
        "/Game/Hotel/Data",
        "/Game/Hotel/UI",
        "/Game/Hotel/VFX",
    ]:
        unreal.EditorAssetLibrary.make_directory(path)
    SOURCE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_MESH_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_TEXTURE_DIR.mkdir(parents=True, exist_ok=True)


def write_wav(path: pathlib.Path, seconds: float, sample_func, sample_rate: int = 44100) -> None:
    frame_count = int(seconds * sample_rate)
    with wave.open(str(path), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for index in range(frame_count):
            t = index / sample_rate
            value = max(-1.0, min(1.0, sample_func(t)))
            wav.writeframesraw(struct.pack("<h", int(value * 32767)))


def write_png_rgb(path: pathlib.Path, width: int, height: int, pixels: list[tuple[int, int, int]]) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    raw = bytearray()
    for row in range(height):
        raw.append(0)
        start = row * width
        for red, green, blue in pixels[start : start + width]:
            raw.extend((red, green, blue))

    payload = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)),
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)),
            chunk(b"IEND", b""),
        ]
    )
    path.write_bytes(payload)


def generate_source_textures() -> dict[str, pathlib.Path]:
    UPDATED_SOURCE_TEXTURES.clear()

    def wallpaper_pixel(x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
        u = x / max(1, width - 1)
        v = y / max(1, height - 1)
        noise = (
            math.sin(x * 0.113 + y * 0.071)
            + math.sin(x * 0.037 + y * 0.191 + 1.7)
            + math.sin(x * 0.251 - y * 0.043 + 4.1)
        ) / 3.0
        stripe = 0.5 + 0.5 * math.sin((u * 8.0 + 0.035 * math.sin(v * 18.0)) * 2.0 * math.pi)
        seam = 0.0
        for seam_u in (0.18, 0.39, 0.61, 0.83):
            seam += max(0.0, 1.0 - abs(u - seam_u) / 0.006)
        stain_a = max(0.0, 1.0 - (((u - 0.72) / 0.21) ** 2 + ((v - 0.34) / 0.27) ** 2))
        stain_b = max(0.0, 1.0 - (((u - 0.30) / 0.17) ** 2 + ((v - 0.72) / 0.16) ** 2))
        drip = max(0.0, 1.0 - abs(u - (0.58 + 0.018 * math.sin(v * 16.0))) / 0.008) * max(0.0, v - 0.16)
        scratch = 0.0
        for offset in (0.12, 0.28, 0.46, 0.67, 0.78):
            scratch += max(0.0, 1.0 - abs((u + 0.10 * v) - offset) / 0.003) * (0.25 + 0.75 * max(0.0, math.sin(v * 21.0 + offset * 8.0)))

        red = 103 + 18 * stripe + 12 * noise
        green = 91 + 14 * stripe + 10 * noise
        blue = 69 + 10 * stripe + 8 * noise
        darken = 32 * stain_a + 22 * stain_b + 24 * drip + 18 * seam
        brighten = 18 * scratch
        return (
            max(0, min(255, int(red - darken + brighten))),
            max(0, min(255, int(green - darken * 0.88 + brighten * 0.78))),
            max(0, min(255, int(blue - darken * 0.70 + brighten * 0.45))),
        )

    def return_slip_pixel(x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
        u = x / max(1, width - 1)
        v = y / max(1, height - 1)
        fiber = (
            math.sin(x * 0.211 + y * 0.031)
            + math.sin(x * 0.047 - y * 0.173 + 1.8)
            + math.sin(x * 0.379 + y * 0.091 + 3.4)
        ) / 3.0
        vertical_fold = max(0.0, 1.0 - abs(u - 0.63) / 0.018)
        lower_thumb = max(0.0, 1.0 - (((u - 0.36) / 0.22) ** 2 + ((v - 0.72) / 0.16) ** 2))
        damp_corner = max(0.0, 1.0 - (((u - 0.82) / 0.18) ** 2 + ((v - 0.20) / 0.24) ** 2))
        edge_shadow = max(0.0, 1.0 - min(u, 1.0 - u, v, 1.0 - v) / 0.055)
        crease = max(0.0, 1.0 - abs((u + v * 0.13) - 0.46) / 0.010) * (0.35 + 0.65 * v)
        pin_prick = 0.0
        for px, py in ((0.18, 0.16), (0.24, 0.18), (0.77, 0.84)):
            pin_prick += max(0.0, 1.0 - (((u - px) / 0.018) ** 2 + ((v - py) / 0.014) ** 2))

        red = 146 + 5 * fiber
        green = 128 + 4 * fiber
        blue = 94 + 3 * fiber
        darken = 11 * edge_shadow + 10 * damp_corner + 7 * lower_thumb + 6 * vertical_fold + 5 * crease + 10 * pin_prick
        warm = 4 * (0.5 + 0.5 * math.sin((u * 3.0 + v * 1.7) * math.pi))
        return (
            max(0, min(255, int(red + warm - darken))),
            max(0, min(255, int(green + warm * 0.55 - darken * 0.82))),
            max(0, min(255, int(blue + warm * 0.25 - darken * 0.64))),
        )

    def report_log_filed_paper_pixel(x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
        u = x / max(1, width - 1)
        v = y / max(1, height - 1)
        fiber = (
            math.sin(x * 0.157 + y * 0.049)
            + math.sin(x * 0.043 - y * 0.193 + 2.1)
            + math.sin(x * 0.331 + y * 0.067 + 0.8)
        ) / 3.0
        edge_shadow = max(0.0, 1.0 - min(u, 1.0 - u, v, 1.0 - v) / 0.052)
        thumb_oil = max(0.0, 1.0 - (((u - 0.72) / 0.20) ** 2 + ((v - 0.84) / 0.12) ** 2))
        coffee_bleed = max(0.0, 1.0 - (((u - 0.18) / 0.16) ** 2 + ((v - 0.16) / 0.10) ** 2))
        fold = max(0.0, 1.0 - abs(u - 0.54) / 0.012) * (0.35 + 0.65 * v)

        r = 193 + 8 * fiber
        g = 173 + 6 * fiber
        b = 130 + 5 * fiber
        darken = 12 * edge_shadow + 7 * thumb_oil + 6 * coffee_bleed + 4 * fold
        r -= darken
        g -= darken * 0.83
        b -= darken * 0.63

        def mix(red: float, green: float, blue: float, amount: float) -> None:
            nonlocal r, g, b
            a = max(0.0, min(1.0, amount))
            r = r * (1.0 - a) + red * a
            g = g * (1.0 - a) + green * a
            b = b * (1.0 - a) + blue * a

        def rect(x0: float, x1: float, y0: float, y1: float, feather: float = 0.002) -> float:
            if u < x0 - feather or u > x1 + feather or v < y0 - feather or v > y1 + feather:
                return 0.0
            inside = min(u - x0, x1 - u, v - y0, y1 - v)
            return max(0.0, min(1.0, (inside + feather) / max(feather, 0.0001)))

        def line_x(x0: float, x1: float, y0: float, thickness: float) -> float:
            return rect(x0, x1, y0 - thickness * 0.5, y0 + thickness * 0.5, thickness * 0.28)

        def line_y(x0: float, y0: float, y1: float, thickness: float) -> float:
            return rect(x0 - thickness * 0.5, x0 + thickness * 0.5, y0, y1, thickness * 0.28)

        def outline(x0: float, x1: float, y0: float, y1: float, thickness: float) -> float:
            return max(
                line_x(x0, x1, y0, thickness),
                line_x(x0, x1, y1, thickness),
                line_y(x0, y0, y1, thickness),
                line_y(x1, y0, y1, thickness),
            )

        ink = (31, 25, 21)
        faded = (64, 46, 33)
        red = (142, 30, 24)
        mix(*faded, outline(0.055, 0.945, 0.055, 0.945, 0.007) * 0.78)
        mix(*ink, line_x(0.105, 0.62, 0.122, 0.012) * 0.65)
        mix(*faded, line_x(0.105, 0.90, 0.205, 0.006) * 0.65)
        mix(*faded, line_x(0.105, 0.90, 0.305, 0.005) * 0.55)
        mix(*faded, line_x(0.105, 0.90, 0.405, 0.005) * 0.55)
        mix(*faded, line_x(0.105, 0.54, 0.505, 0.005) * 0.55)
        mix(*faded, outline(0.095, 0.165, 0.585, 0.655, 0.007) * 0.85)
        mix(*red, line_x(0.104, 0.137, 0.636, 0.010) * 0.92)
        mix(*red, line_x(0.129, 0.178, 0.606, 0.010) * 0.92)
        mix(*red, outline(0.602, 0.900, 0.610, 0.760, 0.010) * 0.72)
        mix(*red, line_x(0.630, 0.872, 0.690, 0.010) * 0.46)
        mix(*red, line_x(0.632, 0.795, 0.728, 0.008) * 0.44)
        mix(*red, line_y(0.670, 0.632, 0.742, 0.007) * 0.50)
        mix(*red, line_y(0.742, 0.632, 0.742, 0.007) * 0.50)
        mix(*red, line_y(0.820, 0.632, 0.742, 0.007) * 0.50)
        mix(*red, max(
            line_x(0.235, 0.345, 0.248, 0.012),
            line_x(0.235, 0.345, 0.288, 0.012),
            line_x(0.235, 0.345, 0.328, 0.012),
            line_y(0.345, 0.248, 0.328, 0.012),
            line_y(0.235, 0.288, 0.328, 0.012),
        ) * 0.70)

        for offset, strength in ((0.00, 0.60), (0.028, 0.42), (0.058, 0.30)):
            wave = max(0.0, 1.0 - abs(v - (0.805 + offset + 0.012 * math.sin(u * 31.0))) / 0.006)
            span = rect(0.20, 0.76, 0.785 + offset, 0.825 + offset, 0.004)
            mix(*ink, wave * span * strength)

        return (
            max(0, min(255, int(r))),
            max(0, min(255, int(g))),
            max(0, min(255, int(b))),
        )

    def room_door_pixel(x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
        u = x / max(1, width - 1)
        v = y / max(1, height - 1)
        draw_v = 1.0 - v
        grain = (
            math.sin(x * 0.097 + y * 0.021)
            + math.sin(x * 0.019 - y * 0.163 + 1.4)
            + math.sin(x * 0.231 + y * 0.047 + 2.9)
        ) / 3.0
        panel_shadow = 0.0
        for panel_u in (0.13, 0.38, 0.62, 0.87):
            panel_shadow += max(0.0, 1.0 - abs(u - panel_u) / 0.010)
        horizontal_wear = 0.0
        for panel_v in (0.18, 0.49, 0.73, 0.92):
            horizontal_wear += max(0.0, 1.0 - abs(v - panel_v) / 0.012)
        edge_oil = max(0.0, 1.0 - min(u, 1.0 - u, v, 1.0 - v) / 0.045)
        handle_grime = max(0.0, 1.0 - (((u - 0.82) / 0.18) ** 2 + ((v - 0.50) / 0.20) ** 2))
        latch_drag = max(0.0, 1.0 - abs((u - 0.80) + (v - 0.50) * 0.10) / 0.013) * max(0.0, 1.0 - abs(v - 0.50) / 0.24)
        scratches = 0.0
        for scratch_u in (0.18, 0.24, 0.34, 0.57, 0.66, 0.76, 0.91):
            scratches += max(0.0, 1.0 - abs(u - (scratch_u + 0.012 * math.sin(v * 19.0))) / 0.004) * max(0.0, math.sin(v * 17.0 + scratch_u * 12.0))
        paint_chips = 0.0
        for chip_u, chip_v, chip_w, chip_h in (
            (0.06, 0.15, 0.035, 0.075),
            (0.10, 0.66, 0.030, 0.060),
            (0.88, 0.38, 0.040, 0.105),
            (0.73, 0.74, 0.055, 0.040),
            (0.42, 0.25, 0.036, 0.036),
        ):
            chip = max(0.0, 1.0 - (((u - chip_u) / chip_w) ** 2 + ((v - chip_v) / chip_h) ** 2))
            paint_chips += chip

        red = 67 + 8 * grain
        green = 51 + 6 * grain
        blue = 37 + 5 * grain
        darken = 20 * edge_oil + 26 * panel_shadow + 18 * handle_grime + 16 * latch_drag + 9 * horizontal_wear
        brighten = 34 * paint_chips + 15 * scratches
        r = red - darken + brighten
        g = green - darken * 0.84 + brighten * 0.72
        b = blue - darken * 0.66 + brighten * 0.48

        def inside_rect(x0: float, x1: float, y0: float, y1: float) -> bool:
            return x0 <= u <= x1 and y0 <= draw_v <= y1

        def soft_rect(x0: float, x1: float, y0: float, y1: float, feather: float) -> float:
            if not inside_rect(x0 - feather, x1 + feather, y0 - feather, y1 + feather):
                return 0.0
            edge = min(u - x0, x1 - u, draw_v - y0, y1 - draw_v)
            return max(0.0, min(1.0, (edge + feather) / max(feather, 0.001)))

        def segment_hit(cx: float, cy: float, scale: float, segments: tuple[str, ...]) -> float:
            local_x = (u - cx) / scale
            local_y = (draw_v - cy) / scale
            thickness = 0.055
            hit = 0.0
            segment_defs = {
                "top": (-0.32, 0.32, 0.39, 0.48),
                "mid": (-0.32, 0.32, -0.04, 0.05),
                "bottom": (-0.32, 0.32, -0.48, -0.39),
                "ul": (-0.42, -0.30, 0.02, 0.40),
                "ur": (0.30, 0.42, 0.02, 0.40),
                "ll": (-0.42, -0.30, -0.40, -0.02),
                "lr": (0.30, 0.42, -0.40, -0.02),
            }
            for name in segments:
                x0, x1, y0, y1 = segment_defs[name]
                if x0 - thickness <= local_x <= x1 + thickness and y0 - thickness <= local_y <= y1 + thickness:
                    hit = max(hit, 1.0)
            return hit

        plate = soft_rect(0.105, 0.330, 0.748, 0.842, 0.008)
        if plate:
            r = r * (1.0 - 0.88 * plate) + 10 * plate
            g = g * (1.0 - 0.88 * plate) + 9 * plate
            b = b * (1.0 - 0.88 * plate) + 8 * plate
        digit = max(
            segment_hit(0.150, 0.796, 0.105, ("top", "ur", "mid", "ll", "bottom")),
            segment_hit(0.218, 0.796, 0.105, ("top", "ul", "ur", "ll", "lr", "bottom")),
            segment_hit(0.286, 0.796, 0.105, ("top", "ur", "mid", "lr", "bottom")),
        )
        if digit:
            uneven = 0.78 + 0.22 * math.sin(x * 0.41 + y * 0.19)
            r = r * 0.24 + 178 * digit * uneven
            g = g * 0.24 + 134 * digit * uneven
            b = b * 0.24 + 82 * digit * uneven

        paper = soft_rect(0.305, 0.560, 0.405, 0.585, 0.012)
        if paper:
            paper_fiber = 0.5 + 0.5 * math.sin(x * 0.51 + y * 0.19)
            r = r * (1.0 - 0.92 * paper) + (132 + 18 * paper_fiber) * paper
            g = g * (1.0 - 0.92 * paper) + (118 + 12 * paper_fiber) * paper
            b = b * (1.0 - 0.92 * paper) + (88 + 8 * paper_fiber) * paper
        writing = 0.0
        for line_y, slope, start, end in (
            (0.550, -0.02, 0.330, 0.530),
            (0.510, 0.01, 0.325, 0.545),
            (0.475, -0.01, 0.342, 0.520),
        ):
            center = line_y + slope * (u - 0.43)
            if start <= u <= end:
                writing = max(writing, max(0.0, 1.0 - abs(draw_v - center) / 0.004))
        slash = max(0.0, 1.0 - abs((u - 0.435) - (draw_v - 0.495) * 0.38) / 0.006) if inside_rect(0.350, 0.515, 0.430, 0.570) else 0.0
        writing = max(writing, slash)
        if writing:
            r = r * (1.0 - 0.85 * writing) + 42 * writing
            g = g * (1.0 - 0.85 * writing) + 24 * writing
            b = b * (1.0 - 0.85 * writing) + 14 * writing
        tape = soft_rect(0.330, 0.535, 0.386, 0.408, 0.004)
        if tape:
            r = r * (1.0 - 0.70 * tape) + 144 * tape
            g = g * (1.0 - 0.70 * tape) + 83 * tape
            b = b * (1.0 - 0.70 * tape) + 30 * tape

        handle_plate = soft_rect(0.855, 0.935, 0.390, 0.640, 0.006)
        if handle_plate:
            r = r * (1.0 - 0.72 * handle_plate) + 18 * handle_plate
            g = g * (1.0 - 0.72 * handle_plate) + 17 * handle_plate
            b = b * (1.0 - 0.72 * handle_plate) + 15 * handle_plate
        for screw_u, screw_v in ((0.895, 0.605), (0.895, 0.425)):
            screw = max(0.0, 1.0 - (((u - screw_u) / 0.012) ** 2 + ((draw_v - screw_v) / 0.012) ** 2))
            if screw:
                r = r * (1.0 - 0.55 * screw) + 80 * screw
                g = g * (1.0 - 0.55 * screw) + 72 * screw
                b = b * (1.0 - 0.55 * screw) + 58 * screw

        return (
            max(0, min(255, int(r))),
            max(0, min(255, int(g))),
            max(0, min(255, int(b))),
        )

    monitor_glyphs = {
        "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
        "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
        "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
        "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
        "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
        "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
        "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
        "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
        "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
        "9": ("01110", "10001", "10001", "01111", "00001", "00010", "11100"),
        "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
        "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
        "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
        "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
        "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
        "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01111"),
        "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
        "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
        "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
        "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
        "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
        "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
        "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
        "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
        "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
        "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
        "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
        "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
        "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
        ":": ("0", "1", "1", "0", "1", "1", "0"),
        "-": ("0", "0", "0", "111", "0", "0", "0"),
    }

    def monitor_text_mask(local_u: float, local_v: float, text: str, origin_u: float, origin_v: float, cell: float) -> float:
        cursor_u = origin_u
        for char in text.upper():
            if char == " ":
                cursor_u += cell * 3.0
                continue
            glyph = monitor_glyphs.get(char)
            if glyph is None:
                cursor_u += cell * 6.0
                continue
            glyph_width = max(len(row) for row in glyph)
            glyph_height = len(glyph)
            if cursor_u <= local_u < cursor_u + glyph_width * cell and origin_v <= local_v < origin_v + glyph_height * cell:
                col = int((local_u - cursor_u) / cell)
                row = int((local_v - origin_v) / cell)
                glyph_row = glyph[row]
                if col < len(glyph_row) and glyph_row[col] == "1":
                    return 1.0
            cursor_u += (glyph_width + 1) * cell
        return 0.0

    def frontdesk_hero_board_pixel(x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
        u = x / max(1, width - 1)
        v = y / max(1, height - 1)
        grain = (
            math.sin(x * 0.091 + y * 0.037)
            + math.sin(x * 0.021 - y * 0.171 + 1.6)
            + math.sin(x * 0.317 + y * 0.061 + 3.2)
        ) / 3.0
        edge_shadow = max(0.0, 1.0 - min(u, 1.0 - u, v, 1.0 - v) / 0.055)
        old_tape = max(0.0, 1.0 - abs(v - 0.18) / 0.020) * max(0.0, 1.0 - abs(u - 0.12) / 0.095)
        old_tape = max(old_tape, max(0.0, 1.0 - abs(v - 0.82) / 0.020) * max(0.0, 1.0 - abs(u - 0.88) / 0.095))
        screw_a = max(0.0, 1.0 - (((u - 0.055) / 0.018) ** 2 + ((v - 0.105) / 0.025) ** 2))
        screw_b = max(0.0, 1.0 - (((u - 0.945) / 0.018) ** 2 + ((v - 0.105) / 0.025) ** 2))
        amber_rule = max(0.0, 1.0 - abs(v - 0.385) / 0.006) * max(0.0, 1.0 - abs(u - 0.50) / 0.42)

        red = 50 + 8 * grain
        green = 38 + 6 * grain
        blue = 25 + 4 * grain
        red -= 20 * edge_shadow
        green -= 16 * edge_shadow
        blue -= 12 * edge_shadow
        red += 88 * old_tape + 52 * amber_rule
        green += 58 * old_tape + 30 * amber_rule
        blue += 24 * old_tape + 10 * amber_rule
        red += 34 * (screw_a + screw_b)
        green += 30 * (screw_a + screw_b)
        blue += 24 * (screw_a + screw_b)

        title = monitor_text_mask(u, v, "NIGHT RECEPTION", 0.075, 0.145, 0.016)
        call = monitor_text_mask(u, v, "ROOM203 CALL 02:13", 0.078, 0.455, 0.012)
        camera = monitor_text_mask(u, v, "CHECK CAMERA", 0.078, 0.612, 0.012)
        keys = monitor_text_mask(u, v, "KEYS 201 202 203", 0.078, 0.760, 0.0105)
        title_wear = 0.72 + 0.28 * max(0.0, math.sin(x * 0.23 + y * 0.11))
        text_wear = 0.62 + 0.38 * max(0.0, math.sin(x * 0.37 - y * 0.13))
        red += 178 * title * title_wear + 120 * call * text_wear + 90 * camera * text_wear + 82 * keys * text_wear
        green += 135 * title * title_wear + 64 * call * text_wear + 110 * camera * text_wear + 90 * keys * text_wear
        blue += 76 * title * title_wear + 28 * call * text_wear + 58 * camera * text_wear + 42 * keys * text_wear
        return (
            max(0, min(255, int(red))),
            max(0, min(255, int(green))),
            max(0, min(255, int(blue))),
        )

    def security_monitor_feed_pixel(x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
        u = x / max(1, width - 1)
        v = y / max(1, height - 1)
        qx = 0 if u < 0.5 else 1
        qy = 0 if v < 0.5 else 1
        local_u = (u - qx * 0.5) * 2.0
        local_v = (v - qy * 0.5) * 2.0
        scanline = 0.78 + 0.22 * (1.0 if y % 4 < 2 else 0.0)
        static = (
            math.sin(x * 0.91 + y * 0.31)
            + math.sin(x * 0.17 - y * 1.11 + 2.4)
            + math.sin(x * 1.73 + y * 0.07 + 5.2)
        ) / 3.0
        border = 0.0
        if abs(u - 0.5) < 0.006 or abs(v - 0.5) < 0.008:
            border = 1.0
        if local_u < 0.035 or local_u > 0.965 or local_v < 0.045 or local_v > 0.955:
            border = max(border, 0.75)

        red = 5 + 7 * static
        green = 42 + 22 * static
        blue = 23 + 10 * static

        # Hallway perspective lines in the main Room 203 feed.
        if qx == 0 and qy == 0:
            center = 0.52
            left_wall = 0.12 + 0.28 * local_v
            right_wall = 0.88 - 0.24 * local_v
            floor_line = 0.70 + 0.12 * abs(local_u - center)
            ceiling_line = 0.18 - 0.04 * abs(local_u - center)
            wall_hit = max(0.0, 1.0 - abs(local_u - left_wall) / 0.012)
            wall_hit = max(wall_hit, max(0.0, 1.0 - abs(local_u - right_wall) / 0.012))
            floor_hit = max(0.0, 1.0 - abs(local_v - floor_line) / 0.012)
            ceiling_hit = max(0.0, 1.0 - abs(local_v - ceiling_line) / 0.010)
            door = 1.0 if 0.61 <= local_u <= 0.78 and 0.30 <= local_v <= 0.79 else 0.0
            door_frame = max(0.0, 1.0 - abs(local_u - 0.61) / 0.010) if 0.28 <= local_v <= 0.82 else 0.0
            door_frame = max(door_frame, max(0.0, 1.0 - abs(local_u - 0.78) / 0.010) if 0.28 <= local_v <= 0.82 else 0.0)
            door_frame = max(door_frame, max(0.0, 1.0 - abs(local_v - 0.30) / 0.010) if 0.58 <= local_u <= 0.81 else 0.0)
            ajar_gap = max(0.0, 1.0 - abs(local_u - (0.755 + (local_v - 0.30) * 0.035)) / 0.008) if 0.34 <= local_v <= 0.78 else 0.0
            plate = 1.0 if 0.66 <= local_u <= 0.73 and 0.34 <= local_v <= 0.40 else 0.0
            label_203 = monitor_text_mask(local_u, local_v, "CAM 203 HALL", 0.055, 0.070, 0.010)
            no_guest = monitor_text_mask(local_u, local_v, "NO GUEST", 0.055, 0.820, 0.012)
            timestamp_203 = monitor_text_mask(local_u, local_v, "02:13:47", 0.600, 0.860, 0.010)
            red += 3 * (wall_hit + floor_hit + ceiling_hit) + 8 * door + 20 * plate + 8 * door_frame + 18 * ajar_gap
            green += 46 * (wall_hit + floor_hit + ceiling_hit) + 26 * door + 76 * plate + 78 * door_frame + 118 * ajar_gap
            blue += 18 * (wall_hit + floor_hit + ceiling_hit) + 10 * door + 32 * plate + 30 * door_frame + 50 * ajar_gap
            red += 10 * (label_203 + timestamp_203) + 44 * no_guest
            green += 94 * (label_203 + timestamp_203) + 48 * no_guest
            blue += 38 * (label_203 + timestamp_203) + 14 * no_guest

        # Empty lobby feed: visible counter edge, no figure.
        if qx == 1 and qy == 0:
            counter = 1.0 if 0.18 <= local_v <= 0.28 and 0.10 <= local_u <= 0.92 else 0.0
            glass_line = max(0.0, 1.0 - abs(local_u - 0.74) / 0.012) if 0.28 < local_v < 0.86 else 0.0
            lobby_label = monitor_text_mask(local_u, local_v, "LOBBY EMPTY", 0.055, 0.070, 0.010)
            red += 4 * counter + 5 * glass_line
            green += 42 * counter + 48 * glass_line
            blue += 16 * counter + 30 * glass_line
            red += 10 * lobby_label
            green += 86 * lobby_label
            blue += 36 * lobby_label

        # Stair/elevator feed: the split route is represented without adding another mechanic.
        if qx == 0 and qy == 1:
            elevator_seam = max(0.0, 1.0 - abs(local_u - 0.36) / 0.010) if 0.18 < local_v < 0.84 else 0.0
            stair_sign = 1.0 if 0.58 <= local_u <= 0.86 and 0.20 <= local_v <= 0.31 else 0.0
            stair_label = monitor_text_mask(local_u, local_v, "STAIR LOCK", 0.055, 0.070, 0.010)
            red += 15 * stair_sign + 4 * elevator_seam
            green += 50 * stair_sign + 42 * elevator_seam
            blue += 30 * stair_sign + 18 * elevator_seam
            red += 9 * stair_label
            green += 84 * stair_label
            blue += 35 * stair_label

        # Alert/status feed: warm pixels must remain readable after filmic tonemapping.
        if qx == 1 and qy == 1:
            red_bar = 1.0 if 0.18 <= local_u <= 0.84 and 0.305 <= local_v <= 0.322 else 0.0
            red_bar = max(red_bar, 1.0 if 0.24 <= local_u <= 0.76 and 0.487 <= local_v <= 0.502 else 0.0)
            slash = max(0.0, 1.0 - abs((local_u - 0.28) - (local_v - 0.62) * 0.55) / 0.010) if 0.18 < local_u < 0.78 and 0.56 < local_v < 0.80 else 0.0
            alert_label = monitor_text_mask(local_u, local_v, "ROOM203 OPEN", 0.055, 0.070, 0.010)
            no_guest_alert = monitor_text_mask(local_u, local_v, "NO GUEST", 0.245, 0.600, 0.014)
            warm_line = max(red_bar, slash)
            warm_text = max(alert_label, no_guest_alert)
            red += 138 * warm_line + 228 * warm_text
            green += 44 * warm_line + 56 * warm_text
            blue += 18 * warm_line + 20 * warm_text

        # CCTV text is a tiny project-authored bitmap font, not an external font asset.
        rec = monitor_text_mask(local_u, local_v, "REC", 0.835, 0.070, 0.010)
        timestamp = monitor_text_mask(local_u, local_v, "02:13", 0.695, 0.875, 0.010)
        label = rec
        red += 7 * (label + timestamp) + 18 * border
        green += 70 * (label + timestamp) + 80 * border
        blue += 30 * (label + timestamp) + 36 * border

        green *= scanline
        red *= scanline
        blue *= scanline
        vignette = 1.0 - 0.42 * max(0.0, math.sqrt((u - 0.5) ** 2 + (v - 0.5) ** 2) - 0.35)
        return (
            max(0, min(255, int(red * vignette))),
            max(0, min(255, int(green * vignette))),
            max(0, min(255, int(blue * vignette))),
        )

    def lobby_door_smudged_glass_pixel(x: int, y: int, width: int, height: int) -> tuple[int, int, int]:
        u = x / max(1, width - 1)
        v = y / max(1, height - 1)
        noise = (
            math.sin(x * 0.111 + y * 0.047)
            + math.sin(x * 0.027 - y * 0.183 + 1.9)
            + math.sin(x * 0.431 + y * 0.071 + 4.3)
        ) / 3.0
        vertical_grime = 0.0
        for stain_u in (0.18, 0.31, 0.48, 0.64, 0.82):
            vertical_grime += max(0.0, 1.0 - abs(u - stain_u) / 0.018) * (0.22 + 0.78 * v)
        palm_oil = max(0.0, 1.0 - (((u - 0.29) / 0.18) ** 2 + ((v - 0.62) / 0.20) ** 2))
        sleeve_smear = max(0.0, 1.0 - (((u - 0.72) / 0.22) ** 2 + ((v - 0.38) / 0.15) ** 2))
        tape_residue = max(0.0, 1.0 - abs(v - 0.23) / 0.020) * max(0.0, 1.0 - abs(u - 0.50) / 0.38)
        tape_residue = max(tape_residue, max(0.0, 1.0 - abs(u - 0.52) / 0.018) * max(0.0, 1.0 - abs(v - 0.23) / 0.34))
        crack = 0.0
        for slope, intercept, span_min, span_max in (
            (0.62, 0.11, 0.35, 0.83),
            (-0.45, 0.78, 0.18, 0.64),
            (0.18, 0.49, 0.20, 0.88),
        ):
            center = slope * u + intercept
            if span_min <= u <= span_max:
                crack = max(crack, max(0.0, 1.0 - abs(v - center) / 0.004))
        edge_dirt = max(0.0, 1.0 - min(u, 1.0 - u, v, 1.0 - v) / 0.045)
        reflection = max(0.0, 1.0 - abs((u + v * 0.18) - 0.76) / 0.018) * 0.55

        red = 25 + 12 * noise + 28 * reflection + 34 * tape_residue + 42 * crack
        green = 43 + 16 * noise + 44 * reflection + 42 * tape_residue + 58 * crack
        blue = 54 + 18 * noise + 58 * reflection + 50 * tape_residue + 72 * crack
        darken = 17 * edge_dirt + 18 * vertical_grime + 16 * sleeve_smear
        lighten = 32 * palm_oil
        return (
            max(0, min(255, int(red - darken + lighten))),
            max(0, min(255, int(green - darken * 0.88 + lighten * 0.96))),
            max(0, min(255, int(blue - darken * 0.75 + lighten * 1.05))),
        )

    textures = {
        "TX_Hotel_Room203WallpaperPanel_v0": (512, 512, wallpaper_pixel),
        "TX_Hotel_RoomDoorPaint_v0": (512, 512, room_door_pixel),
        "TX_Hotel_ReturnRouteSlipPaper_v0": (512, 512, return_slip_pixel),
        "TX_Hotel_SecurityMonitorFeed_v0": (512, 512, security_monitor_feed_pixel),
        "TX_Hotel_ReportLogFiledPaper_v0": (512, 512, report_log_filed_paper_pixel),
        "TX_Hotel_LobbyDoorSmudgedGlass_v0": (512, 512, lobby_door_smudged_glass_pixel),
        "TX_Hotel_FrontDeskHeroBoard_v0": (512, 256, frontdesk_hero_board_pixel),
    }
    output: dict[str, pathlib.Path] = {}
    for name, (width, height, pixel_func) in textures.items():
        path = SOURCE_TEXTURE_DIR / f"{name}.png"
        pixels = [pixel_func(x, y, width, height) for y in range(height) for x in range(width)]
        previous = path.read_bytes() if path.exists() else None
        write_png_rgb(path, width, height, pixels)
        if previous != path.read_bytes():
            UPDATED_SOURCE_TEXTURES.add(name)
        output[name] = path
    return output


def generate_source_audio() -> dict[str, pathlib.Path]:
    def phone_ring(t: float) -> float:
        cycle = t % 1.25
        active = cycle < 0.38 or 0.55 < cycle < 0.93
        if not active:
            return 0.0
        env = 0.65
        return env * (math.sin(2 * math.pi * 440 * t) + 0.45 * math.sin(2 * math.pi * 480 * t)) * 0.45

    def lobby_hum(t: float) -> float:
        slow = math.sin(2 * math.pi * 0.17 * t) * 0.08
        return 0.18 * math.sin(2 * math.pi * 60 * t) + 0.06 * math.sin(2 * math.pi * 120 * t) + slow

    def phone_pickup(t: float) -> float:
        click = 0.0
        for start, pitch in ((0.025, 840), (0.105, 360), (0.205, 1200)):
            dt = t - start
            if 0.0 <= dt <= 0.055:
                click += math.exp(-dt * 55.0) * math.sin(2 * math.pi * pitch * dt)
        cable = 0.12 * math.sin(2 * math.pi * 180 * t) if 0.12 <= t <= 0.36 else 0.0
        return 0.48 * click + cable

    def phone_line_static(t: float) -> float:
        hiss = 0.05 * math.sin(2 * math.pi * 3100 * t) + 0.035 * math.sin(2 * math.pi * 4970 * t)
        cable = 0.045 * math.sin(2 * math.pi * 126 * t)
        whisper_gate = 1.0 if 0.35 < t < 1.8 else 0.0
        whisper = whisper_gate * (0.08 * math.sin(2 * math.pi * 178 * t) + 0.035 * math.sin(2 * math.pi * 221 * t))
        clicks = 0.0
        for start in (0.18, 1.92, 2.34):
            dt = t - start
            if 0.0 <= dt <= 0.035:
                clicks += math.exp(-dt * 85.0) * math.sin(2 * math.pi * 920 * dt)
        return hiss + cable + whisper + 0.34 * clicks

    def hallway_drone(t: float) -> float:
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * 0.11 * t)
        return 0.16 * math.sin(2 * math.pi * 82 * t) + 0.035 * pulse * math.sin(2 * math.pi * 610 * t)

    def elevator_shaft_groan(t: float) -> float:
        motor_gate = 0.45 + 0.55 * math.sin(2 * math.pi * 0.08 * t)
        cable = 0.12 * math.sin(2 * math.pi * 47 * t) + 0.07 * math.sin(2 * math.pi * 93 * t)
        brake_ticks = 0.0
        for start in (0.8, 2.55, 4.2):
            dt = t - start
            if 0.0 <= dt <= 0.08:
                brake_ticks += math.exp(-dt * 34.0) * math.sin(2 * math.pi * 310 * dt)
        return 0.7 * motor_gate * cable + 0.26 * brake_ticks

    def stairwell_air(t: float) -> float:
        vent = 0.09 * math.sin(2 * math.pi * 71 * t) + 0.035 * math.sin(2 * math.pi * 143 * t)
        flutter = (0.5 + 0.5 * math.sin(2 * math.pi * 0.21 * t)) * 0.035 * math.sin(2 * math.pi * 520 * t)
        distant = 0.045 * math.sin(2 * math.pi * 38 * t)
        return vent + flutter + distant

    def door_knock(t: float) -> float:
        total = 0.0
        for start in (0.18, 0.42, 0.91):
            dt = t - start
            if 0.0 <= dt <= 0.16:
                total += math.exp(-dt * 28.0) * (math.sin(2 * math.pi * 135 * dt) + 0.35 * math.sin(2 * math.pi * 260 * dt))
        return 0.55 * total

    def room203_aftershock_rustle(t: float) -> float:
        paper = 0.0
        for start, pitch in ((0.04, 1280), (0.16, 1730), (0.31, 960), (0.58, 1410)):
            dt = t - start
            if 0.0 <= dt <= 0.20:
                paper += math.exp(-dt * 18.0) * (
                    0.55 * math.sin(2 * math.pi * pitch * dt)
                    + 0.25 * math.sin(2 * math.pi * (pitch * 1.73) * dt)
                )
        chain_tail = 0.0
        for start, pitch in ((0.10, 214), (0.38, 176), (0.72, 241)):
            dt = t - start
            if 0.0 <= dt <= 0.08:
                chain_tail += math.exp(-dt * 42.0) * math.sin(2 * math.pi * pitch * dt)
        hall_body = 0.05 * math.sin(2 * math.pi * 58 * t) * math.exp(-t * 1.4)
        return 0.18 * paper + 0.34 * chain_tail + hall_body

    def report_log_filed(t: float) -> float:
        stamp = 0.0
        for start, pitch in ((0.035, 190), (0.085, 520), (0.16, 132)):
            dt = t - start
            if 0.0 <= dt <= 0.11:
                stamp += math.exp(-dt * 38.0) * math.sin(2 * math.pi * pitch * dt)
        scratch = 0.05 * math.sin(2 * math.pi * 1550 * t) if 0.18 <= t <= 0.38 else 0.0
        paper = 0.08 * math.sin(2 * math.pi * 240 * t) if 0.10 <= t <= 0.34 else 0.0
        return 0.48 * stamp + scratch + paper

    def patrol_listen_drop(t: float) -> float:
        floor_bloom = 0.18 * math.sin(2 * math.pi * 54 * t) * math.exp(-t * 1.2)
        elevator_reply = 0.0
        for start, pitch in ((0.18, 112), (0.62, 74), (1.08, 92)):
            dt = t - start
            if 0.0 <= dt <= 0.42:
                elevator_reply += math.exp(-dt * 5.2) * math.sin(2 * math.pi * pitch * dt)
        dry_click = 0.0
        for start in (0.06, 0.42, 1.35):
            dt = t - start
            if 0.0 <= dt <= 0.035:
                dry_click += math.exp(-dt * 95.0) * math.sin(2 * math.pi * 720 * dt)
        stair_breath = 0.05 * math.sin(2 * math.pi * 186 * t) if 1.2 <= t <= 2.2 else 0.0
        return floor_bloom + 0.28 * elevator_reply + 0.24 * dry_click + stair_breath

    def return_route_knockback(t: float) -> float:
        total = 0.0
        for start, pitch in ((0.04, 96), (0.34, 141), (0.72, 83), (1.18, 128)):
            dt = t - start
            if 0.0 <= dt <= 0.18:
                total += math.exp(-dt * 24.0) * (math.sin(2 * math.pi * pitch * dt) + 0.24 * math.sin(2 * math.pi * (pitch * 2.1) * dt))
        reverse_hum = 0.07 * math.sin(2 * math.pi * 58 * t) * math.exp(-max(0.0, t - 0.55) * 0.8)
        cold_scrape = 0.035 * math.sin(2 * math.pi * 690 * t) if 0.92 <= t <= 1.42 else 0.0
        return 0.52 * total + reverse_hum + cold_scrape

    def return_route_pursuit_tail(t: float) -> float:
        floor_ticks = 0.0
        for start, pitch in ((0.05, 72), (0.42, 84), (0.92, 68), (1.44, 92)):
            dt = t - start
            if 0.0 <= dt <= 0.20:
                floor_ticks += math.exp(-dt * 22.0) * (
                    math.sin(2 * math.pi * pitch * dt) + 0.22 * math.sin(2 * math.pi * (pitch * 2.7) * dt)
                )
        paper_answer = 0.0
        for start in (0.36, 0.78, 1.18, 1.70):
            dt = t - start
            if 0.0 <= dt <= 0.18:
                paper_answer += math.exp(-dt * 28.0) * math.sin(2 * math.pi * (540 + 120 * math.sin(start * 5.0)) * dt)
        air_pull = 0.06 * math.sin(2 * math.pi * 43 * t) * math.exp(-max(0.0, t - 0.18) * 0.65)
        dry_edge = 0.028 * math.sin(2 * math.pi * 1240 * t) if 1.32 <= t <= 2.34 else 0.0
        return 0.42 * floor_ticks + 0.20 * paper_answer + air_pull + dry_edge

    def post_report_monitor_mismatch(t: float) -> float:
        scan = 0.045 * math.sin(2 * math.pi * 2860 * t) + 0.028 * math.sin(2 * math.pi * 4120 * t)
        low_relay = 0.0
        for start, pitch in ((0.06, 116), (0.28, 74), (0.74, 103)):
            dt = t - start
            if 0.0 <= dt <= 0.18:
                low_relay += math.exp(-dt * 18.0) * math.sin(2 * math.pi * pitch * dt)
        frame_skip = 0.0
        for start in (0.18, 0.42, 0.66, 0.92):
            dt = t - start
            if 0.0 <= dt <= 0.025:
                frame_skip += math.exp(-dt * 120.0) * math.sin(2 * math.pi * 960 * dt)
        dead_air = 0.05 * math.sin(2 * math.pi * 52 * t) if 0.55 <= t <= 1.25 else 0.0
        return scan + 0.42 * low_relay + 0.30 * frame_skip + dead_air

    def monitor_check_glitch(t: float) -> float:
        relay = 0.0
        for start, pitch in ((0.015, 1140), (0.075, 360), (0.19, 840), (0.33, 128)):
            dt = t - start
            if 0.0 <= dt <= 0.075:
                relay += math.exp(-dt * 48.0) * math.sin(2 * math.pi * pitch * dt)
        scan = 0.055 * math.sin(2 * math.pi * 3180 * t) if 0.06 <= t <= 0.52 else 0.0
        sync = 0.035 * math.sin(2 * math.pi * 68 * t) * math.exp(-t * 3.0)
        frame_tick = 0.0
        for start in (0.11, 0.25, 0.41):
            dt = t - start
            if 0.0 <= dt <= 0.024:
                frame_tick += math.exp(-dt * 128.0) * math.sin(2 * math.pi * 1540 * dt)
        return 0.34 * relay + scan + sync + 0.26 * frame_tick

    def post_report_desk_wait_rattle(t: float) -> float:
        glass = 0.0
        for start, pitch in ((0.05, 162), (0.18, 91), (0.42, 126), (0.68, 73)):
            dt = t - start
            if 0.0 <= dt <= 0.22:
                glass += math.exp(-dt * 20.0) * (
                    math.sin(2 * math.pi * pitch * dt) + 0.28 * math.sin(2 * math.pi * (pitch * 3.1) * dt)
                )
        handle_tick = 0.0
        for start in (0.11, 0.55, 0.92):
            dt = t - start
            if 0.0 <= dt <= 0.035:
                handle_tick += math.exp(-dt * 95.0) * math.sin(2 * math.pi * 780 * dt)
        outside_air = 0.055 * math.sin(2 * math.pi * 46 * t) * math.exp(-max(0.0, t - 0.25) * 0.9)
        return 0.48 * glass + 0.26 * handle_tick + outside_air

    def post_report_log_self_correction(t: float) -> float:
        paper_drag = 0.0
        for start, pitch in ((0.04, 420), (0.16, 680), (0.32, 510)):
            dt = t - start
            if 0.0 <= dt <= 0.16:
                paper_drag += math.exp(-dt * 26.0) * math.sin(2 * math.pi * pitch * dt)
        pen_tick = 0.0
        for start in (0.22, 0.48, 0.82):
            dt = t - start
            if 0.0 <= dt <= 0.028:
                pen_tick += math.exp(-dt * 120.0) * math.sin(2 * math.pi * 1120 * dt)
        low_page = 0.06 * math.sin(2 * math.pi * 73 * t) * math.exp(-t * 1.6)
        dry_line = 0.04 * math.sin(2 * math.pi * 1780 * t) if 0.36 <= t <= 0.98 else 0.0
        return 0.36 * paper_drag + 0.24 * pen_tick + low_page + dry_line

    sources = {
        "SFX_PhoneRing_v0": (2.5, phone_ring),
        "SFX_PhonePickup_v0": (0.45, phone_pickup),
        "SFX_PhoneLineStatic_v0": (3.2, phone_line_static),
        "AMB_LobbyFluorescentHum_v0": (6.0, lobby_hum),
        "AMB_GuestHallDrone_v0": (6.0, hallway_drone),
        "AMB_ElevatorShaftGroan_v0": (6.0, elevator_shaft_groan),
        "AMB_StairwellAir_v0": (6.0, stairwell_air),
        "SFX_DoorKnock203_v0": (1.4, door_knock),
        "SFX_Room203AftershockRustle_v0": (1.1, room203_aftershock_rustle),
        "SFX_ReportLogFiled_v0": (0.55, report_log_filed),
        "SFX_PatrolListenDrop_v0": (2.4, patrol_listen_drop),
        "SFX_ReturnRouteKnockback_v0": (1.7, return_route_knockback),
        "SFX_ReturnRoutePursuitTail_v0": (2.6, return_route_pursuit_tail),
        "SFX_MonitorCheckGlitch_v0": (0.72, monitor_check_glitch),
        "SFX_PostReportMonitorMismatch_v0": (1.55, post_report_monitor_mismatch),
        "SFX_PostReportDeskWaitRattle_v0": (1.65, post_report_desk_wait_rattle),
        "SFX_PostReportLogSelfCorrection_v0": (1.25, post_report_log_self_correction),
    }

    output: dict[str, pathlib.Path] = {}
    for name, (seconds, sample_func) in sources.items():
        path = SOURCE_AUDIO_DIR / f"{name}.wav"
        write_wav(path, seconds, sample_func)
        output[name] = path
    return output


def import_audio(source_paths: dict[str, pathlib.Path]) -> dict[str, unreal.SoundWave]:
    tasks = []
    sounds: dict[str, unreal.SoundWave] = {}
    for name, path in source_paths.items():
        asset_path = f"/Game/Hotel/Audio/{name}"
        existing_asset = (
            unreal.EditorAssetLibrary.load_asset(asset_path)
            if unreal.EditorAssetLibrary.does_asset_exist(asset_path)
            else None
        )
        if existing_asset:
            sounds[name] = existing_asset
            continue
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", str(path))
        task.set_editor_property("destination_path", "/Game/Hotel/Audio")
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        tasks.append(task)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    for name in source_paths:
        if name in sounds:
            continue
        asset = unreal.EditorAssetLibrary.load_asset(f"/Game/Hotel/Audio/{name}")
        if asset:
            sounds[name] = asset
    return sounds


def write_obj(
    path: pathlib.Path,
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    uv_axes: tuple[str, str] = ("x", "y"),
    fit_uv: bool = False,
) -> bool:
    axis_index = {"x": 0, "y": 1, "z": 2}
    u_axis, v_axis = axis_index[uv_axes[0]], axis_index[uv_axes[1]]
    u_values = [vertex[u_axis] for vertex in vertices]
    v_values = [vertex[v_axis] for vertex in vertices]
    min_u, max_u = min(u_values, default=-100.0), max(u_values, default=100.0)
    min_v, max_v = min(v_values, default=-100.0), max(v_values, default=100.0)
    span_u = max(max_u - min_u, 1.0)
    span_v = max(max_v - min_v, 1.0)

    lines = [
        "# Project-authored procedural mesh for Hotel Night Shift Horror.\n",
        "# Generated by Automation/Unreal/create_hotel_spine_slice.py; no third-party geometry.\n",
    ]
    for x, y, z in vertices:
        lines.append(f"v {x:.5f} {y:.5f} {z:.5f}\n")
    for vertex in vertices:
        if fit_uv:
            u = (vertex[u_axis] - min_u) / span_u
            v = (vertex[v_axis] - min_v) / span_v
        else:
            u = (vertex[u_axis] + 100.0) / 200.0
            v = (vertex[v_axis] + 100.0) / 200.0
        lines.append(f"vt {u:.5f} {v:.5f}\n")
    for face in faces:
        lines.append("f " + " ".join(f"{index + 1}/{index + 1}" for index in face) + "\n")

    next_contents = "".join(lines)
    if path.exists() and path.read_text(encoding="utf-8") == next_contents:
        return False

    path.write_text(next_contents, encoding="utf-8", newline="\n")
    return True


def append_box(
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    center: tuple[float, float, float],
    size: tuple[float, float, float],
) -> None:
    x, y, z = center
    sx, sy, sz = size[0] * 0.5, size[1] * 0.5, size[2] * 0.5
    base = len(vertices)
    vertices.extend([
        (x - sx, y - sy, z - sz),
        (x + sx, y - sy, z - sz),
        (x + sx, y + sy, z - sz),
        (x - sx, y + sy, z - sz),
        (x - sx, y - sy, z + sz),
        (x + sx, y - sy, z + sz),
        (x + sx, y + sy, z + sz),
        (x - sx, y + sy, z + sz),
    ])
    faces.extend([
        (base + 0, base + 1, base + 2, base + 3),
        (base + 4, base + 7, base + 6, base + 5),
        (base + 0, base + 4, base + 5, base + 1),
        (base + 1, base + 5, base + 6, base + 2),
        (base + 2, base + 6, base + 7, base + 3),
        (base + 3, base + 7, base + 4, base + 0),
    ])


def rounded_ring(width: float, depth: float, z: float, segments: int = 32, power: float = 0.36) -> list[tuple[float, float, float]]:
    points: list[tuple[float, float, float]] = []
    for index in range(segments):
        theta = 2.0 * math.pi * index / segments
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        x = math.copysign(abs(cos_t) ** power, cos_t) * width * 0.5
        y = math.copysign(abs(sin_t) ** power, sin_t) * depth * 0.5
        points.append((x, y, z))
    return points


def create_phone_body_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    segments = 32
    rings = [
        rounded_ring(106.0, 72.0, -12.0, segments),
        rounded_ring(112.0, 76.0, -4.0, segments),
        rounded_ring(92.0, 62.0, 8.0, segments),
        rounded_ring(64.0, 48.0, 18.0, segments),
    ]
    vertices = [vertex for ring in rings for vertex in ring]
    faces: list[tuple[int, ...]] = []
    for ring_index in range(len(rings) - 1):
        base = ring_index * segments
        next_base = (ring_index + 1) * segments
        for index in range(segments):
            faces.append((base + index, base + ((index + 1) % segments), next_base + ((index + 1) % segments), next_base + index))
    faces.append(tuple(reversed(range(segments))))
    top_base = (len(rings) - 1) * segments
    faces.append(tuple(top_base + index for index in range(segments)))
    return vertices, faces


def create_receiver_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    length_segments = 18
    radial_segments = 12
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for length_index in range(length_segments + 1):
        u = length_index / length_segments
        x = -50.0 + 100.0 * u
        arch = math.sin(math.pi * u)
        end_weight = 1.0 - arch
        center_y = -5.5 * arch
        center_z = 5.5 * arch
        radius_y = 7.8 + 9.2 * end_weight
        radius_z = 5.6 + 7.4 * end_weight
        for radial_index in range(radial_segments):
            theta = 2.0 * math.pi * radial_index / radial_segments
            vertices.append((
                x,
                center_y + math.cos(theta) * radius_y,
                center_z + math.sin(theta) * radius_z,
            ))

    for length_index in range(length_segments):
        base = length_index * radial_segments
        next_base = (length_index + 1) * radial_segments
        for radial_index in range(radial_segments):
            faces.append((
                base + radial_index,
                base + ((radial_index + 1) % radial_segments),
                next_base + ((radial_index + 1) % radial_segments),
                next_base + radial_index,
            ))
    faces.append(tuple(reversed(range(radial_segments))))
    end_base = length_segments * radial_segments
    faces.append(tuple(end_base + index for index in range(radial_segments)))
    return vertices, faces


def create_coiled_cord_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    path_segments = 72
    radial_segments = 8
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for path_index in range(path_segments + 1):
        u = path_index / path_segments
        theta = 2.0 * math.pi * 6.0 * u
        center = (
            -50.0 + 100.0 * u,
            math.sin(theta) * 10.0,
            math.cos(theta) * 6.0,
        )
        for radial_index in range(radial_segments):
            radial_theta = 2.0 * math.pi * radial_index / radial_segments
            vertices.append((
                center[0],
                center[1] + math.cos(radial_theta) * 2.6,
                center[2] + math.sin(radial_theta) * 2.6,
            ))

    for path_index in range(path_segments):
        base = path_index * radial_segments
        next_base = (path_index + 1) * radial_segments
        for radial_index in range(radial_segments):
            faces.append((
                base + radial_index,
                base + ((radial_index + 1) % radial_segments),
                next_base + ((radial_index + 1) % radial_segments),
                next_base + radial_index,
            ))
    return vertices, faces


def create_curled_pages_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    columns = 12
    rows = 8
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for layer_z in (0.0, -4.0):
        for row in range(rows + 1):
            y_norm = row / rows
            y = -35.0 + 70.0 * y_norm
            for column in range(columns + 1):
                x_norm = column / columns
                x = -50.0 + 100.0 * x_norm
                right_curl = max(0.0, x_norm - 0.72) ** 2 * 38.0
                lower_corner = max(0.0, 0.18 - y_norm) ** 2 * 34.0
                page_wave = math.sin(x_norm * math.pi * 2.0) * math.sin(y_norm * math.pi) * 1.2
                z = layer_z + (right_curl + lower_corner + page_wave if layer_z == 0.0 else 0.0)
                vertices.append((x, y, z))

    stride = columns + 1
    top_offset = 0
    bottom_offset = (rows + 1) * stride
    for row in range(rows):
        for column in range(columns):
            a = top_offset + row * stride + column
            b = a + 1
            c = a + stride + 1
            d = a + stride
            faces.append((a, b, c, d))
            faces.append((bottom_offset + d, bottom_offset + c, bottom_offset + b, bottom_offset + a))

    for column in range(columns):
        top_a = top_offset + column
        top_b = top_a + 1
        bottom_a = bottom_offset + column
        bottom_b = bottom_a + 1
        faces.append((bottom_a, bottom_b, top_b, top_a))

        top_c = top_offset + rows * stride + column
        top_d = top_c + 1
        bottom_c = bottom_offset + rows * stride + column
        bottom_d = bottom_c + 1
        faces.append((top_c, top_d, bottom_d, bottom_c))

    for row in range(rows):
        top_a = top_offset + row * stride
        top_b = top_a + stride
        bottom_a = bottom_offset + row * stride
        bottom_b = bottom_a + stride
        faces.append((top_a, top_b, bottom_b, bottom_a))

        top_c = top_offset + row * stride + columns
        top_d = top_c + stride
        bottom_c = bottom_offset + row * stride + columns
        bottom_d = bottom_c + stride
        faces.append((bottom_c, bottom_d, top_d, top_c))

    return vertices, faces


def create_frontdesk_log_pen_body_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    length_segments = 20
    radial_segments = 10
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for length_index in range(length_segments + 1):
        u = length_index / length_segments
        x = -42.0 + 84.0 * u
        center_y = math.sin(u * math.pi) * -1.6
        center_z = math.sin(u * math.pi) * 1.4
        radius_y = 3.8 + 0.9 * math.sin(u * math.pi)
        radius_z = 3.2 + 0.6 * math.sin(u * math.pi)
        for radial_index in range(radial_segments):
            theta = 2.0 * math.pi * radial_index / radial_segments
            vertices.append((
                x,
                center_y + math.cos(theta) * radius_y,
                center_z + math.sin(theta) * radius_z,
            ))

    for length_index in range(length_segments):
        base = length_index * radial_segments
        next_base = (length_index + 1) * radial_segments
        for radial_index in range(radial_segments):
            faces.append((
                base + radial_index,
                base + ((radial_index + 1) % radial_segments),
                next_base + ((radial_index + 1) % radial_segments),
                next_base + radial_index,
            ))
    faces.append(tuple(reversed(range(radial_segments))))
    end_base = length_segments * radial_segments
    faces.append(tuple(end_base + index for index in range(radial_segments)))

    append_box(vertices, faces, (-8.0, -5.2, 5.1), (36.0, 1.4, 1.2))
    append_box(vertices, faces, (22.0, 3.4, 0.0), (8.0, 1.2, 7.0))
    return vertices, faces


def create_frontdesk_log_pen_nib_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_flat_polygon(
        vertices,
        faces,
        [
            (-12.0, -0.7, -4.0),
            (8.0, -0.8, -3.0),
            (18.0, -0.9, 0.0),
            (8.0, -0.8, 3.0),
            (-12.0, -0.7, 4.0),
        ],
        double_sided=True,
    )
    append_planar_stroke(vertices, faces, [(-6.0, 0.0), (10.0, 0.0)], 0.7, 0.4, y=-1.1)
    return vertices, faces


def create_frontdesk_report_log_filed_paper_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    columns = 5
    rows = 7
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    for row in range(rows + 1):
        v = row / rows
        for column in range(columns + 1):
            u = column / columns
            edge = 1.0 if row in (0, rows) or column in (0, columns) else 0.0
            x = -55.0 + 110.0 * u + math.sin(row * 1.7 + column * 0.9) * edge * 1.3
            y = -38.0 + 76.0 * v + math.sin(row * 0.8 + column * 1.3) * edge * 0.9
            z = 0.5 + 1.8 * edge * max(0.0, v - 0.78) + 0.35 * math.sin(u * math.pi) * math.sin(v * math.pi)
            vertices.append((x, y, z))

    stride = columns + 1
    for row in range(rows):
        for column in range(columns):
            a = row * stride + column
            b = a + 1
            c = a + stride + 1
            d = a + stride
            faces.append((a, b, c, d))
    return vertices, faces


def create_frontdesk_filed_stamp_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_box(vertices, faces, (0.0, 0.0, -2.0), (44.0, 20.0, 5.0))
    append_box(vertices, faces, (0.0, -1.0, 6.0), (35.0, 15.0, 8.0))
    append_box(vertices, faces, (0.0, -2.0, 18.0), (24.0, 10.0, 18.0))
    append_box(vertices, faces, (0.0, -2.8, 31.0), (34.0, 8.0, 7.0))
    append_planar_stroke(vertices, faces, [(-16.0, -6.0), (14.0, -6.0)], 1.4, 0.5, y=-11.0)
    append_planar_stroke(vertices, faces, [(-15.0, 0.0), (12.0, 0.0)], 1.1, 1.5, y=-11.1)
    append_planar_stroke(vertices, faces, [(-13.0, 6.0), (16.0, 6.0)], 1.2, 2.5, y=-11.2)
    return vertices, faces


def create_frontdesk_report_filed_ink_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_planar_stroke_xy(vertices, faces, [(-28.0, 8.0), (-12.0, 10.0), (8.0, 7.0), (30.0, 10.0)], 1.4, 0.3, z=0.32)
    append_planar_stroke_xy(vertices, faces, [(-28.0, 0.0), (-8.0, -2.0), (14.0, 1.0), (28.0, -2.0)], 1.1, 1.4, z=0.34)
    append_planar_stroke_xy(vertices, faces, [(-24.0, -9.0), (-4.0, -7.0), (18.0, -10.0)], 1.0, 2.3, z=0.36)
    append_planar_stroke_xy(vertices, faces, [(-32.0, 16.0), (-18.0, -16.0)], 1.7, 3.1, z=0.38)
    append_planar_blob_xy(vertices, faces, 21.0, -13.0, 8.0, 3.0, 9, 1.9, z=0.40)
    return vertices, faces


def create_room203_paneled_door_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_box(vertices, faces, (0.0, 0.0, 0.0), (260.0, 8.0, 240.0))
    append_box(vertices, faces, (0.0, -6.0, 112.0), (246.0, 6.0, 16.0))
    append_box(vertices, faces, (0.0, -6.0, -112.0), (246.0, 6.0, 16.0))
    append_box(vertices, faces, (-122.0, -6.0, 0.0), (16.0, 6.0, 224.0))
    append_box(vertices, faces, (122.0, -6.0, 0.0), (16.0, 6.0, 224.0))
    append_box(vertices, faces, (0.0, -7.0, 46.0), (166.0, 7.0, 14.0))
    append_box(vertices, faces, (0.0, -7.0, -52.0), (166.0, 7.0, 14.0))
    append_box(vertices, faces, (-90.0, -7.0, -3.0), (14.0, 7.0, 112.0))
    append_box(vertices, faces, (90.0, -7.0, -3.0), (14.0, 7.0, 112.0))
    append_box(vertices, faces, (0.0, -9.0, 0.0), (138.0, 3.0, 70.0))
    append_box(vertices, faces, (0.0, -9.0, -72.0), (138.0, 3.0, 44.0))
    append_box(vertices, faces, (98.0, -9.5, 10.0), (6.0, 4.0, 168.0))
    return vertices, faces


def create_room203_chain_links_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    path_segments = 18
    radial_segments = 8

    def append_link(center_x: float, center_z: float, radius_x: float, radius_z: float, tube_radius: float) -> None:
        base = len(vertices)
        for path_index in range(path_segments):
            theta = 2.0 * math.pi * path_index / path_segments
            normal_x = math.cos(theta)
            normal_z = math.sin(theta)
            path_x = center_x + normal_x * radius_x
            path_z = center_z + normal_z * radius_z
            for radial_index in range(radial_segments):
                phi = 2.0 * math.pi * radial_index / radial_segments
                vertices.append((
                    path_x + normal_x * math.cos(phi) * tube_radius,
                    math.sin(phi) * tube_radius,
                    path_z + normal_z * math.cos(phi) * tube_radius,
                ))
        for path_index in range(path_segments):
            next_path = (path_index + 1) % path_segments
            for radial_index in range(radial_segments):
                faces.append((
                    base + path_index * radial_segments + radial_index,
                    base + path_index * radial_segments + ((radial_index + 1) % radial_segments),
                    base + next_path * radial_segments + ((radial_index + 1) % radial_segments),
                    base + next_path * radial_segments + radial_index,
                ))

    for index, center_x in enumerate((-36.0, -18.0, 0.0, 18.0, 36.0)):
        if index % 2 == 0:
            append_link(center_x, 0.0, 10.0, 6.0, 2.4)
        else:
            append_link(center_x, 0.0, 6.0, 10.0, 2.4)
    return vertices, faces


def create_room203_torn_notice_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    columns = 5
    rows = 4
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    for row in range(rows + 1):
        z_norm = row / rows
        for column in range(columns + 1):
            x_norm = column / columns
            edge_bias = 1.0 if column in (0, columns) or row in (0, rows) else 0.0
            x = -34.0 + 68.0 * x_norm + math.sin(row * 1.7 + column * 0.9) * edge_bias * 2.6
            z = -24.0 + 48.0 * z_norm + math.sin(column * 1.1 + row * 0.5) * edge_bias * 2.0
            curled_corner = max(0.0, x_norm - 0.72) ** 2 * 9.0 + max(0.0, 0.22 - z_norm) ** 2 * 7.0
            y = -curled_corner
            vertices.append((x, y, z))

    stride = columns + 1
    for row in range(rows):
        for column in range(columns):
            a = row * stride + column
            b = a + 1
            c = a + stride + 1
            d = a + stride
            faces.append((a, b, c, d))
    return vertices, faces


def create_room203_handle_lever_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    length_segments = 18
    radial_segments = 10
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_box(vertices, faces, (18.0, 1.0, 0.0), (18.0, 6.0, 62.0))
    tube_base = len(vertices)
    for length_index in range(length_segments + 1):
        u = length_index / length_segments
        x = 8.0 - 70.0 * u
        center_y = -4.0 - math.sin(math.pi * u) * 6.0
        center_z = -8.0 * math.sin(math.pi * u)
        radius = 3.2 + (1.0 - math.sin(math.pi * u)) * 1.2
        for radial_index in range(radial_segments):
            theta = 2.0 * math.pi * radial_index / radial_segments
            vertices.append((
                x,
                center_y + math.cos(theta) * radius,
                center_z + math.sin(theta) * radius,
            ))
    for length_index in range(length_segments):
        base = tube_base + length_index * radial_segments
        next_base = tube_base + (length_index + 1) * radial_segments
        for radial_index in range(radial_segments):
            faces.append((
                base + radial_index,
                base + ((radial_index + 1) % radial_segments),
                next_base + ((radial_index + 1) % radial_segments),
                next_base + radial_index,
            ))
    faces.append(tuple(reversed(range(tube_base, tube_base + radial_segments))))
    end_base = tube_base + length_segments * radial_segments
    faces.append(tuple(end_base + index for index in range(radial_segments)))
    return vertices, faces


def append_planar_stroke(
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    points: list[tuple[float, float]],
    thickness: float,
    phase: float,
    y: float = -0.4,
) -> None:
    base = len(vertices)
    for index, (x, z) in enumerate(points):
        if index == 0:
            dx, dz = points[1][0] - x, points[1][1] - z
        elif index == len(points) - 1:
            dx, dz = x - points[index - 1][0], z - points[index - 1][1]
        else:
            dx, dz = points[index + 1][0] - points[index - 1][0], points[index + 1][1] - points[index - 1][1]
        length = math.sqrt(dx * dx + dz * dz) or 1.0
        px, pz = -dz / length, dx / length
        wobble = math.sin(index * 1.37 + phase) * thickness * 0.10
        half = thickness * (0.54 + 0.10 * math.cos(index * 1.11 + phase))
        vertices.append((x + px * (half + wobble), y, z + pz * (half + wobble)))
        vertices.append((x - px * (half - wobble * 0.35), y - 0.05, z - pz * (half - wobble * 0.35)))

    for index in range(len(points) - 1):
        a = base + index * 2
        b = a + 1
        c = a + 3
        d = a + 2
        faces.append((a, b, c, d))
        faces.append((d, c, b, a))


def append_planar_stroke_xy(
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    points: list[tuple[float, float]],
    thickness: float,
    phase: float,
    z: float = 0.3,
) -> None:
    base = len(vertices)
    for index, (x, y) in enumerate(points):
        if index == 0:
            dx, dy = points[1][0] - x, points[1][1] - y
        elif index == len(points) - 1:
            dx, dy = x - points[index - 1][0], y - points[index - 1][1]
        else:
            dx, dy = points[index + 1][0] - points[index - 1][0], points[index + 1][1] - points[index - 1][1]
        length = math.sqrt(dx * dx + dy * dy) or 1.0
        px, py = -dy / length, dx / length
        wobble = math.sin(index * 1.37 + phase) * thickness * 0.10
        half = thickness * (0.54 + 0.10 * math.cos(index * 1.11 + phase))
        vertices.append((x + px * (half + wobble), y + py * (half + wobble), z))
        vertices.append((x - px * (half - wobble * 0.35), y - py * (half - wobble * 0.35), z + 0.02))

    for index in range(len(points) - 1):
        a = base + index * 2
        b = a + 1
        c = a + 3
        d = a + 2
        faces.append((a, b, c, d))
        faces.append((d, c, b, a))


def append_planar_blob(
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    center_x: float,
    center_z: float,
    radius_x: float,
    radius_z: float,
    count: int,
    phase: float,
    y: float = -0.45,
) -> None:
    points: list[tuple[float, float, float]] = []
    for index in range(count):
        theta = 2.0 * math.pi * index / count
        wobble = 1.0 + 0.10 * math.sin(index * 1.71 + phase) + 0.07 * math.cos(index * 2.43 + phase)
        points.append((center_x + math.cos(theta) * radius_x * wobble, y, center_z + math.sin(theta) * radius_z * wobble))
    append_flat_polygon(vertices, faces, points, double_sided=True)


def append_planar_blob_xy(
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    center_x: float,
    center_y: float,
    radius_x: float,
    radius_y: float,
    count: int,
    phase: float,
    z: float = 0.3,
) -> None:
    points: list[tuple[float, float, float]] = []
    for index in range(count):
        theta = 2.0 * math.pi * index / count
        wobble = 1.0 + 0.10 * math.sin(index * 1.71 + phase) + 0.07 * math.cos(index * 2.43 + phase)
        points.append((center_x + math.cos(theta) * radius_x * wobble, center_y + math.sin(theta) * radius_y * wobble, z))
    append_flat_polygon(vertices, faces, points, double_sided=True)


def append_planar_stroke_yz(
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    points: list[tuple[float, float]],
    thickness: float,
    phase: float,
    plane_x: float = 0.0,
) -> None:
    base = len(vertices)
    for index, (y, z) in enumerate(points):
        if index == 0:
            dy, dz = points[1][0] - y, points[1][1] - z
        elif index == len(points) - 1:
            dy, dz = y - points[index - 1][0], z - points[index - 1][1]
        else:
            dy, dz = points[index + 1][0] - points[index - 1][0], points[index + 1][1] - points[index - 1][1]
        length = math.sqrt(dy * dy + dz * dz) or 1.0
        py, pz = -dz / length, dy / length
        wobble = math.sin(index * 1.47 + phase) * thickness * 0.14
        half = thickness * (0.54 + 0.13 * math.cos(index * 1.23 + phase))
        vertices.append((plane_x, y + py * (half + wobble), z + pz * (half + wobble)))
        vertices.append((plane_x - 0.08, y - py * (half - wobble * 0.40), z - pz * (half - wobble * 0.40)))

    for index in range(len(points) - 1):
        a = base + index * 2
        b = a + 1
        c = a + 3
        d = a + 2
        faces.append((a, b, c, d))
        faces.append((d, c, b, a))


def append_planar_blob_yz(
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    center_y: float,
    center_z: float,
    radius_y: float,
    radius_z: float,
    count: int,
    phase: float,
    plane_x: float = 0.0,
) -> None:
    points: list[tuple[float, float, float]] = []
    for index in range(count):
        theta = 2.0 * math.pi * index / count
        wobble = 1.0 + 0.12 * math.sin(index * 1.71 + phase) + 0.08 * math.cos(index * 2.31 + phase)
        points.append((plane_x, center_y + math.cos(theta) * radius_y * wobble, center_z + math.sin(theta) * radius_z * wobble))
    append_flat_polygon(vertices, faces, points, double_sided=True)


def create_room203_number_digits_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_plate_bar(center_x: float, center_z: float, width: float, height: float, y: float = -0.48) -> None:
        append_flat_polygon(
            vertices,
            faces,
            [
                (center_x - width * 0.5, y, center_z - height * 0.5),
                (center_x + width * 0.5, y, center_z - height * 0.5),
                (center_x + width * 0.5, y, center_z + height * 0.5),
                (center_x - width * 0.5, y, center_z + height * 0.5),
            ],
            double_sided=True,
        )

    def append_digit(center_x: float, segments: tuple[str, ...]) -> None:
        segment_shapes = {
            "top": (center_x, 11.0, 21.0, 3.2),
            "mid": (center_x, 0.0, 21.0, 3.0),
            "bottom": (center_x, -11.0, 21.0, 3.2),
            "ul": (center_x - 10.0, 5.7, 3.2, 12.0),
            "ur": (center_x + 10.0, 5.7, 3.2, 12.0),
            "ll": (center_x - 10.0, -5.7, 3.2, 12.0),
            "lr": (center_x + 10.0, -5.7, 3.2, 12.0),
        }
        for name in segments:
            append_plate_bar(*segment_shapes[name])

    # Room number is authored as geometry, not font/text, so the public repo has no font dependency.
    append_digit(-24.0, ("top", "ur", "mid", "ll", "bottom"))
    append_digit(0.0, ("top", "ul", "ur", "ll", "lr", "bottom"))
    append_digit(24.0, ("top", "ur", "mid", "lr", "bottom"))
    return vertices, faces


def create_room203_door_grime_streaks_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    streaks = [
        [(-105.0, 105.0), (-108.0, 70.0), (-102.0, 34.0), (-111.0, -8.0)],
        [(-74.0, 74.0), (-70.0, 38.0), (-76.0, -3.0), (-69.0, -58.0)],
        [(-32.0, 34.0), (-36.0, 4.0), (-31.0, -42.0)],
        [(18.0, 96.0), (14.0, 56.0), (21.0, 18.0), (12.0, -20.0)],
        [(66.0, 52.0), (72.0, 22.0), (64.0, -8.0), (70.0, -56.0)],
        [(100.0, 86.0), (94.0, 44.0), (103.0, 2.0), (98.0, -74.0)],
    ]
    for index, points in enumerate(streaks):
        append_planar_stroke(vertices, faces, points, 1.35 + 0.25 * (index % 2), index * 0.7, y=-0.50)
    append_planar_stroke(vertices, faces, [(-82.0, -95.0), (-34.0, -88.0), (28.0, -96.0), (78.0, -84.0)], 2.1, 4.8, y=-0.52)
    return vertices, faces


def create_room203_door_paint_chips_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    for center_x, center_z, radius_x, radius_z, count, phase in (
        (-116.0, 70.0, 7.5, 24.0, 10, 0.2),
        (-116.0, -46.0, 8.0, 32.0, 11, 1.1),
        (116.0, 28.0, 8.0, 36.0, 12, 2.0),
        (80.0, -66.0, 15.0, 6.0, 10, 2.9),
        (-18.0, 82.0, 10.0, 5.5, 9, 3.8),
        (36.0, -6.0, 8.0, 5.0, 8, 4.6),
    ):
        append_planar_blob(vertices, faces, center_x, center_z, radius_x, radius_z, count, phase, y=-0.60)
    return vertices, faces


def create_room203_lock_hardware_breakup_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_planar_blob(vertices, faces, 0.0, 46.0, 12.0, 12.0, 18, 0.1, y=-0.70)
    append_planar_blob(vertices, faces, 0.0, 0.0, 9.5, 9.5, 16, 0.8, y=-0.70)
    append_planar_stroke(vertices, faces, [(-6.0, 0.0), (7.0, 0.0)], 1.8, 1.2, y=-0.76)
    append_planar_stroke(vertices, faces, [(0.0, 6.0), (0.0, -6.0)], 1.2, 1.6, y=-0.77)
    append_planar_stroke(vertices, faces, [(-11.0, -31.0), (8.0, -29.0), (16.0, -20.0)], 2.2, 2.2, y=-0.72)
    for screw_x, screw_z, phase in ((-8.0, 62.0, 2.9), (8.0, 30.0, 3.4), (-8.0, -58.0, 4.2), (8.0, -42.0, 4.8)):
        append_planar_blob(vertices, faces, screw_x, screw_z, 2.8, 2.8, 10, phase, y=-0.78)
    return vertices, faces


def create_room203_sconce_glass_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_planar_blob(vertices, faces, -7.0, 2.0, 13.0, 28.0, 22, 0.4, y=-0.62)
    append_planar_blob(vertices, faces, 10.0, 0.0, 10.0, 23.0, 19, 1.6, y=-0.66)
    append_planar_stroke(vertices, faces, [(-18.0, -24.0), (-4.0, -29.0), (12.0, -25.0)], 2.2, 2.5, y=-0.70)
    return vertices, faces


def create_room203_sconce_bracket_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_planar_stroke(vertices, faces, [(-25.0, 30.0), (-20.0, 6.0), (-24.0, -28.0)], 3.0, 0.2, y=-0.72)
    append_planar_stroke(vertices, faces, [(24.0, 28.0), (20.0, 4.0), (22.0, -26.0)], 2.6, 1.0, y=-0.73)
    append_planar_stroke(vertices, faces, [(-16.0, 2.0), (0.0, -5.0), (17.0, 1.0)], 3.0, 1.8, y=-0.74)
    append_planar_blob(vertices, faces, 0.0, -34.0, 8.0, 5.0, 14, 2.4, y=-0.76)
    return vertices, faces


def create_room203_notice_writing_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    strokes = [
        [(-24.0, 13.0), (-10.0, 12.0), (5.0, 14.0), (24.0, 10.0)],
        [(-21.0, 5.0), (-4.0, 7.0), (15.0, 4.0), (26.0, 6.0)],
        [(-26.0, -3.0), (-8.0, -2.0), (9.0, -5.0), (22.0, -3.0)],
        [(-18.0, -12.0), (-2.0, -10.0), (14.0, -14.0)],
    ]
    for index, points in enumerate(strokes):
        append_planar_stroke(vertices, faces, points, 0.75 + 0.1 * (index % 2), index * 0.8, y=-0.78)
    append_planar_stroke(vertices, faces, [(-12.0, 18.0), (6.0, -18.0)], 1.4, 4.1, y=-0.80)
    return vertices, faces


def create_room203_notice_tape_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    strip = [
        (-30.0, 3.0, 0.0),
        (-18.0, 5.0, 0.0),
        (-4.0, 2.0, 0.0),
        (10.0, 5.0, 0.0),
        (32.0, 2.0, 0.0),
        (31.0, -5.0, 0.0),
        (12.0, -4.0, 0.0),
        (-2.0, -7.0, 0.0),
        (-17.0, -4.0, 0.0),
        (-32.0, -6.0, 0.0),
    ]
    append_flat_polygon(vertices, faces, [(x, -0.75, z) for x, z, _ in strip], double_sided=True)
    return vertices, faces


def create_guesthall_service_cart_silhouette_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_box(vertices, faces, (0.0, 0.0, -30.0), (128.0, 44.0, 7.0))
    append_box(vertices, faces, (-56.0, -18.0, 4.0), (6.0, 6.0, 76.0))
    append_box(vertices, faces, (54.0, -18.0, 2.0), (6.0, 6.0, 70.0))
    append_box(vertices, faces, (0.0, -18.0, 39.0), (116.0, 6.0, 5.0))
    append_box(vertices, faces, (-42.0, 18.0, 8.0), (5.0, 6.0, 62.0))
    append_box(vertices, faces, (38.0, 18.0, 6.0), (5.0, 6.0, 58.0))
    append_box(vertices, faces, (-3.0, 18.0, 30.0), (84.0, 6.0, 5.0))
    cloth_front = [
        (-48.0, -24.0, 31.0),
        (-28.0, -25.0, 43.0),
        (-3.0, -23.0, 36.0),
        (22.0, -26.0, 44.0),
        (49.0, -24.0, 29.0),
        (43.0, -25.0, -11.0),
        (19.0, -27.0, -27.0),
        (-8.0, -26.0, -21.0),
        (-36.0, -24.0, -32.0),
        (-53.0, -25.0, -8.0),
    ]
    append_flat_polygon(vertices, faces, cloth_front, double_sided=True)
    cloth_side = [
        (48.0, -20.0, 28.0),
        (58.0, -2.0, 23.0),
        (52.0, 18.0, 7.0),
        (48.0, 15.0, -18.0),
        (43.0, -24.0, -11.0),
    ]
    append_flat_polygon(vertices, faces, cloth_side, double_sided=True)
    for wheel_x, wheel_y in ((-45.0, -24.0), (43.0, -24.0), (-36.0, 22.0), (34.0, 20.0)):
        append_planar_blob(vertices, faces, wheel_x, -38.0, 7.0, 7.0, 14, wheel_x * 0.02, y=wheel_y)
    return vertices, faces


def append_flat_polygon(
    vertices: list[tuple[float, float, float]],
    faces: list[tuple[int, ...]],
    points: list[tuple[float, float, float]],
    double_sided: bool = False,
) -> None:
    base = len(vertices)
    vertices.extend(points)
    for index in range(1, len(points) - 1):
        faces.append((base, base + index, base + index + 1))
        if double_sided:
            faces.append((base + index + 1, base + index, base))


def create_guesthall_peeling_wallpaper_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    columns = 5
    rows = 6
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    for row in range(rows + 1):
        z_norm = row / rows
        for column in range(columns + 1):
            x_norm = column / columns
            ragged = 1.0 if column in (0, columns) or row in (0, rows) else 0.0
            lower_curl = max(0.0, 0.28 - z_norm) ** 2 * 18.0
            side_curl = max(0.0, x_norm - 0.72) ** 2 * 14.0
            x = -58.0 + 116.0 * x_norm + math.sin(row * 1.31 + column * 0.77) * ragged * 5.5
            z = -76.0 + 152.0 * z_norm + math.sin(column * 1.13 + row * 0.61) * ragged * 4.5
            y = -(lower_curl + side_curl)
            vertices.append((x, y, z))

    stride = columns + 1
    for row in range(rows):
        for column in range(columns):
            a = row * stride + column
            b = a + 1
            c = a + stride + 1
            d = a + stride
            faces.append((a, b, c, d))
    return vertices, faces


def create_guesthall_room203_aftershock_paper_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_strip(
        center_x: float,
        top_z: float,
        width: float,
        height: float,
        curl: float,
        phase: float,
        columns: int = 4,
        rows: int = 8,
    ) -> None:
        base = len(vertices)
        for row in range(rows + 1):
            v = row / rows
            taper = 1.0 - 0.32 * v
            for column in range(columns + 1):
                u = column / columns
                edge = abs(u - 0.5) * 2.0
                ragged = math.sin(row * 1.71 + column * 0.83 + phase) * (0.8 + 2.8 * edge)
                x = center_x + (u - 0.5) * width * taper + ragged
                z = top_z - height * v + math.sin(u * math.pi + phase) * 2.2 * edge
                y = -(curl * 0.18 * (v ** 1.65) + 0.85 * edge * v + math.sin(v * math.pi * 2.0 + phase) * 0.45)
                vertices.append((x, y, z))

        stride = columns + 1
        for row in range(rows):
            for column in range(columns):
                a = base + row * stride + column
                b = a + 1
                c = a + stride + 1
                d = a + stride
                faces.append((a, b, c, d))
                faces.append((d, c, b, a))

    append_strip(-50.0, 82.0, 22.0, 132.0, 31.0, 0.1, columns=4, rows=9)
    append_strip(-23.0, 75.0, 17.0, 96.0, 24.0, 0.9, columns=3, rows=8)
    append_strip(5.0, 86.0, 20.0, 116.0, 28.0, 1.6, columns=4, rows=9)
    append_strip(31.0, 70.0, 16.0, 84.0, 22.0, 2.4, columns=3, rows=7)
    append_strip(52.0, 54.0, 13.0, 64.0, 16.0, 3.2, columns=3, rows=6)
    return vertices, faces


def create_guesthall_room203_aftershock_shadow_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_backing_island(
        center_x: float,
        center_z: float,
        width: float,
        height: float,
        phase: float,
        rows: int,
        columns: int,
    ) -> None:
        base = len(vertices)
        for row in range(rows + 1):
            v = row / rows
            pinch = 1.0 - 0.22 * math.sin(v * math.pi + phase)
            left_bias = math.sin(row * 1.41 + phase) * 4.0
            for column in range(columns + 1):
                u = column / columns
                edge_weight = abs(u - 0.5) * 2.0
                ragged = math.sin(row * 1.29 + column * 2.11 + phase) * (1.0 + edge_weight * 3.2)
                x = center_x + (u - 0.5) * width * pinch + left_bias + ragged
                z = center_z + (0.5 - v) * height + math.cos(column * 1.37 + row * 0.67 + phase) * (1.4 + edge_weight * 2.0)
                y = -1.2 - edge_weight * 0.9 - 0.28 * math.sin(row + column + phase)
                vertices.append((x, y, z))

        stride = columns + 1
        for row in range(rows):
            for column in range(columns):
                a = base + row * stride + column
                b = a + 1
                c = a + stride + 1
                d = a + stride
                faces.append((a, b, c, d))
                faces.append((d, c, b, a))

    append_backing_island(-38.0, 22.0, 46.0, 128.0, 0.2, rows=7, columns=3)
    append_backing_island(5.0, 2.0, 38.0, 146.0, 1.1, rows=8, columns=3)
    append_backing_island(39.0, -12.0, 30.0, 104.0, 2.0, rows=6, columns=3)
    append_backing_island(12.0, 66.0, 74.0, 34.0, 3.0, rows=3, columns=5)
    return vertices, faces


def create_guesthall_room203_aftershock_raw_edge_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_ragged_ribbon(points: list[tuple[float, float]], thickness: float, phase: float) -> None:
        base = len(vertices)
        for index, (x, z) in enumerate(points):
            if index == 0:
                nx, nz = points[1][0] - x, points[1][1] - z
            elif index == len(points) - 1:
                nx, nz = x - points[index - 1][0], z - points[index - 1][1]
            else:
                nx, nz = points[index + 1][0] - points[index - 1][0], points[index + 1][1] - points[index - 1][1]
            length = math.sqrt(nx * nx + nz * nz) or 1.0
            px, pz = -nz / length, nx / length
            wobble = math.sin(index * 1.73 + phase) * 1.4
            half = thickness * (0.58 + 0.20 * math.sin(index * 0.91 + phase))
            y_lift = -0.35 - 0.35 * math.cos(index * 0.77 + phase)
            vertices.append((x + px * (half + wobble), y_lift - 0.7, z + pz * (half + wobble)))
            vertices.append((x - px * (half - wobble * 0.4), y_lift, z - pz * (half - wobble * 0.4)))

        for index in range(len(points) - 1):
            a = base + index * 2
            b = a + 1
            c = a + 3
            d = a + 2
            faces.append((a, b, c, d))
            faces.append((d, c, b, a))

    append_ragged_ribbon([(-73, 77), (-53, 87), (-20, 83), (16, 92), (56, 78)], 3.2, 0.2)
    append_ragged_ribbon([(-76, 71), (-65, 38), (-70, 4), (-56, -42), (-63, -82)], 3.6, 0.9)
    append_ragged_ribbon([(60, 66), (46, 35), (54, 6), (41, -34), (45, -76)], 3.3, 1.7)
    append_ragged_ribbon([(-42, -90), (-10, -80), (18, -89), (47, -73)], 3.0, 2.5)
    append_ragged_ribbon([(-17, 72), (-8, 34), (-20, -7), (-6, -48), (-16, -86)], 1.9, 3.3)
    append_ragged_ribbon([(18, 67), (8, 30), (24, -5), (13, -44), (24, -76)], 1.7, 4.0)
    return vertices, faces


def create_guesthall_floor_scuff_cluster_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    strips = [
        [(-170.0, -24.0, 0.0), (-86.0, -31.0, 0.0), (4.0, -22.0, 0.0), (156.0, -30.0, 0.0), (174.0, -18.0, 0.0), (18.0, -9.0, 0.0), (-98.0, -13.0, 0.0), (-184.0, -7.0, 0.0)],
        [(-138.0, 18.0, 0.0), (-34.0, 9.0, 0.0), (118.0, 13.0, 0.0), (166.0, 26.0, 0.0), (46.0, 34.0, 0.0), (-72.0, 32.0, 0.0), (-152.0, 30.0, 0.0)],
        [(-82.0, -58.0, 0.0), (38.0, -64.0, 0.0), (126.0, -54.0, 0.0), (112.0, -44.0, 0.0), (-12.0, -45.0, 0.0), (-90.0, -48.0, 0.0)],
    ]
    for strip in strips:
        append_flat_polygon(vertices, faces, strip)
    return vertices, faces


def create_guesthall_return_route_floor_echo_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_jagged_smear(center_x: float, center_y: float, length: float, width: float, phase: float) -> None:
        points: list[tuple[float, float, float]] = []
        steps = 7
        for index in range(steps):
            alpha = index / (steps - 1)
            x = center_x - length * 0.5 + length * alpha
            y = center_y + math.sin(alpha * math.pi * 2.2 + phase) * width * 0.20
            half = width * (0.26 + 0.16 * math.sin(index * 1.41 + phase))
            points.append((x, y + half, 0.0))
        for index in reversed(range(steps)):
            alpha = index / (steps - 1)
            x = center_x - length * 0.5 + length * alpha
            y = center_y + math.sin(alpha * math.pi * 2.2 + phase) * width * 0.20
            half = width * (0.20 + 0.12 * math.cos(index * 1.17 + phase))
            points.append((x + math.sin(index * 0.73 + phase) * 4.0, y - half, 0.0))
        append_flat_polygon(vertices, faces, points, double_sided=True)

    append_jagged_smear(-54.0, -95.0, 170.0, 34.0, 0.4)
    append_jagged_smear(34.0, -28.0, 235.0, 40.0, 1.6)
    append_jagged_smear(-18.0, 52.0, 190.0, 30.0, 2.7)
    append_jagged_smear(92.0, 104.0, 118.0, 24.0, 3.5)

    echo_islands = [
        [(-176.0, -38.0, 0.0), (-126.0, -48.0, 0.0), (-84.0, -34.0, 0.0), (-111.0, -18.0, 0.0), (-168.0, -18.0, 0.0)],
        [(126.0, 16.0, 0.0), (176.0, 22.0, 0.0), (158.0, 44.0, 0.0), (106.0, 38.0, 0.0)],
        [(-116.0, 96.0, 0.0), (-68.0, 86.0, 0.0), (-48.0, 110.0, 0.0), (-92.0, 126.0, 0.0)],
    ]
    for island in echo_islands:
        append_flat_polygon(vertices, faces, island, double_sided=True)
    return vertices, faces


def create_guesthall_return_route_wall_echo_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_wall_ribbon(points: list[tuple[float, float]], thickness: float, phase: float) -> None:
        base = len(vertices)
        for index, (x, z) in enumerate(points):
            if index == 0:
                dx, dz = points[1][0] - x, points[1][1] - z
            elif index == len(points) - 1:
                dx, dz = x - points[index - 1][0], z - points[index - 1][1]
            else:
                dx, dz = points[index + 1][0] - points[index - 1][0], points[index + 1][1] - points[index - 1][1]
            length = math.sqrt(dx * dx + dz * dz) or 1.0
            px, pz = -dz / length, dx / length
            wobble = math.sin(index * 1.61 + phase) * 2.8
            half = thickness * (0.56 + 0.22 * math.cos(index * 1.09 + phase))
            vertices.append((x + px * (half + wobble), 0.0, z + pz * (half + wobble)))
            vertices.append((x - px * (half - wobble * 0.45), -1.1, z - pz * (half - wobble * 0.45)))

        for index in range(len(points) - 1):
            a = base + index * 2
            b = a + 1
            c = a + 3
            d = a + 2
            faces.append((a, b, c, d))
            faces.append((d, c, b, a))

    append_wall_ribbon([(-130.0, 46.0), (-72.0, 68.0), (-8.0, 58.0), (62.0, 70.0), (136.0, 50.0)], 5.8, 0.1)
    append_wall_ribbon([(-118.0, 30.0), (-90.0, -2.0), (-96.0, -46.0), (-62.0, -78.0), (-34.0, -118.0)], 5.2, 0.9)
    append_wall_ribbon([(118.0, 28.0), (84.0, -6.0), (92.0, -46.0), (58.0, -78.0), (42.0, -112.0)], 4.8, 1.8)
    append_wall_ribbon([(-64.0, -128.0), (-18.0, -112.0), (28.0, -126.0), (76.0, -104.0)], 4.3, 2.6)
    append_wall_ribbon([(-20.0, 42.0), (-4.0, 4.0), (-22.0, -34.0), (2.0, -72.0), (-10.0, -108.0)], 2.6, 3.4)
    return vertices, faces


def create_guesthall_return_route_hand_shadow_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_shadow_blob(center_x: float, center_z: float, radius_x: float, radius_z: float, points_count: int, phase: float) -> None:
        points: list[tuple[float, float, float]] = []
        for index in range(points_count):
            theta = 2.0 * math.pi * index / points_count
            wobble = 1.0 + 0.16 * math.sin(index * 1.71 + phase) + 0.08 * math.cos(index * 2.43 + phase)
            points.append(
                (
                    center_x + math.cos(theta) * radius_x * wobble,
                    -0.6 - 0.25 * math.sin(index * 1.37 + phase),
                    center_z + math.sin(theta) * radius_z * wobble,
                )
            )
        append_flat_polygon(vertices, faces, points, double_sided=True)

    def append_shadow_ribbon(points: list[tuple[float, float]], thickness: float, phase: float) -> None:
        base = len(vertices)
        for index, (x, z) in enumerate(points):
            if index == 0:
                dx, dz = points[1][0] - x, points[1][1] - z
            elif index == len(points) - 1:
                dx, dz = x - points[index - 1][0], z - points[index - 1][1]
            else:
                dx, dz = points[index + 1][0] - points[index - 1][0], points[index + 1][1] - points[index - 1][1]
            length = math.sqrt(dx * dx + dz * dz) or 1.0
            px, pz = -dz / length, dx / length
            pulse = math.sin(index * 1.19 + phase)
            half = thickness * (0.70 + 0.18 * pulse)
            vertices.append((x + px * half, -0.9, z + pz * half))
            vertices.append((x - px * half * (0.82 + 0.12 * pulse), -1.4, z - pz * half * (0.82 + 0.12 * pulse)))

        for index in range(len(points) - 1):
            a = base + index * 2
            b = a + 1
            c = a + 3
            d = a + 2
            faces.append((a, b, c, d))
            faces.append((d, c, b, a))

    append_shadow_blob(-4.0, -2.0, 32.0, 37.0, 22, 0.2)
    append_shadow_blob(-46.0, -12.0, 18.0, 12.0, 14, 1.7)
    append_shadow_ribbon([(-34.0, 25.0), (-44.0, 66.0), (-54.0, 102.0)], 8.0, 0.4)
    append_shadow_ribbon([(-16.0, 30.0), (-18.0, 76.0), (-24.0, 125.0)], 8.8, 1.2)
    append_shadow_ribbon([(4.0, 31.0), (10.0, 82.0), (4.0, 132.0)], 8.2, 2.0)
    append_shadow_ribbon([(24.0, 24.0), (36.0, 64.0), (36.0, 104.0)], 7.0, 2.8)
    append_shadow_ribbon([(27.0, -24.0), (66.0, -18.0), (96.0, -8.0)], 7.5, 3.6)
    append_shadow_ribbon([(-12.0, -36.0), (-6.0, -76.0), (16.0, -116.0)], 14.0, 4.3)
    return vertices, faces


def create_guesthall_return_route_torn_slip_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    columns = 4
    rows = 8
    base = len(vertices)
    for row in range(rows + 1):
        v = row / rows
        center_z = 48.0 - 96.0 * v
        left = -29.0 + math.sin(row * 1.37) * 2.7 + (3.0 if row in (0, rows) else 0.0)
        right = 30.0 + math.cos(row * 1.11 + 0.6) * 2.4 - (2.0 if row == rows else 0.0)
        if row == 1:
            left += 5.0
        if row == 6:
            right -= 6.0
        for column in range(columns + 1):
            u = column / columns
            edge = 1.0 if column in (0, columns) else 0.0
            x = left + (right - left) * u + math.sin(row * 0.83 + column * 1.91) * (0.35 + edge * 1.7)
            z = center_z + math.sin(row * 1.23 + column * 0.71) * (0.6 + edge * 1.4)
            y = -0.08 - 0.012 * edge
            vertices.append((x, y, z))

    stride = columns + 1
    for row in range(rows):
        for column in range(columns):
            a = base + row * stride + column
            b = a + 1
            c = a + stride + 1
            d = a + stride
            faces.append((a, b, c, d))
            faces.append((d, c, b, a))

    append_flat_polygon(vertices, faces, [(-35.0, -0.11, -11.0), (-28.0, -0.10, -4.0), (-31.0, -0.10, 9.0), (-38.0, -0.12, 3.0)], double_sided=True)
    append_flat_polygon(vertices, faces, [(9.0, -0.11, -55.0), (21.0, -0.12, -42.0), (17.0, -0.10, -31.0), (5.0, -0.11, -41.0)], double_sided=True)
    append_flat_polygon(vertices, faces, [(-5.0, -0.10, 8.0), (5.0, -0.11, 5.0), (4.0, -0.10, -6.0), (-6.0, -0.11, -4.0)], double_sided=True)
    return vertices, faces


def create_guesthall_return_route_warning_underline_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    top: list[tuple[float, float, float]] = []
    bottom: list[tuple[float, float, float]] = []
    for index in range(8):
        alpha = index / 7.0
        x = -50.0 + alpha * 100.0
        z = math.sin(alpha * math.pi * 3.2) * 2.5
        top.append((x, -0.7, z + 4.2 + math.sin(index * 1.9) * 0.8))
        bottom.append((x + math.sin(index * 0.8) * 2.4, -1.0, z - 3.8 + math.cos(index * 1.6) * 0.7))
    append_flat_polygon(vertices, faces, top + list(reversed(bottom)), double_sided=True)
    return vertices, faces


def create_guesthall_return_route_slip_writing_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_stroke(points: list[tuple[float, float]], thickness: float, phase: float) -> None:
        base = len(vertices)
        for index, (x, z) in enumerate(points):
            if index == 0:
                dx, dz = points[1][0] - x, points[1][1] - z
            elif index == len(points) - 1:
                dx, dz = x - points[index - 1][0], z - points[index - 1][1]
            else:
                dx, dz = points[index + 1][0] - points[index - 1][0], points[index + 1][1] - points[index - 1][1]
            length = math.sqrt(dx * dx + dz * dz) or 1.0
            px, pz = -dz / length, dx / length
            wobble = math.sin(index * 1.43 + phase) * 0.35
            half = thickness * (0.54 + 0.18 * math.cos(index * 1.17 + phase))
            vertices.append((x + px * (half + wobble), -0.36, z + pz * (half + wobble)))
            vertices.append((x - px * (half - wobble * 0.45), -0.46, z - pz * (half - wobble * 0.45)))

        for index in range(len(points) - 1):
            a = base + index * 2
            b = a + 1
            c = a + 3
            d = a + 2
            faces.append((a, b, c, d))
            faces.append((d, c, b, a))

    # Thin marker scars, not readable UI text.
    append_stroke([(-21.0, 13.0), (-8.0, 16.0), (5.0, 12.0)], 1.1, 0.1)
    append_stroke([(10.0, 14.0), (23.0, 11.0), (16.0, 6.0)], 1.0, 0.8)
    append_stroke([(-24.0, -2.0), (-8.0, -5.0), (8.0, -3.0), (22.0, -7.0)], 1.1, 1.5)
    append_stroke([(-18.0, -15.0), (-4.0, -12.0), (12.0, -16.0)], 0.9, 2.1)
    append_stroke([(24.0, -2.0), (33.0, 3.0), (27.0, 7.0)], 0.9, 2.9)
    append_stroke([(-30.0, 5.0), (-20.0, 1.0), (-28.0, -5.0)], 0.8, 3.7)
    return vertices, faces


def create_guesthall_return_route_footprint_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_floor_blob(center_x: float, center_y: float, radius_x: float, radius_y: float, count: int, phase: float) -> None:
        points: list[tuple[float, float, float]] = []
        for index in range(count):
            theta = 2.0 * math.pi * index / count
            wobble = 1.0 + 0.14 * math.sin(index * 1.33 + phase) + 0.06 * math.cos(index * 2.51 + phase)
            points.append((center_x + math.cos(theta) * radius_x * wobble, center_y + math.sin(theta) * radius_y * wobble, 0.0))
        append_flat_polygon(vertices, faces, points, double_sided=True)

    append_floor_blob(-16.0, -8.0, 14.0, 33.0, 18, 0.3)
    append_floor_blob(-19.0, 31.0, 11.0, 9.0, 14, 1.5)
    append_floor_blob(18.0, 15.0, 13.0, 29.0, 18, 2.1)
    append_floor_blob(21.0, 50.0, 10.0, 8.0, 14, 3.0)
    append_flat_polygon(
        vertices,
        faces,
        [(-42.0, -24.0, 0.0), (-23.0, -27.0, 0.0), (-4.0, -19.0, 0.0), (-22.0, -14.0, 0.0)],
        double_sided=True,
    )
    append_flat_polygon(
        vertices,
        faces,
        [(8.0, -12.0, 0.0), (30.0, -16.0, 0.0), (43.0, -7.0, 0.0), (21.0, 1.0, 0.0)],
        double_sided=True,
    )
    return vertices, faces


def create_guesthall_return_route_cold_vein_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_vein(points: list[tuple[float, float]], thickness: float, phase: float) -> None:
        base = len(vertices)
        for index, (x, y) in enumerate(points):
            if index == 0:
                dx, dy = points[1][0] - x, points[1][1] - y
            elif index == len(points) - 1:
                dx, dy = x - points[index - 1][0], y - points[index - 1][1]
            else:
                dx, dy = points[index + 1][0] - points[index - 1][0], points[index + 1][1] - points[index - 1][1]
            length = math.sqrt(dx * dx + dy * dy) or 1.0
            px, py = -dy / length, dx / length
            wobble = math.sin(index * 1.47 + phase) * thickness * 0.18
            half = thickness * (0.46 + 0.20 * math.cos(index * 1.31 + phase))
            vertices.append((x + px * (half + wobble), y + py * (half + wobble), 0.0))
            vertices.append((x - px * (half - wobble * 0.35), y - py * (half - wobble * 0.35), 0.0))

        for index in range(len(points) - 1):
            a = base + index * 2
            b = a + 1
            c = a + 3
            d = a + 2
            faces.append((a, b, c, d))
            faces.append((d, c, b, a))

    append_flat_polygon(
        vertices,
        faces,
        [
            (-156.0, -112.0, 0.0),
            (-96.0, -142.0, 0.0),
            (-18.0, -128.0, 0.0),
            (58.0, -146.0, 0.0),
            (142.0, -98.0, 0.0),
            (172.0, -16.0, 0.0),
            (128.0, 68.0, 0.0),
            (36.0, 128.0, 0.0),
            (-72.0, 118.0, 0.0),
            (-164.0, 50.0, 0.0),
            (-188.0, -38.0, 0.0),
        ],
        double_sided=True,
    )
    append_flat_polygon(
        vertices,
        faces,
        [(-84.0, -44.0, 0.0), (-18.0, -62.0, 0.0), (48.0, -38.0, 0.0), (82.0, 16.0, 0.0), (18.0, 44.0, 0.0), (-58.0, 24.0, 0.0)],
        double_sided=True,
    )
    append_vein([(-182.0, -30.0), (-104.0, -18.0), (-18.0, -38.0), (72.0, -18.0), (152.0, 28.0)], 9.0, 0.2)
    append_vein([(-116.0, 98.0), (-72.0, 48.0), (-26.0, -2.0), (20.0, -58.0), (82.0, -124.0)], 6.2, 1.1)
    append_vein([(120.0, 78.0), (62.0, 48.0), (8.0, 6.0), (-52.0, -56.0), (-120.0, -108.0)], 5.4, 2.0)
    return vertices, faces


def create_guesthall_return_route_direction_scratch_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    def append_scratch(points: list[tuple[float, float]], thickness: float, phase: float) -> None:
        base = len(vertices)
        for index, (x, y) in enumerate(points):
            if index == 0:
                dx, dy = points[1][0] - x, points[1][1] - y
            elif index == len(points) - 1:
                dx, dy = x - points[index - 1][0], y - points[index - 1][1]
            else:
                dx, dy = points[index + 1][0] - points[index - 1][0], points[index + 1][1] - points[index - 1][1]
            length = math.sqrt(dx * dx + dy * dy) or 1.0
            px, py = -dy / length, dx / length
            taper = 1.0 - abs((index / max(1, len(points) - 1)) - 0.5) * 0.58
            nick = math.sin(index * 2.13 + phase) * thickness * 0.20
            half = thickness * taper * (0.58 + 0.18 * math.cos(index * 1.37 + phase))
            vertices.append((x + px * (half + nick), y + py * (half + nick), 0.0))
            vertices.append((x - px * (half - nick * 0.42), y - py * (half - nick * 0.42), 0.0))

        for index in range(len(points) - 1):
            a = base + index * 2
            b = a + 1
            c = a + 3
            d = a + 2
            faces.append((a, b, c, d))
            faces.append((d, c, b, a))

    append_scratch([(-104.0, -7.0), (-56.0, -9.0), (-8.0, -4.0), (42.0, 2.0), (94.0, 8.0)], 3.6, 0.2)
    append_scratch([(32.0, 30.0), (62.0, 14.0), (100.0, 8.0), (62.0, -8.0), (28.0, -28.0)], 3.1, 1.2)
    append_scratch([(-76.0, 17.0), (-38.0, 11.0), (8.0, 14.0), (56.0, 21.0)], 2.1, 2.0)
    append_scratch([(-68.0, -30.0), (-18.0, -24.0), (36.0, -21.0), (82.0, -18.0)], 1.8, 2.8)

    chips = [
        [(-112.0, 8.0, 0.0), (-92.0, 14.0, 0.0), (-82.0, 4.0, 0.0), (-104.0, -2.0, 0.0)],
        [(-12.0, 24.0, 0.0), (8.0, 28.0, 0.0), (2.0, 38.0, 0.0), (-18.0, 34.0, 0.0)],
        [(92.0, -28.0, 0.0), (112.0, -22.0, 0.0), (102.0, -10.0, 0.0), (82.0, -15.0, 0.0)],
    ]
    for chip in chips:
        append_flat_polygon(vertices, faces, chip, double_sided=True)
    return vertices, faces


def create_guesthall_ceiling_water_stain_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    points: list[tuple[float, float, float]] = []
    for index in range(18):
        theta = -2.0 * math.pi * index / 18.0
        radius_x = 92.0 + 18.0 * math.sin(index * 1.7)
        radius_y = 46.0 + 11.0 * math.cos(index * 2.1)
        points.append((math.cos(theta) * radius_x, math.sin(theta) * radius_y, 0.0))
    append_flat_polygon(vertices, faces, points)
    return vertices, faces


def create_lobbydoor_smudged_glass_pane_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices = [
        (0.06, -132.0, -104.0),
        (0.06, 132.0, -104.0),
        (0.06, 132.0, 104.0),
        (0.06, -132.0, 104.0),
    ]
    return vertices, [(0, 1, 2, 3), (3, 2, 1, 0)]


def create_lobbydoor_palm_smear_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_planar_blob_yz(vertices, faces, -74.0, 8.0, 19.0, 25.0, 22, 0.4)
    for index, finger_y in enumerate((-101.0, -89.0, -77.0, -65.0)):
        append_planar_stroke_yz(
            vertices,
            faces,
            [(finger_y, 20.0), (finger_y + 4.0, 50.0), (finger_y + math.sin(index) * 3.0, 82.0)],
            4.8 - index * 0.35,
            index * 0.8,
        )
    append_planar_stroke_yz(vertices, faces, [(-55.0, 6.0), (-36.0, 25.0), (-28.0, 51.0)], 5.2, 4.0)
    append_planar_stroke_yz(vertices, faces, [(-108.0, -21.0), (-82.0, -31.0), (-48.0, -24.0)], 4.2, 4.9)
    return vertices, faces


def create_lobbydoor_crack_web_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_planar_stroke_yz(vertices, faces, [(-78.0, 72.0), (-42.0, 48.0), (-8.0, 30.0), (26.0, 10.0), (70.0, -12.0)], 0.58, 0.2)
    append_planar_stroke_yz(vertices, faces, [(-6.0, 30.0), (-19.0, 55.0), (-34.0, 79.0)], 0.42, 1.0)
    append_planar_stroke_yz(vertices, faces, [(4.0, 27.0), (27.0, 53.0), (51.0, 73.0)], 0.36, 1.8)
    append_planar_stroke_yz(vertices, faces, [(22.0, 12.0), (43.0, 11.0), (66.0, 20.0)], 0.34, 2.4)
    append_planar_stroke_yz(vertices, faces, [(-42.0, 47.0), (-55.0, 22.0), (-82.0, 6.0)], 0.38, 3.0)
    append_planar_blob_yz(vertices, faces, -8.0, 30.0, 1.2, 1.2, 10, 3.6)
    return vertices, faces


def create_lobbydoor_torn_tape_cross_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []

    horizontal = [
        (-18.0, 20.0, 0.0),
        (-9.0, 22.0, 0.0),
        (3.0, 20.5, 0.0),
        (15.0, 23.0, 0.0),
        (22.0, 20.0, 0.0),
        (23.5, 15.0, 0.0),
        (11.0, 13.0, 0.0),
        (-2.0, 15.5, 0.0),
        (-12.0, 14.0, 0.0),
        (-21.0, 15.5, 0.0),
    ]
    vertical = [
        (-5.0, 34.0, 0.0),
        (3.0, 32.5, 0.0),
        (4.0, 20.0, 0.0),
        (0.5, 5.0, 0.0),
        (3.0, -12.0, 0.0),
        (-3.0, -27.0, 0.0),
        (-10.0, -25.0, 0.0),
        (-8.0, -9.0, 0.0),
        (-9.5, 6.0, 0.0),
        (-7.0, 21.0, 0.0),
    ]
    loose = [
        (21.0, 19.0, 0.0),
        (30.0, 16.0, 0.0),
        (31.5, 10.0, 0.0),
        (23.0, 13.0, 0.0),
    ]
    append_flat_polygon(vertices, faces, [(0.0, y, z) for y, z, _ in horizontal], double_sided=True)
    append_flat_polygon(vertices, faces, [(0.0, y, z) for y, z, _ in vertical], double_sided=True)
    append_flat_polygon(vertices, faces, [(0.0, y, z) for y, z, _ in loose], double_sided=True)
    return vertices, faces


def create_lobbydoor_latch_plate_mesh() -> tuple[list[tuple[float, float, float]], list[tuple[int, ...]]]:
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    append_box(vertices, faces, (0.0, 0.0, 0.0), (3.2, 9.0, 24.0))
    append_box(vertices, faces, (-2.8, 0.0, -1.4), (2.0, 20.0, 3.0))
    append_box(vertices, faces, (-3.2, -10.5, -1.4), (1.8, 4.0, 5.4))
    append_box(vertices, faces, (-3.2, 10.5, -1.4), (1.8, 4.0, 5.4))
    append_planar_blob_yz(vertices, faces, 0.0, 7.5, 1.9, 1.9, 12, 0.5, plane_x=-2.1)
    append_planar_blob_yz(vertices, faces, 0.0, -8.0, 1.9, 1.9, 12, 1.3, plane_x=-2.1)
    append_planar_stroke_yz(vertices, faces, [(-7.0, 0.0), (-1.0, 1.5), (7.5, -0.5)], 0.7, 2.4, plane_x=-2.2)
    return vertices, faces


def generate_source_meshes() -> dict[str, pathlib.Path]:
    UPDATED_SOURCE_MESHES.clear()
    mesh_builders = {
        "SM_FrontDesk_OldPhoneBody_v0": create_phone_body_mesh,
        "SM_FrontDesk_CurvedReceiver_v0": create_receiver_mesh,
        "SM_FrontDesk_CoiledPhoneCord_v0": create_coiled_cord_mesh,
        "SM_FrontDesk_CurledLedgerPages_v0": create_curled_pages_mesh,
        "SM_FrontDesk_LogPenBody_v0": create_frontdesk_log_pen_body_mesh,
        "SM_FrontDesk_LogPenNib_v0": create_frontdesk_log_pen_nib_mesh,
        "SM_FrontDesk_ReportLogFiledPaper_v0": create_frontdesk_report_log_filed_paper_mesh,
        "SM_FrontDesk_FiledStamp_v0": create_frontdesk_filed_stamp_mesh,
        "SM_FrontDesk_ReportFiledInk_v0": create_frontdesk_report_filed_ink_mesh,
        "SM_Room203_PaneledDoor_v0": create_room203_paneled_door_mesh,
        "SM_Room203_ChainLinks_v0": create_room203_chain_links_mesh,
        "SM_Room203_TornNotice_v0": create_room203_torn_notice_mesh,
        "SM_Room203_HandleLever_v0": create_room203_handle_lever_mesh,
        "SM_Room203_NumberDigits_v0": create_room203_number_digits_mesh,
        "SM_Room203_DoorGrimeStreaks_v0": create_room203_door_grime_streaks_mesh,
        "SM_Room203_DoorPaintChips_v0": create_room203_door_paint_chips_mesh,
        "SM_Room203_LockHardwareBreakup_v0": create_room203_lock_hardware_breakup_mesh,
        "SM_Room203_SconceGlass_v0": create_room203_sconce_glass_mesh,
        "SM_Room203_SconceBracket_v0": create_room203_sconce_bracket_mesh,
        "SM_Room203_NoticeWriting_v0": create_room203_notice_writing_mesh,
        "SM_Room203_NoticeTape_v0": create_room203_notice_tape_mesh,
        "SM_GuestHall_ServiceCartSilhouette_v0": create_guesthall_service_cart_silhouette_mesh,
        "SM_GuestHall_PeelingWallpaperPatch_v0": create_guesthall_peeling_wallpaper_mesh,
        "SM_GuestHall_Room203AftershockPaper_v0": create_guesthall_room203_aftershock_paper_mesh,
        "SM_GuestHall_Room203AftershockTearShadow_v0": create_guesthall_room203_aftershock_shadow_mesh,
        "SM_GuestHall_Room203AftershockRawEdge_v0": create_guesthall_room203_aftershock_raw_edge_mesh,
        "SM_GuestHall_FloorScuffCluster_v0": create_guesthall_floor_scuff_cluster_mesh,
        "SM_GuestHall_ReturnRouteFloorEcho_v0": create_guesthall_return_route_floor_echo_mesh,
        "SM_GuestHall_ReturnRouteWallEcho_v0": create_guesthall_return_route_wall_echo_mesh,
        "SM_GuestHall_ReturnRouteHandShadow_v0": create_guesthall_return_route_hand_shadow_mesh,
        "SM_GuestHall_ReturnRouteTornSlip_v0": create_guesthall_return_route_torn_slip_mesh,
        "SM_GuestHall_ReturnRouteWarningUnderline_v0": create_guesthall_return_route_warning_underline_mesh,
        "SM_GuestHall_ReturnRouteSlipWriting_v0": create_guesthall_return_route_slip_writing_mesh,
        "SM_GuestHall_ReturnRouteFootprint_v0": create_guesthall_return_route_footprint_mesh,
        "SM_GuestHall_ReturnRouteColdVein_v0": create_guesthall_return_route_cold_vein_mesh,
        "SM_GuestHall_ReturnRouteDirectionScratch_v0": create_guesthall_return_route_direction_scratch_mesh,
        "SM_GuestHall_CeilingWaterStain_v0": create_guesthall_ceiling_water_stain_mesh,
        "SM_LobbyDoor_SmudgedGlassPane_v0": create_lobbydoor_smudged_glass_pane_mesh,
        "SM_LobbyDoor_PalmSmear_v0": create_lobbydoor_palm_smear_mesh,
        "SM_LobbyDoor_CrackWeb_v0": create_lobbydoor_crack_web_mesh,
        "SM_LobbyDoor_TornTapeCross_v0": create_lobbydoor_torn_tape_cross_mesh,
        "SM_LobbyDoor_LatchPlate_v0": create_lobbydoor_latch_plate_mesh,
    }

    output: dict[str, pathlib.Path] = {}
    texture_uv_meshes = {
        "SM_Room203_PaneledDoor_v0": ("x", "z"),
        "SM_GuestHall_ReturnRouteTornSlip_v0": ("x", "z"),
        "SM_FrontDesk_ReportLogFiledPaper_v0": ("x", "y"),
        "SM_LobbyDoor_SmudgedGlassPane_v0": ("y", "z"),
    }
    for name, builder in mesh_builders.items():
        path = SOURCE_MESH_DIR / f"{name}.obj"
        vertices, faces = builder()
        if name in texture_uv_meshes:
            changed = write_obj(path, vertices, faces, texture_uv_meshes[name], True)
        else:
            changed = write_obj(path, vertices, faces)
        if changed:
            UPDATED_SOURCE_MESHES.add(name)
        output[name] = path
    return output


def import_static_meshes(source_paths: dict[str, pathlib.Path]) -> dict[str, unreal.StaticMesh]:
    meshes: dict[str, unreal.StaticMesh] = {}
    tasks = []
    for name, path in source_paths.items():
        asset_path = f"/Game/Hotel/Meshes/{name}"
        if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
            asset = unreal.EditorAssetLibrary.load_asset(asset_path)
            if asset and name not in UPDATED_SOURCE_MESHES:
                meshes[name] = asset
                continue

        task = unreal.AssetImportTask()
        task.set_editor_property("filename", str(path))
        task.set_editor_property("destination_path", "/Game/Hotel/Meshes")
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        tasks.append(task)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    for name in source_paths:
        if name in meshes:
            continue
        asset = unreal.EditorAssetLibrary.load_asset(f"/Game/Hotel/Meshes/{name}")
        if asset:
            meshes[name] = asset
    return meshes


def import_textures(source_paths: dict[str, pathlib.Path]) -> dict[str, unreal.Texture2D]:
    textures: dict[str, unreal.Texture2D] = {}
    tasks = []
    for name, path in source_paths.items():
        asset_path = f"/Game/Hotel/Textures/{name}"
        if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
            asset = unreal.EditorAssetLibrary.load_asset(asset_path)
            if asset and name not in UPDATED_SOURCE_TEXTURES and name not in ALWAYS_REIMPORT_TEXTURES:
                textures[name] = asset
                continue

        task = unreal.AssetImportTask()
        task.set_editor_property("filename", str(path))
        task.set_editor_property("destination_path", "/Game/Hotel/Textures")
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        tasks.append(task)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

    for name in source_paths:
        if name in textures:
            continue
        asset = unreal.EditorAssetLibrary.load_asset(f"/Game/Hotel/Textures/{name}")
        if asset:
            textures[name] = asset
    return textures


def scrub_texture_import_metadata(source_paths: dict[str, pathlib.Path]) -> None:
    for name, source_path in source_paths.items():
        asset_path = PROJECT_ROOT / "Content" / "Hotel" / "Textures" / f"{name}.uasset"
        if not asset_path.exists():
            continue

        data = asset_path.read_bytes()
        replacements = []
        for raw_source in {str(source_path), source_path.as_posix()}:
            old = f"Factory_{raw_source}".encode("utf-8")
            new_base = f"Factory_SourceAssets/TextureGenerated/{source_path.name}".encode("utf-8")
            if len(new_base) > len(old):
                log(f"Skipping texture import metadata scrub for {name}: replacement is longer than source path.")
                continue
            replacements.append((old, new_base + (b"_" * (len(old) - len(new_base)))))

        changed = False
        for old, new in replacements:
            if old in data:
                data = data.replace(old, new)
                changed = True

        if changed:
            asset_path.write_bytes(data)
            log(f"Scrubbed local texture import metadata for {name}.")


def ensure_material(
    name: str,
    color: unreal.LinearColor,
    roughness: float,
    emissive: unreal.LinearColor | None = None,
    two_sided: bool = False,
    force_recreate: bool = False,
) -> unreal.MaterialInterface:
    def enable_runtime_usage(material: unreal.MaterialInterface) -> None:
        usage_names = (
            "MATUSAGE_STATIC_MESH",
            "MATUSAGE_StaticMesh",
            "MATUSAGE_NANITE",
            "MATUSAGE_Nanite",
        )
        for usage_name in usage_names:
            usage = getattr(unreal.MaterialUsage, usage_name, None)
            if usage is None:
                continue
            try:
                unreal.MaterialEditingLibrary.set_base_material_usage(material, usage, True)
            except Exception:
                try:
                    material.set_material_usage(usage)
                except Exception:
                    pass

    path = f"/Game/Hotel/Materials/{name}"
    if force_recreate and unreal.EditorAssetLibrary.does_asset_exist(path):
        unreal.EditorAssetLibrary.delete_asset(path)
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        material = unreal.EditorAssetLibrary.load_asset(path)
        if two_sided:
            try:
                material.set_editor_property("two_sided", True)
            except Exception:
                pass
        enable_runtime_usage(material)
        try:
            unreal.MaterialEditingLibrary.recompile_material(material)
            unreal.EditorAssetLibrary.save_asset(path)
        except Exception:
            pass
        return material

    material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        name,
        "/Game/Hotel/Materials",
        unreal.Material,
        unreal.MaterialFactoryNew(),
    )

    if two_sided:
        try:
            material.set_editor_property("two_sided", True)
        except Exception:
            pass

    base = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionConstant3Vector, -360, -120
    )
    base.set_editor_property("constant", color)
    unreal.MaterialEditingLibrary.connect_material_property(base, "", unreal.MaterialProperty.MP_BASE_COLOR)

    rough = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionConstant, -360, 80
    )
    rough.set_editor_property("r", roughness)
    unreal.MaterialEditingLibrary.connect_material_property(rough, "", unreal.MaterialProperty.MP_ROUGHNESS)

    if emissive:
        glow = unreal.MaterialEditingLibrary.create_material_expression(
            material, unreal.MaterialExpressionConstant3Vector, -360, 260
        )
        glow.set_editor_property("constant", emissive)
        unreal.MaterialEditingLibrary.connect_material_property(glow, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)

    enable_runtime_usage(material)
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_asset(path)
    return material


def ensure_textured_material(
    name: str,
    texture: unreal.Texture2D,
    roughness: float,
    two_sided: bool = False,
    emissive: bool = False,
    emissive_strength: float = 1.0,
    force_recreate: bool = False,
) -> unreal.MaterialInterface:
    def enable_runtime_usage(material: unreal.MaterialInterface) -> None:
        usage_names = (
            "MATUSAGE_STATIC_MESH",
            "MATUSAGE_StaticMesh",
            "MATUSAGE_NANITE",
            "MATUSAGE_Nanite",
        )
        for usage_name in usage_names:
            usage = getattr(unreal.MaterialUsage, usage_name, None)
            if usage is None:
                continue
            try:
                unreal.MaterialEditingLibrary.set_base_material_usage(material, usage, True)
            except Exception:
                try:
                    material.set_material_usage(usage)
                except Exception:
                    pass

    path = f"/Game/Hotel/Materials/{name}"
    if force_recreate and unreal.EditorAssetLibrary.does_asset_exist(path):
        unreal.EditorAssetLibrary.delete_asset(path)
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        material = unreal.EditorAssetLibrary.load_asset(path)
        if two_sided:
            try:
                material.set_editor_property("two_sided", True)
            except Exception:
                pass
        enable_runtime_usage(material)
        try:
            unreal.MaterialEditingLibrary.recompile_material(material)
            unreal.EditorAssetLibrary.save_asset(path)
        except Exception:
            pass
        return material

    material = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        name,
        "/Game/Hotel/Materials",
        unreal.Material,
        unreal.MaterialFactoryNew(),
    )

    if two_sided:
        try:
            material.set_editor_property("two_sided", True)
        except Exception:
            pass

    sample = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionTextureSample, -420, -120
    )
    sample.set_editor_property("texture", texture)
    unreal.MaterialEditingLibrary.connect_material_property(sample, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)
    if emissive:
        if emissive_strength == 1.0:
            unreal.MaterialEditingLibrary.connect_material_property(sample, "RGB", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
        else:
            emissive_multiply = unreal.MaterialEditingLibrary.create_material_expression(
                material, unreal.MaterialExpressionMultiply, -160, -120
            )
            emissive_value = unreal.MaterialEditingLibrary.create_material_expression(
                material, unreal.MaterialExpressionConstant, -360, 90
            )
            emissive_value.set_editor_property("r", emissive_strength)
            unreal.MaterialEditingLibrary.connect_material_expressions(sample, "RGB", emissive_multiply, "A")
            unreal.MaterialEditingLibrary.connect_material_expressions(emissive_value, "", emissive_multiply, "B")
            unreal.MaterialEditingLibrary.connect_material_property(
                emissive_multiply,
                "",
                unreal.MaterialProperty.MP_EMISSIVE_COLOR,
            )

    rough = unreal.MaterialEditingLibrary.create_material_expression(
        material, unreal.MaterialExpressionConstant, -420, 90
    )
    rough.set_editor_property("r", roughness)
    unreal.MaterialEditingLibrary.connect_material_property(rough, "", unreal.MaterialProperty.MP_ROUGHNESS)

    enable_runtime_usage(material)
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_asset(path)
    return material


def prepare_level() -> None:
    if unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        unreal.EditorLevelLibrary.load_level(MAP_PATH)
        for actor in unreal.EditorLevelLibrary.get_all_level_actors():
            if not isinstance(actor, unreal.WorldSettings):
                unreal.EditorLevelLibrary.destroy_actor(actor)
    else:
        unreal.EditorLevelLibrary.new_level(MAP_PATH)


def tag_actor(actor: unreal.Actor, *tags: str) -> None:
    if not tags:
        return
    actor.tags = [unreal.Name(tag) for tag in tags]


def try_set_property(obj, name: str, value) -> None:
    try:
        obj.set_editor_property(name, value)
    except Exception:
        pass


def make_rotator(pitch: float, yaw: float, roll: float = 0.0) -> unreal.Rotator:
    return unreal.Rotator(roll, pitch, yaw)


def add_cube(
    label: str,
    location,
    size,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
) -> unreal.Actor:
    cube = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        make_rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(size[0] / 100.0, size[1] / 100.0, size[2] / 100.0))
    component = actor.static_mesh_component
    component.set_static_mesh(cube)
    component.set_material(0, material)
    component.set_editor_property("mobility", mobility)
    if no_collision:
        try:
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        except Exception:
            pass
    tag_actor(actor, *tags)
    return actor


def add_mesh(
    label: str,
    mesh_path: str,
    location,
    size,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
    rotation=(0.0, 0.0, 0.0),
) -> unreal.Actor:
    mesh = unreal.EditorAssetLibrary.load_asset(mesh_path)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        make_rotator(*rotation),
    )
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(size[0] / 100.0, size[1] / 100.0, size[2] / 100.0))
    component = actor.static_mesh_component
    component.set_static_mesh(mesh)
    component.set_material(0, material)
    component.set_editor_property("mobility", mobility)
    if no_collision:
        try:
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        except Exception:
            pass
    tag_actor(actor, *tags)
    return actor


def add_cylinder(
    label: str,
    location,
    diameter: float,
    height: float,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
    rotation=(0.0, 0.0, 0.0),
) -> unreal.Actor:
    return add_mesh(
        label,
        "/Engine/BasicShapes/Cylinder.Cylinder",
        location,
        (diameter, diameter, height),
        material,
        tags,
        mobility,
        no_collision,
        rotation,
    )


def add_sphere(
    label: str,
    location,
    size,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
) -> unreal.Actor:
    return add_mesh(
        label,
        "/Engine/BasicShapes/Sphere.Sphere",
        location,
        size,
        material,
        tags,
        mobility,
        no_collision,
    )


def add_light(
    label: str,
    cls,
    location,
    rotation,
    intensity: float,
    color: unreal.Color,
    tags=(),
    attenuation_radius: float = 1400.0,
    source_width: float | None = None,
    source_height: float | None = None,
):
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        cls,
        unreal.Vector(*location),
        make_rotator(*rotation),
    )
    actor.set_actor_label(label)
    component_name = "light_component"
    if hasattr(actor, "rect_light_component"):
        component_name = "rect_light_component"
    component = actor.get_editor_property(component_name)
    component.set_editor_property("intensity", intensity)
    component.set_editor_property("light_color", color)
    try_set_property(component, "mobility", unreal.ComponentMobility.MOVABLE)
    try_set_property(component, "attenuation_radius", attenuation_radius)
    if source_width is not None:
        try_set_property(component, "source_width", source_width)
    if source_height is not None:
        try_set_property(component, "source_height", source_height)
    tag_actor(actor, *tags)
    return actor


def add_camera(label: str, location, rotation, fov: float = 62.0, tags=()) -> unreal.Actor:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.CameraActor,
        unreal.Vector(*location),
        make_rotator(*rotation),
    )
    actor.set_actor_label(label)
    try:
        component = actor.get_editor_property("camera_component")
        component.set_editor_property("field_of_view", fov)
        component.set_editor_property("post_process_blend_weight", 1.0)
        settings = component.get_editor_property("post_process_settings")
        exposure_overrides = {
            "override_auto_exposure_method": True,
            "override_auto_exposure_min_brightness": True,
            "override_auto_exposure_max_brightness": True,
            "override_auto_exposure_bias": True,
            "auto_exposure_min_brightness": 1.0,
            "auto_exposure_max_brightness": 1.0,
            "auto_exposure_bias": 2.55,
        }
        for name, value in exposure_overrides.items():
            try_set_property(settings, name, value)
        try:
            settings.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
        except Exception:
            pass
        component.set_editor_property("post_process_settings", settings)
    except Exception:
        pass
    tag_actor(actor, *tags)
    return actor


def add_audio(label: str, sound: unreal.SoundWave, location, auto_activate: bool, tags=()) -> unreal.Actor:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.AmbientSound,
        unreal.Vector(*location),
        make_rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label(label)
    component = actor.get_editor_property("audio_component")
    component.set_editor_property("sound", sound)
    component.set_editor_property("auto_activate", auto_activate)
    tag_actor(actor, *tags)
    return actor


def add_post_process_volume(label: str) -> unreal.Actor:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PostProcessVolume,
        unreal.Vector(2100, 0, 120),
        make_rotator(0.0, 0.0, 0.0),
    )
    actor.set_actor_label(label)
    try_set_property(actor, "b_unbound", True)
    try_set_property(actor, "unbound", True)
    try_set_property(actor, "priority", 10.0)

    try:
        settings = actor.get_editor_property("settings")
    except Exception:
        settings = None
    if settings:
        exposure_overrides = {
            "override_auto_exposure_method": True,
            "override_auto_exposure_min_brightness": True,
            "override_auto_exposure_max_brightness": True,
            "override_auto_exposure_bias": True,
            "auto_exposure_min_brightness": 1.0,
            "auto_exposure_max_brightness": 1.0,
            "auto_exposure_bias": 2.55,
        }
        for name, value in exposure_overrides.items():
            try_set_property(settings, name, value)
        try:
            settings.set_editor_property("auto_exposure_method", unreal.AutoExposureMethod.AEM_MANUAL)
        except Exception:
            pass
        try_set_property(actor, "settings", settings)

    tag_actor(actor, "Hotel.Capture.Readability")
    return actor


def add_authored_mesh(
    label: str,
    mesh: unreal.StaticMesh,
    location,
    scale,
    material: unreal.MaterialInterface,
    tags=(),
    mobility=unreal.ComponentMobility.STATIC,
    no_collision=False,
    rotation=(0.0, 0.0, 0.0),
) -> unreal.Actor:
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor,
        unreal.Vector(*location),
        make_rotator(*rotation),
    )
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    component = actor.static_mesh_component
    component.set_static_mesh(mesh)
    component.set_material(0, material)
    component.set_editor_property("mobility", mobility)
    if no_collision:
        try:
            component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        except Exception:
            pass
    tag_actor(actor, *tags)
    return actor


def build_level(
    sounds: dict[str, unreal.SoundWave],
    meshes: dict[str, unreal.StaticMesh],
    textures: dict[str, unreal.Texture2D],
) -> None:
    prepare_level()

    room203_wallpaper_texture = textures.get("TX_Hotel_Room203WallpaperPanel_v0")
    room_door_texture = textures.get("TX_Hotel_RoomDoorPaint_v0")
    return_slip_texture = textures.get("TX_Hotel_ReturnRouteSlipPaper_v0")
    security_monitor_texture = textures.get("TX_Hotel_SecurityMonitorFeed_v0")
    report_log_paper_texture = textures.get("TX_Hotel_ReportLogFiledPaper_v0")
    lobby_glass_texture = textures.get("TX_Hotel_LobbyDoorSmudgedGlass_v0")
    frontdesk_hero_board_texture = textures.get("TX_Hotel_FrontDeskHeroBoard_v0")
    materials = {
        "floor": ensure_material("M_Hotel_WornFloor_v0", unreal.LinearColor(0.15, 0.13, 0.11, 1.0), 0.92),
        "wall": ensure_material("M_Hotel_AgedWall_v0", unreal.LinearColor(0.42, 0.38, 0.31, 1.0), 0.86),
        "guesthall_wallpaper": ensure_textured_material("M_Hotel_Room203WallpaperPanel_v0", room203_wallpaper_texture, 0.95)
        if room203_wallpaper_texture
        else ensure_material("M_Hotel_AgedWall_v0", unreal.LinearColor(0.42, 0.38, 0.31, 1.0), 0.86),
        "trim": ensure_material("M_Hotel_DarkTrim_v0", unreal.LinearColor(0.09, 0.08, 0.075, 1.0), 0.74),
        "desk": ensure_material("M_Hotel_FrontDeskWood_v0", unreal.LinearColor(0.19, 0.11, 0.065, 1.0), 0.68),
        "black": ensure_material("M_Hotel_BlackPlastic_v0", unreal.LinearColor(0.01, 0.012, 0.014, 1.0), 0.55),
        "brass": ensure_material("M_Hotel_TarnishedBrass_v0", unreal.LinearColor(0.62, 0.43, 0.20, 1.0), 0.58),
        "dull_metal": ensure_material("M_Hotel_DullDeskMetal_v0", unreal.LinearColor(0.30, 0.29, 0.27, 1.0), 0.72),
        "deep_red": ensure_material("M_Hotel_AgedLedgerRed_v0", unreal.LinearColor(0.46, 0.045, 0.032, 1.0), 0.82),
        "return_faded_ink": ensure_material("M_Hotel_ReturnRouteFadedInk_v0", unreal.LinearColor(0.24, 0.115, 0.055, 1.0), 0.94),
        "paper": ensure_material("M_Hotel_AgedCallSlipPaper_v0", unreal.LinearColor(0.72, 0.64, 0.48, 1.0), 0.81),
        "button": ensure_material("M_Hotel_PhoneBoneButton_v0", unreal.LinearColor(0.58, 0.54, 0.46, 1.0), 0.62),
        "route_mark": ensure_material("M_Hotel_WornRouteTape_v0", unreal.LinearColor(0.46, 0.42, 0.32, 1.0), 0.88),
        "lobby_tape_cloth": ensure_material(
            "M_Hotel_LobbyDoorAgedTape_v0",
            unreal.LinearColor(0.055, 0.046, 0.036, 1.0),
            0.98,
            two_sided=True,
            force_recreate=True,
        ),
        "wall_peel": ensure_material("M_Hotel_PeeledWallpaperPaper_v0", unreal.LinearColor(0.72, 0.63, 0.46, 1.0), 0.93, two_sided=True),
        "wall_damp": ensure_material("M_Hotel_WallDampStain_v0", unreal.LinearColor(0.052, 0.050, 0.044, 1.0), 0.97, two_sided=True),
        "paper_tear_shadow": ensure_material("M_Hotel_PaperTearShadowBack_v0", unreal.LinearColor(0.13, 0.105, 0.078, 1.0), 0.96, two_sided=True),
        "paper_backing": ensure_material("M_Hotel_ExposedWallpaperBacking_v0", unreal.LinearColor(0.33, 0.265, 0.18, 1.0), 0.95, two_sided=True),
        "paper_edge": ensure_material("M_Hotel_TornPaperEdgeLight_v0", unreal.LinearColor(0.86, 0.74, 0.52, 1.0), 0.9, two_sided=True),
        "paper_stripe": ensure_material("M_Hotel_FadedWallpaperStripe_v0", unreal.LinearColor(0.055, 0.051, 0.043, 1.0), 0.97, two_sided=True),
        "floor_scuff": ensure_material("M_Hotel_FloorScuffDark_v0", unreal.LinearColor(0.040, 0.035, 0.031, 1.0), 0.95, two_sided=True),
        "return_cold_glow": ensure_material(
            "M_Hotel_ReturnRouteColdGlow_v0",
            unreal.LinearColor(0.040, 0.18, 0.22, 1.0),
            0.34,
            unreal.LinearColor(0.08, 1.05, 1.55, 1.0),
            two_sided=True,
        ),
        "return_slip_paper": ensure_textured_material("M_Hotel_ReturnRouteSlipPaperTextured_v0", return_slip_texture, 0.92, two_sided=True)
        if return_slip_texture
        else ensure_material(
            "M_Hotel_ReturnRouteSlipPaper_v0",
            unreal.LinearColor(0.82, 0.73, 0.55, 1.0),
            0.9,
            unreal.LinearColor(0.035, 0.026, 0.015, 1.0),
            two_sided=True,
        ),
        "ceiling_stain": ensure_material("M_Hotel_CeilingWaterStain_v0", unreal.LinearColor(0.105, 0.089, 0.063, 1.0), 0.98, two_sided=True),
        "paint_chip": ensure_material("M_Hotel_DoorPaintChipLight_v0", unreal.LinearColor(0.38, 0.33, 0.25, 1.0), 0.93),
        "screen": ensure_material("M_Hotel_MonitorGreen_v0", unreal.LinearColor(0.02, 0.18, 0.11, 1.0), 0.35),
        "door": ensure_textured_material("M_Hotel_RoomDoorPaintTextured_v0", room_door_texture, 0.83)
        if room_door_texture
        else ensure_material("M_Hotel_RoomDoorPaint_v0", unreal.LinearColor(0.23, 0.18, 0.13, 1.0), 0.77),
        "warn": ensure_material("M_Hotel_ServiceAmber_v0", unreal.LinearColor(0.75, 0.43, 0.12, 1.0), 0.63),
        "screen_glow": ensure_material(
            "M_Hotel_MonitorGreenGlow_v0",
            unreal.LinearColor(0.02, 0.22, 0.13, 1.0),
            0.28,
            unreal.LinearColor(0.0, 0.55, 0.28, 1.0),
        ),
        "security_monitor_feed": ensure_textured_material(
            "M_Hotel_SecurityMonitorFeed_v0",
            security_monitor_texture,
            0.42,
            emissive=True,
            emissive_strength=1.45,
            force_recreate=True,
        )
        if security_monitor_texture
        else ensure_material("M_Hotel_MonitorGreen_v0", unreal.LinearColor(0.02, 0.18, 0.11, 1.0), 0.35),
        "lobby_glass_smudge": ensure_textured_material("M_Hotel_LobbyDoorSmudgedGlass_v0", lobby_glass_texture, 0.63, two_sided=True)
        if lobby_glass_texture
        else ensure_material(
            "M_Hotel_LobbyDoorSmudgedGlass_v0",
            unreal.LinearColor(0.11, 0.18, 0.21, 1.0),
            0.66,
            unreal.LinearColor(0.02, 0.09, 0.12, 1.0),
            two_sided=True,
        ),
        "lobby_hand_oil": ensure_material(
            "M_Hotel_LobbyDoorHandOil_v0",
            unreal.LinearColor(0.09, 0.12, 0.12, 1.0),
            0.98,
            two_sided=True,
            force_recreate=True,
        ),
        "lobby_crack_light": ensure_material(
            "M_Hotel_LobbyDoorCrackLight_v0",
            unreal.LinearColor(0.12, 0.18, 0.19, 1.0),
            0.92,
            unreal.LinearColor(0.004, 0.018, 0.022, 1.0),
            two_sided=True,
            force_recreate=True,
        ),
        "warn_glow": ensure_material(
            "M_Hotel_ServiceAmberGlow_v0",
            unreal.LinearColor(0.85, 0.48, 0.14, 1.0),
            0.48,
            unreal.LinearColor(1.4, 0.62, 0.18, 1.0),
        ),
        "fluorescent_panel": ensure_material(
            "M_Hotel_FluorescentPanelGlow_v0",
            unreal.LinearColor(0.62, 0.72, 0.82, 1.0),
            0.22,
            unreal.LinearColor(1.45, 1.65, 1.95, 1.0),
        ),
        "desk_lamp": ensure_material(
            "M_Hotel_DeskLampGlow_v0",
            unreal.LinearColor(0.68, 0.48, 0.27, 1.0),
            0.72,
            unreal.LinearColor(0.055, 0.030, 0.012, 1.0),
        ),
        "frontdesk_hero_board": ensure_textured_material(
            "M_Hotel_FrontDeskHeroBoard_v0",
            frontdesk_hero_board_texture,
            0.78,
            emissive=True,
            emissive_strength=0.18,
            force_recreate=True,
        )
        if frontdesk_hero_board_texture
        else ensure_material("M_Hotel_FrontDeskHeroBoard_v0", unreal.LinearColor(0.19, 0.13, 0.08, 1.0), 0.84),
    }
    materials["report_log_paper"] = (
        ensure_textured_material("M_Hotel_ReportLogFiledPaper_v0", report_log_paper_texture, 0.89, two_sided=True)
        if report_log_paper_texture
        else materials["paper"]
    )

    # Front desk / lobby work hub.
    add_cube("AREA_FrontDesk_WorkHub_Floor", (0, 0, -10), (2500, 1600, 20), materials["floor"])
    add_cube("AREA_FrontDesk_BackWall_AgedBusinessHotel", (-900, 0, 140), (24, 1600, 280), materials["wall"])
    add_cube("AREA_FrontDesk_LeftWall_LobbyEdge", (0, -790, 140), (2500, 24, 280), materials["wall"])
    add_cube("AREA_FrontDesk_RightWall_ServiceEdge", (0, 790, 140), (2500, 24, 280), materials["wall"])
    add_cube("AREA_FrontDesk_Ceiling_LowPressure", (0, 0, 286), (2500, 1600, 20), materials["trim"])
    add_cube("PROP_FrontDesk_Counter_PlayerWorkSurface", (-430, -410, 55), (520, 120, 110), materials["desk"])
    add_cube("PROP_FrontDesk_BackShelf_KeyAndLogSilhouette", (-880, -400, 145), (30, 520, 170), materials["trim"])
    front_desk_art_tags = ("Hotel.Capture.Readability", "Hotel.ArtDensity.FrontDesk")
    hero_frontdesk_tags = front_desk_art_tags + ("Hotel.Capture.FirstSteamShot",)
    add_cube(
        "PROP_FrontDesk_BackWall_NightReceptionHeroBoard",
        (-884, -292, 205),
        (6, 278, 92),
        materials["frontdesk_hero_board"],
        hero_frontdesk_tags,
        no_collision=True,
    )
    add_cube("PROP_FrontDesk_BackWall_HeroBoardTopFrame", (-879, -292, 254), (8, 292, 5), materials["brass"], hero_frontdesk_tags, no_collision=True)
    add_cube("PROP_FrontDesk_BackWall_HeroBoardBottomFrame", (-879, -292, 156), (8, 292, 5), materials["brass"], hero_frontdesk_tags, no_collision=True)
    add_cube("PROP_FrontDesk_BackWall_HeroBoardLeftFrame", (-879, -436, 205), (8, 5, 100), materials["brass"], hero_frontdesk_tags, no_collision=True)
    add_cube("PROP_FrontDesk_BackWall_HeroBoardRightFrame", (-879, -148, 205), (8, 5, 100), materials["brass"], hero_frontdesk_tags, no_collision=True)
    add_cube("PROP_FrontDesk_KeyRack_DarkWoodBacking", (-874, -512, 164), (10, 132, 78), materials["desk"], hero_frontdesk_tags, no_collision=True)
    add_cube("PROP_FrontDesk_KeyRack_Missing203HookGlowTape", (-866, -492, 184), (6, 34, 4), materials["warn"], hero_frontdesk_tags, no_collision=True)
    add_cube("PROP_FrontDesk_KeyRack_Room203EmptySlotShadow", (-865, -492, 158), (7, 42, 22), materials["black"], hero_frontdesk_tags, no_collision=True)
    add_cube("PROP_FrontDesk_NightAuditPinnedNote_Room203", (-866, -566, 174), (7, 54, 38), materials["report_log_paper"], hero_frontdesk_tags, no_collision=True)
    add_cube("PROP_FrontDesk_NightAuditPinnedNote_203Underline", (-862, -566, 176), (8, 34, 3), materials["warn"], hero_frontdesk_tags, no_collision=True)
    phone_visual_tags = ("Hotel.Capture.Readability", "Hotel.Feedback.PhoneResponseVisual")

    add_cube("PROP_FrontDesk_DeskMat_UnderPhoneOnly", (-430, -529, 118), (170, 112, 6), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_BaseHeavyOldDeskSet", (-430, -525, 126), (108, 68, 18), materials["black"], ("Hotel.Capture.Readability",))
    add_cube("PROP_FrontDesk_Phone_AnswerLoopPlaceholder", (-430, -525, 140), (82, 48, 22), materials["black"], ("Hotel.Interact.Phone", "Hotel.Capture.Readability"))
    add_cube("PROP_FrontDesk_Phone_Keypad_ReadableCue", (-430, -523, 154), (56, 32, 5), materials["button"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_ButtonRowTop", (-430, -535, 160), (44, 5, 4), materials["paper"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_ButtonRowBottom", (-430, -516, 160), (44, 5, 4), materials["paper"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_CradleLeftHook", (-465, -550, 154), (10, 18, 12), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_CradleRightHook", (-395, -550, 154), (10, 18, 12), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_HookSwitch_DepressedCue", (-430, -548, 158), (34, 10, 8), materials["button"], phone_visual_tags, no_collision=True)
    authored_mesh_tags = ("Hotel.Capture.Readability", "Hotel.ArtDensity.FrontDesk", "Hotel.ArtSource.AuthoredMesh")
    authored_receiver_tags = (
        "Hotel.Feedback.PhoneReceiver",
        "Hotel.Capture.Readability",
        "Hotel.ArtDensity.FrontDesk",
        "Hotel.ArtSource.AuthoredMesh",
    )
    if "SM_FrontDesk_OldPhoneBody_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_Phone_AuthoredCurvedBody",
            meshes["SM_FrontDesk_OldPhoneBody_v0"],
            (-430, -525, 143),
            (1.0, 1.0, 1.0),
            materials["black"],
            authored_mesh_tags,
            no_collision=True,
        )
    if "SM_FrontDesk_CurvedReceiver_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_Phone_ReceiverAuthoredSilhouette",
            meshes["SM_FrontDesk_CurvedReceiver_v0"],
            (-430, -558, 153),
            (0.92, 1.0, 1.0),
            materials["black"],
            authored_receiver_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_cube(
        "PROP_FrontDesk_Phone_ReceiverCue",
        (-430, -558, 150),
        (74, 14, 12),
        materials["black"],
        ("Hotel.Feedback.PhoneReceiver", "Hotel.Capture.Readability"),
        unreal.ComponentMobility.MOVABLE,
    )
    add_cube(
        "PROP_FrontDesk_Phone_ReceiverLeftCap",
        (-466, -558, 151),
        (18, 22, 16),
        materials["black"],
        ("Hotel.Feedback.PhoneReceiver", "Hotel.Capture.Readability"),
        unreal.ComponentMobility.MOVABLE,
    )
    add_cube(
        "PROP_FrontDesk_Phone_ReceiverRightCap",
        (-394, -558, 151),
        (18, 22, 16),
        materials["black"],
        ("Hotel.Feedback.PhoneReceiver", "Hotel.Capture.Readability"),
        unreal.ComponentMobility.MOVABLE,
    )
    add_cube("PROP_FrontDesk_Phone_CradleShadow", (-430, -547, 138), (86, 44, 12), materials["trim"])
    add_cube("PROP_FrontDesk_Phone_CoiledCordCue", (-378, -556, 137), (42, 8, 8), materials["trim"])
    add_cube("PROP_FrontDesk_Phone_CoiledCordLoopA", (-354, -553, 137), (16, 8, 8), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_CoiledCordLoopB", (-336, -560, 137), (16, 8, 8), materials["trim"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_Phone_CoiledCordLoopC", (-318, -553, 137), (16, 8, 8), materials["trim"], phone_visual_tags, no_collision=True)
    receiver_art_tags = ("Hotel.Feedback.PhoneReceiver", "Hotel.Capture.Readability", "Hotel.ArtDensity.FrontDesk")
    if "SM_FrontDesk_CoiledPhoneCord_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_Phone_AuthoredCoiledCord",
            meshes["SM_FrontDesk_CoiledPhoneCord_v0"],
            (-356, -558, 140),
            (0.74, 0.7, 0.7),
            materials["black"],
            authored_mesh_tags + ("Hotel.Feedback.PhoneCordTug",),
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_cylinder("PROP_FrontDesk_Phone_RoundedDialPlate", (-430, -523, 162), 54, 7, materials["button"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_DialFingerHoleTop", (-430, -542, 167), 9, 4, materials["black"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_DialFingerHoleLeft", (-448, -523, 167), 9, 4, materials["black"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_DialFingerHoleRight", (-412, -523, 167), 9, 4, materials["black"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_DialFingerStop", (-400, -542, 168), 6, 18, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_ReceiverLeftRoundCup", (-466, -558, 159), 26, 10, materials["black"], receiver_art_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cylinder("PROP_FrontDesk_Phone_ReceiverRightRoundCup", (-394, -558, 159), 26, 10, materials["black"], receiver_art_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_sphere("PROP_FrontDesk_Phone_CordRoundLoopA", (-354, -553, 140), (15, 9, 7), materials["black"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_Phone_CordRoundLoopB", (-336, -560, 140), (15, 9, 7), materials["black"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_Phone_CordRoundLoopC", (-318, -553, 140), (15, 9, 7), materials["black"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_ServiceBell_Dome", (-525, -505, 133), 40, 18, materials["dull_metal"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_ServiceBell_Button", (-525, -505, 149), (14, 14, 10), materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_DeskLamp_RoundFoot", (-300, -557, 132), 28, 7, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_DeskLamp_ThinStem", (-300, -557, 154), 5, 40, materials["brass"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_DeskLamp_ShadeCurvedSilhouette", (-294, -553, 169), (35, 17, 12), materials["desk_lamp"], front_desk_art_tags, no_collision=True)
    add_cube("LIGHTMESH_FrontDesk_PhoneCallLamp", (-395, -555, 158), (18, 8, 10), materials["warn_glow"], ("Hotel.Feedback.PhoneRingLamp", "Hotel.Capture.Readability"))
    monitor_feed_tags = (
        "Hotel.Interact.Monitor",
        "Hotel.Capture.Readability",
        "Hotel.Capture.SecurityMonitorFeed",
    )
    monitor_feedback_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.SecurityMonitorFeed",
        "Hotel.Feedback.MonitorCheckVisual",
    )
    monitor_art_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.SecurityMonitorFeed",
        "Hotel.ArtDensity.FrontDesk",
    )
    add_cube("PROP_Surveillance_Monitor_CRT_Housing", (-620, -520, 160), (168, 34, 106), materials["black"], ("Hotel.Capture.Readability", "Hotel.Capture.SecurityMonitorFeed"), no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PlayerChecksHall", (-620, -541, 160), (132, 6, 74), materials["security_monitor_feed"], monitor_feed_tags)
    add_cube("PROP_Surveillance_Monitor_CRT_BezelTop", (-620, -548, 202), (148, 7, 8), materials["black"], monitor_art_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_CRT_BezelBottom", (-620, -548, 118), (148, 7, 10), materials["black"], monitor_art_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_CRT_BezelLeft", (-692, -548, 160), (8, 7, 82), materials["black"], monitor_art_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_CRT_BezelRight", (-548, -548, 160), (8, 7, 82), materials["black"], monitor_art_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_ChannelLabelTape203", (-642, -553, 209), (30, 1, 2), materials["report_log_paper"], monitor_art_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_RecordRedLED", (-552, -554, 128), (7, 3, 7), materials["deep_red"], monitor_art_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_ControlButtonRow", (-607, -554, 127), (34, 3, 5), materials["dull_metal"], monitor_art_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_ControlKnobA", (-578, -554, 128), (8, 3, 8), materials["brass"], monitor_art_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_ControlKnobB", (-565, -554, 128), (7, 3, 7), materials["brass"], monitor_art_tags, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_CheckFeedGlassReflection", (-676, -545, 160), (3, 2, 38), materials["screen_glow"], ("Hotel.Capture.Readability", "Hotel.Capture.SecurityMonitorFeed"), no_collision=True)
    add_cube("PROP_Surveillance_Monitor_CheckScanlineSweepA", (-642, -548, 176), (20, 1, 1), materials["screen_glow"], monitor_feedback_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_CheckScanlineSweepB", (-600, -548, 144), (22, 1, 1), materials["screen_glow"], monitor_feedback_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_CheckRoom203TargetBox", (-585, -549, 159), (1, 1, 8), materials["screen_glow"], monitor_feedback_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_CheckNoGuestUnderline", (-646, -549, 134), (12, 1, 1), materials["warn"], monitor_feedback_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_CheckTimestampBlock", (-574, -549, 186), (8, 1, 1), materials["screen_glow"], monitor_feedback_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("LIGHTMESH_Surveillance_Monitor_CheckGlow", (-620, -550, 122), (118, 3, 4), materials["screen_glow"], ("Hotel.Capture.Readability", "Hotel.Capture.SecurityMonitorFeed"), no_collision=True)
    monitor_mismatch_tags = ("Hotel.Capture.Readability", "Hotel.Capture.PostReportMonitorMismatch", "Hotel.Feedback.PostReportMonitorMismatchVisual")
    add_cube("PROP_Surveillance_Monitor_PostReportFeedFrame", (-620, -536, 160), (112, 5, 58), materials["screen"], monitor_mismatch_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportStaticBarA", (-646, -540, 178), (16, 1, 1), materials["screen_glow"], monitor_mismatch_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportStaticBarB", (-602, -540, 143), (18, 1, 1), materials["screen_glow"], monitor_mismatch_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportOpenDoorGlyph", (-585, -542, 159), (1, 1, 9), materials["warn_glow"], monitor_mismatch_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportRoom203Dot", (-608, -543, 174), (2, 1, 2), materials["warn"], monitor_mismatch_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Surveillance_Monitor_PostReportTimestampSmear", (-656, -542, 132), (12, 1, 1), materials["screen_glow"], monitor_mismatch_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_PullOutWritingShelf", (-185, -590, 130), (150, 112, 14), materials["desk"], ("Hotel.Capture.Readability", "Hotel.ArtDensity.FrontDesk"), no_collision=True)
    add_cube("PROP_ReportLog_ReturnAndRecordPoint", (-185, -590, 139), (118, 72, 2), materials["paper"], ("Hotel.Interact.ReportLog",))
    if "SM_FrontDesk_ReportLogFiledPaper_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_NightLog_OpenPage_Readable",
            meshes["SM_FrontDesk_ReportLogFiledPaper_v0"],
            (-185, -590, 146),
            (1.22, 1.02, 1.0),
            materials["report_log_paper"],
            authored_mesh_tags + ("Hotel.Feedback.ReportLogVisual",),
            no_collision=True,
        )
    else:
        add_cube("PROP_FrontDesk_NightLog_OpenPage_Readable", (-220, -592, 141), (84, 50, 2), materials["paper"], ("Hotel.Capture.Readability",), no_collision=True)
    if "SM_FrontDesk_CurledLedgerPages_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_ReportLog_AuthoredCurledPages",
            meshes["SM_FrontDesk_CurledLedgerPages_v0"],
            (-232, -617, 147),
            (0.24, 0.16, 0.18),
            materials["paper"],
            authored_mesh_tags + ("Hotel.Feedback.ReportLogFiledReaction",),
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    report_log_tags = ("Hotel.Capture.Readability", "Hotel.Feedback.ReportLogVisual")
    report_log_filed_tags = ("Hotel.Capture.Readability", "Hotel.Feedback.ReportLogVisual", "Hotel.Feedback.ReportLogFiled")
    report_log_filing_reaction_tags = report_log_filed_tags + ("Hotel.Feedback.ReportLogFiledReaction",)
    add_cube("PROP_FrontDesk_ReportLog_ClipboardClip_Readable", (-185, -626, 149), (26, 4, 0.45), materials["trim"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_IncidentHeaderCue", (-185, -612, 148), (40, 1.3, 0.28), materials["return_faded_ink"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_Room203EntryLine", (-191, -597, 148), (44, 1.3, 0.28), materials["return_faded_ink"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_TimeBoxCue", (-146, -583, 148), (20, 5, 0.28), materials["return_faded_ink"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_RefusedCheckbox", (-227, -582, 148), (5, 5, 0.28), materials["return_faded_ink"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_RefusedCheckmarkShort", (-229, -580, 148.4), (2, 6, 0.35), materials["warn"], report_log_tags, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_RefusedCheckmarkLong", (-223, -578, 148.4), (11, 2, 0.35), materials["warn"], report_log_tags, no_collision=True)
    if "SM_FrontDesk_FiledStamp_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_ReportLog_FiledStampCue",
            meshes["SM_FrontDesk_FiledStamp_v0"],
            (-211, -609, 149.7),
            (0.16, 0.16, 0.16),
            materials["warn"],
            report_log_filing_reaction_tags + ("Hotel.ArtSource.AuthoredMesh",),
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
            rotation=(0.0, 0.0, -8.0),
        )
    else:
        add_cube("PROP_FrontDesk_ReportLog_FiledStampCue", (-236, -586, 145), (38, 16, 3), materials["warn"], report_log_filing_reaction_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    if "SM_FrontDesk_LogPenBody_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_ReportLog_AuthoredPenBody",
            meshes["SM_FrontDesk_LogPenBody_v0"],
            (-118, -601, 150.8),
            (0.30, 0.30, 0.30),
            materials["black"],
            report_log_tags + ("Hotel.Feedback.ReportLogFiledReaction", "Hotel.ArtSource.AuthoredMesh"),
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
            rotation=(0.0, 0.0, -8.0),
        )
    if "SM_FrontDesk_LogPenNib_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_ReportLog_AuthoredPenNib",
            meshes["SM_FrontDesk_LogPenNib_v0"],
            (-104, -604, 150.8),
            (0.30, 0.30, 0.30),
            materials["warn"],
            report_log_tags + ("Hotel.Feedback.ReportLogFiledReaction", "Hotel.ArtSource.AuthoredMesh"),
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
            rotation=(0.0, 0.0, -8.0),
        )
    if "SM_FrontDesk_ReportFiledInk_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_ReportLog_FiledInkStrokes",
            meshes["SM_FrontDesk_ReportFiledInk_v0"],
            (-183, -583, 148.9),
            (0.34, 0.34, 0.34),
            materials["deep_red"],
            report_log_filing_reaction_tags + ("Hotel.ArtSource.AuthoredMesh",),
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
            rotation=(0.0, 0.0, -4.0),
        )
    add_cylinder("PROP_FrontDesk_ReportLog_BinderRingTop", (-240, -616, 150), 5, 5, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_ReportLog_BinderRingBottom", (-240, -579, 150), 5, 5, materials["brass"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_ReportLog_RedInkSmear", (-173, -587, 149), (10, 3, 1), materials["deep_red"], front_desk_art_tags, no_collision=True)
    log_self_correction_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.PostReportLogSelfCorrection",
        "Hotel.Feedback.PostReportLogSelfCorrection",
    )
    log_self_correction_visual_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.PostReportLogSelfCorrection",
        "Hotel.Feedback.PostReportLogSelfCorrectionVisual",
    )
    add_cube("PROP_FrontDesk_ReportLog_SelfCorrectedRoom203OpenLine", (-170, -591, 148), (62, 4, 3), materials["warn_glow"], log_self_correction_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_SelfCorrectedNoGuestLine", (-167, -581, 148), (54, 4, 3), materials["screen_glow"], log_self_correction_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_FrontDesk_ReportLog_SelfCorrectedTimestampSlash", (-191, -571, 148), (30, 4, 3), materials["warn"], log_self_correction_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("LIGHTMESH_FrontDesk_ReportLog_SelfCorrectionCue", (-155, -601, 168), (38, 8, 10), materials["warn_glow"], log_self_correction_visual_tags, no_collision=True)
    night_audit_work_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.FirstSteamShot",
        "Hotel.ArtDensity.FrontDesk",
    )
    if "SM_FrontDesk_ReportLogFiledPaper_v0" in meshes:
        add_authored_mesh(
            "PROP_FrontDesk_NightAudit_OpenLedgerWarmPage",
            meshes["SM_FrontDesk_ReportLogFiledPaper_v0"],
            (-520, -604, 130.8),
            (0.72, 0.52, 0.52),
            materials["report_log_paper"],
            night_audit_work_tags + ("Hotel.ArtSource.AuthoredMesh",),
            no_collision=True,
            rotation=(0.0, 0.0, 7.0),
        )
        add_authored_mesh(
            "PROP_FrontDesk_NightAudit_CheckoutSlipCurl",
            meshes["SM_FrontDesk_ReportLogFiledPaper_v0"],
            (-590, -572, 131.2),
            (0.45, 0.32, 0.32),
            materials["paper"],
            night_audit_work_tags + ("Hotel.ArtSource.AuthoredMesh",),
            no_collision=True,
            rotation=(0.0, 0.0, -13.0),
        )
    else:
        add_cube("PROP_FrontDesk_NightAudit_OpenLedgerWarmPage", (-520, -604, 131), (96, 58, 3), materials["report_log_paper"], night_audit_work_tags, no_collision=True)
    add_cube("PROP_FrontDesk_NightAudit_Room203AmberTab", (-516, -622, 134), (78, 9, 2), materials["warn"], night_audit_work_tags, no_collision=True)
    add_cube("PROP_FrontDesk_NightAudit_DeskShiftCard", (-585, -615, 134), (62, 26, 2), materials["warn"], night_audit_work_tags, no_collision=True)
    add_cube("PROP_FrontDesk_NightAudit_StampPadAgedBrown", (-555, -543, 133), (54, 28, 8), materials["return_faded_ink"], night_audit_work_tags, no_collision=True)
    add_cube("PROP_FrontDesk_NightAudit_KeyReturnTrayBrassLip", (-498, -568, 134), (72, 8, 6), materials["brass"], night_audit_work_tags, no_collision=True)
    add_cube("PROP_FrontDesk_CallSlip_Room203_CameraMismatchCue", (-315, -565, 131), (76, 38, 4), materials["paper"], phone_visual_tags, no_collision=True)
    add_cube("PROP_FrontDesk_CallSlip_Underline203", (-315, -565, 135), (42, 4, 3), materials["warn"], phone_visual_tags, no_collision=True)
    add_cube("LIGHTMESH_FrontDesk_DeskLampPractical", (-294, -553, 169), (28, 8, 8), materials["desk_lamp"], ("Hotel.Capture.Readability", "Hotel.Feedback.ReportLogFiledReaction"), unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cylinder("PROP_FrontDesk_BackShelf_KeyHookA", (-858, -560, 176), 6, 28, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_BackShelf_KeyHookB", (-858, -495, 176), 6, 28, materials["brass"], front_desk_art_tags, no_collision=True)
    add_cylinder("PROP_FrontDesk_BackShelf_KeyHookC", (-858, -430, 176), 6, 28, materials["brass"], front_desk_art_tags, no_collision=True)
    add_sphere("PROP_FrontDesk_BackShelf_KeyTag203", (-858, -495, 148), (22, 10, 26), materials["paper"], front_desk_art_tags, no_collision=True)
    add_cube("AREA_Lobby_GuestAdmissionThreshold", (780, 0, -8), (620, 1280, 16), materials["floor"])
    add_cube("PROP_Lobby_MainGlassDoor_Silhouette", (1080, -250, 110), (28, 270, 220), materials["lobby_glass_smudge"])
    add_cube("PROP_Lobby_MainGlassDoor_RefuseLine", (1080, 250, 110), (28, 270, 220), materials["lobby_glass_smudge"])
    post_report_desk_wait_tags = ("Hotel.Capture.Readability", "Hotel.Capture.PostReportDeskWait", "Hotel.Feedback.PostReportDeskWaitVisual")
    add_cube("PROP_FrontDesk_FloorWaitMarker_PostReport", (-260, -620, 4), (220, 80, 4), materials["route_mark"], post_report_desk_wait_tags, no_collision=True)
    add_cube("PROP_FrontDesk_CounterHoldLine_PostReport", (-210, -475, 122), (180, 6, 5), materials["warn"], post_report_desk_wait_tags, no_collision=True)
    retired_blockout_size = (0.2, 0.2, 0.2)
    add_cube("PROP_Lobby_GlassDoor_PostReportHoldClosedTape", (1062, -250, 172), retired_blockout_size, materials["lobby_tape_cloth"], post_report_desk_wait_tags, no_collision=True)
    add_cube("PROP_Lobby_GlassDoor_PostReportOutsidePalmSmear", (1060, -312, 132), retired_blockout_size, materials["lobby_hand_oil"], post_report_desk_wait_tags, no_collision=True)
    add_cube("PROP_Lobby_GlassDoor_PostReportNoGuestReflection", (1058, -188, 112), retired_blockout_size, materials["black"], post_report_desk_wait_tags, no_collision=True)
    add_cube("LIGHTMESH_LobbyDoor_PostReportRattleCue", (1035, -308, 181), retired_blockout_size, materials["lobby_crack_light"], post_report_desk_wait_tags, no_collision=True)
    post_report_lobby_art_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.PostReportDeskWait",
        "Hotel.Feedback.PostReportDeskWaitVisual",
        "Hotel.ArtDensity.FrontDesk",
        "Hotel.ArtSource.AuthoredMesh",
    )
    desk_wait_rattle_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.PostReportDeskWait",
        "Hotel.Feedback.PostReportDeskWaitRattle",
        "Hotel.ArtDensity.FrontDesk",
    )
    desk_wait_authored_rattle_tags = desk_wait_rattle_tags + ("Hotel.ArtSource.AuthoredMesh",)
    if "SM_LobbyDoor_SmudgedGlassPane_v0" in meshes:
        add_authored_mesh(
            "PROP_Lobby_GlassDoor_PostReportSmudgedPane_Authored",
            meshes["SM_LobbyDoor_SmudgedGlassPane_v0"],
            (1054, -250, 114),
            (0.01, 0.01, 0.01),
            materials["lobby_glass_smudge"],
            post_report_lobby_art_tags,
            no_collision=True,
        )
    if "SM_LobbyDoor_PalmSmear_v0" in meshes:
        add_authored_mesh(
            "PROP_Lobby_GlassDoor_PostReportPalmSmear_Authored",
            meshes["SM_LobbyDoor_PalmSmear_v0"],
            (1051, -250, 126),
            (0.18, 0.18, 0.18),
            materials["lobby_hand_oil"],
            post_report_lobby_art_tags,
            no_collision=True,
        )
    if "SM_LobbyDoor_CrackWeb_v0" in meshes:
        add_authored_mesh(
            "PROP_Lobby_GlassDoor_PostReportCrackWeb_Authored",
            meshes["SM_LobbyDoor_CrackWeb_v0"],
            (1049, -250, 126),
            (1.0, 1.0, 1.0),
            materials["lobby_crack_light"],
            post_report_lobby_art_tags + (
                "Hotel.Feedback.PostReportDeskWaitRattle",
                "Hotel.Feedback.PostReportDeskWaitCrack",
            ),
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_LobbyDoor_TornTapeCross_v0" in meshes:
        add_authored_mesh(
            "PROP_Lobby_GlassDoor_PostReportTapeCross_Authored",
            meshes["SM_LobbyDoor_TornTapeCross_v0"],
            (1047, -266, 111),
            (0.32, 0.32, 0.32),
            materials["lobby_tape_cloth"],
            desk_wait_authored_rattle_tags + ("Hotel.Feedback.PostReportDeskWaitTape",),
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_LobbyDoor_LatchPlate_v0" in meshes:
        add_authored_mesh(
            "PROP_Lobby_GlassDoor_PostReportLatchPlate_Authored",
            meshes["SM_LobbyDoor_LatchPlate_v0"],
            (1048, -250, 142),
            (0.72, 0.72, 0.72),
            materials["dull_metal"],
            desk_wait_authored_rattle_tags + ("Hotel.Feedback.PostReportDeskWaitLatch",),
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_cylinder("PROP_Lobby_GlassDoor_PostReportHandleRattleBar", (1055, -250, 134), 0.2, 0.2, materials["dull_metal"], desk_wait_rattle_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cylinder("PROP_Lobby_GlassDoor_PostReportLatchRattlePin", (1048, -250, 158), 0.2, 0.2, materials["brass"], desk_wait_rattle_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    add_cube("PROP_Lobby_GlassDoor_PostReportTapeLooseEnd", (1053, -355, 178), retired_blockout_size, materials["lobby_tape_cloth"], desk_wait_rattle_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)

    # Controlled transition from work hub to guest-floor response.
    add_cube("AREA_Transition_CarpetRun_ToGuestHall_NoVoid", (1625, 0, -9), (750, 560, 18), materials["floor"])
    add_cube("AREA_Transition_LeftSightlineWall_ToGuestHall", (1625, -290, 140), (750, 24, 280), materials["wall"])
    add_cube("AREA_Transition_RightSightlineWall_ToGuestHall", (1625, 290, 140), (750, 24, 280), materials["wall"])
    transition_tags = ("Hotel.Capture.Readability", "Hotel.Capture.TransitionFear")
    add_cube("TRANSITION_Elevator_Door_AudibleBeforeSeen", (1160, 565, 120), (34, 280, 240), materials["door"], transition_tags)
    add_cube("TRANSITION_Elevator_CallPanel_SoundCueAnchor", (1125, 385, 120), (12, 30, 80), materials["warn_glow"], transition_tags, no_collision=True)
    add_cube("TRANSITION_Elevator_FloorIndicator_WrongFloorCue", (1124, 565, 214), (10, 92, 24), materials["warn_glow"], transition_tags, no_collision=True)
    add_cube("TRANSITION_Elevator_ClosedSeam_ShadowCue", (1142, 565, 121), (6, 10, 214), materials["black"], transition_tags, no_collision=True)
    add_cube("TRANSITION_EmergencyStair_Door_AlternateRoute", (1160, -565, 120), (34, 280, 240), materials["door"], transition_tags)
    add_cube("TRANSITION_EmergencyStair_ExitSign_ColdCue", (1125, -565, 230), (10, 120, 26), materials["screen_glow"], transition_tags, no_collision=True)
    add_cube("TRANSITION_EmergencyStair_DoorHandle_ShadowCue", (1135, -450, 126), (12, 30, 16), materials["black"], transition_tags, no_collision=True)
    add_cube("TRANSITION_ServiceBackHall_LockedShortcut", (430, 770, 110), (330, 26, 220), materials["trim"], transition_tags)
    add_cube("TRANSITION_ServiceBackHall_ChainLockedShortcutCue", (430, 745, 142), (210, 8, 10), materials["warn"], transition_tags, no_collision=True)
    patrol_decision_tags = ("Hotel.Capture.Readability", "Hotel.Capture.TransitionFear", "Hotel.Capture.PatrolDecision")
    add_cube("PATROL_Route_DecisionStopLine_ListenBeforeMoving", (930, 0, 3), (260, 10, 4), materials["route_mark"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_DecisionStopLine_CenterBreak", (930, 0, 8), (24, 24, 5), materials["warn"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_ElevatorTrack_FootstepA", (980, 210, 5), (42, 18, 4), materials["trim"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_ElevatorTrack_FootstepB", (1040, 320, 5), (42, 18, 4), materials["trim"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_ElevatorTrack_FootstepStopped", (1085, 440, 5), (44, 20, 4), materials["trim"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_StairReturn_FootstepA", (980, -185, 5), (42, 18, 4), materials["black"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_StairReturn_FootstepB", (1035, -310, 5), (42, 18, 4), materials["black"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_StairReturn_ScrapeMark", (1090, -438, 5), (76, 8, 4), materials["route_mark"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_DroppedKeyTag_ReturnCue", (955, -70, 9), (44, 24, 5), materials["warn"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_NightAuditClipboard_ElevatorOrStairChoice", (1015, 0, 16), (92, 64, 5), materials["paper"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_Clipboard_ElevatorMark", (1015, 22, 20), (56, 5, 3), materials["warn"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_Clipboard_StairMark", (1015, -22, 20), (56, 5, 3), materials["screen_glow"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_WallArrow_ElevatorNoiseCue", (1110, 205, 112), (8, 86, 12), materials["warn_glow"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_WallArrow_StairAirCue", (1110, -210, 112), (8, 86, 12), materials["screen_glow"], patrol_decision_tags, no_collision=True)
    add_cube("PATROL_Route_StairDoor_ColdLightLeak", (1136, -565, 30), (8, 206, 14), materials["screen_glow"], patrol_decision_tags, no_collision=True)

    # Guest hallway response line.
    add_cube("AREA_GuestHall_Floor_OneDoorSlice", (3250, 0, -10), (2500, 560, 20), materials["floor"])
    add_cube("AREA_GuestHall_LeftWall_CameraMismatchSide", (3250, -290, 140), (2500, 24, 280), materials["wall"])
    add_cube("AREA_GuestHall_RightWall_DoorDecisionSide", (3250, 290, 140), (2500, 24, 280), materials["guesthall_wallpaper"])
    add_cube("AREA_GuestHall_Ceiling_LowPressure", (3250, 0, 286), (2500, 560, 20), materials["trim"])
    add_cube("PROP_GuestHall_Camera_MonitorMismatchAnchor", (2600, -282, 220), (36, 20, 28), materials["black"])
    guesthall_decay_tags = (
        "Hotel.Capture.Readability",
        "Hotel.Capture.GuestDoor",
        "Hotel.Capture.Room203Surface",
        "Hotel.ArtDensity.GuestHall",
        "Hotel.ArtDensity.Room203",
        "Hotel.ArtSurface.Room203MaterialPass",
        "Hotel.ArtSource.ProjectAuthoredMaterial",
    )
    guesthall_authored_decay_tags = guesthall_decay_tags + ("Hotel.ArtSource.AuthoredMesh",)
    room203_wallpaper_flutter_tags = guesthall_authored_decay_tags + (
        "Hotel.Feedback.Room203WallpaperFlutter",
        "Hotel.Capture.Room203Aftershock",
    )
    add_cube("PROP_GuestHall_RightWall_Baseboard_RunTo203_A", (3260, 274, 25), (940, 12, 28), materials["trim"], guesthall_decay_tags, no_collision=True)
    add_cube("PROP_GuestHall_RightWall_Baseboard_RunTo203_B", (4300, 274, 25), (330, 12, 28), materials["trim"], guesthall_decay_tags, no_collision=True)
    add_cube("PROP_GuestHall_LeftWall_Baseboard_CameraSide", (3320, -274, 24), (1460, 12, 26), materials["trim"], guesthall_decay_tags, no_collision=True)
    add_cube("PROP_GuestHall_Room203_FramePaintChip_LeftTop", (3785, 255, 194), (9, 5, 31), materials["paint_chip"], guesthall_decay_tags, no_collision=True)
    add_cube("PROP_GuestHall_Room203_FramePaintChip_LeftLow", (3785, 255, 83), (9, 5, 42), materials["paint_chip"], guesthall_decay_tags, no_collision=True)
    add_cube("PROP_GuestHall_Room203_FramePaintChip_RightMid", (4055, 255, 142), (9, 5, 53), materials["paint_chip"], guesthall_decay_tags, no_collision=True)
    add_cube("PROP_GuestHall_Room203_ThresholdDustCollect", (3920, 251, 8), (250, 20, 5), materials["floor_scuff"], guesthall_decay_tags, no_collision=True)
    add_sphere("PROP_GuestHall_LeftWall_DampPatch_CameraSide", (2980, -273, 172), (170, 7, 92), materials["wall_damp"], guesthall_decay_tags, no_collision=True)
    stripe_tags = guesthall_decay_tags + ("Hotel.Capture.Room203Aftershock",)
    add_cube("PROP_GuestHall_RightWall_FadedWallpaperStripe_Room203_A", (3558, 278, 158), (1, 1, 118), materials["wall_damp"], stripe_tags, no_collision=True)
    add_cube("PROP_GuestHall_RightWall_FadedWallpaperStripe_Room203_B", (3666, 278, 154), (1, 1, 130), materials["wall_damp"], stripe_tags, no_collision=True)
    add_cube("PROP_GuestHall_RightWall_FadedWallpaperStripe_Room203_C", (3788, 278, 160), (1, 1, 108), materials["wall_damp"], stripe_tags, no_collision=True)
    add_cube("PROP_GuestHall_RightWall_FadedWallpaperStripe_Room203_D", (3912, 278, 157), (1, 1, 122), materials["wall_damp"], stripe_tags, no_collision=True)
    add_cube("PROP_GuestHall_RightWall_FadedWallpaperWaterline_Room203", (3760, 279, 226), (410, 3, 4), materials["wall_damp"], stripe_tags, no_collision=True)
    if "SM_GuestHall_PeelingWallpaperPatch_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_RightWall_AuthoredDampUnderPeel_Room203Approach",
            meshes["SM_GuestHall_PeelingWallpaperPatch_v0"],
            (3536, 275, 158),
            (1.08, 1.0, 0.98),
            materials["wall_damp"],
            guesthall_authored_decay_tags,
            no_collision=True,
        )
        add_authored_mesh(
            "PROP_GuestHall_RightWall_AuthoredPeelingWallpaper_CameraReadable",
            meshes["SM_GuestHall_PeelingWallpaperPatch_v0"],
            (3445, 276, 135),
            (0.82, 1.0, 0.78),
            materials["paper_edge"],
            room203_wallpaper_flutter_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
        add_authored_mesh(
            "PROP_GuestHall_RightWall_AuthoredPeelingWallpaper_Room203",
            meshes["SM_GuestHall_PeelingWallpaperPatch_v0"],
            (3624, 276, 158),
            (0.54, 1.0, 0.72),
            materials["wall_peel"],
            room203_wallpaper_flutter_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_GuestHall_Room203AftershockTearShadow_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_RightWall_Room203AftershockTearShadow",
            meshes["SM_GuestHall_Room203AftershockTearShadow_v0"],
            (3702, 274, 165),
            (1.02, 1.0, 1.03),
            materials["paper_tear_shadow"],
            guesthall_authored_decay_tags + ("Hotel.Capture.Room203Aftershock",),
            no_collision=True,
        )
        add_authored_mesh(
            "PROP_GuestHall_RightWall_Room203AftershockInteriorCuts",
            meshes["SM_GuestHall_Room203AftershockTearShadow_v0"],
            (3616, 273, 154),
            (0.46, 1.0, 0.54),
            materials["paper_tear_shadow"],
            guesthall_authored_decay_tags + ("Hotel.Capture.Room203Aftershock",),
            no_collision=True,
        )
    if "SM_GuestHall_Room203AftershockPaper_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_RightWall_Room203AftershockLoosePaper",
            meshes["SM_GuestHall_Room203AftershockPaper_v0"],
            (3700, 277, 166),
            (0.82, 1.0, 0.82),
            materials["paper_edge"],
            room203_wallpaper_flutter_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
        add_authored_mesh(
            "PROP_GuestHall_RightWall_Room203AftershockHighCurl",
            meshes["SM_GuestHall_Room203AftershockPaper_v0"],
            (3568, 277, 192),
            (0.46, 1.0, 0.46),
            materials["paper_edge"],
            room203_wallpaper_flutter_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
        add_authored_mesh(
            "PROP_GuestHall_RightWall_Room203AftershockLowCurl",
            meshes["SM_GuestHall_Room203AftershockPaper_v0"],
            (3810, 278, 124),
            (0.42, 1.0, 0.40),
            materials["paper_edge"],
            room203_wallpaper_flutter_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_GuestHall_Room203AftershockRawEdge_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_RightWall_Room203AftershockRawEdgeThreads",
            meshes["SM_GuestHall_Room203AftershockRawEdge_v0"],
            (3705, 279, 166),
            (1.0, 1.0, 1.0),
            materials["paper_edge"],
            guesthall_authored_decay_tags + ("Hotel.Capture.Room203Aftershock",),
            no_collision=True,
        )
    if "SM_GuestHall_FloorScuffCluster_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Floor_AuthoredScuffPath_ToRoom203",
            meshes["SM_GuestHall_FloorScuffCluster_v0"],
            (3370, -20, 2),
            (1.0, 1.0, 1.0),
            materials["floor_scuff"],
            guesthall_authored_decay_tags,
            no_collision=True,
        )
    if "SM_GuestHall_CeilingWaterStain_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Ceiling_AuthoredWaterStain_FluorescentB",
            meshes["SM_GuestHall_CeilingWaterStain_v0"],
            (3920, 20, 274),
            (1.0, 0.72, 1.0),
            materials["ceiling_stain"],
            guesthall_authored_decay_tags,
            no_collision=True,
        )
    return_route_tags = ("Hotel.Capture.Readability", "Hotel.Capture.ReturnRouteAnomaly")
    return_route_backknock_tags = return_route_tags + ("Hotel.Feedback.ReturnRouteBackKnock",)
    return_route_authored_tags = return_route_backknock_tags + ("Hotel.ArtSource.AuthoredMesh",)
    if "SM_GuestHall_ReturnRouteFloorEcho_v0" in meshes:
        add_authored_mesh(
            "RETURN_Route_Floor_AuthoredBackstepSmear_Foreground",
            meshes["SM_GuestHall_ReturnRouteFloorEcho_v0"],
            (2885, -38, 3),
            (1.0, 1.0, 1.0),
            materials["floor_scuff"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
        add_authored_mesh(
            "RETURN_Route_Floor_ColdRipple_AfterRefusal",
            meshes["SM_GuestHall_ReturnRouteFloorEcho_v0"],
            (2862, 28, 4),
            (0.72, 0.88, 1.0),
            materials["return_cold_glow"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_GuestHall_ReturnRouteWallEcho_v0" in meshes:
        add_authored_mesh(
            "RETURN_Route_RightWall_BackKnockShadow_Echo",
            meshes["SM_GuestHall_ReturnRouteWallEcho_v0"],
            (3285, 276, 136),
            (0.48, 1.0, 0.36),
            materials["wall_damp"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
        add_authored_mesh(
            "RETURN_Route_RightWall_ColdPressureRipple",
            meshes["SM_GuestHall_ReturnRouteWallEcho_v0"],
            (3204, 274, 116),
            (0.12, 1.0, 0.12),
            materials["wall_damp"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_GuestHall_ReturnRouteHandShadow_v0" in meshes:
        add_authored_mesh(
            "RETURN_Route_RightWall_PalmDragShadow_BackKnock",
            meshes["SM_GuestHall_ReturnRouteHandShadow_v0"],
            (3098, 277, 158),
            (0.30, 1.0, 0.30),
            materials["paper_tear_shadow"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_GuestHall_ReturnRouteColdVein_v0" in meshes:
        add_authored_mesh(
            "RETURN_Route_FloorColdPatch_AfterRefusal",
            meshes["SM_GuestHall_ReturnRouteColdVein_v0"],
            (2860, 0, 4),
            (1.0, 1.0, 1.0),
            materials["return_cold_glow"],
            return_route_tags + ("Hotel.ArtSource.AuthoredMesh",),
            no_collision=True,
        )
    else:
        add_cube("RETURN_Route_FloorColdPatch_AfterRefusal", (2860, 0, 4), (270, 360, 3), materials["return_cold_glow"], return_route_tags, no_collision=True)
    if "SM_GuestHall_ReturnRouteDirectionScratch_v0" in meshes:
        add_authored_mesh(
            "RETURN_Route_BackKnockDirectionStripe",
            meshes["SM_GuestHall_ReturnRouteDirectionScratch_v0"],
            (2860, -84, 9),
            (0.62, 0.62, 0.62),
            materials["floor_scuff"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
        add_authored_mesh(
            "RETURN_Route_BackKnockDirectionStripe_Return",
            meshes["SM_GuestHall_ReturnRouteDirectionScratch_v0"],
            (2860, 84, 9),
            (0.34, 0.34, 0.34),
            materials["floor_scuff"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
            rotation=(0.0, 180.0, 0.0),
        )
    else:
        add_cube("RETURN_Route_BackKnockDirectionStripe", (2860, -84, 9), (196, 7, 3), materials["warn"], return_route_backknock_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
        add_cube("RETURN_Route_BackKnockDirectionStripe_Return", (2860, 84, 9), (196, 7, 3), materials["warn"], return_route_backknock_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    if "SM_GuestHall_ReturnRouteTornSlip_v0" in meshes:
        add_authored_mesh(
            "RETURN_Route_WallStatusSlip_ReportAfterHall",
            meshes["SM_GuestHall_ReturnRouteTornSlip_v0"],
            (3135, 268, 126),
            (0.28, 1.0, 0.30),
            materials["return_slip_paper"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    else:
        add_cube("RETURN_Route_WallStatusSlip_ReportAfterHall", (3135, 276, 126), (82, 6, 48), materials["paper"], return_route_backknock_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    if "SM_GuestHall_ReturnRouteWarningUnderline_v0" in meshes:
        add_authored_mesh(
            "RETURN_Route_WallStatusSlip_Underline",
            meshes["SM_GuestHall_ReturnRouteWarningUnderline_v0"],
            (3135, 264, 101),
            (0.16, 1.0, 0.18),
            materials["return_faded_ink"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    else:
        add_cube("RETURN_Route_WallStatusSlip_Underline", (3135, 273, 106), (56, 4, 4), materials["warn"], return_route_backknock_tags, unreal.ComponentMobility.MOVABLE, no_collision=True)
    if "SM_GuestHall_ReturnRouteSlipWriting_v0" in meshes:
        add_authored_mesh(
            "RETURN_Route_WallStatusSlip_FranticWriting",
            meshes["SM_GuestHall_ReturnRouteSlipWriting_v0"],
            (3135, 263, 126),
            (0.10, 1.0, 0.10),
            materials["return_faded_ink"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_GuestHall_ReturnRouteFootprint_v0" in meshes:
        add_authored_mesh(
            "RETURN_Route_FootprintBacktrackA",
            meshes["SM_GuestHall_ReturnRouteFootprint_v0"],
            (3040, -90, 5),
            (0.78, 0.78, 0.78),
            materials["floor_scuff"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
            rotation=(0.0, -8.0, 0.0),
        )
        add_authored_mesh(
            "RETURN_Route_FootprintBacktrackB",
            meshes["SM_GuestHall_ReturnRouteFootprint_v0"],
            (2920, -32, 5),
            (0.70, 0.70, 0.70),
            materials["floor_scuff"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
            rotation=(0.0, -17.0, 0.0),
        )
        add_authored_mesh(
            "RETURN_Route_FootprintBacktrackC",
            meshes["SM_GuestHall_ReturnRouteFootprint_v0"],
            (2785, 48, 5),
            (0.64, 0.64, 0.64),
            materials["floor_scuff"],
            return_route_authored_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
            rotation=(0.0, -24.0, 0.0),
        )
    else:
        add_cube("RETURN_Route_FootprintBacktrackA", (3040, -90, 5), (32, 12, 2), materials["black"], return_route_tags, no_collision=True)
        add_cube("RETURN_Route_FootprintBacktrackB", (2920, -32, 5), (32, 12, 2), materials["black"], return_route_tags, no_collision=True)
        add_cube("RETURN_Route_FootprintBacktrackC", (2785, 48, 5), (32, 12, 2), materials["black"], return_route_tags, no_collision=True)
    add_cube("RETURN_Route_CeilingLightmesh_ColdPulseCue", (2860, -90, 273), (280, 34, 9), materials["fluorescent_panel"], return_route_tags, no_collision=True)
    add_cube(
        "RETURN_Route_CeilingLightmesh_PursuitTailCue",
        (3020, -30, 270),
        (180, 24, 7),
        materials["return_cold_glow"],
        return_route_tags + ("Hotel.Feedback.ReturnRouteTailLight",),
        no_collision=True,
    )
    door_decision_tags = ("Hotel.Capture.Readability", "Hotel.Feedback.Room203DoorDecisionVisual")
    door_refusal_tags = ("Hotel.Feedback.Room203Refusal", "Hotel.Capture.Readability")
    door_latch_refusal_tags = door_refusal_tags + ("Hotel.Feedback.Room203LatchJolt",)
    door_chain_refusal_tags = door_refusal_tags + ("Hotel.Feedback.Room203ChainJolt",)
    door_surface_refusal_tags = door_refusal_tags + ("Hotel.Feedback.Room203DoorSurfaceJolt",)
    door_evidence_reaction_tags = door_refusal_tags + ("Hotel.Feedback.Room203EvidenceReaction",)
    room203_art_tags = ("Hotel.Capture.Readability", "Hotel.ArtDensity.Room203", "Hotel.ArtSource.AuthoredMesh")
    add_cube("PROP_GuestHall_RoomDoor203_OpenRefuseDecision", (3920, 302, 120), (260, 28, 240), materials["door"], ("Hotel.Interact.Room203Door",))
    if "SM_Room203_PaneledDoor_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_AuthoredPaneledDoor",
            meshes["SM_Room203_PaneledDoor_v0"],
            (3920, 264, 120),
            (1.0, 1.0, 1.0),
            materials["door"],
            room203_art_tags + door_surface_refusal_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_cube("PROP_GuestHall_Room203_LeftDoorJamb", (3784, 272, 122), (14, 12, 244), materials["trim"])
    add_cube("PROP_GuestHall_Room203_RightDoorJamb", (4056, 272, 122), (14, 12, 244), materials["trim"])
    add_cube("PROP_GuestHall_Room203_TopDoorJamb", (3920, 272, 245), (286, 12, 14), materials["trim"])
    add_cube("PROP_GuestHall_Room203_DarkLatchGap", (4042, 266, 122), (8, 8, 188), materials["black"])
    add_cube(
        "PROP_GuestHall_Room203_NumberPlate",
        (3840, 257, 190),
        (76, 3, 30),
        materials["black"],
        room203_art_tags + door_decision_tags + door_evidence_reaction_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    if "SM_Room203_NumberDigits_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_NumberDigits_Authored",
            meshes["SM_Room203_NumberDigits_v0"],
            (3838, 252, 190),
            (0.92, 1.0, 0.92),
            materials["paper_edge"],
            room203_art_tags + door_decision_tags + door_evidence_reaction_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_Room203_DoorGrimeStreaks_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_DoorGrimeStreaks_Authored",
            meshes["SM_Room203_DoorGrimeStreaks_v0"],
            (3920, 255, 120),
            (1.0, 1.0, 1.0),
            materials["floor_scuff"],
            room203_art_tags + door_surface_refusal_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_Room203_DoorPaintChips_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_DoorPaintChips_Authored",
            meshes["SM_Room203_DoorPaintChips_v0"],
            (3920, 254, 120),
            (0.58, 1.0, 0.58),
            materials["paint_chip"],
            room203_art_tags + door_surface_refusal_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_cube(
        "PROP_GuestHall_Room203_HandleBackplate_Readable",
        (4028, 257, 132),
        (16, 5, 58),
        materials["black"],
        door_decision_tags + door_evidence_reaction_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    if "SM_Room203_LockHardwareBreakup_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_LockHardwareBreakup_Authored",
            meshes["SM_Room203_LockHardwareBreakup_v0"],
            (4028, 253, 132),
            (1.0, 1.0, 1.0),
            materials["dull_metal"],
            room203_art_tags + door_latch_refusal_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_Room203_HandleLever_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_AuthoredHandleLever",
            meshes["SM_Room203_HandleLever_v0"],
            (4028, 256, 132),
            (1.0, 1.0, 1.0),
            materials["dull_metal"],
            room203_art_tags + door_latch_refusal_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_cube(
        "PROP_GuestHall_Room203_LatchJoltCue",
        (4046, 257, 143),
        (28, 6, 7),
        materials["dull_metal"],
        door_latch_refusal_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    add_cube(
        "PROP_GuestHall_Room203_ChainJoltCue",
        (3992, 258, 166),
        (26, 4, 4),
        materials["dull_metal"],
        door_chain_refusal_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    if "SM_Room203_ChainLinks_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_AuthoredChainLinks",
            meshes["SM_Room203_ChainLinks_v0"],
            (3992, 257, 166),
            (0.40, 0.40, 0.40),
            materials["dull_metal"],
            room203_art_tags + door_chain_refusal_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_cube(
        "PROP_GuestHall_Room203_DoorEdgeSlamShadowCue",
        (4042, 255, 124),
        (10, 6, 168),
        materials["black"],
        door_surface_refusal_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    add_cube(
        "PROP_GuestHall_Room203_NoticeCornerJoltCue",
        (3908, 256, 124),
        (11, 4, 9),
        materials["paper_edge"],
        door_surface_refusal_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    if "SM_Room203_TornNotice_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_AuthoredTornNotice",
            meshes["SM_Room203_TornNotice_v0"],
            (3880, 255, 112),
            (1.0, 1.0, 1.0),
            materials["paper"],
            room203_art_tags + door_surface_refusal_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_sphere(
        "PROP_GuestHall_Room203_PeepholeBlackCue",
        (3920, 257, 186),
        (16, 4, 16),
        materials["black"],
        door_decision_tags + door_evidence_reaction_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    if "SM_Room203_NoticeWriting_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_DoNotOpenNotice",
            meshes["SM_Room203_NoticeWriting_v0"],
            (3880, 252, 112),
            (1.0, 1.0, 1.0),
            materials["return_faded_ink"],
            room203_art_tags + door_decision_tags + door_evidence_reaction_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    else:
        add_cube(
            "PROP_GuestHall_Room203_DoNotOpenNotice",
            (3880, 256, 112),
            (42, 4, 24),
            materials["paper"],
            door_decision_tags + door_evidence_reaction_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_Room203_NoticeTape_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203_NoticeUnderline",
            meshes["SM_Room203_NoticeTape_v0"],
            (3880, 252, 101),
            (0.78, 1.0, 0.78),
            materials["warn"],
            room203_art_tags + door_decision_tags + door_evidence_reaction_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    else:
        add_cube(
            "PROP_GuestHall_Room203_NoticeUnderline",
            (3880, 256, 101),
            (34, 4, 3),
            materials["warn"],
            door_decision_tags + door_evidence_reaction_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    add_cube(
        "PROP_GuestHall_Room203_ThresholdShadow",
        (3920, 257, 2),
        (230, 18, 6),
        materials["black"],
        door_decision_tags,
        unreal.ComponentMobility.MOVABLE,
        no_collision=True,
    )
    if "SM_Room203_SconceGlass_v0" in meshes:
        add_authored_mesh(
            "LIGHTMESH_GuestHall_Room203DoorPractical",
            meshes["SM_Room203_SconceGlass_v0"],
            (3778, 254, 214),
            (0.46, 0.46, 0.46),
            materials["warn_glow"],
            room203_art_tags + ("Hotel.Capture.Readability",) + door_evidence_reaction_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    else:
        add_cube(
            "LIGHTMESH_GuestHall_Room203DoorPractical",
            (3775, 260, 212),
            (32, 4, 24),
            materials["warn_glow"],
            ("Hotel.Capture.Readability",) + door_evidence_reaction_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_Room203_SconceBracket_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_Room203DoorPractical_Bracket",
            meshes["SM_Room203_SconceBracket_v0"],
            (3778, 253, 214),
            (0.52, 0.52, 0.52),
            materials["dull_metal"],
            room203_art_tags + ("Hotel.Capture.Readability",) + door_evidence_reaction_tags,
            unreal.ComponentMobility.MOVABLE,
            no_collision=True,
        )
    if "SM_GuestHall_ServiceCartSilhouette_v0" in meshes:
        add_authored_mesh(
            "PROP_GuestHall_ServiceCart_BlockingSightline",
            meshes["SM_GuestHall_ServiceCartSilhouette_v0"],
            (3370, -208, 52),
            (1.0, 1.0, 1.0),
            materials["trim"],
            guesthall_authored_decay_tags,
            no_collision=True,
        )
    else:
        add_cube("PROP_GuestHall_ServiceCart_BlockingSightline", (3380, -205, 46), (120, 58, 78), materials["trim"])
    add_cube("PROP_GuestHall_EndShadow_NoSmallRoomExtension", (4450, 0, 125), (44, 520, 250), materials["black"])
    add_cube("LIGHTMESH_GuestHall_FluorescentPanelA", (2820, 0, 274), (260, 28, 6), materials["fluorescent_panel"], ("Hotel.Capture.Readability",))
    add_cube("LIGHTMESH_GuestHall_FluorescentPanelB", (3920, 0, 274), (260, 28, 6), materials["fluorescent_panel"], ("Hotel.Capture.Readability",))
    add_cube("LIGHTMESH_FrontDesk_OverheadFluorescent", (-260, -330, 276), (460, 54, 10), materials["fluorescent_panel"], ("Hotel.Capture.Readability",))

    # Lighting and atmosphere: final-intent mood direction, still placeholder geometry.
    add_light("LIGHT_FrontDesk_TiredWarmCounter", unreal.RectLight, (-250, -440, 232), (-68, 0, 0), 2800.0, unreal.Color(255, 184, 116, 255), attenuation_radius=1250.0, source_width=360.0, source_height=90.0)
    add_light("LIGHT_FrontDesk_WorkSurfacePracticalFill", unreal.PointLight, (-455, -590, 178), (0, 0, 0), 1100.0, unreal.Color(255, 184, 104, 255), ("Hotel.Capture.Readability", "Hotel.Capture.FirstSteamShot"), attenuation_radius=640.0)
    add_light("LIGHT_FrontDesk_PhoneCallLampPulse", unreal.PointLight, (-395, -555, 158), (0, 0, 0), 360.0, unreal.Color(255, 168, 72, 255), ("Hotel.Feedback.PhoneRingLamp", "Hotel.Capture.Readability"), attenuation_radius=280.0)
    add_light("LIGHT_FrontDesk_CaptureEvidenceSoftFill", unreal.PointLight, (-110, -565, 210), (0, 0, 0), 900.0, unreal.Color(255, 205, 145, 255), ("Hotel.Capture.Readability",), attenuation_radius=900.0)
    add_light("LIGHT_FrontDesk_PhoneResponseEvidenceFill", unreal.PointLight, (-390, -650, 188), (0, 0, 0), 2600.0, unreal.Color(255, 196, 132, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PhoneResponse"), attenuation_radius=780.0)
    add_light("LIGHT_FrontDesk_NightAuditLedgerWarmPractical", unreal.PointLight, (-525, -610, 164), (0, 0, 0), 1800.0, unreal.Color(255, 178, 92, 255), ("Hotel.Capture.Readability", "Hotel.Capture.FirstSteamShot"), attenuation_radius=520.0)
    add_light("LIGHT_FrontDesk_HeroBoardWarmSkim", unreal.PointLight, (-735, -300, 218), (0, 0, 0), 680.0, unreal.Color(255, 174, 84, 255), ("Hotel.Capture.Readability", "Hotel.Capture.FirstSteamShot"), attenuation_radius=460.0)
    add_light("LIGHT_Surveillance_Monitor_CheckPulse", unreal.PointLight, (-620, -552, 178), (0, 0, 0), 420.0, unreal.Color(86, 255, 164, 255), ("Hotel.Capture.Readability", "Hotel.Capture.SecurityMonitorFeed", "Hotel.Feedback.MonitorCheckLight"), attenuation_radius=360.0)
    add_light("LIGHT_Lobby_ColdExteriorSpill", unreal.RectLight, (1000, 0, 230), (-75, 0, 180), 2200.0, unreal.Color(120, 165, 255, 255), attenuation_radius=950.0, source_width=280.0, source_height=240.0)
    add_light("LIGHT_Elevator_SickAmberTransition", unreal.PointLight, (1120, 565, 210), (0, 0, 0), 1400.0, unreal.Color(255, 198, 90, 255), attenuation_radius=780.0)
    add_light("LIGHT_Transition_ElevatorCallPanelDread", unreal.PointLight, (1122, 398, 150), (0, 0, 0), 980.0, unreal.Color(255, 155, 58, 255), ("Hotel.Capture.TransitionFear",), attenuation_radius=360.0)
    add_light("LIGHT_Transition_StairExitCold", unreal.PointLight, (1122, -560, 230), (0, 0, 0), 720.0, unreal.Color(92, 210, 170, 255), ("Hotel.Capture.TransitionFear",), attenuation_radius=420.0)
    add_light("LIGHT_Transition_CaptureEvidenceSoftFill", unreal.PointLight, (925, 0, 190), (0, 0, 0), 4300.0, unreal.Color(178, 218, 205, 255), ("Hotel.Capture.Readability", "Hotel.Capture.TransitionFear"), attenuation_radius=980.0)
    add_light("LIGHT_Transition_EvidenceWideFill", unreal.PointLight, (770, 0, 185), (0, 0, 0), 17000.0, unreal.Color(164, 214, 205, 255), ("Hotel.Capture.Readability", "Hotel.Capture.TransitionFear"), attenuation_radius=1600.0)
    add_light("LIGHT_PatrolRoute_DecisionCueFloorFill", unreal.PointLight, (955, 0, 115), (0, 0, 0), 1100.0, unreal.Color(190, 218, 194, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PatrolDecision", "Hotel.Feedback.PatrolListenLight"), attenuation_radius=520.0)
    add_light("LIGHT_GuestHall_WeakFluorescentA", unreal.RectLight, (2820, 0, 262), (-90, 0, 0), 4800.0, unreal.Color(205, 225, 255, 255), attenuation_radius=1120.0, source_width=380.0, source_height=55.0)
    add_light("LIGHT_ReturnRoute_ColdPulseAfterRefusal", unreal.PointLight, (2860, -90, 188), (0, 0, 0), 620.0, unreal.Color(120, 225, 255, 255), ("Hotel.Capture.Readability", "Hotel.Capture.ReturnRouteAnomaly", "Hotel.Feedback.ReturnRouteLight"), attenuation_radius=680.0)
    add_light("LIGHT_ReturnRoute_PursuitTailColdSkim", unreal.PointLight, (3020, -30, 174), (0, 0, 0), 120.0, unreal.Color(95, 220, 255, 255), ("Hotel.Capture.Readability", "Hotel.Capture.ReturnRouteAnomaly", "Hotel.Feedback.ReturnRouteTailLight"), attenuation_radius=560.0)
    add_light("LIGHT_ReturnRoute_BackKnockWallSkim", unreal.PointLight, (3190, 220, 154), (0, 0, 0), 1650.0, unreal.Color(118, 225, 255, 255), ("Hotel.Capture.Readability", "Hotel.Capture.ReturnRouteAnomaly"), attenuation_radius=520.0)
    add_light("LIGHT_GuestHall_WeakFluorescentB_TargetDoor", unreal.RectLight, (3920, 0, 262), (-90, 0, 0), 4200.0, unreal.Color(178, 206, 255, 255), ("Hotel.Feedback.Room203Light",), attenuation_radius=1160.0, source_width=380.0, source_height=55.0)
    add_light(
        "LIGHT_GuestHall_Room203PlatePractical",
        unreal.PointLight,
        (3785, 252, 205),
        (0, 0, 0),
        460.0,
        unreal.Color(255, 178, 82, 255),
        ("Hotel.Capture.Readability", "Hotel.Feedback.Room203DoorPracticalLight"),
        attenuation_radius=320.0,
    )
    add_light("LIGHT_GuestHall_CaptureEvidenceDoorFill", unreal.PointLight, (3590, 105, 215), (0, 0, 0), 8800.0, unreal.Color(210, 230, 255, 255), ("Hotel.Capture.Readability", "Hotel.Capture.Room203Surface"), attenuation_radius=1180.0)
    add_light("LIGHT_GuestHall_TrailerProofDoorKicker", unreal.PointLight, (3340, -170, 178), (0, 0, 0), 2200.0, unreal.Color(195, 224, 255, 255), ("Hotel.Capture.Readability", "Hotel.Capture.Room203Surface"), attenuation_radius=820.0)
    add_light("LIGHT_GuestHall_Room203AftershockPaperSkimFill", unreal.PointLight, (3705, 118, 178), (0, 0, 0), 4600.0, unreal.Color(255, 214, 158, 255), ("Hotel.Capture.Readability", "Hotel.Capture.Room203Aftershock"), attenuation_radius=820.0)
    add_light("LIGHT_GuestHall_Room203TornPaperEdgeRim", unreal.PointLight, (3435, 72, 138), (0, 0, 0), 2100.0, unreal.Color(255, 225, 176, 255), ("Hotel.Capture.Readability", "Hotel.Capture.Room203Aftershock"), attenuation_radius=560.0)
    add_light("LIGHT_MonitorToHall_CaptureEvidenceGreenFill", unreal.PointLight, (-575, -555, 188), (0, 0, 0), 1250.0, unreal.Color(120, 255, 190, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PostReportMonitorMismatch", "Hotel.Feedback.PostReportMonitorMismatchLight"), attenuation_radius=560.0)
    add_light("LIGHT_FrontDesk_ReportLogFiledDeskLampPulse", unreal.PointLight, (-294, -553, 169), (0, 0, 0), 180.0, unreal.Color(255, 198, 132, 255), ("Hotel.Capture.Readability", "Hotel.Capture.ReportLogFiledPressure", "Hotel.Feedback.ReportLogFiledLight"), attenuation_radius=360.0)
    add_light("LIGHT_LobbyDoor_PostReportRattleColdPulse", unreal.PointLight, (1035, -250, 170), (0, 0, 0), 920.0, unreal.Color(120, 190, 255, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PostReportDeskWait", "Hotel.Feedback.PostReportDeskWaitLight"), attenuation_radius=620.0)
    add_light("LIGHT_LobbyDoor_PostReportSurfaceSkim", unreal.PointLight, (845, -460, 188), (0, 0, 0), 2500.0, unreal.Color(150, 205, 245, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PostReportDeskWait", "Hotel.Feedback.PostReportDeskWaitLight"), attenuation_radius=680.0)
    add_light("LIGHT_PostReportDeskWait_EvidenceFill", unreal.PointLight, (-290, -650, 190), (0, 0, 0), 7200.0, unreal.Color(185, 220, 255, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PostReportDeskWait"), attenuation_radius=1250.0)
    add_light("LIGHT_FrontDesk_ReportLog_SelfCorrectionAmberPulse", unreal.PointLight, (-190, -520, 166), (0, 0, 0), 520.0, unreal.Color(255, 190, 120, 255), ("Hotel.Capture.Readability", "Hotel.Capture.PostReportLogSelfCorrection", "Hotel.Feedback.PostReportLogSelfCorrectionLight"), attenuation_radius=420.0)

    fog = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.ExponentialHeightFog,
        unreal.Vector(2100, 0, 0),
        make_rotator(0, 0, 0),
    )
    fog.set_actor_label("ATMOS_SubtleHotelDustFog")
    add_post_process_volume("PPV_HotelNightShift_ReadableHorrorExposure")

    player_start = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.PlayerStart,
        unreal.Vector(-260, -635, 92),
        make_rotator(0.0, 54.0, 0.0),
    )
    player_start.set_actor_label("PLAYERSTART_FrontDesk_FacingPhoneAndMonitor")

    add_camera("CAPTURE_FrontDesk_FirstSteamShotCandidate", (-250, -730, 230), (-20.0, 135, 0), 72.0, ("Hotel.Capture.FirstSteamShot",))
    add_camera("CAPTURE_SecurityMonitorFeed_ReadabilityCandidate", (-445, -710, 178), (0.5, 126, 0), 62.0, ("Hotel.Capture.SecurityMonitorFeed",))
    add_camera("CAPTURE_ReportLog_ReadabilityCandidate", (-255, -660, 218), (-28, 90, 0), 48.0)
    add_camera("CAPTURE_PhoneResponse_LiftReceiverCandidate", (-255, -704, 208), (-18, 136, 0), 62.0)
    add_camera("CAPTURE_Transition_ElevatorStair_AudioFearCandidate", (760, -18, 168), (1, 0, 0), 76.0)
    add_camera("CAPTURE_PatrolRoute_DecisionCueCandidate", (780, -430, 214), (-20, 58, 0), 78.0)
    add_camera("CAPTURE_GuestDoor_15SecondBeatCandidate", (3185, -205, 164), (1.5, 30, 0), 52.0, ("Hotel.Capture.Room203Surface", "Hotel.Capture.Room203Aftershock"))
    add_camera("CAPTURE_ReturnRoute_BackKnockCandidate", (2668, -248, 158), (0.5, 43, 0), 46.0, ("Hotel.Capture.ReturnRouteAnomaly",))
    add_camera("CAPTURE_PostReportMonitorMismatchCandidate", (-780, -620, 180), (2, 28, 0), 72.0)
    add_camera("CAPTURE_PostReportDeskWait_DoNotAnswerCandidate", (-350, -720, 174), (1, 22, 0), 72.0)
    add_camera("CAPTURE_PostReportLogSelfCorrectionCandidate", (-265, -690, 218), (-30, 88, 0), 52.0)

    if "AMB_LobbyFluorescentHum_v0" in sounds:
        add_audio("AMB_Lobby_FluorescentHum_Source_v0", sounds["AMB_LobbyFluorescentHum_v0"], (-180, -450, 210), True)
    if "AMB_GuestHallDrone_v0" in sounds:
        add_audio("AMB_GuestHall_Drone_Source_v0", sounds["AMB_GuestHallDrone_v0"], (3380, 0, 210), True)
    if "AMB_ElevatorShaftGroan_v0" in sounds:
        add_audio("AMB_Elevator_ShaftGroan_Source_v0", sounds["AMB_ElevatorShaftGroan_v0"], (1120, 565, 180), True, ("Hotel.Audio.ElevatorShaftGroan",))
        add_audio("AMB_PatrolRoute_ElevatorGroanBleed_Source_v0", sounds["AMB_ElevatorShaftGroan_v0"], (960, 250, 164), True, ("Hotel.Audio.ElevatorShaftGroan", "Hotel.Audio.PatrolDecision"))
    if "AMB_StairwellAir_v0" in sounds:
        add_audio("AMB_Stairwell_Air_Source_v0", sounds["AMB_StairwellAir_v0"], (1120, -565, 180), True, ("Hotel.Audio.StairwellAir",))
        add_audio("AMB_PatrolRoute_StairAirBleed_Source_v0", sounds["AMB_StairwellAir_v0"], (960, -250, 164), True, ("Hotel.Audio.StairwellAir", "Hotel.Audio.PatrolDecision"))
    if "SFX_PatrolListenDrop_v0" in sounds:
        add_audio("SFX_PatrolListen_StopLine_ManualTrigger_v0", sounds["SFX_PatrolListenDrop_v0"], (930, 0, 72), False, ("Hotel.Audio.PatrolListen",))
    if "SFX_ReturnRouteKnockback_v0" in sounds:
        add_audio("SFX_ReturnRoute_BackKnock_ManualTrigger_v0", sounds["SFX_ReturnRouteKnockback_v0"], (3420, 270, 150), False, ("Hotel.Audio.ReturnRoute",))
    if "SFX_ReturnRoutePursuitTail_v0" in sounds:
        add_audio("SFX_ReturnRoute_PursuitTail_ManualTrigger_v0", sounds["SFX_ReturnRoutePursuitTail_v0"], (3020, -70, 155), False, ("Hotel.Audio.ReturnRouteTail",))
    if "SFX_PostReportMonitorMismatch_v0" in sounds:
        add_audio("SFX_PostReportMonitorMismatch_ManualTrigger_v0", sounds["SFX_PostReportMonitorMismatch_v0"], (-620, -542, 172), False, ("Hotel.Audio.PostReportMonitorMismatch",))
    if "SFX_PostReportDeskWaitRattle_v0" in sounds:
        add_audio("SFX_PostReportDeskWait_Rattle_ManualTrigger_v0", sounds["SFX_PostReportDeskWaitRattle_v0"], (1080, -250, 150), False, ("Hotel.Audio.PostReportDeskWait",))
    if "SFX_PostReportLogSelfCorrection_v0" in sounds:
        add_audio("SFX_PostReportLogSelfCorrection_ManualTrigger_v0", sounds["SFX_PostReportLogSelfCorrection_v0"], (-214, -494, 154), False, ("Hotel.Audio.PostReportLogSelfCorrection",))
    if "SFX_PhoneRing_v0" in sounds:
        add_audio("SFX_PhoneRing_FrontDesk_ManualTrigger_v0", sounds["SFX_PhoneRing_v0"], (-430, -525, 150), False, ("Hotel.Audio.PhoneRing",))
    if "SFX_PhonePickup_v0" in sounds:
        add_audio("SFX_PhonePickup_FrontDesk_ManualTrigger_v0", sounds["SFX_PhonePickup_v0"], (-430, -548, 150), False, ("Hotel.Audio.PhonePickup",))
    if "SFX_PhoneLineStatic_v0" in sounds:
        add_audio("SFX_PhoneLineStatic_FrontDesk_ConnectedCue_v0", sounds["SFX_PhoneLineStatic_v0"], (-438, -552, 154), False, ("Hotel.Audio.PhoneLineStatic",))
    if "SFX_MonitorCheckGlitch_v0" in sounds:
        add_audio("SFX_MonitorCheckGlitch_FrontDesk_ManualTrigger_v0", sounds["SFX_MonitorCheckGlitch_v0"], (-620, -542, 172), False, ("Hotel.Audio.MonitorCheck",))
    if "SFX_DoorKnock203_v0" in sounds:
        add_audio("SFX_DoorKnock203_ManualTrigger_v0", sounds["SFX_DoorKnock203_v0"], (3920, 285, 150), False, ("Hotel.Audio.Room203Knock",))
    if "SFX_Room203AftershockRustle_v0" in sounds:
        add_audio("SFX_Room203AftershockRustle_ManualTrigger_v0", sounds["SFX_Room203AftershockRustle_v0"], (3725, 276, 168), False, ("Hotel.Audio.Room203Aftershock",))
    if "SFX_ReportLogFiled_v0" in sounds:
        add_audio("SFX_ReportLogFiled_FrontDesk_ManualTrigger_v0", sounds["SFX_ReportLogFiled_v0"], (-185, -583, 154), False, ("Hotel.Audio.ReportLogFiled",))

    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)


def main() -> None:
    log("Preparing directories.")
    ensure_dirs()
    log("Generating project-authored placeholder WAV sources.")
    source_audio = generate_source_audio()
    log("Generating project-authored procedural OBJ meshes.")
    source_meshes = generate_source_meshes()
    log("Generating project-authored procedural texture sources.")
    source_textures = generate_source_textures()
    log("Importing audio into /Game/Hotel/Audio.")
    sounds = import_audio(source_audio)
    log("Importing authored meshes into /Game/Hotel/Meshes.")
    meshes = import_static_meshes(source_meshes)
    log("Importing authored textures into /Game/Hotel/Textures.")
    textures = import_textures(source_textures)
    log("Building production-intent hotel spine level.")
    build_level(sounds, meshes, textures)
    log("Scrubbing public-repo unsafe texture import metadata.")
    scrub_texture_import_metadata(source_textures)
    log("Done.")


main()
