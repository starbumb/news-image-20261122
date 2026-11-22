#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news poster (1024x1024 PNG).

Everything is drawn from scratch with PIL primitives and DejaVu fonts:
no photographs, no downloaded assets.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (22, 22, 28)
RED = (178, 34, 34)
NAVY = (24, 42, 84)
GOLD = (184, 134, 11)
GREY = (92, 92, 100)
CARD = (255, 253, 247)
LINE = (200, 192, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------- little drawn icons ----------

def icon_tanker(d, cx, cy, s):
    # hull
    d.polygon([(cx - s, cy), (cx + s, cy), (cx + s * 0.72, cy + s * 0.42),
               (cx - s * 0.72, cy + s * 0.42)], fill=NAVY)
    d.rectangle([cx - s * 0.55, cy - s * 0.34, cx + s * 0.1, cy], fill=NAVY)
    d.rectangle([cx + s * 0.35, cy - s * 0.5, cx + s * 0.62, cy], fill=NAVY)
    # flame
    fx, fy = cx - s * 0.2, cy - s * 0.75
    d.polygon([(fx, fy - s * 0.55), (fx + s * 0.34, fy + s * 0.1),
               (fx + s * 0.12, fy + s * 0.3), (fx - s * 0.12, fy + s * 0.3),
               (fx - s * 0.34, fy + s * 0.1)], fill=RED)
    d.ellipse([fx - s * 0.1, fy - s * 0.05, fx + s * 0.1, fy + s * 0.25],
              fill=(240, 140, 30))
    # waves
    for i in range(3):
        wy = cy + s * (0.58 + i * 0.16)
        pts = [(cx - s + j * s * 0.25, wy + (s * 0.05 if j % 2 else -s * 0.05))
               for j in range(9)]
        d.line(pts, fill=(70, 110, 160), width=4)


def icon_leaf(d, cx, cy, s):
    d.pieslice([cx - s * 0.7, cy - s * 0.9, cx + s * 0.7, cy + s * 0.5],
               start=270, end=90, fill=(46, 125, 50))
    d.pieslice([cx - s * 0.7, cy - s * 0.9, cx + s * 0.7, cy + s * 0.5],
               start=90, end=270, fill=(76, 160, 80))
    d.line([(cx - s * 0.55, cy + s * 0.55), (cx + s * 0.45, cy - s * 0.65)],
           fill=(27, 80, 32), width=5)
    d.line([(cx - s * 0.55, cy + s * 0.55), (cx - s * 0.75, cy + s * 0.85)],
           fill=(27, 80, 32), width=5)


def icon_badge(d, cx, cy, s):
    d.polygon([(cx, cy - s * 0.85), (cx + s * 0.7, cy - s * 0.55),
               (cx + s * 0.7, cy + s * 0.15), (cx, cy + s * 0.85),
               (cx - s * 0.7, cy + s * 0.15), (cx - s * 0.7, cy - s * 0.55)],
              fill=GOLD, outline=INK, width=4)
    # star
    import math
    pts = []
    for i in range(10):
        r = s * 0.42 if i % 2 == 0 else s * 0.18
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a) - s * 0.05))
    d.polygon(pts, fill=PAPER)


def icon_chart_down(d, cx, cy, s):
    d.line([(cx - s * 0.8, cy + s * 0.7), (cx + s * 0.85, cy + s * 0.7)],
           fill=INK, width=4)
    d.line([(cx - s * 0.8, cy + s * 0.7), (cx - s * 0.8, cy - s * 0.8)],
           fill=INK, width=4)
    pts = [(cx - s * 0.6, cy - s * 0.5), (cx - s * 0.15, cy - s * 0.15),
           (cx + s * 0.2, cy - s * 0.35), (cx + s * 0.65, cy + s * 0.45)]
    d.line(pts, fill=RED, width=7)
    d.polygon([(cx + s * 0.65, cy + s * 0.62), (cx + s * 0.42, cy + s * 0.3),
               (cx + s * 0.78, cy + s * 0.22)], fill=RED)


def icon_summit(d, cx, cy, s):
    # table
    d.rounded_rectangle([cx - s * 0.85, cy + s * 0.1, cx + s * 0.85, cy + s * 0.55],
                        radius=10, fill=(110, 74, 40))
    # three leaders: heads + shoulders
    for dx, col in [(-0.55, NAVY), (0.0, RED), (0.55, (46, 125, 50))]:
        hx = cx + dx * s
        d.ellipse([hx - s * 0.16, cy - s * 0.55, hx + s * 0.16, cy - s * 0.23],
                  fill=(232, 190, 150), outline=INK, width=3)
        d.pieslice([hx - s * 0.28, cy - s * 0.28, hx + s * 0.28, cy + s * 0.22],
                   start=180, end=360, fill=col)


