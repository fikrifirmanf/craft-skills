#!/usr/bin/env python3
"""Lint a design.md: structure, token sanity, and the patterns strong systems share.

Usage: lint_design_md.py design.md

Reports ERROR (must fix), WARN and INFO (advisory; intentional choices are valid).
Exits 1 on structural errors or contrast failures. Stylistic thresholds are optional
historical heuristics; see references/token-ranges.md. Use only for full design docs.
"""
import colorsys
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from designmd import SECTIONS, body_sections, color_tokens, load, parse_color, px  # noqa: E402

out = {"ERROR": [], "WARN": [], "INFO": []}


def report(level, msg):
    out[level].append(msg)


def check_structure(fm, body):
    for key in ("name", "description"):
        if not fm.get(key) or "<" in str(fm.get(key)):
            report("ERROR", f"frontmatter `{key}` is missing or still a placeholder")
    for group in ("colors", "typography", "spacing", "rounded", "components"):
        if not isinstance(fm.get(group), dict) or not fm.get(group):
            report("ERROR", f"frontmatter group `{group}` is missing or empty")
    secs = body_sections(body)
    names = {}
    for want in SECTIONS:
        hit = next((h for h in secs if h.lower().lstrip("0123456789. ").startswith(want.lower())), None)
        if hit:
            names[want.lower()] = hit
    for s in SECTIONS:
        if s.lower() not in names:
            report("ERROR", f"section `## {s}` is missing")
            continue
        text = secs[names[s.lower()]]
        if not text or re.search(r"<[^>]{8,}>", text):
            report("WARN", f"`## {s}` is empty or still contains a placeholder")
    g = secs.get(names.get("guardrails", ""), "")
    bullets = [l for l in g.splitlines() if l.strip().startswith(("-", "*"))]
    vague = [b for b in bullets if not re.search(r"#[0-9a-fA-F]{3,8}|\d+(px|ms|%|em)|`|[a-z]+-[a-z]+", b)]
    if len(vague) > max(1, len(bullets) // 2):
        report("WARN", "most guardrails name no token, value or component; make them specific")
    c = secs.get(names.get("colors", ""), "")
    if c and not re.search(r"reserv|ration|only|never|exclusively|confined", c, re.I):
        report("WARN", "`## Colors` doesn't say what the accent is reserved for (its roles and where it never goes)")


def check_colors(fm):
    light = {k: v for t, k, v in color_tokens(fm) if t == "light"}
    parsed = {k: parse_color(v) for k, v in light.items()}
    bad = [k for k, v in parsed.items() if v is None and "{" not in str(light[k])]
    for k in bad:
        report("WARN", f"colour `{k}` is not a parseable hex/rgb value: {light[k]!r}")
    parsed = {k: v for k, v in parsed.items() if v}
    core = [k for k in parsed if not re.search(r"^on-|-on-|hover|pressed|active|focus|success|warning|danger|error|info", k.lower())]
    n = len(core)
    if n and n < 6:
        report("WARN", f"only {n} colours; most systems need 7-12 (field, surface, 3 ink steps, border, accent, semantics)")
    if n > 14:
        report("WARN", f"{n} core colours (excluding states, on-colours and semantics); above about 14, near-duplicates creep in. Merge them")
    keys = " ".join(k.lower() for k in parsed)
    for role, rx in (("background", r"background|canvas|bg\b"), ("primary text", r"text|ink|foreground"),
                     ("accent", r"accent|primary|brand"), ("border", r"border|divider|hairline|line")):
        if not re.search(rx, keys):
            report("WARN", f"no `{role}` colour role found")
    semantic = re.compile(r"success|warning|danger|error|info|positive|negative|caution")
    chroma = []
    for k, c in parsed.items():
        if semantic.search(k.lower()):
            continue
        h, l, s = colorsys.rgb_to_hls(*c[:3])
        if s > 0.35 and 0.15 < l < 0.85:
            chroma.append((k, round(h * 360)))
    hues = []
    for k, h in chroma:
        if all(min(abs(h - x), 360 - abs(h - x)) > 25 for x in hues):
            hues.append(h)
    if len(hues) > 3:
        report("WARN", f"{len(hues)} distinct saturated hue families ({', '.join(k for k, _ in chroma)}); "
                       "strong systems ration 1-2. Give extra hues a single defined job or cut them")
    if not chroma:
        report("INFO", "fully achromatic palette; fine for monochrome systems, but make sure actions and focus remain obvious")
    for k, c in parsed.items():
        if k.lower() in ("background", "bg", "canvas") and c[:3] in ((1, 1, 1), (0, 0, 0)):
            report("INFO", f"`{k}` is pure {'white' if c[0] else 'black'}; two-thirds of strong systems tint the field (warm or cool)")


def check_type(fm):
    ty = fm.get("typography", {})
    if not isinstance(ty, dict):
        return
    styles = {k: v for k, v in ty.items() if isinstance(v, dict)}
    if len(styles) < 4:
        report("WARN", f"only {len(styles)} type styles; define 5-7 (display, headline, title, body, label, caption)")
    if len(styles) > 9:
        report("WARN", f"{len(styles)} type styles; more than about 8 usually means the hierarchy is unclear")
    fams = {str(v.get("fontFamily", "")).split(",")[0].strip().strip("'\"") for v in styles.values() if v.get("fontFamily")}
    fams.discard("")
    if len(fams) > 3:
        report("WARN", f"{len(fams)} font families ({', '.join(sorted(fams))}); give each one a job, or cut to 2-3")
    weights = {str(v.get("fontWeight")) for v in styles.values() if v.get("fontWeight")}
    if len(weights) > 4:
        report("INFO", f"{len(weights)} font weights in use ({', '.join(sorted(weights))}); 2-3 is typical")
    sizes = []
    for name, v in styles.items():
        size = px(v.get("fontSize", "")) if v.get("fontSize") else None
        if not size:
            report("WARN", f"type style `{name}` has no fontSize")
            continue
        sizes.append((size, name))
        lh = v.get("lineHeight")
        lhv = px(lh) if lh else None
        if lhv and lhv > 4:
            lhv = lhv / size
        ls = v.get("letterSpacing")
        lsem = 0.0
        if ls:
            m = re.match(r"\s*(-?[\d.]+)\s*(px|em|rem|%)?", str(ls))
            if m:
                x, u = float(m.group(1)), m.group(2)
                lsem = x if u == "em" else x / 100 if u == "%" else (x * 16 / size if u == "rem" else x / size)
        if size >= 40 and lsem > -0.005:
            report("WARN", f"`{name}` is {size:g}px with tracking {ls or 0}; display sizes look loose without "
                           "tightening (typically -0.02 to -0.04em)")
        if lhv:
            if size >= 40 and lhv > 1.3:
                report("WARN", f"`{name}` {size:g}px has line-height {lhv:.2f}; large type usually sits at 0.95-1.15")
            if size <= 18 and lhv < 1.3 and not re.search(r"label|button|caption|overline|eyebrow|mono|tag", name, re.I):
                report("WARN", f"`{name}` {size:g}px has line-height {lhv:.2f}; running text needs about 1.4-1.6")
        if size < 12:
            report("WARN", f"`{name}` is {size:g}px; below 12px is hard to read, so use it for non-essential labels only")
    if sizes:
        body = [s for s, n in sizes if re.search(r"body|paragraph|text", n, re.I)] or [s for s, _ in sizes if 14 <= s <= 18]
        if body:
            b = body[0]
            if not 14 <= b <= 20:
                report("WARN", f"body size {b:g}px is outside the usual 14-20px")
            ratio = max(s for s, _ in sizes) / b
            if ratio < 1.6:
                report("INFO", f"display / body ratio is {ratio:.1f}x; hierarchy will feel flat (typical is 2.2-4.5x)")


def check_spacing_radius(fm):
    sp = fm.get("spacing", {})
    vals = [(k, px(v)) for k, v in sp.items()] if isinstance(sp, dict) else []
    vals = [(k, v) for k, v in vals if v is not None]
    off = [f"{k}={v:g}" for k, v in vals if v % 4 and v > 2]
    if vals and len(off) > len(vals) // 3:
        report("WARN", f"spacing values off the 4px grid: {', '.join(off)}")
    if len(vals) > 12:
        report("INFO", f"{len(vals)} spacing tokens; a small scale (5-10) is easier to apply consistently")
    rd = fm.get("rounded", {})
    rvals = [(k, px(v)) for k, v in rd.items()] if isinstance(rd, dict) else []
    rvals = [(k, v) for k, v in rvals if v is not None]
    distinct = sorted({v for _, v in rvals if v < 999})
    if len(distinct) > 5:
        report("WARN", f"{len(distinct)} distinct radii ({', '.join(f'{d:g}' for d in distinct)}); a family of 2-4 "
                       "with roles reads as deliberate")
    named = {k.lower(): v for k, v in rvals}
    ctrl = next((v for k, v in named.items() if re.search(r"control|button|input|sm", k)), None)
    card = next((v for k, v in named.items() if re.search(r"card|panel|container|lg|sheet", k)), None)
    if ctrl is not None and card is not None and 0 < card < ctrl:
        report("INFO", f"card radius ({card:g}) is below control radius ({ctrl:g}); nested elements usually get the "
                       "smaller radius. Fine if deliberate, but say so in Layout")


def check_components(fm):
    comps = fm.get("components", {})
    if not isinstance(comps, dict):
        return
    kinds = {re.split(r"[-_]", k.lower())[0] for k in comps}
    for need in ("button", "input", "card"):
        if need not in kinds:
            report("INFO", f"no `{need}*` component tokens; add them if the product uses {need}s")
    buttons = [k for k in comps if k.lower().startswith("button")]
    if len(buttons) == 1:
        report("WARN", "only one button variant; define primary, secondary and ghost/tertiary so hierarchy is possible")
    for name, spec in comps.items():
        if not isinstance(spec, dict):
            continue
        h = px(spec.get("height", "")) if spec.get("height") else None
        if h and h < 32 and re.search(r"button|input", name, re.I):
            report("INFO", f"`{name}` height {h:g}px; touch targets need 44pt (iOS) / 48dp (Android), so confirm the hit area")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    fm, body = load(path)
    if not fm:
        sys.exit(f"{path}: no YAML frontmatter found (file must start with ---)")
    check_structure(fm, body)
    check_colors(fm)
    check_type(fm)
    check_spacing_radius(fm)
    check_components(fm)
    for level in ("ERROR", "WARN", "INFO"):
        for m in out[level]:
            print(f"{level:5s} {m}")
    print(f"\n{len(out['ERROR'])} errors, {len(out['WARN'])} warnings, {len(out['INFO'])} info")
    print("\n--- contrast ---", flush=True)
    r = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_contrast.py"), path])
    sys.exit(1 if out["ERROR"] or r.returncode else 0)


if __name__ == "__main__":
    main()
