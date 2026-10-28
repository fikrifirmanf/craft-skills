# Craft Skills

Agent skills for UI design, motion graphics, frontend and backend code, mobile apps, tests, and copy.

Each skill lives in its own folder under `skills/`. Install the whole collection or pick the skills you need.

## Skills

| Skill | What it covers |
|---|---|
| [rich-ui](skills/rich-ui/SKILL.md) | Type, layout, color, tokens, and visual review. Small fixes use a shorter workflow. |
| [motion-graphic-design](skills/motion-graphic-design/SKILL.md) | Kinetic type, product films, animated explainers, 3D demonstrations, and rendering checks. |
| [ui-unslop](skills/ui-unslop/SKILL.md) | Web UI consistency, accessibility, contrast, and interaction states. |
| [frontend-unslop](skills/frontend-unslop/SKILL.md) | React, Next.js, TypeScript, and Tailwind implementation checks. |
| [backend-unslop](skills/backend-unslop/SKILL.md) | API validation, database queries, error handling, and backend reliability. |
| [mobile-unslop](skills/mobile-unslop/SKILL.md) | iOS, Android, React Native, and Flutter implementation checks. |
| [test-unslop](skills/test-unslop/SKILL.md) | Tests that check behavior and fail when that behavior breaks. |
| [copy-unslop](skills/copy-unslop/SKILL.md) | Specific product copy and microcopy in English and Bahasa Indonesia. |

`rich-ui` guides visual decisions. `ui-unslop` checks web UI rules. Their scopes overlap; install only what fits your workflow.

`motion-graphic-design` covers authored animation sequences, from storyboards through export. It includes references for choreography, 3D scenes, rendering, and [the sources studied](skills/motion-graphic-design/references/sources.md).

## Install

Requires Bash and Python 3.8 or later. The Python installer uses the standard library.

```bash
git clone https://github.com/fikrifirmanf/craft-skills.git
cd craft-skills
./install.sh
```

By default, this copies all eight skills into `~/.agents/skills`, the shared personal skill directory used by Codex. For Claude Code:

```bash
./install.sh --target claude
```

| Option | Destination |
|---|---|
| `--target agents` | `~/.agents/skills` (default) |
| `--target codex` | `~/.agents/skills` |
| `--target claude` | `~/.claude/skills` |
| `--target all` | Both shared and Claude Code directories |
| `--dir PATH` | A custom skill directory |

See the official [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skill documentation](https://code.claude.com/docs/en/skills) for discovery and invocation details.

### Choose skills or preview an install

```bash
./install.sh --list
./install.sh --skill rich-ui
./install.sh --skill motion-graphic-design
./install.sh --skill frontend-unslop --skill test-unslop --target claude
./install.sh --target all --dry-run
./install.sh --dir ../my-project/.agents/skills --skill rich-ui
```

Installs are copies. Editing this checkout does not change installed copies. Installs leave out test data, tests, and Python caches.

For example, ask your agent:

```text
Use $motion-graphic-design to create a 15-second product launch animation.
```

### Update installed copies

```bash
git pull --ff-only
./install.sh --force
```

Existing skill folders are preserved unless you pass `--force`. An update first copies the new skill to a staging directory, then moves the old folder into `.craft-skills-backups/` beside the destination skill directory. The installer prints each backup path. To restore a backup, move the current installed folder aside and put the backup back at its original path.

Use the same target and skill options when updating a selected installation. The installer does not change agent settings or configure MCP servers.

## Companion tools

`rich-ui` includes local Python checks for design documents, contrast, and token values. Browser or simulator rendering comes from your agent environment.

`motion-graphic-design` uses the project's animation and rendering tools, such as GSAP, Remotion, Three.js, or Blender. It has no required companion MCP server. Renderers, browsers, media tools, and assets are not bundled with the skill.

The six `*-unslop` skills require their matching MCP servers for the verification tools named in their instructions. The installer copies skill files only; it does not supply these servers. Connect these tools to run the checks in each skill.

| Skill | Companion server and setup |
|---|---|
| frontend-unslop | [frontend-unslop-mcp](https://github.com/fikrifirmanf/frontend-unslop-mcp) |
| backend-unslop | [backend-unslop-mcp](https://github.com/fikrifirmanf/backend-unslop-mcp) |
| ui-unslop | [ui-unslop-mcp](https://github.com/fikrifirmanf/ui-unslop-mcp) |
| mobile-unslop | [mobile-unslop-mcp](https://github.com/fikrifirmanf/mobile-unslop-mcp) |
| test-unslop | [test-unslop-mcp](https://github.com/fikrifirmanf/test-unslop-mcp) |
| copy-unslop | [copy-unslop-mcp](https://github.com/fikrifirmanf/copy-unslop-mcp) |

Each server explains how to set it up in your agent. Without the tools, the agent cannot run those checks.

## Development

Run both test suites:

```bash
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s skills/rich-ui/tests -v
bash -n install.sh
```

CI runs these commands on Linux with Python 3.10 and 3.13, and on macOS with Python 3.13.

When adding a skill, keep its folder name and frontmatter `name` identical. Include `SKILL.md` and only the scripts, references, and assets the skill needs. Keep descriptions focused on when the skill applies. The installer discovers new skill folders automatically.

MIT licensed. See [LICENSE](LICENSE).
