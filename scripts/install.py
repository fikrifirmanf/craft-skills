#!/usr/bin/env python3
"""Copy selected skills into an agent's skill directory with recoverable updates."""
import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path
from uuid import uuid4

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / 'skills'
EXCLUDED = shutil.ignore_patterns('evals', 'tests', '__pycache__', '*.pyc', '.DS_Store', '.git', '.pytest_cache')


def discover_skills():
    skills = {}
    for path in sorted(SKILLS_ROOT.iterdir()):
        if not path.is_dir() or not (path / 'SKILL.md').is_file():
            continue
        header = (path / 'SKILL.md').read_text(encoding='utf-8').split('---', 2)
        if len(header) != 3 or header[0].strip():
            raise ValueError('Missing frontmatter: ' + str(path / 'SKILL.md'))
        name = re.search(r'^name:\s*([a-z0-9-]+)\s*$', header[1], re.MULTILINE)
        if not name or name.group(1) != path.name:
            raise ValueError('Skill name must match its folder: ' + str(path))
        skills[path.name] = path
    if not skills:
        raise ValueError('No skills found in ' + str(SKILLS_ROOT))
    return skills


def destination_roots(target, directory):
    if directory:
        roots = [Path(directory).expanduser().resolve()]
    else:
        home = Path.home()
        shared = home / '.agents' / 'skills'
        claude = home / '.claude' / 'skills'
        roots = [shared, claude] if target == 'all' else [claude if target == 'claude' else shared]
    source_root = SKILLS_ROOT.resolve()
    for root in roots:
        resolved = root.resolve()
        if resolved == source_root or source_root in resolved.parents or resolved in source_root.parents:
            raise ValueError('Destination must not overlap the repository skills directory: ' + str(root))
    return roots


def exists(path):
    return path.exists() or path.is_symlink()


def install_one(source, destination, force=False):
    if exists(destination) and not force:
        raise FileExistsError('Already exists: ' + str(destination))
    destination.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    with tempfile.TemporaryDirectory(prefix='.craft-skills-stage-', dir=str(destination.parent)) as staging:
        staged = Path(staging) / source.name
        shutil.copytree(source, staged, ignore=EXCLUDED)
        if exists(destination):
            backup = destination.parent.parent / '.craft-skills-backups' / uuid4().hex / destination.name
            backup.parent.mkdir(parents=True, exist_ok=True)
            destination.rename(backup)
        try:
            staged.rename(destination)
        except OSError:
            if backup is not None and not exists(destination):
                backup.rename(destination)
            raise
    return backup


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    targets = parser.add_mutually_exclusive_group()
    targets.add_argument('--target', choices=('agents', 'codex', 'claude', 'all'), default='agents',
                         help='agents/codex: shared skills; claude: Claude Code; all: both (default: agents)')
    targets.add_argument('--dir', help='custom destination skills directory; supports project-local installs')
    parser.add_argument('--skill', action='append', dest='selected', metavar='NAME',
                        help='install only this skill; repeat to select several (default: all)')
    parser.add_argument('--list', action='store_true', help='list available skills and exit')
    parser.add_argument('--dry-run', action='store_true', help='show the plan without creating files')
    parser.add_argument('--force', action='store_true', help='back up and replace existing selected skill folders')
    args = parser.parse_args(argv)
    try:
        skills = discover_skills()
        if args.list:
            print('\n'.join(skills))
            return 0
        names = list(dict.fromkeys(args.selected or skills))
        unknown = [name for name in names if name not in skills]
        if unknown:
            parser.error('Unknown skill: ' + ', '.join(unknown) + '. Use --list to see available skills.')
        roots = destination_roots(args.target, args.dir)
        plan = [(skills[name], root / name) for root in roots for name in names]
        conflicts = [str(destination) for _, destination in plan if exists(destination)]
        if conflicts and not args.force and not args.dry_run:
            parser.error('Existing skill folders need --force for a backed-up update:\n' + '\n'.join(conflicts))
        if args.dry_run:
            for source, destination in plan:
                action = ('Back up and replace' if args.force else 'Exists (needs --force)') if exists(destination) else 'Install'
                print(action + ': ' + str(source) + ' -> ' + str(destination))
            return 0
        for source, destination in plan:
            backup = install_one(source, destination, args.force)
            print('Installed: ' + str(destination))
            if backup:
                print('Backup: ' + str(backup))
        print('Installed ' + str(len(plan)) + ' skill copies. Start a new agent session to load them.')
        return 0
    except (OSError, ValueError) as error:
        print('Install failed: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
