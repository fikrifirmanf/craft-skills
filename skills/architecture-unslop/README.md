# architecture-unslop

Asks before it builds. When you start a backend project, service or module, this skill reads your idea, recommends an architecture with a reason, lets you pick or type your own, saves the choice as an ADR, scaffolds the folders with one working example slice, and then checks that later changes keep the layer boundaries.

## What it does

1. **Checks for a saved decision.** If the repo already has an architecture ADR, it skips the questions and follows it.
2. **Reads your idea.** It looks for signals such as money, approvals, dashboards, audit needs and team size. If your message doesn't say what the software does, it asks one short question first.
3. **Shows a picker** with explained options and a recommendation tied to your own words:
   - Base: Layered/MVC, Hexagonal, Clean/Onion, Modular Monolith, Microservices, Vertical Slice
   - Modeling: Full DDD, Tactical DDD, Simple models
   - Add-ons: CQRS, Event Sourcing, Event-Driven
   - Stack: TypeScript, Python, Go, Rust, Java/Kotlin, C#, PHP, Ruby

   You can type your own answer instead. Agents without a picker get a numbered list.
4. **Adds domain notes** when the idea involves money, audit, booking or webhooks: ledger entries, idempotency keys, signed webhooks, a licensing caution for holding other people's funds.
5. **Warns once** if you pick something heavier than the idea needs, then follows your choice.
6. **Records the decision** in `docs/adr/NNNN-architecture.md`. A later change creates a new ADR that supersedes the old one.
7. **Scaffolds** after you confirm the tree: one vertical slice through every layer, built around the core concept of your idea. It never overwrites files and never installs packages.
8. **Checks boundaries** with `scripts/check_boundaries.py` (domain importing infrastructure, application importing adapters, one module reaching into another's internals).

It answers in your language. Pattern names stay in English.

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | The workflow |
| `references/signals.md`, `picker.md`, `domain-notes.md`, `example-slice.md` | Recommendation rules, picker wording, domain advice, slice contents |
| `references/base/`, `modeling/`, `addons/` | Rules and layout for each pattern |
| `references/stacks/` | Naming, folders and idioms for 8 languages |
| `assets/adr.md.template` | The decision record template |
| `scripts/find_adr.py` | Reads the saved decision |
| `scripts/check_boundaries.py` | Scans imports for boundary violations in 8 languages |

Both scripts use only the Python standard library.

## Benchmark

Latest run (iteration 2): 5 test cases, each run twice with the skill and once without it. A run passes a check when its output meets it; checks were graded by reading the outputs and running `check_boundaries.py`.

| Test case | What it checks | With skill | Without skill |
|---|---|---|---|
| crud-blog | Light recommendation for a simple blog, no add-ons pushed | 4/4, 4/4 | 2/4 |
| fintech-wallet | Hexagonal + DDD + Event Sourcing for an audited wallet, ADR written, clean domain | 7/7, 7/7 | 1/7 |
| marketplace | Modular Monolith for 3 people, CQRS only for the dashboard, Indonesian output, money notes | 5/5, 5/5 | 5/5 |
| vague-prompt | Asks one question about the app before offering options | 3/3, 3/3 | 2/3 |
| existing-adr | Follows a saved ADR without re-asking, rule on the aggregate | 5/5, 5/5 | 4/5 |
| **Total** | | **100%** (10 of 10 runs) | **62%** |

| Metric | With skill | Without skill |
|---|---|---|
| Mean time per run | 87 s | 160 s |
| Mean tokens per run | 58,840 | 57,424 |

### What the numbers show
- Without the skill, the agent usually builds straight away, or asks five questions where one would do. With it, the agent recommends and waits for a choice.
- In the fintech case, the baseline's core ledger package imported the database driver. The skill's domain code imported no infrastructure and passed the boundary check.
- Marketplace ties. The baseline reached a modular monolith on its own, in Indonesian. The skill's domain notes (added after the first run) now match the baseline's money advice.

### What the numbers don't show
- The skill's author also wrote the checks and graded the runs. Read 100% as "no regression found", not proof.
- The baseline is a single run per case, reused from iteration 1 and re-graded only on the checks that changed.
- Go is not installed on the test machine, so no generated Go was compiled or tested.
- Not tested: a live interactive picker, the numbered-list fallback, stacks other than TypeScript, Python and Go, and a user who picks an overkill option.

### History
| Iteration | With skill | Without skill | Change |
|---|---|---|---|
| 1 | 97% (22 of 23 checks, one run each) | 62% | First version |
| 2 | 100% (two runs each) | 62% | Added `domain-notes.md`; rewrote three checks that only the skill's own files could pass; added a domain-notes check |

The test cases live in `evals/` and are not copied by the installer.

## Install

From the repo root:

```bash
./install.sh --skill architecture-unslop --target claude
```

See the main README for other targets.
