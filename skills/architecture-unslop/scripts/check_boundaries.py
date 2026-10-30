#!/usr/bin/env python3
"""Scan source imports for architecture boundary violations.

Usage: check_boundaries.py [SOURCE_ROOT ...]

Rules (all ERROR):
  DOMAIN_IMPORTS_OUTER         domain code imports the application or adapter layer
  APPLICATION_IMPORTS_ADAPTER  application code imports the adapter layer
  DOMAIN_IMPORTS_INFRA_LIB     domain code imports a database, HTTP, queue or framework library
  CROSS_CONTEXT_INTERNALS      one module/context/slice imports another one's internals
  SUPPRESSION_WITHOUT_REASON   an unslop-ignore comment has no "-- reason"

Layers and contexts are recognised by folder names. Test files are not scanned.
Suppress a verified false positive on the line or the line above:
  unslop-ignore RULE_ID -- why this is safe

Exit codes: 0 PASS or SKIPPED, 1 FAIL, 2 usage error. SKIPPED means no layer or
context folders were found, so nothing was verified.
"""
import posixpath
import re
import sys
from pathlib import Path

DOMAIN = {'domain', 'entities'}
APPLICATION = {'application', 'usecases', 'use_cases', 'use-cases'}
ADAPTER = {'adapters', 'adapter', 'infrastructure', 'infra', 'persistence', 'presentation', 'controllers'}
CONTEXT_PARENTS = {'modules', 'contexts', 'bounded_contexts', 'bounded-contexts', 'features', 'slices'}
PUBLIC_ENTRIES = {'index', '__init__', 'api', 'public', 'contracts', 'mod', 'lib'}
SKIP_DIRS = {'.git', 'node_modules', 'vendor', 'dist', 'build', 'target', '.venv', 'venv', '__pycache__',
             'bin', 'obj', '.next', 'coverage', 'tests', 'test', '__tests__', 'spec', 'specs', 'testdata'}
TEST_FILE = re.compile(r'(\.(test|spec)\.[a-z]+$|_test\.(go|py|rb)$|^test_.*\.py$|(Test|Tests)\.(java|kt|cs)$|_spec\.rb$)')

LANGUAGES = {
    '.ts': 'js', '.tsx': 'js', '.mts': 'js', '.cts': 'js', '.js': 'js', '.jsx': 'js', '.mjs': 'js', '.cjs': 'js',
    '.py': 'py', '.go': 'go', '.rs': 'rs', '.java': 'jvm', '.kt': 'jvm', '.kts': 'jvm',
    '.cs': 'cs', '.php': 'php', '.rb': 'rb',
}

# A prefix ending in a separator matches by plain prefix; otherwise it matches exactly or followed by a separator.
INFRA_LIBS = {
    'js': ['pg', 'pg-promise', 'mysql', 'mysql2', 'mongodb', 'mongoose', 'typeorm', '@prisma/client', 'prisma',
           'sequelize', 'knex', 'drizzle-orm', 'kysely', 'redis', 'ioredis', 'bullmq', 'bull', 'kafkajs', 'amqplib',
           'express', 'fastify', 'koa', 'hono', '@nestjs/', 'axios', 'node-fetch', 'got', 'undici', '@aws-sdk/',
           'http', 'https', 'net', 'fs', 'child_process', 'node:http', 'node:https', 'node:net', 'node:fs',
           'node:child_process'],
    'py': ['sqlalchemy', 'django', 'flask', 'fastapi', 'starlette', 'psycopg', 'psycopg2', 'asyncpg', 'pymongo',
           'motor', 'redis', 'requests', 'httpx', 'aiohttp', 'boto3', 'botocore', 'celery', 'kafka', 'aiokafka',
           'pika', 'peewee', 'tortoise', 'sqlmodel'],
    'go': ['database/sql', 'net/http', 'github.com/jackc/pgx', 'github.com/lib/pq', 'gorm.io', 'github.com/jmoiron/sqlx',
           'github.com/gin-gonic', 'github.com/labstack/echo', 'github.com/gofiber', 'github.com/go-chi',
           'github.com/redis/go-redis', 'github.com/go-redis', 'go.mongodb.org', 'github.com/aws/aws-sdk-go',
           'github.com/segmentio/kafka-go', 'github.com/rabbitmq'],
    'rs': ['sqlx', 'diesel', 'sea_orm', 'tokio_postgres', 'postgres', 'mongodb', 'redis', 'axum', 'actix_web', 'rocket',
           'warp', 'hyper', 'reqwest', 'rdkafka', 'lapin', 'aws_sdk_'],
    'jvm': ['javax.persistence', 'jakarta.persistence', 'org.springframework', 'org.hibernate', 'java.sql', 'javax.sql',
            'javax.servlet', 'jakarta.servlet', 'io.ktor', 'org.jetbrains.exposed', 'org.jooq', 'okhttp3', 'retrofit2',
            'software.amazon.awssdk', 'org.apache.kafka', 'io.micronaut', 'io.quarkus'],
    'cs': ['Microsoft.EntityFrameworkCore', 'Microsoft.AspNetCore', 'System.Data', 'Dapper', 'Npgsql', 'MongoDB.Driver',
           'StackExchange.Redis', 'System.Net.Http', 'Amazon.', 'Confluent.Kafka', 'RabbitMQ'],
    'php': ['Illuminate\\', 'Doctrine\\ORM', 'Doctrine\\DBAL', 'Symfony\\Component\\HttpFoundation',
            'Symfony\\Component\\HttpKernel', 'Symfony\\Component\\Routing', 'GuzzleHttp', 'Predis', 'MongoDB\\',
            'Laravel\\'],
    'rb': ['active_record', 'activerecord', 'rails', 'sinatra', 'sequel', 'pg', 'mysql2', 'redis', 'faraday', 'httparty',
           'net/http', 'sidekiq', 'aws-sdk', 'mongoid'],
}
SEPARATORS = {'js': '/', 'py': '.', 'go': '/', 'rs': '::', 'jvm': '.', 'cs': '.', 'php': '\\', 'rb': '/'}

