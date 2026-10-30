#!/usr/bin/env python3
"""Find the active architecture ADR written by this skill and print it as JSON.

Usage: find_adr.py [REPO_ROOT]

Prints {"found": bool, "active": {...} | null, "superseded": [...], "conflicts": [...],
"suggested_path": "..."}. "conflicts" lists extra Accepted ADRs when more than one is active.
"""
import json
import re
import sys
from pathlib import Path

MARKER = '<!-- architecture-unslop -->'
ADR_DIRS = ('docs/adr', 'doc/adr', 'docs/decisions', 'docs/architecture/decisions', 'adr', 'decisions')
SKIP_DIRS = {'.git', 'node_modules', 'vendor', 'dist', 'build', 'target', '.venv', 'venv', '__pycache__',
             'bin', 'obj', '.next', 'coverage', '.idea', '.vscode'}
MAX_DEPTH = 5
DECISION_KEYS = ('base', 'modeling', 'addons', 'stack', 'framework')
NUMBERED = re.compile(r'^(\d{4})-.*\.md$')


def candidate_files(root):
    stack = [(root, 0)]
    while stack:
        folder, depth = stack.pop()
        try:
            entries = sorted(folder.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                if entry.name not in SKIP_DIRS and depth < MAX_DEPTH:
                    stack.append((entry, depth + 1))
            elif entry.suffix == '.md':
                yield entry


def parse_adr(path):
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return None
    if MARKER not in text[:500]:
        return None
    status = re.search(r'^\s*-\s*Status:\s*(.+?)\s*$', text, re.MULTILINE)
    decision = {}
    for key, value in re.findall(r'^\|\s*([a-z]+)\s*\|\s*(.*?)\s*\|\s*$', text, re.MULTILINE):
        if key in DECISION_KEYS:
            decision[key] = value
    addons = decision.get('addons', '')
    return {
        'status': status.group(1) if status else 'Unknown',
        'base': decision.get('base', ''),
        'modeling': decision.get('modeling', ''),
        'addons': [] if addons.lower() in ('', 'none', '-') else [a.strip() for a in addons.split(',') if a.strip()],
        'stack': decision.get('stack', ''),
        'framework': decision.get('framework', ''),
    }


def suggested_path(root):
    for relative in ADR_DIRS:
        folder = root / relative
        if folder.is_dir():
            numbers = [int(m.group(1)) for p in folder.iterdir() if (m := NUMBERED.match(p.name))]
            return str(Path(relative) / '{:04d}-architecture.md'.format(max(numbers, default=0) + 1))
    return str(Path('docs/adr/0001-architecture.md'))


def find(root):
    active, superseded = [], []
    for path in candidate_files(root):
        adr = parse_adr(path)
        if adr is None:
            continue
        adr['path'] = str(path.relative_to(root))
        (active if adr['status'].lower().startswith('accepted') else superseded).append(adr)
    active.sort(key=lambda a: a['path'])
    return {
        'found': bool(active),
        'active': active[-1] if active else None,
        'conflicts': [a['path'] for a in active[:-1]],
        'superseded': [a['path'] for a in superseded],
        'suggested_path': suggested_path(root),
    }


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else '.').resolve()
    if not root.is_dir():
        print('Not a directory: ' + str(root), file=sys.stderr)
        return 2
    print(json.dumps(find(root), indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
