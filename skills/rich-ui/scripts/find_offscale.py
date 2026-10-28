#!/usr/bin/env python3
"""Find raw colours and sizes in source code that are not design tokens.

Usage:
  find_offscale.py design.md src/ [more paths]   # report values not in design.md
  find_offscale.py src/                          # inventory: every raw value with counts
                                                 # (use it to extract a design.md from existing code)
Options:
  --exclude GLOB   skip matching paths (repeatable); theme/token files belong here
  --limit N        max findings printed per category (default 40)
  --strict-literals report recognized raw literals even when their values match tokens

Works on any text source: CSS/SCSS, JS/TS/JSX/TSX, Vue, Svelte, Astro, HTML,
Swift, Kotlin, Java, Dart, XAML, QML, XML. It detects:
  colours  #RGB/#RRGGBB/#RRGGBBAA, rgb()/rgba(), 0xAARRGGBB (Compose/Flutter)
  sizes    12px / 12dp / 12sp / 12pt, Tailwind arbitrary values like p-[13px],
           SwiftUI .padding(13) / cornerRadius: 13
Values of 0, 1 and 2 are ignored (hairlines and resets).
This regex inventory does not understand token references, geometry, or all color
and unit syntaxes. Default mode checks value membership, not token usage.
"""
import argparse
import collections
import fnmatch
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from designmd import load, parse_color, px  # noqa: E402

EXTS = {".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".vue", ".svelte",
        ".astro", ".html", ".swift", ".kt", ".kts", ".java", ".dart", ".xaml", ".qml", ".xml", ".axaml"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit", "Pods", ".gradle",
             "DerivedData", ".dart_tool", "coverage", "vendor", "out", ".turbo", ".output"}

COLOR_RX = re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b"
                      r"|rgba?\(\s*\d[^)]*\)"
                      r"|\b0x[fF]{2}[0-9a-fA-F]{6}\b")
SIZE_RX = re.compile(r"(?<![\w.#-])(\d+(?:\.\d+)?)\.?(px|dp|sp|pt)\b"
                     r"|\[(\d+(?:\.\d+)?)px\]"
                     r"|\.(?:padding|frame|cornerRadius|spacing)\([^)]*?(\d+(?:\.\d+)?)\)"
                     r"|cornerRadius:\s*(\d+(?:\.\d+)?)")


def norm_color(raw):
    if raw.lower().startswith("0x"):
        raw = "#" + raw[4:]
    c = parse_color(raw)
    if not c:
        return None
    key = "#" + "".join(f"{round(x * 255):02X}" for x in c[:3])
    return key + (f"@{c[3]:.2f}" if c[3] < 1 else "")


def collect_tokens(fm):
    colors, sizes = {}, set()

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + [k])
        elif isinstance(node, str):
            for m in COLOR_RX.finditer(node):
                n = norm_color(m.group(0))
                if n:
                    colors.setdefault(n, ".".join(path))
            for part in re.split(r"[\s,/]+", node):
                v = px(part.replace("px", "") if part.endswith("px") else part)
                if v is not None and part.strip() and re.match(r"^-?[\d.]+(px|rem|dp|sp|pt)?$", part.strip()):
                    sizes.add(round(abs(v), 2))
    walk(fm, [])
    return colors, sizes


def nearest(color, palette):
    c = parse_color(color.split("@")[0])
    best, dist = None, 9e9
    for p, name in palette.items():
        q = parse_color(p.split("@")[0])
        d = sum((c[i] - q[i]) ** 2 for i in range(3)) ** 0.5 * 255
        if d < dist:
            best, dist = name, d
    return best, dist


def files(paths, excludes):
    for root in paths:
        if os.path.isfile(root):
            if not any(fnmatch.fnmatch(root, g) for g in excludes):
                yield root
            continue
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            for fn in fns:
                p = os.path.join(dp, fn)
                if os.path.splitext(fn)[1].lower() in EXTS and not any(fnmatch.fnmatch(p, g) for g in excludes):
                    yield p


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--strict-literals", action="store_true")
    a = ap.parse_args()

    design = None
    if a.paths[0].lower().endswith(".md"):
        design, a.paths = a.paths[0], a.paths[1:]
        if not a.paths:
            ap.error("give source paths after design.md")
    if a.strict_literals and not design:
        ap.error('--strict-literals requires a design.md followed by source paths')

    tok_colors, tok_sizes = ({}, set())
    if design:
        fm, _ = load(design)
        tok_colors, tok_sizes = collect_tokens(fm)

    color_hits = collections.defaultdict(list)
    size_hits = collections.defaultdict(list)
    for path in files(a.paths, a.exclude):
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if s.startswith(("//", "/*", "*", "<!--", "#!")) or "url(" in s or "http" in s:
                continue
            for m in COLOR_RX.finditer(line):
                n = norm_color(m.group(0))
                if n:
                    color_hits[n].append(f"{path}:{i}")
            for m in SIZE_RX.finditer(line):
                num = next(g for g in (m.group(1), m.group(3), m.group(4), m.group(5)) if g)
                v = float(num)
                if v <= 2:
                    continue
                size_hits[round(v, 2)].append(f"{path}:{i}")

    if not design:
        print(f"== Colour inventory ({len(color_hits)} distinct)")
        for c, locs in sorted(color_hits.items(), key=lambda kv: -len(kv[1]))[: a.limit]:
            print(f"{len(locs):5d}  {c:14s}  e.g. {locs[0]}")
        print(f"\n== Size inventory ({len(size_hits)} distinct)")
        for v, locs in sorted(size_hits.items(), key=lambda kv: -len(kv[1]))[: a.limit]:
            print(f"{len(locs):5d}  {v:g}  e.g. {locs[0]}")
        print("\nThe most frequent values are the de facto tokens; near-duplicates are cleanup candidates.")
        return

    bad_c = {c: l for c, l in color_hits.items() if a.strict_literals or c not in tok_colors}
    bad_s = {v: l for v, l in size_hits.items() if a.strict_literals or v not in tok_sizes}
    mode = 'raw literals (review geometry exceptions)' if a.strict_literals else f'values not in {design}'
    print(f"== Colours: {mode}: {len(bad_c)} distinct, {sum(map(len, bad_c.values()))} uses")
    for c, locs in sorted(bad_c.items(), key=lambda kv: -len(kv[1]))[: a.limit]:
        name, d = nearest(c, tok_colors) if tok_colors else (None, 0)
        hint = f"  ~ near `{name}` (Δ{d:.0f}), so use the token" if name and d < 24 else "  ~ review token or geometry use"
        print(f"{len(locs):4d}x {c:14s} {locs[0]}{' (+%d more)' % (len(locs) - 1) if len(locs) > 1 else ''}{hint}")
    print(f"\n== Sizes: {mode}: {len(bad_s)} distinct, {sum(map(len, bad_s.values()))} uses")
    for v, locs in sorted(bad_s.items(), key=lambda kv: -len(kv[1]))[: a.limit]:
        close = min(tok_sizes, key=lambda t: abs(t - v)) if tok_sizes else None
        hint = f"  ~ nearest token {close:g}" if close is not None else ""
        print(f"{len(locs):4d}x {v:<8g} {locs[0]}{' (+%d more)' % (len(locs) - 1) if len(locs) > 1 else ''}{hint}")
    print("\nTheme/token definition files will list their own values; pass them with --exclude.")
    sys.exit(1 if bad_c or bad_s else 0)


if __name__ == "__main__":
    main()
