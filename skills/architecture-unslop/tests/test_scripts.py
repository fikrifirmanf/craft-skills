"""Regression coverage for boundary scanning and ADR discovery on disposable projects."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
TEMPLATE = Path(__file__).resolve().parents[1] / 'assets' / 'adr.md.template'


def write(root, files):
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')


class BoundaryTests(unittest.TestCase):
    def check(self, files, *paths):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            write(root, files)
            result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'check_boundaries.py'), *(str(root / p) for p in paths or ['.'])],
                                    capture_output=True, text=True, check=False)
        rules = [line.split()[1] for line in result.stdout.splitlines() if line.startswith('ERROR')]
        return result, rules

    def test_clean_hexagonal_typescript_slice_passes(self):
        result, rules = self.check({
            'src/modules/orders/domain/order.ts': "import { Money } from './money';\nimport type { OrderPlaced } from './order-events';\n",
            'src/modules/orders/domain/money.ts': 'export class Money {}\n',
            'src/modules/orders/application/place-order.ts': "import { Order } from '../domain/order';\n",
            'src/modules/orders/adapters/out/postgres/repo.ts': "import type { Pool } from 'pg';\nimport { Order } from '../../../domain/order';\n",
        })
        self.assertEqual(rules, [])
        self.assertIn('status: PASS', result.stdout)
        self.assertEqual(result.returncode, 0)

    def test_typescript_domain_importing_adapter_and_pg_fails(self):
        result, rules = self.check({
            'src/modules/orders/domain/order.ts': (
                "import { Pool } from 'pg';\n"
                "import {\n  PostgresOrderRepository,\n} from '../adapters/out/postgres/repo';\n"
            ),
        })
        self.assertEqual(rules, ['DOMAIN_IMPORTS_INFRA_LIB', 'DOMAIN_IMPORTS_OUTER'])
        self.assertIn('order.ts:4 ', result.stdout)
        self.assertEqual(result.returncode, 1)

    def test_application_importing_adapter_fails(self):
        _, rules = self.check({
            'src/orders/application/place_order.py': 'from ..infrastructure.sql_repo import SqlOrderRepository\n',
        })
        self.assertEqual(rules, ['APPLICATION_IMPORTS_ADAPTER'])

    def test_python_relative_and_absolute_imports(self):
        _, rules = self.check({
            'app/modules/orders/domain/order.py': (
                'from . import money\n'
                'from .events import OrderPlaced\n'
                'import sqlalchemy, decimal\n'
                'from app.modules.billing.domain.invoice import Invoice\n'
            ),
        })
        self.assertEqual(rules, ['CROSS_CONTEXT_INTERNALS', 'DOMAIN_IMPORTS_INFRA_LIB'])

    def test_cross_context_public_entry_is_allowed(self):
        _, rules = self.check({
            'src/modules/orders/application/place-order.ts': (
                "import { billing } from '../../billing';\n"
                "import { charge } from '../../billing/index.js';\n"
                "import { Invoice } from '../../billing/domain/invoice';\n"
            ),
        })
        self.assertEqual(rules, ['CROSS_CONTEXT_INTERNALS'])

    def test_go_import_block_and_alias(self):
        result, rules = self.check({
            'internal/orders/domain/order.go': (
                'package domain\n\nimport (\n\t"errors"\n\t"time"\n\n\tsq "database/sql"\n'
                '\t"example.com/shop/internal/orders/adapters/postgres"\n)\n'
            ),
        })
        self.assertEqual(rules, ['DOMAIN_IMPORTS_INFRA_LIB', 'DOMAIN_IMPORTS_OUTER'])
        self.assertIn('order.go:7 ', result.stdout)

    def test_java_public_api_package_allowed_but_internals_flagged(self):
        _, rules = self.check({
            'src/main/java/com/shop/modules/orders/domain/Order.java': (
                'package com.shop.modules.orders.domain;\n'
                'import java.util.List;\n'
                'import jakarta.persistence.Entity;\n'
                'import com.shop.modules.billing.api.BillingApi;\n'
                'import com.shop.modules.billing.domain.Invoice;\n'
            ),
        })
        self.assertEqual(rules, ['DOMAIN_IMPORTS_INFRA_LIB', 'CROSS_CONTEXT_INTERNALS'])

    def test_library_path_containing_layer_word_is_not_a_layer(self):
        _, rules = self.check({
            'src/main/kotlin/shop/orders/domain/Order.kt': 'import io.ktor.server.application.Application\n',
        })
        self.assertEqual(rules, ['DOMAIN_IMPORTS_INFRA_LIB'])

    def test_rust_csharp_php_and_ruby_domain_leaks(self):
        _, rules = self.check({
            'src/orders/domain/order.rs': 'use std::fmt;\nuse sqlx::PgPool;\nuse crate::orders::adapters::pg::Repo;\n',
            'Shop/Orders/Domain/Order.cs': 'using System;\nusing Microsoft.EntityFrameworkCore;\n',
            'src/Orders/Domain/Order.php': "<?php\nnamespace App\\Orders\\Domain;\nuse Illuminate\\Database\\Eloquent\\Model;\n",
            'lib/orders/domain/order.rb': "require 'bigdecimal'\nclass Order < ApplicationRecord\nend\n",
        })
        self.assertEqual(sorted(rules), sorted([
            'DOMAIN_IMPORTS_INFRA_LIB', 'DOMAIN_IMPORTS_OUTER',
            'DOMAIN_IMPORTS_INFRA_LIB', 'DOMAIN_IMPORTS_INFRA_LIB', 'DOMAIN_IMPORTS_INFRA_LIB',
        ]))

    def test_suppression_needs_a_reason(self):
        _, rules = self.check({
            'src/orders/domain/clock.ts': (
                "// unslop-ignore DOMAIN_IMPORTS_INFRA_LIB -- reads a bundled fixture at build time only\n"
                "import { readFileSync } from 'node:fs';\n"
                "import http from 'node:http'; // unslop-ignore DOMAIN_IMPORTS_INFRA_LIB\n"
            ),
        })
        self.assertEqual(rules, ['SUPPRESSION_WITHOUT_REASON'])

    def test_test_files_are_not_scanned(self):
        result, rules = self.check({
            'src/orders/domain/order.ts': 'export class Order {}\n',
            'src/orders/domain/order.test.ts': "import { Pool } from 'pg';\n",
            'tests/orders/domain/order_test.py': 'import sqlalchemy\n',
        })
        self.assertEqual(rules, [])
        self.assertIn('status: PASS', result.stdout)

    def test_unstructured_project_is_skipped_not_passed(self):
        result, rules = self.check({'src/server.ts': "import express from 'express';\n"})
        self.assertEqual(rules, [])
        self.assertIn('status: SKIPPED', result.stdout)

    def test_single_file_argument_keeps_its_layer(self):
        _, rules = self.check({'src/orders/domain/order.ts': "import { Pool } from 'pg';\n"}, 'src/orders/domain/order.ts')
        self.assertEqual(rules, ['DOMAIN_IMPORTS_INFRA_LIB'])


class FindAdrTests(unittest.TestCase):
    def find(self, files):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            write(root, files)
            result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'find_adr.py'), str(root)],
                                    capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def adr(self, status, base, addons='none'):
        return (
            '<!-- architecture-unslop -->\n# ADR: Architecture\n\n'
            '- Status: {}\n- Date: 2026-10-31\n\n## Decision\n\n| Key | Value |\n|---|---|\n'
            '| base | {} |\n| modeling | ddd-tactical |\n| addons | {} |\n| stack | typescript |\n| framework | none |\n'
        ).format(status, base, addons)

    def test_no_adr_suggests_docs_adr(self):
        result = self.find({'README.md': '# Shop\n'})
        self.assertFalse(result['found'])
        self.assertIsNone(result['active'])
        self.assertEqual(result['suggested_path'], 'docs/adr/0001-architecture.md')

    def test_existing_adr_folder_gets_next_number(self):
        result = self.find({'doc/adr/0001-record-decisions.md': '# Record\n', 'doc/adr/0002-use-postgres.md': '# PG\n'})
        self.assertEqual(result['suggested_path'], 'doc/adr/0003-architecture.md')

    def test_active_decision_is_parsed_and_superseded_is_separated(self):
        result = self.find({
            'docs/adr/0001-architecture.md': self.adr('Superseded by ADR-0002', 'layered-mvc'),
            'docs/adr/0002-architecture.md': self.adr('Accepted', 'hexagonal', 'cqrs:orders, event-driven'),
        })
        self.assertTrue(result['found'])
        self.assertEqual(result['active']['path'], 'docs/adr/0002-architecture.md')
        self.assertEqual(result['active']['base'], 'hexagonal')
        self.assertEqual(result['active']['addons'], ['cqrs:orders', 'event-driven'])
        self.assertEqual(result['superseded'], ['docs/adr/0001-architecture.md'])
        self.assertEqual(result['conflicts'], [])
        self.assertEqual(result['suggested_path'], 'docs/adr/0003-architecture.md')

    def test_two_accepted_adrs_are_reported_as_conflict(self):
        result = self.find({
            'docs/adr/0001-architecture.md': self.adr('Accepted', 'layered-mvc'),
            'docs/adr/0002-architecture.md': self.adr('Accepted', 'hexagonal'),
        })
        self.assertEqual(result['active']['base'], 'hexagonal')
        self.assertEqual(result['conflicts'], ['docs/adr/0001-architecture.md'])

    def test_unrelated_adrs_and_dependency_folders_are_ignored(self):
        result = self.find({
            'docs/adr/0001-use-postgres.md': '# Use Postgres\n\n- Status: Accepted\n',
            'node_modules/pkg/docs/adr/0001-architecture.md': self.adr('Accepted', 'microservices'),
        })
        self.assertFalse(result['found'])

    def test_template_parses_once_filled(self):
        text = TEMPLATE.read_text(encoding='utf-8')
        for placeholder, value in {
            '{{number}}': '0001', '{{project}}': 'Shop', '{{date}}': '2026-10-31', '{{supersedes}}': 'none',
            '{{base}}': 'hexagonal', '{{modeling}}': 'ddd-tactical', '{{addons}}': 'none',
            '{{stack}}': 'go', '{{framework}}': 'none',
        }.items():
            text = text.replace(placeholder, value)
        result = self.find({'docs/adr/0001-architecture.md': text})
        self.assertEqual(result['active']['status'], 'Accepted')
        self.assertEqual(result['active']['stack'], 'go')
        self.assertEqual(result['active']['addons'], [])


if __name__ == '__main__':
    unittest.main()
