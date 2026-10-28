---
name: backend-unslop
description: Enforces production-grade polyglot backend architecture, API reliability, and SQL/database hygiene (TypeScript/Node, Python, Go, Rust, Java/Kotlin, C#, PHP, Ruby, PostgreSQL, ClickHouse, Redis, async workers). Trigger whenever writing or modifying API routes, database queries, migrations, background jobs, or backend services.
---

# Backend & SQL Anti-Slop Protocol

Never output naive queries, unvalidated handlers, silent error blocks, or blocking I/O slop across any backend language.

## 1. SQL & database (HARD BANS)
- **No `SELECT *`:** always project explicit columns (PostgreSQL, MySQL, SQLite, and ClickHouse alike).
- **No string-interpolated or concatenated SQL:** never use JS template literals (`${}`), Python f-strings/`.format()`/`%`, Go `fmt.Sprintf`, Rust `format!`, Ruby `#{}` or string `+` concatenation. Always use parameter bindings (`$1`, `?`, `:name`, `%(name)s`, `@p1`) or typed query builders/ORMs.
- **No N+1 in loops:** no DB, Redis, or HTTP calls inside loops (`for`, `for...of`, `.map()`, Python `for ... in`, Go `for range`, Rust `for`). Batch with `ANY($1)`, `IN (...)`, bulk upserts, or `JOIN`.
- **No unbounded reads:** every list query has an explicit `LIMIT` and cursor/offset pagination.
- **Workload separation:** keep OLTP transactions short; no analytics or external HTTP calls inside `BEGIN...COMMIT`.

## 2. API, async & errors (HARD BANS)
- **Validate every boundary:** handlers, webhooks, queue consumers, and RPC/tool entrypoints must validate input with strict schemas before domain logic:
  - **TypeScript/JS:** Zod, TypeBox, Valibot
  - **Python:** Pydantic, msgspec, Marshmallow
  - **Go:** `go-playground/validator` or explicit struct validation
  - **Rust:** `serde` + `validator` / `garde`
  - **Java/Kotlin/C#/PHP/Ruby:** Jakarta Bean Validation (`@Valid`), FluentValidation, Symfony/Laravel FormRequest, Dry-Validation
- **No type escapes:** never use `: any`, `as any`, `@ts-ignore`, `@ts-expect-error`, or `# type: ignore` to bypass validation.
- **No blocking long requests:** work over ~2s goes to a queue/background worker; stream progress via SSE/WebSocket or pollable job status.
- **Idempotency & timeouts:** set explicit timeouts/deadlines (`AbortSignal.timeout`, `context.WithTimeout`, `httpx.Timeout`, `tokio::time::timeout`) on every network/DB call; retried mutations must be idempotent.
- **No silent catch or stack leaks:** never use empty `catch {}`, `except: pass`, empty `if err != nil {}`, or bare `rescue`. Never return raw driver errors, `err.stack`, `traceback.format_exc()`, or `err.Error()` directly to HTTP clients. Return structured error codes and log context server-side.
- **No unfinished placeholders:** never leave `TODO`, `FIXME`, `NotImplementedError`, `todo!()`, or `unimplemented!()` in production handlers.

## 3. Security defaults (HARD BANS)
- **No hardcoded credentials:** API keys, passwords, tokens, private keys and connection strings come from the environment or a secret manager. Never paste a real-looking key, even "temporarily".
- **No `UPDATE`/`DELETE` without `WHERE`.**
- **Never disable TLS verification** (`rejectUnauthorized: false`, `verify=False`, `InsecureSkipVerify: true`). Fix the CA bundle.
- **Passwords:** argon2id, scrypt or bcrypt only. Never md5/sha1/sha256.
- **Tokens, OTPs, reset codes, salts:** `crypto.randomBytes`/`randomUUID`, `secrets`, `crypto/rand`. Never `Math.random()` or `random`.
- **No `eval`, `new Function`, or shell strings built from input.** Pass argv arrays (`execFile`, `subprocess.run([...])`, `exec.Command(bin, args...)`).
- **JWTs:** verify the signature with an explicit `algorithms` allowlist; `jwt.decode` alone is not authentication.
- **CORS:** list the allowed origins explicitly; never `*` with credentials.
- **Outbound calls carry timeouts:** `fetch(url, { signal: AbortSignal.timeout(ms) })`, `requests.get(url, timeout=5)`, `&http.Client{Timeout: ...}`.
- **Go:** never discard an error with `_`. **Rust:** propagate with `?` instead of `.unwrap()` outside tests. **Python:** no bare `except:`.

## 4. Mandatory verification loop
Before claiming a backend/database task is complete:
1. Call MCP tool `audit_backend_slop` with every modified file or directory (omit `files` to audit the git working-tree changes).
2. Call `verify_backend_compile` with the same files. It runs TypeScript (`tsc --noEmit`), Go (`go vet`), Rust (`cargo check`), Python (`py_compile`), PHP (`php -l`) and Ruby (`ruby -c`).
3. On `status: "FAIL"`, fix every ERROR at its root cause and re-run until `PASS`. Review WARN findings.
4. A finding that is a verified false positive may be suppressed with a comment on or above the line: `// unslop-ignore RULE_ID -- why this is safe`. A suppression without a reason is itself an ERROR. Never suppress to get past a real problem.
5. `SKIPPED` means the toolchain is missing: tell the user verification did not run. Never report it as passing.
