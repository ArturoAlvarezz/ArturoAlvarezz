"""Regenera scripts/glyphs.json (solo hace falta si cambian los caracteres o fuentes)."""
import json
import string
from pathlib import Path

from textpath import build_atlas

CHARS = string.ascii_letters + string.digits + " /·:—-_.,+→↗%#()<>=[]$"
atlas = build_atlas(["mono", "mono-bold", "serif-bold"], CHARS)
out = Path(__file__).with_name("glyphs.json")
out.write_text(json.dumps(atlas, separators=(",", ":")), encoding="utf-8")
print(out, round(out.stat().st_size / 1024, 1), "KB")
