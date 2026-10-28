"""Shared helpers: parse a design.md (YAML frontmatter + markdown body), colours, WCAG contrast.

Standard library only, so the scripts run anywhere Python 3.8+ exists.
The frontmatter parser covers the subset design.md uses: nested maps of scalar values.
"""
import re

SECTIONS = ["Overview", "Composition", "Colors", "Typography", "Layout",
            "Components", "Graphics & Effects", "Motion", "Guardrails"]


def _scalar(v):
    v = v.strip()
    if v[:1] in ("\"", "'"):
        end = v.find(v[0], 1)
        return v[1:end] if end > 0 else v[1:]
    if " #" in v:
        v = v.split(" #", 1)[0].strip()
    return v


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}, text
    fm, body = parts[0][3:], parts[1].lstrip("-\n")
    root = {}
    stack = [(-1, root)]
    for raw in fm.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        m = re.match(r"\s*([^:]+?):(?:\s+(.*))?$", raw)
        if not m:
            continue
        key, val = _scalar(m.group(1)), m.group(2)
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if val is None or val.strip() == "" or val.strip() == "|":
            parent[key] = {}
            stack.append((indent, parent[key]))
        else:
            parent[key] = _scalar(val)
    return root, body


def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm, body = parse_frontmatter(text)
    return fm, body


def body_sections(body):
    """Map of '## Heading' -> section text."""
    out = {}
    for m in re.finditer(r"^##\s+(.+?)\s*$(.*?)(?=^##\s|\Z)", body, re.M | re.S):
        out[m.group(1).strip()] = m.group(2).strip()
    return out


_HEX = re.compile(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
_RGB = re.compile(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:[\s,/]+([\d.]+%?))?\s*\)")


def parse_color(s):
    """Return (r, g, b, a) floats 0-1, or None."""
    if not isinstance(s, str):
        return None
    m = _HEX.search(s)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (r, g, b, a)
    m = _RGB.search(s)
    if m:
        r, g, b = (float(m.group(i)) / 255 for i in (1, 2, 3))
        a = m.group(4)
        a = 1.0 if a is None else (float(a[:-1]) / 100 if a.endswith("%") else float(a))
        return (r, g, b, a)
    return None


def blend(fg, bg):
    """Composite a translucent colour over an opaque one."""
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def luminance(c):
    def ch(x):
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def to_hex(c):
    return "#" + "".join(f"{round(x * 255):02X}" for x in c[:3])


def px(value):
    """'16px' / '1rem' / '1.5' -> float px (unitless returns the number). None if unparseable."""
    m = re.match(r"\s*(-?[\d.]+)\s*(px|rem|em|pt|dp|sp)?\s*$", str(value))
    if not m:
        return None
    v = float(m.group(1))
    return v * 16 if m.group(2) == "rem" else v


def color_tokens(fm):
    """Yield (theme, key, raw) for the light palette and any dark palette."""
    cols = fm.get("colors", {})
    if not isinstance(cols, dict):
        return
    for k, v in cols.items():
        if isinstance(v, dict):
            if k.lower() in ("dark", "light"):
                for k2, v2 in v.items():
                    if isinstance(v2, str):
                        yield k.lower(), k2, v2
        else:
            yield "light", k, v
    dark = fm.get("dark")
    if isinstance(dark, dict):
        src = dark.get("colors", dark)
        if isinstance(src, dict):
            for k, v in src.items():
                if isinstance(v, str):
                    yield "dark", k, v