JS_IMPORT = re.compile(r'''(?:\bimport|\bexport)\s[^'";]*?\bfrom\s*['"]([^'"]+)['"]|\bimport\s*\(?\s*['"]([^'"]+)['"]|\brequire\(\s*['"]([^'"]+)['"]\s*\)''')
PY_FROM = re.compile(r'^[ \t]*from[ \t]+(\.*[\w.]*)[ \t]+import\b', re.MULTILINE)
PY_IMPORT = re.compile(r'^[ \t]*import[ \t]+([\w.]+(?:[ \t]*,[ \t]*[\w.]+)*)', re.MULTILINE)
GO_SINGLE = re.compile(r'^[ \t]*import[ \t]+(?:[\w.]+[ \t]+)?"([^"]+)"', re.MULTILINE)
GO_BLOCK = re.compile(r'^[ \t]*import[ \t]*\((.*?)\)', re.MULTILINE | re.DOTALL)
GO_LINE = re.compile(r'^[ \t]*(?:[\w.]+[ \t]+)?"([^"]+)"', re.MULTILINE)
RS_USE = re.compile(r'^[ \t]*(?:pub(?:\([\w:]+\))?[ \t]+)?(?:use|extern[ \t]+crate)[ \t]+([\w:]+)', re.MULTILINE)
JVM_IMPORT = re.compile(r'^[ \t]*import[ \t]+(?:static[ \t]+)?([\w.]+)', re.MULTILINE)
CS_USING = re.compile(r'^[ \t]*(?:global[ \t]+)?using[ \t]+(?:static[ \t]+)?(?:\w+[ \t]*=[ \t]*)?([\w.]+)[ \t]*;', re.MULTILINE)
PHP_USE = re.compile(r'^[ \t]*use[ \t]+(?:function[ \t]+|const[ \t]+)?\\?([\w\\]+)', re.MULTILINE)
RB_REQUIRE = re.compile(r'''^[ \t]*(require(?:_relative)?)[ \t]*\(?[ \t]*['"]([^'"]+)['"]''', re.MULTILINE)
RB_RECORD = re.compile(r'<\s*(ApplicationRecord|ActiveRecord::Base)\b')
SOURCE_EXT = re.compile(r'\.(m?[jt]sx?|c[jt]s|py|rb)$')
SUPPRESSION = re.compile(r'unslop-ignore\s+([A-Z_]+)(\s+--\s*\S.*)?')


def line_of(text, index):
    return text.count('\n', 0, index) + 1


def extract_imports(lang, text):
    """Yield (line, module, kind); kind is 'relative' for paths resolved against the file."""
    if lang == 'js':
        for m in JS_IMPORT.finditer(text):
            group = 1 if m.group(1) else 2 if m.group(2) else 3
            module = m.group(group)
            yield line_of(text, m.start(group)), module, 'relative' if module.startswith('.') else 'absolute'
    elif lang == 'py':
        for m in PY_FROM.finditer(text):
            module = m.group(1)
            yield line_of(text, m.start(1)), module, 'pyrelative' if module.startswith('.') else 'absolute'
        for m in PY_IMPORT.finditer(text):
            for module in re.split(r'[ \t]*,[ \t]*', m.group(1)):
                yield line_of(text, m.start(1)), module, 'absolute'
    elif lang == 'go':
        for m in GO_SINGLE.finditer(text):
            yield line_of(text, m.start(1)), m.group(1), 'absolute'
        for block in GO_BLOCK.finditer(text):
            for m in GO_LINE.finditer(block.group(1)):
                yield line_of(text, block.start(1) + m.start(1)), m.group(1), 'absolute'
    elif lang == 'rb':
        for m in RB_REQUIRE.finditer(text):
            yield line_of(text, m.start(2)), m.group(2), 'relative' if m.group(1) == 'require_relative' else 'absolute'
        for m in RB_RECORD.finditer(text):
            yield line_of(text, m.start(1)), 'active_record', 'absolute'
    else:
        pattern = {'rs': RS_USE, 'jvm': JVM_IMPORT, 'cs': CS_USING, 'php': PHP_USE}[lang]
        for m in pattern.finditer(text):
            yield line_of(text, m.start(1)), m.group(1), 'absolute'


