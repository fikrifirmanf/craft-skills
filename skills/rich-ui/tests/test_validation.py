"""Regression coverage for palette checks, literal scans, and compact design docs."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from check_contrast import check_theme
from designmd import SECTIONS


class ValidationTests(unittest.TestCase):
    def run_script(self, script, *args):
        return subprocess.run(
            [sys.executable, '-B', str(SCRIPTS / script), *map(str, args)],
            capture_output=True, text=True, check=False,
        )

    def test_small_muted_text_below_aa_fails(self):
        rows, errors = check_theme('light', {'background': '#FFFFFF', 'text-muted': '#888888'})
        self.assertEqual(errors, 1)
        self.assertEqual(rows[0][0], 'FAIL')
        self.assertAlmostEqual(rows[0][4], 3.544886, places=5)

    def test_valid_text_passes(self):
        rows, errors = check_theme('light', {'background': '#FFFFFF', 'text-secondary': '#525252'})
        self.assertEqual(errors, 0)
        self.assertEqual(rows[0][0], 'ok')

    def test_explicit_pairs_avoid_unused_surface_combinations(self):
        palette = {'background': '#FFFFFF', 'surface-inverse': '#111111', 'text-primary': '#111111'}
        pairs = {'body': {'foreground': 'text-primary', 'background': 'background'}}
        rows, errors = check_theme('light', palette, pairs)
        self.assertEqual(errors, 0)
        self.assertEqual([(row[2], row[3]) for row in rows], [('text-primary', 'background')])

    def test_large_text_and_ui_have_lower_threshold(self):
        palette = {'background': '#FFFFFF', 'text-muted': '#888888'}
        for usage, expected in [('text', 1), ('large-text', 0), ('ui', 0)]:
            with self.subTest(usage=usage):
                rows, errors = check_theme('light', palette, {
                    'pair': {'foreground': 'text-muted', 'background': 'background', 'usage': usage},
                })
                self.assertEqual(errors, expected)
                self.assertEqual(rows[0][0], 'FAIL' if expected else 'ok')

    def test_invalid_explicit_pairs_are_rejected(self):
        palette = {'background': '#FFFFFF', 'text-primary': '#111111', 'overlay': '#FFFFFF80'}
        invalid = [
            {},
            {'body': 'bad'},
            {'body': {'foreground': 'missing', 'background': 'background'}},
            {'body': {'foreground': 'text-primary', 'background': 'missing'}},
            {'body': {'foreground': 'text-primary', 'background': 'background', 'usage': 'muted'}},
            {'body': {'foreground': 'text-primary', 'background': 'overlay'}},
        ]
        for pairs in invalid:
            with self.subTest(pairs=pairs):
                with self.assertRaises(ValueError):
                    check_theme('light', palette, pairs)

    def test_transparent_foreground_is_composited(self):
        rows, errors = check_theme('light', {'background': '#FFFFFF', 'text-primary': '#00000040'}, {
            'body': {'foreground': 'text-primary', 'background': 'background'},
        })
        self.assertEqual(errors, 1)
        self.assertEqual(rows[0][5], '#BFBFBF')

    def test_pair_cli_uses_text_threshold_unless_usage_is_explicit(self):
        normal = self.run_script('check_contrast.py', '--pair', '#888888', '#FFFFFF')
        self.assertEqual(normal.returncode, 1)
        large = self.run_script('check_contrast.py', '--pair', '#888888', '#FFFFFF', '--usage', 'large-text')
        self.assertEqual(large.returncode, 0)

    def test_cli_rejects_missing_pair_tokens(self):
        with tempfile.TemporaryDirectory() as directory:
            design = Path(directory) / 'design.md'
            design.write_text('---\ncolors:\n  background: "#FFFFFF"\ncontrast:\n  body:\n    foreground: missing\n    background: background\n---\n')
            result = self.run_script('check_contrast.py', design)
            self.assertEqual(result.returncode, 1)
            self.assertIn('unknown or invalid foreground', result.stderr)

    def test_dark_overrides_inherit_base_tokens(self):
        with tempfile.TemporaryDirectory() as directory:
            design = Path(directory) / 'design.md'
            design.write_text('---\ncolors:\n  background: "#FFFFFF"\n  text-primary: "#111111"\n  dark:\n    background: "#111111"\n    text-primary: "#FFFFFF"\ncontrast:\n  body:\n    foreground: text-primary\n    background: background\n---\n')
            result = self.run_script('check_contrast.py', design, '--all')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('2 pairs checked: 2 ok', result.stdout)

    def test_partial_dark_palette_inherits_unchanged_roles(self):
        with tempfile.TemporaryDirectory() as directory:
            design = Path(directory) / 'design.md'
            design.write_text('---\ncolors:\n  background: "#FFFFFF"\n  text-primary: "#111111"\n  dark:\n    background: "#EEEEEE"\ncontrast:\n  body:\n    foreground: text-primary\n    background: background\n---\n')
            result = self.run_script('check_contrast.py', design)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('2 pairs checked: 2 ok', result.stdout)

    def test_no_pairs_does_not_report_success(self):
        with tempfile.TemporaryDirectory() as directory:
            design = Path(directory) / 'design.md'
            design.write_text('---\ncolors:\n  decorative: "#FFFFFF"\n---\n')
            result = self.run_script('check_contrast.py', design)
            self.assertEqual(result.returncode, 1)
            self.assertIn('no contrast pairs checked', result.stderr)

    def test_strict_scan_catches_matching_literals_and_honors_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            design = root / 'design.md'
            design.write_text('---\ncolors:\n  background: "#FFFFFF"\nspacing:\n  md: "16px"\n---\n')
            source = root / 'component.css'
            source.write_text('.card { color: #FFFFFF; padding: 16px; }\n')
            inventory = self.run_script('find_offscale.py', design, source)
            self.assertEqual(inventory.returncode, 0, inventory.stdout)
            strict = self.run_script('find_offscale.py', design, source, '--strict-literals')
            self.assertEqual(strict.returncode, 1)
            self.assertIn('#FFFFFF', strict.stdout)
            excluded = self.run_script('find_offscale.py', design, source, '--strict-literals', '--exclude', str(source))
            self.assertEqual(excluded.returncode, 0, excluded.stdout)
            source.write_text('.card { color: var(--text); padding: var(--space); }\n')
            tokens = self.run_script('find_offscale.py', design, source, '--strict-literals')
            self.assertEqual(tokens.returncode, 0, tokens.stdout)

    def test_compact_full_doc_does_not_require_prose_padding(self):
        with tempfile.TemporaryDirectory() as directory:
            design = Path(directory) / 'design.md'
            frontmatter = '---\nname: Compact\ndescription: A compact interface\ncolors:\n  background: "#FFFFFF"\n  text-primary: "#111111"\ntypography:\n  body:\n    fontSize: "16px"\nspacing:\n  base: "4px"\nrounded:\n  control: "8px"\ncomponents:\n  button-primary:\n    height: "44px"\n---\n'
            design.write_text(frontmatter + '\n'.join(f'## {section}\nNone.\n' for section in SECTIONS))
            result = self.run_script('lint_design_md.py', design)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn('too thin', result.stdout)
            self.assertNotIn('only 0 guardrails', result.stdout)


if __name__ == '__main__':
    unittest.main()
