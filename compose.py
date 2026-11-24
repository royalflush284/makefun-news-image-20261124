#!/usr/bin/env python3
"""THE TELEGRAPH ROOM — NI24 entry composer (Final 1, build v2, written fresh).

Renders the Tuesday 24 November 2026 front page at 3900x4400 with PIL, then
fits it (aspect preserved) onto a 1024x1024 paper-coloured canvas and
quantizes to a 256-colour palette. Run: python3 compose.py A|B
Writes variant_<X>.png (1024x1024) next to this file.
Only used inside the build session; the graded entrypoint (main.py) merely
copies the finished entry.png. PIL is a build-time tool only.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 3900, 4600
M = 80                      # margin
CW = W - 2 * M              # content width 3740
FONTS = "/home/hatch/workspace/makefun/ni22-stage/fonts/"
DEJAVU = "/usr/share/fonts/truetype/dejavu/"

PAPER = (246, 240, 225)
PAPER2 = (238, 229, 206)
INK = (22, 19, 15)
RED = (163, 22, 33)
RED_D = (110, 15, 22)
NAVY = (28, 43, 69)
GREY = (90, 84, 72)
CREAM = (246, 240, 225)
GOLD = (176, 138, 31)


def F(path, size):
    return ImageFont.truetype(path, size)


def pf(size):
    return F(FONTS + "PlayfairDisplay-Black.ttf", size)


def ab(size):
    return F(FONTS + "Archivo-Bold.ttf", size)


def ar(size):
    return F(FONTS + "Archivo.ttf", size)


def mb(size):
    return F(FONTS + "IBMPlexMono-Bold.ttf", size)


def mr(size):
    return F(FONTS + "IBMPlexMono-Regular.ttf", size)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, maxw, lh, fill=INK, align="left"):
    lines = wrap(d, text, font, maxw)
    for ln in lines:
        if align == "center":
            d.text((x + maxw / 2, y), ln, font=font, fill=fill, anchor="la")
            # centre manually: anchor la with x offset computed below
            pass
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def para_c(d, cx, y, text, font, maxw, lh, fill=INK):
    lines = wrap(d, text, font, maxw)
    for ln in lines:
        w = d.textlength(ln, font=font)
        d.text((cx - w / 2, y), ln, font=font, fill=fill)
        y += lh
    return y


def rule(d, x, y, w, h=6, fill=INK):
    d.rectangle([x, y, x + w, y + h], fill=fill)


# ---------------------------------------------------------------- cards
# num, region, place, headline, deck, chip, source, scene kind
CARDS = [
    (1, "MIDDLE EAST · CONFLICT", "GAZA CITY",
     "Israeli strikes kill 3 in Gaza",
     "Three killed Monday in separate strikes, including a UNRWA employee, Shifa Hospital and the agency confirm.",
     "3 KILLED", "AP", "city"),
    (2, "MIDDLE EAST · IRAN SANCTIONS", "WASHINGTON",
     "US sanctions ~30 Iran-linked exchange houses",
     "Treasury names ~30 houses and executives at the core of shadow banking evading sanctions on Iranian banks.",
     "~30 SANCTIONED", "AP / TREASURY", "bank"),
    (3, "MIDDLE EAST · WAR", "WESTERN YEMEN",
     "Strike kills 11 in western Yemen",
     "Houthis say a Saudi-backed forces' strike on Monday killed 11 and wounded 19.",
     "11 KILLED · 19 WOUNDED", "AP", "mountain"),
    (4, "EUROPE · WAR", "BENGHAZI, LIBYA",
     "Ukraine sinks warship Merkury off Libya",
     "Seven sea drones launched; Ka-27 destroyed aboard; MV Angara hit. Zelenskyy: \u201cexemplary\u201d.",
     "7 SEA DRONES · MERKURY SUNK", "CNN / TIMES / AP", "sea"),
    (5, "EUROPE · SEA", "GULF OF FINLAND",
     "Russian cargo ship Sparta II hit, towed clear",
     "Hit by 2 drones; Finland led the rescue, all 16 crew off; towed out Sunday night.",
     "121 M · 16 CREW SAFE", "REUTERS", "tug"),
    (6, "EUROPE · WAR", "KYIV REGION, UKRAINE",
     "Russian strikes kill at least 15 near Kyiv",
     "Kyiv strikes: 11 killed in a block of flats in Dymer; a drone hit a Kyiv block, five injured.",
     "15 KILLED · 11 IN DYMER", "TIMES / AP", "city"),
    (7, "WORLD · CLIMATE", "ANTALYA, T\u00dcRKIYE",
     "COP31 ends with no deal \u2014 first since 2000",
     "44 hours overtime, longest COP ever; fossil fuels dropped; Antalya Pact not adopted.",
     "NO DEAL · FIRST SINCE 2000", "TIMES / GUARDIAN", "summit"),
    (8, "AMERICAS · MARKETS", "NEW YORK",
     "Gold $3,588, up 1.5% on Monday",
     "Bullion +1.5% Monday after worst week in 8 months; PCE inflation report due 25 Nov.",
     "$3,588/OZ · +1.5%", "REUTERS", "chart"),
    (9, "GLOBAL · CRYPTO", "WORLDWIDE",
     "Bitcoin $61,284, steady on Monday",
     "$61,284 at 12:52 UTC Mon, +1.1% in 24 h; Kraken CAD flash crash to ~$17,000 stands.",
     "$61,284 · +1.1%", "COINPAPRIKA", "coins"),
    (10, "AMERICAS · BUSINESS", "LOS ANGELES",
     "GTA VI takes $3.8bn on day one",
     "Biggest entertainment launch on record \u2014 past every game and single-day film box office.",
     "$3.8BN DAY ONE", "ACTIVEINVESTORMAG", "game"),
    (11, "OCEANIA · CRICKET", "WELLINGTON",
     "New Zealand bat out draw with India",
     "NZ 239/5 \u2014 Mitchell 49* off 186, Phillips 26* off 126; India 720/9 declared.",
     "DRAW · 239/5", "HS / WICKETPULSE", "cricket"),
    (12, "EUROPE · FOOTBALL", "LIVERPOOL",
     "Liverpool 4\u20130 Man Utd",
     "Pochettino's debut ends in disaster; Yoro off in the 8th minute; United 19th on 8 points.",
     "4\u20130 · YORO OFF 8'", "MINT", "football"),
    (13, "AMERICAS · POLITICS", "WASHINGTON",
     "Democrats take both chambers",
     "Democrats 258\u2013173, largest House majority since 1992, after a North Carolina pickup.",
     "258\u2013173", "BBC", "capitol"),
    (14, "AMERICAS · POLITICS", "WASHINGTON",
     "Trump: work with Democrats to cap card rates",
     "Rate cap + scrap the debt ceiling; Van Hollen challenges Schumer, ballot 1 Dec.",
     "RATE CAP", "ACTIVEINVESTORMAG", "capitol"),
    (15, "AMERICAS · CYBER", "WASHINGTON",
     "FBI probes hack of its crime database",
     "Washington State pauses van-dealer checks while the breach is assessed.",
     "FBI PROBE", "AP", "shield"),
]

BRIEFS = [
    (16, "Nvidia brings back Huang as CEO; shares +31%. Reuters, 23 Nov"),
    (17, "North Korea weighs shutting its Swiss office. KCNA, 24 Nov"),
    (18, "US weighs training Syrian forces, first since 2024. Reuters"),
    (19, "Congo halts cobalt exports from 30 Nov. Reuters, 23 Nov"),
    (20, "Indonesia factory blaze kills 24, dozens missing. Reuters"),
    (21, "CrowdStrike buys Zscaler in $44bn deal. Reuters, 23 Nov"),
    (22, "Trump hosts gala for meme-coin investors. Reuters, 23 Nov"),
    (23, "US Army to detonate Iowa lead stockpile: 68 barrels. Reuters"),
    (24, "India considers rice export duties. Reuters, 23 Nov"),
    (25, "Euro zone PMI 51.7 in Nov, fifth month of growth. Reuters"),
    (26, "Nepal PM Shah ends Delhi visit; met Modi. IANS, 23 Nov"),
    (27, "Thousands march in Lisbon over living costs. JagranJosh"),
    (28, "UK\u2013EU Brexit reset deal called \u201clandmark\u201d. BBC, 23 Nov"),
    (29, "India\u2013EU trade pact likely signed 16 Dec. JagranJosh, 23 Nov"),
    (30, "Tata Steel sells pipe arm for \u20b928,000 crore. ObserverVoice"),
    (31, "SpiceJet pilot seeks safety audit; IndiGo 65.9%. ObserverVoice"),
    (32, "Solana launches solana.ai for AI agents. Gadgets360, 23 Nov"),
    (33, "Modi opens AI Centre at IIT Patna. ObserverVoice, 23 Nov"),
    (34, "Amit Shah launches \u20b94,000 crore Arunachal push. ObserverVoice"),
    (35, "UN AI weapons talks to continue. salonvision, 23 Nov"),
    (36, "Miley Cyrus weds Maxx Morando in California. BBC, 23 Nov"),
]

NUMSTRIP = [
    ("7", "SEA DRONES"),
    ("15", "KILLED NEAR KYIV"),
    ("NO DEAL", "COP31 · FIRST SINCE 2000"),
    ("~30", "IRAN HOUSES SANCTIONED"),
    ("$3,588", "GOLD · +1.5%"),
    ("$61,284", "BITCOIN"),
    ("$3.8BN", "GTA VI · DAY ONE"),
    ("+31%", "NVIDIA · HUANG BACK"),
]

TIMELINE = [
    ("04:24 WIB \u00b7 TUE 24 NOV", "KCNA: North Korea weighs shutting its Swiss office in Pyongyang.", "REUTERS"),
    ("MON EVENING \u00b7 23 NOV", "Zelenskyy announces the Merkury sinking; Treasury sanctions ~30 Iran exchange houses.", "CNN / AP"),
    ("MON EVENING \u00b7 23 NOV", "COP31 collapses in Antalya: no deal, the first since 2000.", "REUTERS"),
    ("12:52 UTC \u00b7 MON 23 NOV", "Bitcoin trades at $61,284 as markets steady.", "COINPAPRIKA"),
    ("MON EVENING \u00b7 23 NOV", "Liverpool beat Man Utd 4\u20130; Yoro sent off in the 8th minute.", "MINT"),
    ("SUN NIGHT \u00b7 22 NOV", "Sparta II is towed out of Finnish waters; all 16 crew safe.", "REUTERS"),
]

DATECHECK = [
    ("186-drone night over Ukraine, 161 downed", "Fri 21\u2013Sun 22 Nov"),
    ("Hong Kong Election Committee: 856 candidates, 723 seats", "Sun 22 Nov"),
    ("Alcaraz beats Zverev 6\u20132, 7\u20136(9\u20137), first ATP Finals title", "Sun 22 Nov"),
    ("Verstappen wins the Las Vegas Grand Prix", "Sun 22 Nov"),
    ("Wembanyama scores 50, Spurs 114\u201391 Pelicans", "Sun 22 Nov"),
    ("Nvidia CEO Jensen Huang resigns after affair admission", "Thu 12 Nov"),
    ("Myanmar ICJ genocide ruling", "Thu 19 Nov"),
    ("\u2018El Chapo Isidro\u2019 captured", "Fri 20 Nov"),
]

# ---------------------------------------------------------------- scenes
def scene(d, box, kind, bg, fg, acc):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=bg)
    w, h = x1 - x0, y1 - y0
    if kind == "city":
        for i, bh in enumerate([0.55, 0.8, 0.45, 0.95, 0.6, 0.75]):
            bx = x0 + 20 + i * (w - 40) / 6
            bw = (w - 40) / 6 - 12
            d.rectangle([bx, y1 - bh * h, bx + bw, y1], fill=fg)
            for wy in range(3):
                for wx in range(2):
                    d.rectangle([bx + 8 + wx * (bw / 2), y1 - bh * h + 14 + wy * 26,
                                 bx + 8 + wx * (bw / 2) + 12, y1 - bh * h + 26 + wy * 26], fill=acc)
        d.ellipse([x0 + w * 0.62, y0 + 12, x0 + w * 0.62 + 90, y0 + 102], fill=acc)
        d.ellipse([x0 + w * 0.68, y0 + 40, x0 + w * 0.68 + 130, y0 + 170], fill=bg)
    elif kind == "bank":
        d.rectangle([x0 + 20, y0 + 30, x1 - 20, y0 + 70], fill=fg)
        d.polygon([(x0 + 20, y0 + 30), (x0 + w / 2, y0 - 6), (x1 - 20, y0 + 30)], fill=acc)
        for i in range(5):
            cx = x0 + 50 + i * (w - 100) / 4
            d.rectangle([cx - 16, y0 + 80, cx + 16, y1 - 30], fill=fg)
        d.rectangle([x0 + 20, y1 - 30, x1 - 20, y1 - 12], fill=fg)
    elif kind == "mountain":
        d.polygon([(x0, y1), (x0 + w * 0.3, y0 + 30), (x0 + w * 0.55, y1)], fill=fg)
        d.polygon([(x0 + w * 0.35, y1), (x0 + w * 0.65, y0 + 60), (x0 + w * 0.95, y1)], fill=acc)
        d.ellipse([x0 + w * 0.7, y0 + 16, x0 + w * 0.7 + 80, y0 + 96], fill=CREAM)
        d.rectangle([x0, y1 - 26, x1, y1], fill=fg)
    elif kind == "sea":
        for i in range(4):
            yy = y0 + 30 + i * ((h - 40) / 4)
            d.arc([x0 - 40, yy - 26, x0 + w * 0.4, yy + 26], 0, 180, fill=fg, width=10)
            d.arc([x0 + w * 0.45, yy - 26, x0 + w * 0.95, yy + 26], 0, 180, fill=fg, width=10)
        d.polygon([(x0 + w * 0.3, y0 + h * 0.42), (x0 + w * 0.72, y0 + h * 0.42),
                   (x0 + w * 0.66, y0 + h * 0.62), (x0 + w * 0.36, y0 + h * 0.62)], fill=acc)
        d.rectangle([x0 + w * 0.48, y0 + 12, x0 + w * 0.48 + 10, y0 + h * 0.42], fill=CREAM)
        d.polygon([(x0 + w * 0.48 + 10, y0 + 12), (x0 + w * 0.62, y0 + 30),
                   (x0 + w * 0.48 + 10, y0 + 48)], fill=RED)
    elif kind == "tug":
        for i in range(3):
            yy = y0 + 60 + i * 40
            d.arc([x0 - 30, yy - 22, x0 + w * 0.5, yy + 22], 0, 180, fill=fg, width=9)
        d.polygon([(x0 + w * 0.15, y0 + h * 0.35), (x0 + w * 0.85, y0 + h * 0.35),
                   (x0 + w * 0.78, y0 + h * 0.6), (x0 + w * 0.22, y0 + h * 0.6)], fill=acc)
        d.rectangle([x0 + w * 0.55, y0 + 14, x0 + w * 0.55 + 12, y0 + h * 0.35], fill=CREAM)
        d.ellipse([x0 + w * 0.08, y0 + h * 0.55, x0 + w * 0.08 + 46, y0 + h * 0.55 + 46], fill=RED)
    elif kind == "summit":
        d.ellipse([x0 + w * 0.32, y0 + 10, x0 + w * 0.68, y0 + h * 0.62], outline=fg, width=12)
        d.arc([x0 + w * 0.32, y0 + h * 0.2, x0 + w * 0.68, y0 + h * 0.85], 0, 180, fill=fg, width=8)
        d.line([x0 + w * 0.32, y0 + h * 0.36, x0 + w * 0.68, y0 + h * 0.36], fill=fg, width=8)
        for i in range(5):
            fx = x0 + 30 + i * (w - 60) / 4
            d.rectangle([fx, y1 - 90, fx + 10, y1 - 30], fill=fg)
            d.rectangle([fx, y1 - 90, fx + 44, y1 - 66], fill=acc)
        d.rectangle([x0, y1 - 30, x1, y1 - 12], fill=fg)
    elif kind == "chart":
        vals = [0.3, 0.45, 0.4, 0.65, 0.6, 0.9, 0.85, 1.0]
        bw = (w - 60) / len(vals)
        for i, v in enumerate(vals):
            bx = x0 + 30 + i * bw
            col = acc if i in (5, 7) else fg
            d.rectangle([bx + 6, y1 - 20 - v * (h - 60), bx + bw - 6, y1 - 20], fill=col)
        d.line([x0 + 20, y1 - 20, x1 - 20, y1 - 20], fill=CREAM, width=6)
    elif kind == "coins":
        for i, (cx, cy, r, ch) in enumerate([(0.28, 0.5, 0.20, "$"), (0.55, 0.38, 0.26, "$"),
                                            (0.78, 0.55, 0.17, "$")]):
            d.ellipse([x0 + w * cx - r * w / 2, y0 + h * cy - r * w / 2,
                       x0 + w * cx + r * w / 2, y0 + h * cy + r * w / 2],
                      fill=acc if i == 1 else fg, outline=CREAM, width=6)
            d.text((x0 + w * cx, y0 + h * cy), ch, font=pf(int(r * w * 0.9)),
                   fill=CREAM, anchor="mm")
    elif kind == "game":
        for i, bh in enumerate([0.5, 0.75, 0.4, 0.9, 0.55]):
            bx = x0 + 20 + i * (w - 40) / 5
            bw = (w - 40) / 5 - 14
            d.rectangle([bx, y1 - bh * h, bx + bw, y1], fill=fg)
        cx, cy, r = x0 + w * 0.72, y0 + h * 0.30, 70
        d.polygon([(cx, cy - r), (cx + r * 0.3, cy - r * 0.3), (cx + r, cy),
                   (cx + r * 0.3, cy + r * 0.3), (cx, cy + r), (cx - r * 0.3, cy + r * 0.3),
                   (cx - r, cy), (cx - r * 0.3, cy - r * 0.3)], fill=acc)
    elif kind == "cricket":
        d.rectangle([x0 + w * 0.2, y0 + h * 0.25, x0 + w * 0.2 + 34, y0 + h * 0.75], fill=fg)
        d.polygon([(x0 + w * 0.2, y0 + h * 0.25), (x0 + w * 0.42, y0 + h * 0.12),
                   (x0 + w * 0.46, y0 + h * 0.22), (x0 + w * 0.24, y0 + h * 0.35)], fill=fg)
        d.ellipse([x0 + w * 0.68, y0 + h * 0.2, x0 + w * 0.68 + 84, y0 + h * 0.2 + 84], fill=acc)
        for i in range(3):
            sx = x0 + w * 0.82 + i * 22
            d.rectangle([sx, y1 - 110, sx + 10, y1 - 20], fill=fg)
        d.rectangle([x0 + w * 0.8, y1 - 118, x0 + w * 0.8 + 70, y1 - 108], fill=acc)
    elif kind == "football":
        d.ellipse([x0 + w * 0.32, y0 + h * 0.18, x0 + w * 0.68, y0 + h * 0.82], fill=CREAM)
        d.polygon([(x0 + w * 0.5, y0 + h * 0.38), (x0 + w * 0.58, y0 + h * 0.46),
                   (x0 + w * 0.55, y0 + h * 0.56), (x0 + w * 0.45, y0 + h * 0.56),
                   (x0 + w * 0.42, y0 + h * 0.46)], fill=INK)
        d.rectangle([x0 + w * 0.78, y0 + h * 0.3, x0 + w * 0.78 + 12, y1 - 20], fill=fg)
        d.rectangle([x0 + w * 0.78, y0 + h * 0.3, x1 - 16, y0 + h * 0.3 + 12], fill=fg)
        d.line([x0 + 20, y1 - 20, x1 - 20, y1 - 20], fill=fg, width=8)
    elif kind == "capitol":
        d.pieslice([x0 + w * 0.32, y0 + 6, x0 + w * 0.68, y0 + h * 0.6], 180, 360, fill=fg)
        d.rectangle([x0 + w * 0.47, y0, x0 + w * 0.53, y0 + 26], fill=acc)
        for i in range(5):
            cx = x0 + 40 + i * (w - 80) / 4
            d.rectangle([cx - 14, y0 + h * 0.55, cx + 14, y1 - 24], fill=fg)
        d.rectangle([x0 + 20, y1 - 24, x1 - 20, y1 - 10], fill=fg)
    elif kind == "shield":
        d.polygon([(x0 + w * 0.5, y0 + 12), (x0 + w * 0.82, y0 + 40), (x0 + w * 0.82, y0 + h * 0.55),
                   (x0 + w * 0.5, y1 - 16), (x0 + w * 0.18, y0 + h * 0.55), (x0 + w * 0.18, y0 + 40)],
                  fill=acc)
        d.line([x0 + w * 0.36, y0 + h * 0.52, x0 + w * 0.48, y0 + h * 0.64,
                x0 + w * 0.68, y0 + h * 0.34], fill=CREAM, width=14)


# ---------------------------------------------------------------- map
LAND = [
    [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-135, 57), (-130, 54), (-125, 49),
     (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
     (-90, 14), (-86, 12), (-83, 9), (-80, 8), (-77, 7), (-79, 9), (-82, 10), (-84, 13),
     (-87, 15), (-90, 14), (-92, 15), (-95, 16), (-97, 16), (-100, 18), (-105, 20),
     (-110, 23), (-114, 28), (-117, 33), (-122, 37), (-124, 40), (-124, 48), (-125, 49),
     (-130, 55), (-135, 58), (-145, 60), (-155, 58), (-162, 55), (-168, 66)],
    [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74),
     (-30, 76), (-45, 76), (-58, 74), (-62, 70), (-58, 64)],
    [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23),
     (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54), (-66, -55), (-62, -49),
     (-58, -38), (-52, -32), (-48, -27), (-41, -23), (-38, -15), (-35, -9), (-40, -3),
     (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-77, 8)],
    [(-17, 15), (-17, 21), (-15, 27), (-10, 29), (-5, 35), (0, 36), (10, 37), (11, 34),
     (20, 32), (25, 32), (30, 31), (32, 31), (34, 28), (37, 22), (39, 18), (40, 15),
     (43, 12), (46, 11), (51, 12), (51, 10), (46, 5), (42, 0), (40, -5), (40, -10),
     (39, -15), (36, -20), (33, -26), (28, -33), (20, -35), (17, -32), (15, -27),
     (13, -20), (12, -15), (13, -10), (12, -5), (9, 0), (9, 4), (4, 6), (-8, 5),
     (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49), (0, 51),
     (3, 53), (8, 54), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64), (13, 66),
     (18, 69), (25, 71), (30, 70), (35, 68), (40, 68), (45, 68), (50, 69), (55, 69),
     (60, 69), (65, 70), (70, 72), (75, 73), (80, 73), (85, 74), (90, 75), (95, 76),
     (100, 77), (105, 77), (110, 74), (115, 73), (120, 73), (125, 72), (130, 72),
     (135, 71), (140, 72), (145, 72), (150, 70), (155, 69), (160, 69), (162, 66),
     (162, 62), (158, 59), (156, 52), (150, 60), (142, 59), (140, 55), (135, 50),
     (130, 45), (127, 40), (122, 38), (120, 35), (118, 30), (115, 25), (110, 20),
     (108, 15), (105, 10), (103, 7), (100, 8), (98, 10), (95, 15), (92, 20),
     (90, 22), (88, 22), (85, 20), (82, 17), (80, 13), (77, 8), (75, 12), (72, 20),
     (68, 23), (66, 25), (62, 25), (58, 25), (56, 27), (54, 26), (52, 25), (50, 29),
     (48, 30), (50, 26), (52, 24), (54, 24), (56, 24), (58, 22), (60, 22), (58, 20),
     (55, 17), (52, 16), (50, 16), (48, 14), (45, 13), (43, 12), (42, 15), (40, 15),
     (39, 20), (38, 22), (36, 25), (35, 28), (34, 29), (33, 31), (32, 31), (30, 31),
     (28, 31), (26, 31), (24, 33), (22, 33), (20, 32), (18, 33), (16, 34), (14, 35),
     (12, 37), (10, 37), (8, 39), (6, 38), (3, 38), (0, 36), (-2, 37), (-5, 36),
     (-8, 37), (-10, 36)],
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32), (132, -32),
     (135, -35), (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -23), (146, -19), (142, -15), (142, -11), (140, -17), (136, -15), (135, -12),
     (132, -11), (130, -13), (126, -14), (122, -17), (118, -20), (114, -21)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 35), (140, 37), (141, 39),
     (141, 41), (142, 42), (143, 44), (145, 44), (142, 42), (140, 39), (138, 36),
     (135, 34), (132, 33), (130, 31)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9), (143, -8),
     (138, -8), (134, -4), (131, -1)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25), (44, -20), (43, -17)],
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (178, -37), (175, -40),
     (173, -42), (170, -44), (167, -45)],
]
SEAS = [  # cut-outs: Mediterranean, Black Sea, Caspian, Red Sea, Persian Gulf
    [(-6, 36), (0, 36), (3, 38), (8, 39), (10, 37), (12, 37), (15, 38), (16, 39),
     (19, 40), (20, 39), (23, 36), (26, 36), (28, 37), (30, 36), (33, 36), (36, 36),
     (36, 33), (34, 31), (32, 31), (30, 31), (28, 31), (25, 32), (22, 33), (20, 32),
     (18, 33), (15, 34), (12, 34), (10, 34), (8, 35), (5, 36), (0, 35), (-3, 35), (-6, 36)],
    [(28, 41), (30, 41), (33, 42), (36, 42), (39, 41), (41, 41), (41, 43), (38, 44),
     (34, 44), (31, 44), (29, 44), (28, 43)],
    [(47, 37), (49, 38), (51, 39), (53, 38), (54, 37), (53, 36), (51, 36), (49, 37)],
    [(35, 28), (37, 25), (39, 22), (41, 18), (43, 15), (43, 12), (40, 15), (38, 20),
     (36, 24), (34, 28)],
    [(48, 30), (50, 29), (52, 27), (55, 26), (57, 25), (56, 24), (53, 24), (50, 26)],
]


def inside_poly(lon, lat, poly):
    ins = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            x = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < x:
                ins = not ins
        j = i
    return ins


def is_land(lon, lat):
    for p in SEAS:
        if inside_poly(lon, lat, p):
            return False
    for p in LAND:
        if inside_poly(lon, lat, p):
            return True
    return False


PINS = [  # (story number, lon, lat)
    (1, 34.5, 31.5), (2, -77.0, 38.9), (3, 44.2, 15.4), (4, 20.1, 32.1),
    (5, 25.0, 59.9), (6, 30.5, 50.4), (7, 30.7, 36.9), (8, -74.0, 40.7),
    (9, -74.0, 40.7), (10, -118.2, 34.1), (11, 174.8, -41.3), (12, -3.0, 53.4),
    (13, -81.0, 42.0), (14, -73.0, 35.5), (15, -81.0, 35.5),
]


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PAPER2, outline=INK, width=4)
    mw, mh = x1 - x0, y1 - y0
    # dotted land: lon -180..180, lat 78..-58
    step = 2.0
    lat = 78.0
    while lat > -58:
        lon = -180.0
        while lon < 180:
            if is_land(lon, lat):
                px = x0 + (lon + 180) / 360 * mw
                py = y0 + (78 - lat) / 136 * mh
                r = 6
                d.ellipse([px - r, py - r, px + r, py + r], fill=NAVY)
            lon += step
        lat -= step
    # pins (8 and 9 share New York: offset 9 slightly)
    for num, lon, lat in PINS:
        plon = lon + (3.0 if num == 9 else 0)
        plat = lat + (3.0 if num == 9 else 0)
        px = x0 + (plon + 180) / 360 * mw
        py = y0 + (78 - plat) / 136 * mh
        r = 21
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=CREAM, width=3)
        d.text((px, py), str(num), font=ab(26), fill=CREAM, anchor="mm")


# ---------------------------------------------------------------- cards
def draw_lead(d, box, card, variant):
    num, region, place, head, deck, chip, src, kind = card
    x0, y0, x1, y1 = box
    d.rectangle(box, outline=INK, width=4)
    d.rectangle([x0, y0, x1, y0 + 8], fill=RED)
    bg = INK if (variant == "A" and num % 2 == 1) or (variant == "B" and num % 2 == 0) else RED_D
    fg = CREAM
    acc = RED if bg == INK else (246, 200, 90)
    scene(d, (x0 + 4, y0 + 12, x1 - 4, y0 + 312), kind, bg, fg, acc)
    y = y0 + 330
    d.text((x0 + 24, y), "%d  ·  %s" % (num, region), font=mb(40), fill=RED)
    y += 52
    d.text((x0 + 24, y), place, font=ab(38), fill=GREY)
    y += 50
    y = para(d, x0 + 24, y, head, pf(66), x1 - x0 - 48, 74, INK)
    y += 6
    y = para(d, x0 + 24, y, deck, ar(46), x1 - x0 - 48, 56, INK)
    # chip + tag pinned at bottom
    d.rectangle([x0 + 24, y1 - 108, x1 - 24, y1 - 52], fill=INK)
    d.text((x0 + 44, y1 - 96), chip, font=ab(38), fill=CREAM)
    d.text((x0 + 24, y1 - 44), "REPORTED · %s" % src, font=mb(34), fill=RED_D)


def clamp_lines(d, text, font, maxw, maxlines):
    lines = wrap(d, text, font, maxw)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        while lines and d.textlength(lines[-1] + " \u2026", font=font) > maxw:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] = lines[-1] + " \u2026"
    return lines


def draw_mini(d, box, card, variant):
    num, region, place, head, deck, chip, src, kind = card
    x0, y0, x1, y1 = box
    d.rectangle(box, outline=INK, width=3)
    bg = INK if (variant == "A" and num % 2 == 0) or (variant == "B" and num % 2 == 1) else RED_D
    fg = CREAM
    acc = RED if bg == INK else (246, 200, 90)
    scene(d, (x0 + 3, y0 + 3, x1 - 3, y0 + 122), kind, bg, fg, acc)
    y = y0 + 132
    d.text((x0 + 16, y), "%d · %s — %s" % (num, region, place), font=mb(28), fill=RED)
    y += 38
    for ln in clamp_lines(d, head, pf(46), x1 - x0 - 32, 2):
        d.text((x0 + 16, y), ln, font=pf(46), fill=INK)
        y += 52
    y += 2
    for ln in clamp_lines(d, deck, ar(36), x1 - x0 - 32, 2):
        d.text((x0 + 16, y), ln, font=ar(36), fill=INK)
        y += 42
    d.text((x0 + 16, y1 - 32), "%s  ·  REPORTED · %s" % (chip, src), font=mb(28), fill=RED_D)


# ---------------------------------------------------------------- page
def render(variant):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 55
    # kicker
    para_c(d, W // 2, y, "36 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE FROM TUESDAY 24 NOVEMBER 2026",
           mb(46), CW, 56, RED_D)
    y = 122
    rule(d, M, y, CW, 6, INK)
    y = 150
    # masthead
    para_c(d, W // 2, y, "THE TELEGRAPH ROOM", pf(268), CW, 300, INK)
    y = 468
    rule(d, M, y, CW, 10, RED)
    y = 500
    para_c(d, W // 2, y, "TUESDAY 24 NOVEMBER 2026", pf(112), CW, 130, RED)
    y = 646
    para_c(d, W // 2, y, "Gaza, Iran and Yemen lead a day of war, sanctions and collapse \u2014 from Benghazi to Wellington.",
           ar(54), CW, 66, INK)
    # number strip
    y = 730
    strip_h = 150
    if variant == "B":
        d.rectangle([M, y, M + CW, y + strip_h], fill=INK)
    else:
        d.rectangle([M, y, M + CW, y + strip_h], outline=RED, width=5)
    cw8 = CW // 8
    for i, (val, lab) in enumerate(NUMSTRIP):
        cx = M + i * cw8 + cw8 // 2
        if i:
            d.line([M + i * cw8, y + 16, M + i * cw8, y + strip_h - 16],
                   fill=RED if variant == "A" else CREAM, width=3)
        vcol = CREAM if variant == "B" else INK
        lcol = (246, 200, 90) if variant == "B" else RED
        wv = d.textlength(val, font=ab(58))
        d.text((cx - wv / 2, y + 18), val, font=ab(58), fill=vcol)
        wl = d.textlength(lab, font=mb(26))
        d.text((cx - wl / 2, y + 96), lab, font=mb(26), fill=lcol)
    # region strip
    y = 900
    d.text((M, y), "THE 15 LEAD STORIES BY REGION", font=mb(40), fill=INK)
    reg = "EUROPE 4   \u00b7   MIDDLE EAST 3   \u00b7   AMERICAS 5   \u00b7   OCEANIA 1   \u00b7   WORLD 2"
    wr = d.textlength(reg, font=mb(40))
    d.text((M + CW - wr, y), reg, font=mb(40), fill=RED_D)
    # timeline
    y = 962
    rule(d, M, y, CW, 4, INK)
    y = 982
    d.text((M, y), "THE DAY IN TIME \u2014 HOURS AS REPORTED (ZONE MARKED)", font=mb(40), fill=INK)
    y = 1036
    colw = CW // 3
    for i, (t, txt, src) in enumerate(TIMELINE):
        cx = M + (i % 3) * colw
        cy = y + (i // 3) * 118
        d.text((cx + 8, cy), t, font=mb(34), fill=RED)
        para(d, cx + 8, cy + 42, txt + "  [" + src + "]", ar(36), colw - 24, 44, INK)
    # leads
    y = 1290
    lead_h = 820
    lw = (CW - 2 * 36) // 3
    for i in range(3):
        draw_lead(d, (M + i * (lw + 36), y, M + i * (lw + 36) + lw, y + lead_h),
                  CARDS[i], variant)
    # minis 4 x 3
    y = 2150
    mini_h = 400
    mw = (CW - 3 * 28) // 4
    for r in range(3):
        for c in range(4):
            idx = 3 + r * 4 + c
            draw_mini(d, (M + c * (mw + 28), y + r * (mini_h + 24),
                          M + c * (mw + 28) + mw, y + r * (mini_h + 24) + mini_h),
                      CARDS[idx], variant)
    # map + date check
    y = 3438
    box_h = 560
    draw_map(d, (M, y, M + 1750, y + box_h))
    d.text((M + 1750 // 2, y + box_h + 8), "WHERE IT HAPPENED \u2014 PINS MATCH STORY NUMBERS · DOTS: LAND, DRAWN IN CODE",
           font=mb(30), fill=NAVY, anchor="ma")
    dx = M + 1790
    dw = CW - 1790
    d.rectangle([dx, y, dx + dw, y + box_h], outline=RED_D, width=5)
    d.rectangle([dx, y, dx + dw, y + 64], fill=RED_D)
    d.text((dx + 24, y + 12), "DATE CHECK \u2014 NOT TODAY'S NEWS", font=ab(40), fill=CREAM)
    yy = y + 84
    for name, when in DATECHECK:
        d.text((dx + 24, yy), "\u2715  " + name, font=ar(36), fill=INK)
        wn = d.textlength(when, font=mb(32))
        d.text((dx + dw - 24 - wn, yy), when, font=mb(32), fill=RED)
        yy += 50
    d.text((dx + 24, y + box_h - 44), "Tonight's real count: 7 sea drones, at the top of this page.",
           font=ar(34), fill=RED_D)
    # also on
    y = 4060
    rule(d, M, y, CW, 4, INK)
    y = 4072
    d.text((M, y), "ALSO ON \u2014 THE REST OF TUESDAY 24 NOVEMBER 2026", font=mb(40), fill=INK)
    y = 4122
    colw = CW // 3
    for col in range(3):
        cx = M + col * colw
        cy = y
        for n, txt in BRIEFS[col * 7:(col + 1) * 7]:
            lines = wrap(d, "%d. %s" % (n, txt), ar(34), colw - 30)
            for ln in lines[:2]:
                d.text((cx + 8, cy), ln, font=ar(34), fill=INK)
                cy += 42
            cy += 4
    # footer
    y = 4470
    rule(d, M, y, CW, 4, INK)
    y = 4488
    para_c(d, W // 2, y,
           "SOURCES: AP · REUTERS · CNN · THE TIMES · BBC · THE GUARDIAN · COINPAPRIKA · MINT · HS / WICKETPULSE",
           mb(30), CW, 40, GREY)
    y = 4530
    para_c(d, W // 2, y,
           "REPORTED = confirmed by the named outlet. CLAIM = attributed to the named source. Pictures and map: original, drawn in code.",
           ar(30), CW, 40, GREY)
    return img


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    img = render(variant)
    fit = img.copy()
    fit.thumbnail((1024, 1024), Image.LANCZOS)
    canvas = Image.new("RGB", (1024, 1024), PAPER)
    canvas.paste(fit, ((1024 - fit.width) // 2, (1024 - fit.height) // 2))
    out = canvas.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.NONE)
    out.save("variant_%s.png" % variant, optimize=True)
    print("variant", variant, "fitted", fit.size, "bytes", len(open("variant_%s.png" % variant, "rb").read()))


if __name__ == "__main__":
    main()
