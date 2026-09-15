#!/usr/bin/env python3
"""Generate the iOS app icon (opaque 1024×1024 PNG)."""

from pathlib import Path

from PIL import Image, ImageDraw


def star_points(cx: float, cy: float, outer: float, inner: float, n: int = 8) -> list[tuple[float, float]]:
    from math import cos, pi, sin

    pts: list[tuple[float, float]] = []
    for i in range(n * 2):
        r = outer if i % 2 == 0 else inner
        a = -pi / 2 + i * pi / n
        pts.append((cx + r * cos(a), cy + r * sin(a)))
    return pts


def main() -> None:
    size = 1024
    img = Image.new("RGB", (size, size), (196, 85, 47))
    draw = ImageDraw.Draw(img)

    cream = (251, 245, 236)
    gold = (188, 148, 70)
    deep = (139, 58, 34)
    sage = (91, 122, 110)

    margin = 78
    draw.rounded_rectangle(
        (margin, margin, size - margin, size - margin),
        radius=180,
        fill=cream,
    )

    # Inner tile
    inner = 168
    draw.rounded_rectangle(
        (inner, inner, size - inner, size - inner),
        radius=96,
        outline=gold,
        width=14,
    )

    cx = cy = size / 2
    draw.polygon(star_points(cx, cy, 250, 118), fill=deep)
    draw.polygon(star_points(cx, cy, 168, 78), fill=gold)
    draw.ellipse((cx - 64, cy - 64, cx + 64, cy + 64), fill=cream)
    draw.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=sage)

    out_dir = Path(__file__).resolve().parents[1] / "App" / "Assets.xcassets" / "AppIcon.appiconset"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "AppIcon.png"
    img.save(path, "PNG")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
