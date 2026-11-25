#!/usr/bin/env python3
"""Compose the news-image-20261124 front page.

Reads the four clean scene panels generated in this session (panels/),
lays them out as a 2x2 newspaper front page with a masthead and PIL-drawn
headline bars, and writes entry.png (1024x1024). Deterministic: same input
panels always produce the same bytes. No network.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS_DIR = os.path.join(HERE, "panels")

W, H = 1024, 1024
PAPER = (247, 244, 236)  # off-white newsprint
INK = (12, 12, 12)
BAR = (12, 12, 12)
DECK_GREY = (70, 70, 70)
RULE_GREY = (120, 120, 120)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (panel file, headline, deck) — every fact verified against live
# reporting on 24 Nov 2026 (Reuters, CNN, TechCrunch, Just Security).
# The four real stories, in reading order (top-left first).
STORIES = [
    ("panel-nvidia", "HUANG IS BACK AT NVIDIA",
     "Reinstated as CEO 11 days after resigning; shares jump 27%"),
    ("panel-iran", "IRAN VOWS TO FIGHT US BLOCKADE",
     "Tehran vows \u201call available means\u201d; Qatar PM meets Vance, Rubio"),
    ("panel-gaza", "GAZA STRIKE KILLS HAMAS SECURITY CHIEF",
     "Naeem Abu Nahel among seven killed in Gaza City"),
    ("panel-zaporizhzhia", "ZAPORIZHZHIA HIT OVERNIGHT",
     "Russian strike kills 2, wounds 40, including 4 children"),
]


def find_panel(stem):
    for name in sorted(os.listdir(PANELS_DIR)):
        if stem in name and name.lower().endswith((".webp", ".png", ".jpg", ".jpeg")):
            return os.path.join(PANELS_DIR, name)
    raise FileNotFoundError("no panel file for %s in %s" % (stem, PANELS_DIR))


def cover_crop(img, tw, th):
    """Centre-crop img to the target aspect, then resize (LANCZOS)."""
    sw, sh = img.size
    target = tw / th
    src = sw / sh
    if src > target:  # too wide: trim sides
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, sh))
    else:  # too tall: trim top/bottom
        nh = int(sw / target)
        y0 = (sh - nh) // 2
        img = img.crop((0, y0, sw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def wrap_text(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_headline(draw, text, max_w, max_lines=2, size=30, min_size=22):
    """Largest bold size (down to min_size) whose wrap fits max_lines."""
    while size >= min_size:
        font = ImageFont.truetype(SANS_BOLD, size)
        lines = wrap_text(draw, text, font, max_w)
        if len(lines) <= max_lines:
            return font, lines
        size -= 2
    font = ImageFont.truetype(SANS_BOLD, min_size)
    return font, wrap_text(draw, text, font, max_w)


def build():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)

    # ---- Masthead ----
    masthead = ImageFont.truetype(SERIF_BOLD, 74)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=masthead)
    draw.text(((W - tw) / 2, 18), title, font=masthead, fill=INK)
    draw.line([(28, 104), (W - 28, 104)], fill=INK, width=4)
    draw.line([(28, 110), (W - 28, 110)], fill=INK, width=1)
    dateline_font = ImageFont.truetype(SANS_BOLD, 21)
    dateline = "TUESDAY 24 NOVEMBER 2026  \u2014  WORLD NEWS"
    tw = draw.textlength(dateline, font=dateline_font)
    draw.text(((W - tw) / 2, 120), dateline, font=dateline_font, fill=INK)
    draw.line([(28, 152), (W - 28, 152)], fill=INK, width=2)

    # ---- 2x2 grid ----
    margin, gutter = 28, 18
    cell_w = (W - 2 * margin - gutter) // 2
    cell_h = 388
    img_h = 282
    bar_h = 76
    top0 = 168
    deck_font = ImageFont.truetype(SANS, 15)

    for i, (stem, headline, deck) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = margin + col * (cell_w + gutter)
        y = top0 + row * (cell_h + gutter)

        img = Image.open(find_panel(stem)).convert("RGB")
        page.paste(cover_crop(img, cell_w, img_h), (x, y))

        # Headline bar: black, white bold, wrapped to at most 2 lines.
        bar_y = y + img_h
        draw.rectangle([x, bar_y, x + cell_w, bar_y + bar_h], fill=BAR)
        font, lines = fit_headline(draw, headline, cell_w - 24)
        line_h = font.size + 4
        text_h = line_h * len(lines)
        ty = bar_y + (bar_h - text_h) // 2
        for line in lines:
            draw.text((x + 12, ty), line, font=font, fill=(255, 255, 255))
            ty += line_h

        # Deck: one small grey line under the bar.
        draw.text((x + 2, bar_y + bar_h + 6), deck, font=deck_font, fill=DECK_GREY)

    # ---- Footer ----
    foot_font = ImageFont.truetype(SANS, 13)
    foot = "Sources: Reuters \u2022 CNN \u2022 TechCrunch \u2022 Just Security  \u2014  24 November 2026"
    tw = draw.textlength(foot, font=foot_font)
    draw.text(((W - tw) / 2, 986), foot, font=foot_font, fill=RULE_GREY)
    return page


def main():
    page = build()
    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG", optimize=True)
    print("wrote %s (%dx%d, %d bytes)" % (out, W, H, os.path.getsize(out)))


if __name__ == "__main__":
    main()
