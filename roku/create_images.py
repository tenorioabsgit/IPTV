"""
Generate placeholder images for the SepulnationTV Roku channel.

Images produced:
  - icon_focus_hd.png   336x210   (focused channel icon, HD)
  - icon_focus_sd.png   246x140   (focused channel icon, SD)
  - splash_hd.png      1280x720   (splash screen, HD)
  - splash_fhd.png     1920x1080  (splash screen, FHD)

All images use a dark background (#0D0D0D) with cyan (#00E5FF) accent
text and a thin horizontal accent line.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BG_COLOR = "#0D0D0D"
ACCENT_COLOR = "#00E5FF"
APP_NAME = "SepulnationTV"

IMAGES = [
    # (filename, width, height, kind)
    ("icon_focus_hd.png", 336, 210, "icon"),
    ("icon_focus_sd.png", 246, 140, "icon"),
    ("splash_hd.png", 1280, 720, "splash"),
    ("splash_fhd.png", 1920, 1080, "splash"),
]

OUTPUT_DIR = Path(__file__).resolve().parent / "images"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _best_font(size):
    """Return the best available font at the requested pixel size."""
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            return ImageFont.truetype(path, size)
    # Fall back to Pillow's built-in bitmap font.
    return ImageFont.load_default()


def _draw_icon(img):
    """Draw a simple branded icon (small image)."""
    w, h = img.size
    draw = ImageDraw.Draw(img)

    # Choose a font size proportional to the image height.
    font_size = max(14, h // 6)
    font = _best_font(font_size)

    # --- Accent line (horizontal, near the bottom third) ---
    line_y = int(h * 0.72)
    line_margin = int(w * 0.15)
    draw.line(
        [(line_margin, line_y), (w - line_margin, line_y)],
        fill=ACCENT_COLOR,
        width=2,
    )

    # --- App name centred above the line ---
    bbox = draw.textbbox((0, 0), APP_NAME, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = (line_y - th) // 2
    draw.text((tx, ty), APP_NAME, fill=ACCENT_COLOR, font=font)


def _draw_splash(img):
    """Draw a branded splash screen (large image)."""
    w, h = img.size
    draw = ImageDraw.Draw(img)

    # --- Title ---
    title_size = max(28, h // 10)
    title_font = _best_font(title_size)

    bbox = draw.textbbox((0, 0), APP_NAME, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = int(h * 0.38) - th // 2
    draw.text((tx, ty), APP_NAME, fill=ACCENT_COLOR, font=title_font)

    # --- Accent line below the title ---
    line_y = ty + th + int(h * 0.04)
    line_half = int(w * 0.18)
    cx = w // 2
    draw.line(
        [(cx - line_half, line_y), (cx + line_half, line_y)],
        fill=ACCENT_COLOR,
        width=3,
    )

    # --- Subtitle ---
    sub_size = max(16, h // 30)
    sub_font = _best_font(sub_size)
    subtitle = "IPTV Streaming"
    bbox_s = draw.textbbox((0, 0), subtitle, font=sub_font)
    sw = bbox_s[2] - bbox_s[0]
    draw.text(
        ((w - sw) // 2, line_y + int(h * 0.04)),
        subtitle,
        fill=ACCENT_COLOR,
        font=sub_font,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for filename, width, height, kind in IMAGES:
        img = Image.new("RGBA", (width, height), BG_COLOR)

        if kind == "icon":
            _draw_icon(img)
        else:
            _draw_splash(img)

        dest = OUTPUT_DIR / filename
        img.save(dest)
        print(f"  Created {dest}  ({width}x{height})")

    print("\nDone. All images saved to", OUTPUT_DIR)


if __name__ == "__main__":
    main()
