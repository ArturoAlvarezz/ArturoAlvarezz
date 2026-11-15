"""Genera los SVG del perfil con la identidad "Wired Renaissance".

Uso: python3 scripts/build.py   (escribe en assets/)
"""
import base64
from pathlib import Path

from textpath import text, measure, wrap

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

C = {
    "ink": "#05060a",
    "deep": "#0b0f1a",
    "panel": "#111522",
    "panel2": "#171c2c",
    "line": "#2a3042",
    "violet": "#8b5cf6",
    "uv": "#5b2eff",
    "blue": "#2f6bff",
    "eblue": "#63a4ff",
    "lav": "#d8ccff",
    "white": "#f4f6fa",
    "muted": "#9299ad",
    "term": "#73ffb0",
    "alert": "#ff5c8a",
}

STYLE = """
<style>
  .pulse { animation: pulse 2.2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }
  .ring { animation: ring 2.2s ease-out infinite; transform-box: fill-box; transform-origin: center; }
  .blink { animation: blink 1.05s steps(1) infinite; }
  .scan { animation: scan 7s linear infinite; }
  .glitch-a { animation: glitchA 6s steps(1) infinite; opacity: 0; }
  .glitch-b { animation: glitchB 6s steps(1) infinite; opacity: 0; }
  .flicker { animation: flicker 4s linear infinite; }
  .draw { stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: draw 3.2s ease-out forwards; }
  @keyframes pulse { 0%,100% { opacity: 1 } 50% { opacity: .35 } }
  @keyframes ring { 0% { transform: scale(1); opacity: .7 } 100% { transform: scale(3.2); opacity: 0 } }
  @keyframes blink { 0%,49% { opacity: 1 } 50%,100% { opacity: 0 } }
  @keyframes scan { 0% { transform: translateY(-140px) } 100% { transform: translateY(720px) } }
  @keyframes glitchA { 0%,91%,95%,100% { opacity: 0; transform: none }
                       92% { opacity: .85; transform: translate(-6px, 2px) }
                       93% { opacity: .6; transform: translate(4px, -1px) } }
  @keyframes glitchB { 0%,91%,95%,100% { opacity: 0; transform: none }
                       92% { opacity: .85; transform: translate(6px, -2px) }
                       94% { opacity: .5; transform: translate(-3px, 1px) } }
  @keyframes flicker { 0%,100% { opacity: .9 } 47% { opacity: .9 } 48% { opacity: .4 } 49% { opacity: .9 } }
  @keyframes draw { to { stroke-dashoffset: 0 } }
  @media (prefers-reduced-motion: reduce) {
    .pulse, .ring, .blink, .scan, .glitch-a, .glitch-b, .flicker { animation: none }
    .draw { animation: none; stroke-dashoffset: 0 }
  }
</style>
"""


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{title}"><title>{title}</title>{STYLE}{body}</svg>\n'
    )


def grid_defs(pid, step=48):
    return (
        f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
        f'<path d="M{step} 0H0V{step}" fill="none" stroke="{C["eblue"]}" stroke-opacity=".07" stroke-width="1"/>'
        f"</pattern>"
    )


def brackets(x, y, w, h, size=14, color=None, width=1.5):
    c = color or C["violet"]
    s = size
    d = (
        f"M{x} {y+s}V{y}H{x+s} M{x+w-s} {y}H{x+w}V{y+s} "
        f"M{x+w} {y+h-s}V{y+h}H{x+w-s} M{x+s} {y+h}H{x}V{y+h-s}"
    )
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{width}"/>'


def status_dot(cx, cy, color, r=4):
    return (
        f'<circle class="ring" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="1.5"/>'
        f'<circle class="pulse" cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>'
    )


def scanline(w, h, gid):
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{C["eblue"]}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{C["eblue"]}" stop-opacity=".09"/>'
        f'<stop offset="1" stop-color="{C["eblue"]}" stop-opacity="0"/></linearGradient>',
        f'<rect class="scan" x="0" y="0" width="{w}" height="120" fill="url(#{gid})"/>',
    )