# ---------- poster ----------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 148], fill=INK)
    title_f = font(SERIF_B, 62)
    tw = d.textlength("THE WORLD TODAY", font=title_f)
    d.text(((W - tw) / 2, 18), "THE WORLD TODAY", font=title_f, fill=PAPER)
    date_f = font(SANS_B, 27)
    date_txt = "SUNDAY, 22 NOVEMBER 2026"
    dw = d.textlength(date_txt, font=date_f)
    d.text(((W - dw) / 2, 98), date_txt, font=date_f, fill=(240, 200, 90))
    d.rectangle([0, 148, W, 156], fill=RED)

    # lead story panel
    y = 172
    d.rounded_rectangle([36, y, W - 36, y + 262], radius=14, fill=CARD,
                        outline=LINE, width=2)
    d.rectangle([36, y, 48, y + 262], fill=RED)
    kick_f = font(SANS_B, 21)
    d.text((68, y + 20), "LEAD STORY  ·  GULF / MIDDLE EAST", font=kick_f, fill=RED)
    head_f = font(SERIF_B, 40)
    yy = draw_wrapped(d, "Iran strikes Bahrain; tankers hit near Hormuz",
                      head_f, 68, y + 52, 620, INK, 48)
    body_f = font(SANS, 22)
    yy = draw_wrapped(
        d,
        "Iran hit a civilian industrial site in Bahrain and two oil tankers "
        "were struck near the Strait of Hormuz. Bahrain warned residents to "
        "shelter; Gulf markets fell, oil near $90.",
        body_f, 68, yy + 6, 655, (50, 50, 58), 30)
    icon_tanker(d, 840, y + 150, 92)

    # 2x2 story cards
    cards = [
        ("CLIMATE  ·  ANTALYA, TURKEY", "COP31 talks run into overtime",
         "Nearly 200 nations haggle past the deadline over fossil fuels "
         "and climate funding.", icon_leaf),
        ("DIPLOMACY  ·  SHENZHEN, CHINA", "Trump, Xi and Putin meet",
         "The three leaders met in Shenzhen and agreed to open talks on "
         "reducing nuclear risks.", icon_summit),
        ("CRIME  ·  SINALOA, MEXICO", "Cartel boss 'El Chapo Isidro' captured",
         "Mexican forces seized one of the FBI's 10 most wanted; 11 died "
         "in the violence that followed.", icon_badge),
        ("MARKETS  ·  NEW YORK, USA", "AI sell-off drags US stocks down",
         "The Dow and S&P 500 slid into correction as chip shares fell; "
         "the SEC probes Nvidia.", icon_chart_down),
    ]
    top = y + 284
    cw, ch, gap = (W - 72 - 24) // 2, 188, 24
    for i, (kick, head, body, icon) in enumerate(cards):
        cx = 36 + (i % 2) * (cw + gap)
        cy = top + (i // 2) * (ch + gap)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=12, fill=CARD,
                            outline=LINE, width=2)
        icon(d, cx + 62, cy + 92, 46)
        d.text((cx + 118, cy + 16), kick, font=font(SANS_B, 16), fill=RED)
        yy = draw_wrapped(d, head, font(SERIF_B, 25), cx + 118, cy + 40,
                          cw - 134, INK, 31)
        draw_wrapped(d, body, font(SANS, 18), cx + 118, yy + 2,
                     cw - 134, (50, 50, 58), 24)

    # footer strip: also today
    fy = top + 2 * ch + gap + 20
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.text((36, fy + 12), "ALSO TODAY", font=font(SANS_B, 22), fill=(240, 200, 90))
    briefs = [
        "Nigeria: boat carrying mourners capsizes — at least 24 dead",
        "Indonesia: factory fire near Jakarta — 3 dead, 36 missing",
        "Brazil: ex-president Bolsonaro in intensive care",
    ]
    bf = font(SANS, 19)
    by = fy + 46
    for b in briefs:
        d.ellipse([40, by + 7, 50, by + 17], fill=(240, 200, 90))
        d.text((62, by), b, font=bf, fill=PAPER)
        by += 30

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
