"""Mapa de contribuciones con estilo Wired Renaissance -> assets/contributions.svg

Solo usa la biblioteca estándar (corre en GitHub Actions sin instalar nada).
Token: env GITHUB_TOKEN, o `gh auth token` en local.
"""
import datetime as dt
import json
import os
import subprocess
import urllib.request
from pathlib import Path

USER = os.environ.get("PROFILE_USER", "ArturoAlvarezz")
ROOT = Path(__file__).resolve().parent.parent
ATLAS = json.loads((Path(__file__).with_name("glyphs.json")).read_text(encoding="utf-8"))

C = {
    "ink": "#05060a", "deep": "#0b0f1a", "panel": "#111522", "line": "#2a3042",
    "violet": "#8b5cf6", "uv": "#5b2eff", "eblue": "#63a4ff", "lav": "#d8ccff",
    "white": "#f4f6fa", "muted": "#9299ad", "term": "#73ffb0",
}
LEVELS = {
    "NONE": ("#121726", "#1d2335"),
    "FIRST_QUARTILE": ("#2a1d66", "#3a2a85"),
    "SECOND_QUARTILE": ("#5b2eff", "#6d45ff"),
    "THIRD_QUARTILE": ("#8b5cf6", "#a07bff"),
    "FOURTH_QUARTILE": ("#63a4ff", "#9cc4ff"),
}

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}"""


def token():
    t = os.environ.get("GITHUB_TOKEN")
    if t:
        return t
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]


# ---------------------------------------------------------------- texto desde el atlas
def measure(t, font, size, spacing=0.0):
    a = ATLAS[font]
    return sum(a.get(ch, a["#"])[0] * size + spacing for ch in t) - (spacing if t else 0)


def text(t, font, size, x, y, fill, spacing=0.0, anchor="start", extra=""):
    if anchor != "start":
        w = measure(t, font, size, spacing)
        x -= w if anchor == "end" else w / 2
    a = ATLAS[font]
    upm = next(iter(a.values()))[2]
    k = size / upm
    parts, cx = [], 0.0
    for ch in t:
        adv, d, _ = a.get(ch, a["#"])
        if d:
            parts.append(f'<path transform="translate({cx:.0f})" d="{d}"/>')
        cx += adv * upm + spacing / k
    return (f'<g fill="{fill}" transform="translate({x:.1f} {y:.1f}) scale({k:.5f} {-k:.5f})" {extra}>'
            + "".join(parts) + "</g>")


# ---------------------------------------------------------------- métricas
def stats(days, today):
    counts = {d["date"]: d["contributionCount"] for d in days}
    ordered = sorted(counts)
    longest = run = 0
    for date in ordered:
        run = run + 1 if counts[date] else 0
        longest = max(longest, run)
    cur = 0
    day = today if counts.get(today.isoformat(), 0) else today - dt.timedelta(days=1)
    while counts.get(day.isoformat(), 0):
        cur += 1
        day -= dt.timedelta(days=1)
    best = max(days, key=lambda d: d["contributionCount"])
    active = sum(1 for d in days if d["contributionCount"])
    return cur, longest, best, active


def render(cal, today):
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    cur, longest, best, active = stats(days, today)

    W, H = 1200, 400
    cell, gap = 15, 4
    step = cell + gap
    n = len(weeks)
    x0 = (W - n * step + gap) / 2 + 22
    y0 = 128

    css = f"""<style>
      .c {{ opacity: 0; animation: in .5s ease-out forwards; }}
      .sweep {{ animation: sweep 6s linear 2.2s infinite; }}
      .pulse {{ animation: pulse 1.6s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
      .blink {{ animation: blink 1.05s steps(1) infinite; }}
      @keyframes in {{ from {{ opacity: 0; transform: translateY(-4px) }} to {{ opacity: 1; transform: none }} }}
      @keyframes sweep {{ 0% {{ transform: translateX(-80px) }} 100% {{ transform: translateX({W + 80}px) }} }}
      @keyframes pulse {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .3 }} }}
      @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}
      @media (prefers-reduced-motion: reduce) {{ .c {{ opacity: 1; animation: none }} .sweep,.pulse,.blink {{ animation: none }} }}
    </style>"""
    defs = f"""<defs>
      <pattern id="ag" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{C['eblue']}" stroke-opacity=".06"/></pattern>
      <linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{C['eblue']}" stop-opacity="0"/>
        <stop offset=".5" stop-color="{C['eblue']}" stop-opacity=".16"/><stop offset="1" stop-color="{C['eblue']}" stop-opacity="0"/></linearGradient>
      <radialGradient id="ah" cx=".85" cy="0" r=".8"><stop offset="0" stop-color="{C['uv']}" stop-opacity=".25"/><stop offset="1" stop-color="{C['uv']}" stop-opacity="0"/></radialGradient>
      <clipPath id="ac"><rect width="{W}" height="{H}" rx="14"/></clipPath>
    </defs>"""
    b = [css, defs, '<g clip-path="url(#ac)">']
    b.append(f'<rect width="{W}" height="{H}" fill="{C["deep"]}"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#ag)"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#ah)"/>')

    # cabecera
    b.append(f'<rect x="36" y="42" width="9" height="9" fill="{C["violet"]}"/>')
    b.append(text("ACTIVITY.LOG // LAST 365 DAYS", "mono-bold", 14, 56, 52, C["violet"], 2.4))
    b.append(text(f"SYNC {today.isoformat()} UTC", "mono", 12.5, W - 36, 51, C["muted"], 1.6, "end"))
    b.append(f'<path d="M36 72H{W-36}" stroke="{C["line"]}"/>')

    # meses
    last_col = -9
    for i, w in enumerate(weeks):
        first = dt.date.fromisoformat(w["contributionDays"][0]["date"])
        if first.day <= 7 and i - last_col >= 3:
            label = first.strftime("%b").upper()
            b.append(text(label, "mono", 11.5, x0 + i * step, y0 - 14, C["muted"], 1.2))
            last_col = i
    # días
    for row, name in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b.append(text(name, "mono", 11, x0 - 14, y0 + row * step + 11.5, C["muted"], 1.2, "end"))

    # celdas
    today_s = today.isoformat()
    for i, w in enumerate(weeks):
        for d in w["contributionDays"]:
            row = dt.date.fromisoformat(d["date"]).isoweekday() % 7
            fill, stroke = LEVELS.get(d["contributionLevel"], LEVELS["NONE"])
            x, y = x0 + i * step, y0 + row * step
            delay = i * 0.028 + row * 0.01
            cls = "c pulse" if d["date"] == today_s else "c"
            b.append(f'<rect class="{cls}" style="animation-delay:{delay:.2f}s" x="{x:.1f}" y="{y}" '
                     f'width="{cell}" height="{cell}" rx="3" fill="{fill}" stroke="{stroke}"/>')
    b.append(f'<rect class="sweep" x="0" y="{y0 - 8}" width="80" height="{7 * step + 12}" fill="url(#sw)"/>')

    # métricas
    ys = y0 + 7 * step + 34
    b.append(f'<path d="M36 {ys}H{W-36}" stroke="{C["line"]}" stroke-dasharray="3 5"/>')
    best_date = dt.date.fromisoformat(best["date"]).strftime("%d %b").upper()
    metrics = [
        (f"{cal['totalContributions']:,}".replace(",", "."), "CONTRIBUTIONS"),
        (str(active), "ACTIVE DAYS"),
        (f"{cur}d", "CURRENT STREAK"),
        (f"{longest}d", "LONGEST STREAK"),
        (str(best["contributionCount"]), f"BEST DAY · {best_date}"),
    ]
    colw = 176
    for k, (val, lab) in enumerate(metrics):
        x = 36 + k * colw
        b.append(text(val, "serif-bold", 30, x, ys + 50, C["lav"] if k else C["white"], 1))
        b.append(text(lab, "mono", 11, x, ys + 72, C["muted"], 1.6))
    # leyenda
    lx = W - 36
    b.append(text("MORE", "mono", 11, lx, ys + 50, C["muted"], 1.4, "end"))
    lx -= measure("MORE", "mono", 11, 1.4) + 10
    for lvl in reversed(list(LEVELS)):
        lx -= cell
        fill, stroke = LEVELS[lvl]
        b.append(f'<rect x="{lx:.1f}" y="{ys + 38}" width="{cell}" height="{cell}" rx="3" fill="{fill}" stroke="{stroke}"/>')
        lx -= 4
    b.append(text("LESS", "mono", 11, lx - 6, ys + 50, C["muted"], 1.4, "end"))
    b.append(text("$ git log --since=1.year", "mono", 11, W - 36, ys + 72, C["term"], 0.6, "end",
                  'opacity=".8"'))
    b.append("</g>")
    b.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{C["line"]}"/>')

    title = f"{cal['totalContributions']} contribuciones en el último año"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{"".join(b)}</svg>\n')


def main():
    today = dt.datetime.now(dt.timezone.utc).date()
    svg = render(fetch(), today)
    out = ROOT / "assets" / "contributions.svg"
    out.write_text(svg, encoding="utf-8")
    print(out.name, round(len(svg.encode()) / 1024, 1), "KB")


if __name__ == "__main__":
    main()