# ---------------------------------------------------------------- HERO
def hero():
    W, H = 1200, 600
    david = base64.b64encode((ROOT / "src" / "david.webp").read_bytes()).decode()
    scan_def, scan_rect = scanline(W, H, "scanG")
    defs = f"""<defs>
      {grid_defs("grid")}
      {scan_def}
      <radialGradient id="halo" cx=".5" cy=".45" r=".5">
        <stop offset="0" stop-color="{C['uv']}" stop-opacity=".45"/>
        <stop offset=".6" stop-color="{C['violet']}" stop-opacity=".08"/>
        <stop offset="1" stop-color="{C['ink']}" stop-opacity="0"/>
      </radialGradient>
      <linearGradient id="fadeL" x1="0" x2="1">
        <stop offset="0" stop-color="{C['ink']}" stop-opacity="1"/>
        <stop offset=".35" stop-color="{C['ink']}" stop-opacity="0"/>
      </linearGradient>
      <linearGradient id="fadeB" x1="0" y1="0" x2="0" y2="1">
        <stop offset=".75" stop-color="{C['ink']}" stop-opacity="0"/>
        <stop offset="1" stop-color="{C['ink']}" stop-opacity="1"/>
      </linearGradient>
      <linearGradient id="nameG" x1="0" x2="1">
        <stop offset="0" stop-color="{C['lav']}"/>
        <stop offset=".55" stop-color="{C['violet']}"/>
        <stop offset="1" stop-color="{C['blue']}"/>
      </linearGradient>
      <clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}" rx="18"/></clipPath>
    </defs>"""

    b = [defs, '<g clip-path="url(#frame)">']
    b.append(f'<rect width="{W}" height="{H}" fill="{C["ink"]}"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    # David + halo
    b.append(f'<ellipse cx="930" cy="320" rx="330" ry="300" fill="url(#halo)"/>')
    b.append(
        f'<image href="data:image/webp;base64,{david}" x="710" y="44" width="490" height="612" '
        f'preserveAspectRatio="xMidYMin slice" class="flicker"/>'
    )
    b.append(f'<rect x="660" y="0" width="540" height="{H}" fill="url(#fadeL)"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#fadeB)"/>')
    # gran 00 de fondo
    b.append(text("00", "serif", 260, 1170, 640, "none", anchor="end",
                  extra=f'stroke="{C["line"]}" stroke-width="1.5" opacity=".9"'))

    # barra superior
    b.append(text("SIGNAL_ORIGIN: 34.9828°S / 71.2394°W", "mono", 12.5, 56, 54, C["muted"], spacing=1.2))
    b.append(text("ARTURO.ALVAREZ // GITHUB.PROFILE", "mono", 12.5, 1144, 54, C["muted"], spacing=1.2, anchor="end"))
    b.append(f'<path d="M56 72H1144" stroke="{C["line"]}" stroke-width="1"/>')
    b.append(f'<path class="draw" d="M56 72H1144" stroke="{C["violet"]}" stroke-width="1.5"/>')

    # eyebrow
    b.append(f'<rect x="56" y="122" width="10" height="10" fill="{C["violet"]}"/>')
    b.append(text("THE WIRED RENAISSANCE / PORTFOLIO 2026", "mono-bold", 14, 78, 132, C["violet"], spacing=2.6))

    # nombre con glitch
    name1_y, name2_y, size = 256, 386, 128
    b.append(text("ARTURO", "serif", size, 50, name1_y, C["white"], spacing=2))
    for cls, col in (("glitch-a", C["alert"]), ("glitch-b", C["eblue"])):
        b.append(text("ÁLVAREZ", "serif", size, 50, name2_y, col, spacing=2, extra=f'class="{cls}"'))
    b.append(text("ÁLVAREZ", "serif", size, 50, name2_y, "url(#nameG)", spacing=2))

    # rol + cursor
    role = "CLOUD ENGINEER / SYSTEMS BUILDER"
    rw = measure(role, "mono-bold", 19, 2.2)
    b.append(text(">", "mono-bold", 19, 56, 446, C["term"]))
    b.append(text(role, "mono-bold", 19, 82, 446, C["eblue"], spacing=2.2))
    b.append(f'<rect class="blink" x="{82 + rw + 8:.1f}" y="430" width="11" height="20" fill="{C["term"]}"/>')

    # telemetría
    cols = [
        ("LOCATION", "CURICÓ, CL / UTC-4", None),
        ("FOCUS", "CLOUD · DEVOPS · SDN", None),
        ("SYSTEM STATUS", "AVAILABLE", C["term"]),
    ]
    x = 56
    b.append(f'<path d="M56 488H700" stroke="{C["line"]}"/>')
    for label, value, accent in cols:
        b.append(text(label, "mono", 12.5, x, 516, C["muted"], spacing=1.8))
        vx = x
        if accent:
            b.append(status_dot(x + 5, 540, accent))
            vx = x + 18
        b.append(text(value, "mono-bold", 14, vx, 545, accent or C["white"], spacing=1.2))
        x += 228

    b.append(scan_rect)
    b.append("</g>")
    b.append(brackets(16, 16, W - 32, H - 32, size=22))
    b.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{C["line"]}"/>')
    return svg(W, H, "".join(b), "Arturo Álvarez — Cloud Engineer / Systems Builder")


# ---------------------------------------------------------------- SECTION LABELS
def label(idx, name, note):
    W, H = 1200, 64
    b = []
    b.append(text(f"// {idx}", "mono-bold", 15, 0, 38, C["violet"], spacing=2))
    nx = measure(f"// {idx}", "mono-bold", 15, 2) + 22
    b.append(text(name, "serif-bold", 26, nx, 42, C["white"], spacing=3))
    lx = nx + measure(name, "serif-bold", 26, 3) + 24
    nw = measure(note, "mono", 13, 1.6)
    b.append(f'<path d="M{lx:.0f} 33H{W - nw - 24:.0f}" stroke="{C["line"]}"/>')
    b.append(f'<path class="draw" d="M{lx:.0f} 33H{W - nw - 24:.0f}" stroke="{C["violet"]}" stroke-opacity=".7"/>')
    b.append(f'<rect x="{lx:.0f}" y="30" width="6" height="6" fill="{C["violet"]}"/>')
    b.append(text(note, "mono", 13, W, 38, C["muted"], spacing=1.6, anchor="end"))
    return svg(W, H, "".join(b), f"{idx} {name}")


# ---------------------------------------------------------------- PROJECT CARDS
PROJECTS = [
    dict(
        slug="sdn-ami", idx="01", short="SDN / AMI",
        cat="SDN · CLOUD-NATIVE · NETWORKING", status="COMPLETED", scolor="eblue",
        title="Arquitectura SDN resiliente para Infraestructura de Medición Avanzada en redes eléctricas.",
        metrics=[(">99%", "AVAILABILITY"), ("46.4 ms", "AVG LATENCY"), ("100%", "ATTACKS DETECTED")],
        stack=["k3s", "Calico", "Ryu", "Open vSwitch", "FRRouting", "Prometheus"],
        link="REPOSITORY",
    ),
    dict(
        slug="arm64-infra", idx="02", short="ARM64 INFRA",
        cat="LINUX · CONTAINERS · CI/CD", status="IN OPERATION", scolor="term",
        title="Plataforma personal Cloud & DevOps sobre un servidor físico ARM64 con despliegues automatizados.",
        metrics=[("ARM64", "ARCHITECTURE"), ("13", "DOCKER NETWORKS"), ("11", "VOLUMES")],
        stack=["Debian 12", "Docker", "GitHub Actions", "Nginx", "Cloudflare Tunnel"],
        link="HOMELAB",
    ),
    dict(
        slug="fuego-dance", idx="03", short="FUEGO DANCE",
        cat="FULL-STACK · CONTENT · DEVOPS", status="LIVE", scolor="term",
        title="Plataforma web y gestión de contenido para una academia de Salsa Casino en 3 ciudades.",
        metrics=[("LIVE", "STATUS"), ("AMD64/ARM64", "DEPLOYMENT"), ("3", "LOCATIONS")],
        stack=["React 18", "FastAPI", "Tailwind", "Docker", "Nginx", "PostgreSQL"],
        link="FUEGODANCE.CL",
    ),
    dict(
        slug="sherlock-osint", idx="04", short="SHERLOCK OSINT",
        cat="OSINT · CYBERSECURITY · REAL-TIME", status="LIVE", scolor="term",
        title="Dashboard OSINT que transmite coincidencias de identidades digitales en tiempo real.",
        metrics=[("LIVE", "STATUS"), ("SSE", "STREAMING"), ("AMD64/ARM64", "DEPLOYMENT")],
        stack=["Vue 3", "FastAPI", "Sherlock", "SSE", "Docker", "Tailwind"],
        link="LIVE DEMO",
    ),
]


def card(p):
    W, H = 600, 380
    sc = C[p["scolor"]]
    gid = f"cg{p['idx']}"
    b = [f"""<defs>{grid_defs('g' + p['idx'], 40)}
      <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="{C['panel2']}"/><stop offset="1" stop-color="{C['ink']}"/>
      </linearGradient>
      <radialGradient id="gl{p['idx']}" cx="1" cy="0" r=".9">
        <stop offset="0" stop-color="{C['uv']}" stop-opacity=".28"/><stop offset="1" stop-color="{C['uv']}" stop-opacity="0"/>
      </radialGradient></defs>"""]
    b.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="url(#{gid})" stroke="{C["line"]}"/>')
    b.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#g{p["idx"]})"/>')
    b.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#gl{p["idx"]})"/>')
    b.append(brackets(12, 12, W - 24, H - 24, size=12, width=1.2))

    # cabecera
    b.append(text(p["idx"], "serif", 34, 36, 66, C["violet"]))
    b.append(text(p["cat"], "mono", 12, 92, 60, C["muted"], spacing=1.4))
    sw = measure(p["status"], "mono-bold", 12, 1.4)
    b.append(text(p["status"], "mono-bold", 12, W - 36, 60, sc, spacing=1.4, anchor="end"))
    b.append(status_dot(W - 36 - sw - 12, 56, sc, r=3.5))

    # título
    b.append(text(p["short"], "serif", 40, 36, 128, C["white"], spacing=1))
    y = 162
    for line in wrap(p["title"], "sans", 17, W - 72)[:2]:
        b.append(text(line, "sans", 17, 36, y, C["muted"]))
        y += 24

    # métricas
    b.append(f'<path d="M36 222H{W-36}" stroke="{C["line"]}"/>')
    colw = (W - 72) / 3
    for i, (val, lab) in enumerate(p["metrics"]):
        x = 36 + i * colw
        if i:
            b.append(f'<path d="M{x - 14:.0f} 236V286" stroke="{C["line"]}"/>')
        size = 24 if measure(val, "mono-bold", 24, 0) < colw - 24 else 18
        b.append(text(val, "mono-bold", size, x, 264, C["lav"]))
        b.append(text(lab, "mono", 11.5, x, 286, C["muted"], spacing=1.4))
    b.append(f'<path d="M36 304H{W-36}" stroke="{C["line"]}"/>')

    # stack chips
    x = 36
    for t in p["stack"]:
        tw = measure(t, "mono", 12.5, 0.4)
        if x + tw + 20 > W - 150:
            break
        b.append(f'<rect x="{x}" y="322" width="{tw + 18:.1f}" height="26" rx="4" fill="{C["deep"]}" stroke="{C["line"]}"/>')
        b.append(text(t, "mono", 12.5, x + 9, 340, C["eblue"], spacing=0.6))
        x += tw + 26
    b.append(text(p["link"] + " ↗", "mono-bold", 12.5, W - 36, 339, C["violet"], spacing=1.4, anchor="end"))
    return svg(W, H, "".join(b), f"{p['idx']} {p['short']}")


# ---------------------------------------------------------------- STACK
STACK = [
    ("CLOUD & INFRASTRUCTURE", [("AWS", "Hosting, DNS, SSL/TLS y operación"), ("GCP", "Servicios cloud y experimentación"), ("Linux", "Servidores y troubleshooting")]),
    ("CONTAINERS & ORCHESTRATION", [("Docker", "Stacks, redes, volúmenes, healthchecks"), ("Kubernetes / k3s", "Clústeres de alta disponibilidad"), ("Calico", "Networking y políticas de red")]),
    ("NETWORKING & OBSERVABILITY", [("SDN / OpenFlow", "Ryu y Open vSwitch"), ("OSPF / BGP", "Routing dinámico con FRRouting"), ("Prometheus / Grafana", "Métricas y dashboards")]),
    ("AUTOMATION & DEVELOPMENT", [("GitHub Actions", "CI/CD y publicación de imágenes"), ("Python", "FastAPI, Flask y automatización"), ("JS / TypeScript", "React, Next.js, Vue")]),
]


def stack():
    W, H = 1200, 560
    b = [f"<defs>{grid_defs('sg', 40)}</defs>"]
    b.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{C["deep"]}" stroke="{C["line"]}"/>')
    b.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#sg)"/>')
    # barra de ventana
    b.append(f'<path d="M1 15a14 14 0 0 1 14-14H{W-15}a14 14 0 0 1 14 14V48H1Z" fill="{C["panel"]}"/>')
    b.append(f'<path d="M1 48H{W-1}" stroke="{C["line"]}"/>')
    for i, col in enumerate((C["alert"], C["violet"], C["term"])):
        b.append(f'<circle cx="{28 + i * 20}" cy="25" r="5.5" fill="{col}" opacity=".85"/>')
    b.append(text("arturo@wired: ~/stack", "mono", 12.5, W / 2, 29, C["muted"], spacing=0.8, anchor="middle"))
    b.append(text("TTY/01", "mono", 11, W - 28, 29, C["line"], spacing=1.2, anchor="end"))

    b.append(text("$", "mono-bold", 15, 36, 90, C["term"]))
    b.append(text("cat stack.yml --group-by=domain", "mono", 15, 58, 90, C["white"], spacing=0.4))

    colw = (W - 72) / 4
    for i, (title, items) in enumerate(STACK):
        x = 36 + i * colw
        b.append(f'<rect x="{x}" y="118" width="8" height="8" fill="{C["violet"]}"/>')
        for j, part in enumerate(title.split(" & ")):
            label = part + (" &" if j == 0 and "&" in title else "")
            b.append(text(label, "mono-bold", 13.5, x + 16, 128 + j * 19, C["violet"], spacing=1.6))
        y = 186
        for name, desc in items:
            b.append(text(name, "sans-semibold", 22, x, y, C["white"]))
            for k, line in enumerate(wrap(desc, "mono", 13.5, colw - 26)[:2]):
                b.append(text(line, "mono", 13.5, x, y + 26 + k * 18, C["muted"], spacing=0.2))
            y += 90
        if i:
            b.append(f'<path d="M{x - 18:.0f} 116V430" stroke="{C["line"]}"/>')

    # certificación
    b.append(f'<path d="M36 448H{W-36}" stroke="{C["line"]}" stroke-dasharray="3 5"/>')
    b.append(text("CERTIFIED", "mono", 13, 36, 485, C["muted"], spacing=1.8))
    b.append(text("AWS Certified AI Practitioner", "sans-semibold", 20, 160, 486, C["white"]))
    b.append(text("AIF-C01 · 2026", "mono", 14, 160 + measure("AWS Certified AI Practitioner", "sans-semibold", 20) + 16, 486, C["eblue"], spacing=1))
    b.append(text("$", "mono-bold", 15, 36, 526, C["term"]))
    b.append(f'<rect class="blink" x="54" y="511" width="10" height="19" fill="{C["term"]}"/>')
    b.append(text("UPTIME: ALWAYS LEARNING", "mono", 13, W - 36, 526, C["muted"], spacing=1.6, anchor="end"))
    return svg(W, H, "".join(b), "Stack: Cloud, Containers, Networking, Automation")


# ---------------------------------------------------------------- FOOTER
def footer():
    W, H = 1200, 300
    scan_def, scan_rect = scanline(W, H, "fscan")
    b = [f"""<defs>{grid_defs('fg')}{scan_def}
      <radialGradient id="fh" cx=".5" cy="1" r=".7">
        <stop offset="0" stop-color="{C['uv']}" stop-opacity=".35"/><stop offset="1" stop-color="{C['uv']}" stop-opacity="0"/>
      </radialGradient>
      <linearGradient id="fnG" x1="0" x2="1">
        <stop offset="0" stop-color="{C['lav']}"/><stop offset="1" stop-color="{C['violet']}"/>
      </linearGradient>
      <clipPath id="fclip"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>"""]
    b.append('<g clip-path="url(#fclip)">')
    b.append(f'<rect width="{W}" height="{H}" fill="{C["ink"]}"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#fg)"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#fh)"/>')
    b.append(status_dot(W / 2 - measure("SIGNAL OPEN · ACCEPTING TRANSMISSIONS", "mono-bold", 12, 2.4) / 2 - 16, 66, C["term"]))
    b.append(text("SIGNAL OPEN · ACCEPTING TRANSMISSIONS", "mono-bold", 12, W / 2, 70, C["term"], spacing=2.4, anchor="middle"))
    b.append(text("Construyamos algo", "serif", 52, W / 2, 148, C["white"], spacing=1, anchor="middle"))
    b.append(text("resiliente.", "serif", 52, W / 2, 212, "url(#fnG)", spacing=1, anchor="middle"))
    b.append(text("ARTUROALVAREZ.DEV  ↗", "mono-bold", 14, W / 2, 260, C["eblue"], spacing=2.6, anchor="middle"))
    b.append(scan_rect)
    b.append("</g>")
    b.append(brackets(16, 16, W - 32, H - 32, size=18))
    b.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{C["line"]}"/>')
    return svg(W, H, "".join(b), "Contacto — arturoalvarez.dev")


def main():
    OUT.mkdir(exist_ok=True)
    files = {"hero.svg": hero(), "stack.svg": stack(), "footer.svg": footer()}
    files["label-profile.svg"] = label("01", "PROFILE", "WHOAMI")
    files["label-activity.svg"] = label("02", "ACTIVITY", "SYNCED DAILY / GITHUB ACTIONS")
    files["label-work.svg"] = label("03", "SELECTED WORK", "4 SYSTEMS / PRODUCTION + LAB")
    files["label-stack.svg"] = label("04", "STACK", "TOOLING / DOMAINS")
    files["label-contact.svg"] = label("05", "CONTACT", "OPEN CHANNEL")
    for p in PROJECTS:
        files[f"project-{p['slug']}.svg"] = card(p)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"{name:32s} {len(content.encode()) / 1024:7.1f} KB")


if __name__ == "__main__":
    main()
