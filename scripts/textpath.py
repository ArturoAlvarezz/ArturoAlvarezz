"""Convierte texto en paths SVG usando fuentes locales (GitHub no carga fuentes dentro de SVG)."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONTS = {
    "serif": ("/usr/share/fonts/google-noto-serif-cjk-vf-fonts/NotoSerifCJK-VF.ttc", 0, {"wght": 900}),
    "serif-bold": ("/usr/share/fonts/google-noto-serif-cjk-vf-fonts/NotoSerifCJK-VF.ttc", 0, {"wght": 700}),
    "mono": ("/usr/share/fonts/google-noto-vf/NotoSansMono[wght].ttf", None, {"wght": 500}),
    "mono-bold": ("/usr/share/fonts/google-noto-vf/NotoSansMono[wght].ttf", None, {"wght": 600}),
    "sans": ("/usr/share/fonts/rsms-inter-fonts/Inter-Regular.ttf", None, None),
    "sans-medium": ("/usr/share/fonts/rsms-inter-fonts/Inter-Medium.ttf", None, None),
    "sans-semibold": ("/usr/share/fonts/rsms-inter-fonts/Inter-SemiBold.ttf", None, None),
}

_cache = {}


def _num(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def _font(key):
    if key not in _cache:
        path, idx, loc = FONTS[key]
        f = TTFont(path, fontNumber=idx) if idx is not None else TTFont(path)
        gs = f.getGlyphSet(location=loc) if loc else f.getGlyphSet()
        _cache[key] = (f, gs, f.getBestCmap(), f["head"].unitsPerEm)
    return _cache[key]


def _glyph(ch, font):
    """Glifo del carácter; si la fuente no lo tiene, lo toma de Inter."""
    f, gs, cmap, upm = _font(font)
    if ord(ch) not in cmap:
        f, gs, cmap, upm = _font("sans-semibold")
    return gs[cmap.get(ord(ch), cmap[ord("?")])], upm


def measure(text, font, size, spacing=0.0):
    w = 0.0
    for ch in text:
        g, upm = _glyph(ch, font)
        w += g.width * size / upm + spacing
    return w - (spacing if text else 0)


def text_d(text, font, size, x, y, spacing=0.0, anchor="start"):
    """Devuelve el atributo d de un path con el texto en (x, y) = línea base."""
    gs = _font(font)[1]
    if anchor != "start":
        w = measure(text, font, size, spacing)
        x -= w if anchor == "end" else w / 2
    pen = SVGPathPen(gs, ntos=_num)
    cx = x
    for ch in text:
        g, upm = _glyph(ch, font)
        s = size / upm
        if ch != " ":
            g.draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += g.width * s + spacing
    return pen.getCommands()


def text(t, font, size, x, y, fill, spacing=0.0, anchor="start", extra=""):
    d = text_d(t, font, size, x, y, spacing, anchor)
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def wrap(t, font, size, max_w, spacing=0.0):
    lines, cur = [], ""
    for word in t.split():
        trial = f"{cur} {word}".strip()
        if measure(trial, font, size, spacing) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines
