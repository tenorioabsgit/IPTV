"""Generate Roku channel images: posters, splash screens, and UI assets."""
from PIL import Image, ImageDraw, ImageFont
import os

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")

# New premium dark color scheme
BG_COLOR = (13, 13, 13)         # #0D0D0D - near black
SURFACE_COLOR = (22, 22, 22)    # #161616 - elevated surface
ACCENT_COLOR = (0, 212, 255)    # #00D4FF - cyan accent
TEXT_COLOR = (229, 229, 229)    # #E5E5E5 - off-white
TEXT_DIM = (85, 85, 85)         # #555555 - muted text


def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.pieslice([x0, y0, x0 + 2 * radius, y0 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x1 - 2 * radius, y0, x1, y0 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2 * radius, x0 + 2 * radius, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2 * radius, y1 - 2 * radius, x1, y1], 0, 90, fill=fill)


def draw_play_icon(draw, cx, cy, size, color):
    """Draw a modern play triangle."""
    half = size // 2
    pts = [
        (cx - half // 2, cy - half),
        (cx - half // 2, cy + half),
        (cx + half, cy),
    ]
    draw.polygon(pts, fill=color)


def create_poster(width, height, filename):
    """Create channel poster icon with premium dark design."""
    img = Image.new("RGBA", (width, height), BG_COLOR + (255,))
    draw = ImageDraw.Draw(img)

    # Subtle border
    draw.rectangle([0, 0, width - 1, height - 1], outline=ACCENT_COLOR + (100,), width=2)

    # Play icon centered
    icon_size = min(width, height) // 3
    draw_play_icon(draw, width // 2, height // 2 - 12, icon_size, ACCENT_COLOR)

    # Accent line below icon
    line_w = width // 3
    draw.rectangle(
        [width // 2 - line_w // 2, height // 2 + icon_size // 2 + 5,
         width // 2 + line_w // 2, height // 2 + icon_size // 2 + 8],
        fill=ACCENT_COLOR
    )

    try:
        font_big = ImageFont.truetype("arial.ttf", max(16, height // 7))
        font_small = ImageFont.truetype("arial.ttf", max(12, height // 10))
    except OSError:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # "Pira" text
    text = "Pira"
    bbox = draw.textbbox((0, 0), text, font=font_big)
    tw = bbox[2] - bbox[0]
    draw.text((width // 2 - tw // 2, height - 52), text, fill=ACCENT_COLOR, font=font_big)

    # "IPTV" text
    text2 = "IPTV"
    bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((width // 2 - tw2 // 2, height - 28), text2, fill=TEXT_DIM, font=font_small)

    img.save(os.path.join(IMAGES_DIR, filename))
    print(f"Created {filename} ({width}x{height})")


def create_splash(width, height, filename):
    """Create splash screen with cinematic dark design."""
    img = Image.new("RGBA", (width, height), BG_COLOR + (255,))
    draw = ImageDraw.Draw(img)

    # Central panel - subtle elevated surface
    pw, ph = width // 3, height // 4
    px = width // 2 - pw // 2
    py = height // 2 - ph // 2
    draw_rounded_rect(draw, (px, py, px + pw, py + ph), 16, SURFACE_COLOR + (220,))

    # Accent line at top of panel
    draw.rectangle([px, py, px + pw, py + 3], fill=ACCENT_COLOR)

    # Play icon
    icon_size = min(pw, ph) // 3
    draw_play_icon(draw, width // 2, height // 2 - 25, icon_size, ACCENT_COLOR)

    try:
        font_title = ImageFont.truetype("arial.ttf", max(24, height // 15))
        font_sub = ImageFont.truetype("arial.ttf", max(16, height // 25))
    except OSError:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # "Pira IPTV"
    title = "Pira IPTV"
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text((width // 2 - tw // 2, height // 2 + 30), title, fill=ACCENT_COLOR, font=font_title)

    # "Canais ao vivo"
    sub = "Canais ao vivo"
    bbox2 = draw.textbbox((0, 0), sub, font=font_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((width // 2 - tw2 // 2, height // 2 + 75), sub, fill=TEXT_DIM, font=font_sub)

    img.save(os.path.join(IMAGES_DIR, filename))
    print(f"Created {filename} ({width}x{height})")


def create_card_overlay(width, height, filename):
    """Create a vertical gradient from transparent to dark for channel card overlays."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        progress = y / max(height - 1, 1)
        # Exponential curve for smoother gradient
        alpha = int(210 * (progress ** 1.4))
        draw.line([(0, y), (width - 1, y)], fill=(0, 0, 0, alpha))
    img.save(os.path.join(IMAGES_DIR, filename))
    print(f"Created {filename} ({width}x{height})")


if __name__ == "__main__":
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Channel posters (Roku requirements)
    create_poster(336, 210, "channel-poster_hd.png")   # HD poster: 336x210
    create_poster(246, 140, "channel-poster_sd.png")   # SD poster: 246x140

    # Splash screens
    create_splash(1280, 720, "splash-screen_hd.png")    # HD: 1280x720
    create_splash(1920, 1080, "splash-screen_fhd.png")  # FHD: 1920x1080

    # UI assets
    create_card_overlay(260, 85, "card-overlay.png")    # Channel card gradient overlay

    print("All images created successfully!")
