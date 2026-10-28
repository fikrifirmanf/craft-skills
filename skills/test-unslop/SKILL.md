---
name: test-unslop
description: Enforces tests that fail when the code is wrong and eliminates fake, tautological or flaky AI-written tests (JS/TS with Jest/Vitest/node:test/Playwright, Python pytest/unittest, Go, Rust, Swift XCTest/Swift Testing, Kotlin/Java JUnit). Trigger whenever writing, fixing or reviewing tests, or before claiming that tests pass.
---

# Test Anti-Slop Protocol

A test exists to fail when behaviour breaks. AI-written tests often cannot fail: they render a component and assert nothing, compare a value with itself, or mock the unit under test. Then the agent reports "all tests pass" after a run that executed zero tests.

## 1. Every test can fail (HARD RULES)
- **Assert on behaviour:** each test checks an output, a state change, a rendered result, an emitted call or a thrown error. Rendering or calling without asserting is not a test.
- **No tautologies:** never `expect(true).toBe(true)`, `expect(x).toEqual(x)`, `assert True`, `assertTrue(true)`.
- **Assert the value, not existence:** prefer `toEqual({...})` or `toBe(3)` over `toBeDefined()`, `toBeTruthy()` or `is not None`.
- **Prove it:** for new tests, briefly break the code under test (or invert the expectation) and confirm the test fails, then restore it.
- **Never weaken an assertion, delete a test, or add `.skip` just to get green.** Fix the code or tell the user the test exposes a bug.

## 2. Failures must surface (HARD BANS)
- No `try { ... } catch {}` around assertions; use `expect(() => f()).toThrow()` or `pytest.raises`.
- Always `await` (or `return`) `expect(promise).rejects/resolves`; an un-awaited one never runs.
- No `.only` / `fit` / `fdescribe` left in the code.
- Skips carry a reason and a link: `@pytest.mark.skip(reason="needs GPU, see #42")`.

## 3. Deterministic and hermetic
- No fixed sleeps (`setTimeout` promises, `time.sleep`, `waitForTimeout`). Use fake timers, `findBy`/`waitFor`, or await the event.
- No real external network in unit tests: stub with MSW, nock, respx, `httptest` or a local server.
- No unseeded randomness or wall-clock dependence: fixed data, seeded faker, frozen time.
- Each test sets up its own state; order must not matter.

## 4. Test the right thing
- Mock at the boundary (network, clock, filesystem, payment provider), not your own modules. More than a handful of module mocks means you are testing the mocks.
- Cover the edge cases that matter: empty input, boundaries, invalid input, error paths, concurrency where relevant.
- Snapshots supplement explicit assertions; they do not replace them.
- UI tests query by role and accessible name (`getByRole('button', { name: 'Save' })`), not CSS classes or test ids, where possible.
- Name tests after the behaviour: `rejects expired coupons`, not `test1` or `works`.

## 5. Mandatory verification loop
Before claiming a testing task (or any task that changed tested code) is complete:
1. Call `audit_test_slop` with the modified test files (omit `files` to audit git changes).
2. Call `find_missing_tests` with the changed source files and add tests for uncovered logic, or tell the user why none are needed.
3. Call `run_tests`. Report the real result: `FAIL` means fix; zero tests run is a `FAIL`; `SKIPPED` means the runner is missing and tests did not run. Never claim "tests pass" without a `PASS` from this tool.
4. Suppress a verified false positive with `// unslop-ignore RULE_ID -- reason`; a suppression without a reason is an ERROR.
