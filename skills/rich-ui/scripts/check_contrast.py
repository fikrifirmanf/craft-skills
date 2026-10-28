#!/usr/bin/env python3
"""Check declared contrast pairs, or infer candidate pairs from token names.

Usage:
  check_contrast.py design.md            # check all role pairs, light and dark
  check_contrast.py --pair "#71717A" "#0A0A0A" [--usage text|large-text|ui]

Pairs are inferred from token names:
  text-*, ink-*, foreground, link      vs every surface   needs 4.5:1
  text-tertiary / muted / placeholder  vs every surface   needs 4.5:1
  accent / primary / brand / focus     vs every surface   3:1 (non-text UI); flagged if < 4.5 for text use
  on-X                                 vs X               4.5:1
  *-inverse / *-dark / *-deep / *-band   pair only with each other (name inverted bands this way)
An optional `contrast` map declares foreground/background token keys and usage
(text, large-text, ui). It replaces inferred pairs. See design-md-format.md.
This is a palette check, not a rendered accessibility audit.
Exit code 1 if any pair fails its threshold or explicit configuration is invalid.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from designmd import blend, color_tokens, contrast, load, parse_color, to_hex  # noqa: E402

BG = re.compile(r"^(background|bg|canvas|field|page|base|ground)$|^(surface|bg-|background-|canvas-|panel|card)")
TEXT = re.compile(r"(^|-)(text|ink|foreground|fg|link|heading|body)(-|$)")
SKIP = re.compile(r"disabled|shadow|overlay|scrim|glass|gradient|wash|glow")
ACCENTISH = re.compile(r"^(accent|primary|brand|focus|ring|link)")
INVERSE = re.compile(r"inverse|dark|night|deep|band|footer")
TINT = re.compile(r"soft|tint|subtle|wash|bg|background|surface|muted|light")


def classify(key):
    k = key.lower()
    if SKIP.search(k):
        return None
    if k.startswith("on-"):
        return "on"
    if BG.search(k) and not TEXT.search(k):
        return "bg"
    if TEXT.search(k):
        return "text"
    if ACCENTISH.search(k) and not TINT.search(k):
        return "accent"
    return None


def check_theme(name, tokens, pair_specs=None):
    rows, errors = [], 0
    parsed = {k: parse_color(v) for k, v in tokens.items()}
    parsed = {k: v for k, v in parsed.items() if v}
    base = next((parsed[k] for k in parsed if k.lower() in ("background", "bg", "canvas", "page")), None)
    if base is None:
        base = (1, 1, 1, 1) if name == "light" else (0, 0, 0, 1)
    base = base[:3] + (1.0,) if base[3] >= 1 else blend(base, (1, 1, 1, 1))

    def solid(c, under):
        return c if c[3] >= 1 else blend(c, under)

    if pair_specs is not None:
        if not isinstance(pair_specs, dict) or not pair_specs:
            raise ValueError('contrast must be a nonempty map of named pairs')
        for label, spec in pair_specs.items():
            if not isinstance(spec, dict):
                raise ValueError(f'contrast.{label} must be a map')
            fk, bk = spec.get('foreground'), spec.get('background')
            if not isinstance(fk, str) or fk not in parsed:
                raise ValueError(f'[{name}] contrast.{label}: unknown or invalid foreground {fk!r}')
            if not isinstance(bk, str) or bk not in parsed:
                raise ValueError(f'[{name}] contrast.{label}: unknown or invalid background {bk!r}')
            usage = spec.get('usage', 'text')
            if not isinstance(usage, str) or usage not in ('text', 'large-text', 'ui'):
                raise ValueError(f'contrast.{label}: usage must be text, large-text, or ui')
            if parsed[bk][3] < 1:
                raise ValueError(f'[{name}] contrast.{label}: background must be opaque; supply its composite color')
            need = 4.5 if usage == 'text' else 3.0
            fc, bc = solid(parsed[fk], parsed[bk]), parsed[bk]
            ratio = contrast(fc, bc)
            status = 'FAIL' if ratio < need else 'ok'
            errors += status == 'FAIL'
            rows.append((status, name, fk, bk, ratio, to_hex(fc), to_hex(bc)))
        return rows, errors

    bgs = {k: solid(v, base) for k, v in parsed.items() if classify(k) == "bg"}
    for fk, fc in parsed.items():
        kind = classify(fk)
        if kind in (None, "bg"):
            continue
        if kind == "on":
            target = fk[3:]
            match = next((k for k in parsed if k.lower() == target.lower()), None)
            if not match:
                continue
            pairs = [(match, solid(parsed[match], base))]
            need_hard, need_soft = 4.5, 4.5
        else:
            inverse_text = bool(INVERSE.search(fk.lower()))
            pairs = [(bk, bc) for bk, bc in bgs.items() if bool(INVERSE.search(bk.lower())) == inverse_text]
            if kind == "text":
                need_hard, need_soft = 4.5, 4.5
            else:
                need_hard, need_soft = 3.0, 4.5
        for bk, bc in pairs:
            ratio = contrast(solid(fc, bc), bc)
            if ratio < need_hard:
                status = "FAIL"
                errors += 1
            elif ratio < need_soft:
                status = "WARN" if kind == "text" else "UI-ONLY"
            else:
                status = "ok"
            rows.append((status, name, fk, bk, ratio, to_hex(solid(fc, bc)), to_hex(bc)))
    return rows, errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("design_md", nargs="?")
    ap.add_argument("--pair", nargs=2, metavar=("FG", "BG"))
    ap.add_argument("--all", action="store_true", help="also print passing pairs")
    ap.add_argument("--usage", choices=("text", "large-text", "ui"), default="text",
                    help="threshold for --pair (default: text, 4.5:1)")
    a = ap.parse_args()

    if a.pair:
        fg, bg = parse_color(a.pair[0]), parse_color(a.pair[1])
        if not fg or not bg:
            sys.exit("could not parse colours")
        r = contrast(fg if fg[3] >= 1 else blend(fg, bg), bg)
        verdict = "AAA" if r >= 7 else "AA" if r >= 4.5 else "AA-large/UI" if r >= 3 else "FAIL"
        print(f"{r:.2f}:1  {verdict}")
        threshold = 4.5 if a.usage == "text" else 3.0
        sys.exit(1 if r < threshold else 0)
    if not a.design_md:
        ap.error("give a design.md path or --pair FG BG")

    fm, _ = load(a.design_md)
    themes = {}
    for theme, k, v in color_tokens(fm):
        themes.setdefault(theme, {})[k] = v
    if not themes:
        sys.exit("no colors found in frontmatter")

    all_rows, errors = [], 0
    pair_specs = fm.get('contrast') if 'contrast' in fm else None
    if 'contrast' in fm and (not isinstance(pair_specs, dict) or not pair_specs):
        sys.exit('contrast must be a nonempty map of named pairs')
    try:
        for name, toks in themes.items():
            palette = {**themes.get('light', {}), **toks}
            rows, e = check_theme(name, palette, pair_specs)
            all_rows += rows
            errors += e
    except ValueError as exc:
        sys.exit(str(exc))
    if not all_rows:
        sys.exit('no contrast pairs checked; declare explicit contrast pairs')
    print('Mode: explicit pairs' if pair_specs is not None else 'Mode: inferred pairs (verify actual rendered uses)')

    order = {"FAIL": 0, "WARN": 1, "UI-ONLY": 2, "ok": 3}
    all_rows.sort(key=lambda r: (order[r[0]], r[1], r[2]))
    shown = [r for r in all_rows if a.all or r[0] != "ok"]
    for st, theme, fk, bk, ratio, fh, bh in shown:
        print(f"{st:8s} [{theme}] {fk:22s} on {bk:20s} {ratio:5.2f}:1   {fh} on {bh}")
    passed = sum(1 for r in all_rows if r[0] == "ok")
    print(f"\n{len(all_rows)} pairs checked: {passed} ok, "
          f"{sum(r[0] == 'WARN' for r in all_rows)} warn, "
          f"{sum(r[0] == 'UI-ONLY' for r in all_rows)} ui-only (fine for fills/icons/borders, too low for small text), "
          f"{errors} fail")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
