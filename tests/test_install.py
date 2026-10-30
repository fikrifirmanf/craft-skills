"""Exercise installation against disposable destinations, never personal skills."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('craft_install', ROOT / 'scripts' / 'install.py')
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)
NAMES = {'architecture-unslop', 'backend-unslop', 'copy-unslop', 'frontend-unslop', 'mobile-unslop', 'motion-graphic-design', 'rich-ui', 'test-unslop', 'ui-unslop'}


class InstallerTests(unittest.TestCase):
    def run_installer(self, *args):
        return subprocess.run([sys.executable, '-B', str(ROOT / 'scripts' / 'install.py'), *map(str, args)],
                              capture_output=True, text=True, check=False)

    def test_lists_all_skills(self):
        result = self.run_installer('--list')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(result.stdout.splitlines()), NAMES)

    def test_installs_all_skills_and_runtime_assets_only(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'skills'
            result = self.run_installer('--dir', destination)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({path.name for path in destination.iterdir()}, NAMES)
            for name in NAMES:
                self.assertEqual((destination / name / 'SKILL.md').read_bytes(), (ROOT / 'skills' / name / 'SKILL.md').read_bytes())
            self.assertTrue((destination / 'rich-ui' / 'scripts' / 'check_contrast.py').is_file())
            self.assertTrue((destination / 'rich-ui' / 'assets' / 'design.md.template').is_file())
            for relative in (
                'agents/openai.yaml',
                'references/choreography.md',
                'references/prompt-patterns.md',
                'references/runtime-and-delivery.md',
                'references/sources.md',
                'references/three-dimensional.md',
            ):
                with self.subTest(motion_resource=relative):
                    self.assertEqual(
                        (destination / 'motion-graphic-design' / relative).read_bytes(),
                        (ROOT / 'skills' / 'motion-graphic-design' / relative).read_bytes(),
                    )
            for relative in (
                'scripts/check_boundaries.py',
                'scripts/find_adr.py',
                'assets/adr.md.template',
                'references/picker.md',
                'references/base/hexagonal.md',
                'references/stacks/go.md',
            ):
                with self.subTest(architecture_resource=relative):
                    self.assertTrue((destination / 'architecture-unslop' / relative).is_file())
            self.assertFalse((destination / 'architecture-unslop' / 'evals').exists())
            self.assertFalse((destination / 'architecture-unslop' / 'tests').exists())
            self.assertFalse((destination / 'rich-ui' / 'evals').exists())
            self.assertFalse((destination / 'rich-ui' / 'tests').exists())
            self.assertFalse(list(destination.rglob('__pycache__')))

    def test_selects_and_deduplicates_skills(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'skills'
            result = self.run_installer('--dir', destination, '--skill', 'rich-ui', '--skill', 'rich-ui', '--skill', 'copy-unslop')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({path.name for path in destination.iterdir()}, {'rich-ui', 'copy-unslop'})

    def test_dry_run_creates_no_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'nested' / 'skills'
            result = self.run_installer('--dir', destination, '--dry-run')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(destination.parent.exists())
            self.assertIn('Install:', result.stdout)

    def test_unknown_skill_fails_before_any_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'skills'
            result = self.run_installer('--dir', destination, '--skill', '../escape')
            self.assertEqual(result.returncode, 2)
            self.assertIn('Unknown skill', result.stderr)
            self.assertFalse(destination.exists())

    def test_conflict_fails_before_installing_other_skills(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'skills'
            old = destination / 'ui-unslop'
            old.mkdir(parents=True)
            (old / 'personal.txt').write_text('Keep this customization')
            result = self.run_installer('--dir', destination)
            self.assertEqual(result.returncode, 2)
            self.assertEqual({path.name for path in destination.iterdir()}, {'ui-unslop'})
            self.assertEqual((old / 'personal.txt').read_text(), 'Keep this customization')

    def test_force_keeps_original_in_backup_and_replaces_complete_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'skills'
            old = destination / 'rich-ui'
            old.mkdir(parents=True)
            (old / 'personal.txt').write_text('Original customization')
            result = self.run_installer('--dir', destination, '--skill', 'rich-ui', '--force')
            self.assertEqual(result.returncode, 0, result.stderr)
            backups = list((Path(folder) / '.craft-skills-backups').glob('*/rich-ui/personal.txt'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), 'Original customization')
            self.assertFalse((old / 'personal.txt').exists())
            self.assertEqual((old / 'SKILL.md').read_bytes(), (ROOT / 'skills' / 'rich-ui' / 'SKILL.md').read_bytes())
            self.assertFalse(list(destination.glob('.craft-skills-stage-*')))

    def test_dry_run_conflict_does_not_move_existing_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'skills'
            (destination / 'rich-ui').mkdir(parents=True)
            result = self.run_installer('--dir', destination, '--skill', 'rich-ui', '--dry-run')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('needs --force', result.stdout)
            self.assertFalse((Path(folder) / '.craft-skills-backups').exists())
            self.assertEqual({path.name for path in destination.iterdir()}, {'rich-ui'})

    def test_source_overlap_is_rejected(self):
        for directory in [ROOT / 'skills', ROOT / 'skills' / 'rich-ui', ROOT]:
            with self.subTest(directory=directory):
                result = self.run_installer('--dir', directory, '--skill', 'rich-ui', '--force')
                self.assertEqual(result.returncode, 1)
                self.assertIn('must not overlap', result.stderr)

    def test_copy_failure_keeps_existing_install_untouched(self):
        with tempfile.TemporaryDirectory() as folder:
            old = Path(folder) / 'skills' / 'rich-ui'
            old.mkdir(parents=True)
            (old / 'personal.txt').write_text('Keep me')
            with patch.object(INSTALLER.shutil, 'copytree', side_effect=OSError('disk full')):
                with self.assertRaisesRegex(OSError, 'disk full'):
                    INSTALLER.install_one(ROOT / 'skills' / 'rich-ui', old, force=True)
            self.assertEqual((old / 'personal.txt').read_text(), 'Keep me')
            self.assertFalse((Path(folder) / '.craft-skills-backups').exists())
            self.assertFalse(list(old.parent.glob('.craft-skills-stage-*')))

    def test_publish_failure_restores_previous_install(self):
        with tempfile.TemporaryDirectory() as folder:
            old = Path(folder) / 'skills' / 'rich-ui'
            old.mkdir(parents=True)
            (old / 'personal.txt').write_text('Restore this')
            original_rename = Path.rename

            def fail_staged_rename(path, target):
                if path.parent.name.startswith('.craft-skills-stage-'):
                    raise OSError('cannot publish staged copy')
                return original_rename(path, target)

            with patch.object(Path, 'rename', fail_staged_rename):
                with self.assertRaisesRegex(OSError, 'cannot publish'):
                    INSTALLER.install_one(ROOT / 'skills' / 'rich-ui', old, force=True)
            self.assertEqual((old / 'personal.txt').read_text(), 'Restore this')
            self.assertFalse((old / 'SKILL.md').exists())

    def test_force_moves_symlink_without_writing_into_its_target(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            external = root / 'external'
            external.mkdir()
            (external / 'personal.txt').write_text('External data')
            destination = root / 'skills'
            destination.mkdir()
            (destination / 'rich-ui').symlink_to(external, target_is_directory=True)
            result = self.run_installer('--dir', destination, '--skill', 'rich-ui', '--force')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((destination / 'rich-ui').is_symlink())
            self.assertEqual((external / 'personal.txt').read_text(), 'External data')
            backups = list((root / '.craft-skills-backups').glob('*/rich-ui'))
            self.assertEqual(len(backups), 1)
            self.assertTrue(backups[0].is_symlink())

    def test_shell_entrypoint_handles_checkout_path_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix='craft skills ') as folder:
            checkout = Path(folder) / 'repo with spaces'
            checkout.mkdir()
            (checkout / 'scripts').mkdir()
            (checkout / 'skills').symlink_to(ROOT / 'skills', target_is_directory=True)
            import shutil
            shutil.copy2(ROOT / 'install.sh', checkout / 'install.sh')
            shutil.copy2(ROOT / 'scripts' / 'install.py', checkout / 'scripts' / 'install.py')
            result = subprocess.run(['bash', str(checkout / 'install.sh'), '--dir', str(Path(folder) / 'installed skills'), '--skill', 'copy-unslop'],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((Path(folder) / 'installed skills' / 'copy-unslop' / 'SKILL.md').read_bytes(),
                             (ROOT / 'skills' / 'copy-unslop' / 'SKILL.md').read_bytes())


if __name__ == '__main__':
    unittest.main()