def segments(path):
    return [s.lower() for s in re.split(r'::|[/\\.:]', path) if s]


def resolve(lang, relative_file, module, kind):
    """Return the import as lower-case path segments, resolved against the importing file when relative."""
    folder = posixpath.dirname(relative_file)
    if kind != 'absolute':
        module = SOURCE_EXT.sub('', module)
    if kind == 'relative':
        return segments(posixpath.normpath(posixpath.join(folder, module)))
    if kind == 'pyrelative':
        dots = len(module) - len(module.lstrip('.'))
        base = folder
        for _ in range(dots - 1):
            base = posixpath.dirname(base)
        rest = module[dots:].replace('.', '/')
        return segments(posixpath.normpath(posixpath.join(base, rest)) if rest else base)
    return segments(module)


def layer_of(parts):
    """The innermost layer folder in the path decides the layer."""
    for part in reversed(parts):
        if part in DOMAIN:
            return 'domain'
        if part in APPLICATION:
            return 'application'
        if part in ADAPTER:
            return 'adapter'
    return None


def context_of(parts):
    """Return (context name, path inside the context) for the first context parent folder."""
    for i, part in enumerate(parts[:-1]):
        if part in CONTEXT_PARENTS:
            return parts[i + 1], parts[i + 2:]
    return None, []


def is_infra_lib(lang, module):
    sep = SEPARATORS[lang]
    for lib in INFRA_LIBS[lang]:
        if lib[-1] in '/._\\:':
            if module.startswith(lib):
                return True
        elif module == lib or module.startswith(lib + sep):
            return True
    return False


def check_file(path, relative_file, lang):
    text = path.read_text(encoding='utf-8', errors='replace')
    lines = text.splitlines()
    file_parts = segments(posixpath.dirname(relative_file)) + [Path(relative_file).stem.lower()]
    file_layer = layer_of(file_parts[:-1])
    file_context, _ = context_of(file_parts)
    findings = []
    for line, module, kind in extract_imports(lang, text):
        parts = resolve(lang, relative_file, module, kind)
        library = kind == 'absolute' and is_infra_lib(lang, module)
        target_layer = None if library else layer_of(parts)
        if file_layer == 'domain' and target_layer in ('application', 'adapter'):
            findings.append((line, 'DOMAIN_IMPORTS_OUTER', 'domain imports the {} layer: {}'.format(target_layer, module)))
        elif file_layer == 'application' and target_layer == 'adapter':
            findings.append((line, 'APPLICATION_IMPORTS_ADAPTER', 'application imports an adapter: ' + module))
        if file_layer == 'domain' and library:
            findings.append((line, 'DOMAIN_IMPORTS_INFRA_LIB', 'domain imports infrastructure library: ' + module))
        target_context, inside = context_of(parts)
        if file_context and target_context and target_context != file_context:
            if inside and inside[0] not in PUBLIC_ENTRIES:
                findings.append((line, 'CROSS_CONTEXT_INTERNALS',
                                 '{} imports internals of {}: {}'.format(file_context, target_context, module)))
    results = []
    for line, rule, message in findings:
        suppression = None
        for candidate in (line, line - 1):
            if 1 <= candidate <= len(lines):
                m = SUPPRESSION.search(lines[candidate - 1])
                if m and m.group(1) == rule:
                    suppression = m
                    break
        if suppression is None:
            results.append((line, rule, message))
        elif not suppression.group(2):
            results.append((line, 'SUPPRESSION_WITHOUT_REASON', 'unslop-ignore {} needs "-- reason"'.format(rule)))
    return file_layer is not None or file_context is not None, results


def source_files(root):
    if root.is_file():
        yield root
        return
    stack = [root]
    while stack:
        folder = stack.pop()
        for entry in sorted(folder.iterdir()):
            if entry.is_dir() and not entry.is_symlink():
                if entry.name not in SKIP_DIRS:
                    stack.append(entry)
            elif entry.suffix in LANGUAGES and not TEST_FILE.search(entry.name):
                yield entry


def main(argv):
    roots = [Path(arg).resolve() for arg in argv[1:]] or [Path('.').resolve()]
    missing = [str(r) for r in roots if not r.exists()]
    if missing:
        print('Not found: ' + ', '.join(missing), file=sys.stderr)
        return 2
    scanned = structured = errors = 0
    cwd = Path.cwd().resolve()
    for root in roots:
        base = root if root.is_dir() else cwd if cwd in root.parents else Path(root.anchor)
        for path in source_files(root):
            relative_file = path.relative_to(base).as_posix()
            has_structure, results = check_file(path, relative_file, LANGUAGES[path.suffix])
            scanned += 1
            structured += has_structure
            for line, rule, message in results:
                errors += 1
                print('ERROR {} {}:{} {}'.format(rule, path, line, message))
    if structured == 0:
        print('status: SKIPPED (no domain/application/adapter or module folders in {} files)'.format(scanned))
        return 0
    status = 'FAIL' if errors else 'PASS'
    print('status: {} ({} errors, {} files in layers or modules, {} files scanned)'.format(status, errors, structured, scanned))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
