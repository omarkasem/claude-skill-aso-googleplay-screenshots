#!/usr/bin/env python3
"""
Generate Android (Pixel) device frame template PNG.
Output: assets/device_frame.png — standalone device image (not positioned on canvas).
compose.py positions this dynamically based on text height.
"""

from PIL import Image, ImageDraw, ImageChops

# ── Device dimensions ───────────────────────────────────────────────
# Width is ~80% of 1080 canvas, matching reference screenshots
DEVICE_W = 864
DEVICE_H = 1920           # tall enough to bleed off any canvas
DEVICE_CORNER_R = 50
BEZEL = 12
SCREEN_CORNER_R = 38
PUNCH_HOLE_R = 14         # Front camera punch-hole radius
PUNCH_HOLE_TOP = 28       # offset from top of screen

SCREEN_W = DEVICE_W - 2 * BEZEL
SCREEN_H = DEVICE_H - 2 * BEZEL


def generate():
    frame = Image.new("RGBA", (DEVICE_W, DEVICE_H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)

    # ── Device body (dark grey outer, darker inner) ─────────────────
    fd.rounded_rectangle(
        [0, 0, DEVICE_W - 1, DEVICE_H - 1],
        radius=DEVICE_CORNER_R,
        fill=(30, 30, 30, 255),
    )
    fd.rounded_rectangle(
        [1, 1, DEVICE_W - 2, DEVICE_H - 2],
        radius=DEVICE_CORNER_R - 1,
        fill=(20, 20, 20, 255),
    )

    # ── Screen cutout (transparent) ─────────────────────────────────
    screen_x = BEZEL
    screen_y = BEZEL

    cutout = Image.new("L", (DEVICE_W, DEVICE_H), 255)
    ImageDraw.Draw(cutout).rounded_rectangle(
        [screen_x, screen_y, screen_x + SCREEN_W, screen_y + SCREEN_H],
        radius=SCREEN_CORNER_R,
        fill=0,
    )
    frame.putalpha(ImageChops.multiply(frame.getchannel("A"), cutout))

    # ── Punch-hole camera (centered at top of screen) ───────────────
    ph_x = DEVICE_W // 2
    ph_y = screen_y + PUNCH_HOLE_TOP + PUNCH_HOLE_R
    ImageDraw.Draw(frame).ellipse(
        [ph_x - PUNCH_HOLE_R, ph_y - PUNCH_HOLE_R,
         ph_x + PUNCH_HOLE_R, ph_y + PUNCH_HOLE_R],
        fill=(0, 0, 0, 255),
    )

    # ── Side buttons ────────────────────────────────────────────────
    btn_color = (25, 25, 25, 255)
    fd2 = ImageDraw.Draw(frame)

    # Power button (right side)
    fd2.rounded_rectangle(
        [DEVICE_W, 280, DEVICE_W + 4, 380],
        radius=2, fill=btn_color,
    )
    # Volume up (left side)
    fd2.rounded_rectangle(
        [-4, 260, 0, 340],
        radius=2, fill=btn_color,
    )
    # Volume down (left side)
    fd2.rounded_rectangle(
        [-4, 360, 0, 440],
        radius=2, fill=btn_color,
    )

    out = "assets/device_frame.png"
    frame.save(out, "PNG")
    print(f"✓ {out} ({DEVICE_W}×{DEVICE_H})")
    print(f"  BEZEL={BEZEL}, SCREEN_W={SCREEN_W}, SCREEN_H={SCREEN_H}")
    print(f"  SCREEN_CORNER_R={SCREEN_CORNER_R}")


if __name__ == "__main__":
    generate()
