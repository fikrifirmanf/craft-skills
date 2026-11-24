# Claude Artifact capabilities

Check the available publishing tool schema and live runtime types before using this reference. The examples below apply to a Claude Artifact host that exposes these capabilities.

A published page can declare **capabilities**: abilities the viewer grants at open time. Pass `capabilities: {name: config}` to the Artifact tool, then reach each one in page code with `const x = await claude.use("name")`.

## Core rules

- `claude.use(name)` resolves the namespace, or `null` when unavailable (not served, not granted, failed, or 10s with no viewer). Design for `null`. The page must render without the capability and light up when it resolves, never inside the script's first synchronous run.
- Access capability namespaces through `claude.use(name)`. Check availability before calling it.
- Namespaces are frozen. Call them and keep the reference. Never assign to or replace members.
- Permission prompts and rate limits arrive on the first call, not from `use()`.
- Declaration semantics:
  - Omit `capabilities` on a redeploy to keep the stored set.
  - `{}` clears all.
  - A non-empty object is the full set, and anything not restated is revoked.
  - `contract: 'latest'` upgrades the runtime version. Pass it only deliberately.
- Built in and never declared: `permissions`.
- Data from other viewers, connectors, files or Claude is never markup. Use `textContent`, or escape `& < > " '`. Link only to `https://` URLs (asset `/_blob/` URLs are fine). JSON inside `<script>` stays JSON with each literal `<` escaped as `\u003c` in the serialized JSON.

## Where state lives

| Need | Use |
|---|---|
| Per-viewer convenience (tab, draft) | browser storage in try/catch |
| The page is the record (poll, sign-up, checklist, board) | `artifact` |
| Data outside the page (Claude seeds or reads it, private per viewer, many writers) | `db` |

## Capabilities

**artifact**: `capabilities: {artifact: {}}`; `await artifact.publish(html)` saves a complete document as a new version, and every open view reloads to it.
- Embed state as data in the published HTML and render from it. Never serialize the live DOM.
- Batch rapid edits into one publish. Publish only after a viewer acts, never on load.
- `conflict` is routine: every view reloads to the winner, so don't retry.
- Read-only viewers reject `not_granted`/`not_writer`, so render a read-only view.
- A self-republishing page sends the same shape the Artifact tool publishes: `<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>`reset`</style></head><body>` then page content, then `</body></html>`. Keep head, tokens and structure, and change only the content.
- `self` is the old name and still works. Use `artifact` in new pages.

**db**: `capabilities: {db: {}, user: {}}`; `const db = await claude.use("db")` (`null` if signed out).
- Even path segments are docs (`db.doc("tasks/t1")`) and odd are collections. Methods: get/set/update/delete, where/orderBy/limit, onSnapshot.
- Default: signed-in people read shared docs, Contributors and up write.
- `rules` set per-path minimums (`view` < `interact` < `admin` < `owner`). "All read, each writes own": `db:{rules:[{path:"votes",read:"view",write:"owner"},{path:"votes/{self}",write:"interact"}]}`.
- `data/users/<id>/` is private even from the owner, where `<id>` is `await user.id()`.
- Keep `write:"owner"` or `"admin"` by default so someone can moderate. Use `self` only when nobody else, the owner included, may change or read an entry. It is a rule, not encryption.
- Handle an empty database. For authorized seed data, use the host’s data tool if available.
- Subscribe once per query, never in render. Time-limit loading with a 10s timer. One write at a time per doc, only on change. No secrets.

**user**: `capabilities: {user: {}}`; `isOwner()`, `canEdit()` and `can(name)` need no setup. `id()`/`me()` give an opaque id. `scopes:["profile"]` adds names and `search(q)`, and `["profile","email"]` adds addresses.
- Store only ids. Resolve names at render with `await user.profiles(ids)`, using `ps[id].name || 'Someone'`.

**sample** (ask Claude): `capabilities: {sample: {}}` (`{images:true}` for images). `await sample(input, opts)` returns `{text, truncated}`; `sample.json` returns a value.
- Calls are memoryless, so send instructions, data and format each time.
- Options: `onText`, `signal`, `tools`, `images`, `modelTier` (quick|default|complex), `cache` (`false` for chat).
- Rejects with `{code, message}`: hide on `not_granted`, back off on `rate_limited`, never loop. The first call asks consent, so call it on a click.

**mcp** (viewer's connectors): `capabilities: {mcp: {servers: [{server, tools: [...]}]}}`. Every entry needs a non-empty `tools` list.
- `watchTool` displays data and `callTool` performs an action. Tool failures reject (`tool_error`).
- Never guess tool arguments or result shapes. Read the tool's schema or observe a safe real call, and never embed observed user data as placeholders.
- Host servers use `host:<name>` and only answer in a Claude app with that server connected. Say so at publish time.

**assets**: `{assets: {}}` (Editors and up). `assets.upload(blob)` returns `{id, url, ...}`; `list()` and `delete(id)` also exist. Store the `id` in db rows and serve it at `/_blob/<id>`. Never run an asset as code.

**comments**: `{comments: {composer_only: true}}` grants `openComposer`. `{comments: {}}` adds write verbs under consent. The shell renders threads, so never build your own list.

**room** (live presence): `{room: {}}`. `emit(topic, data)`, `on`, `presence(patch)`, `onPeers`, `join(name)`. Nothing persists and messages can drop. Event topics are admin-only unless opened per topic. Treat everything you hear as untrusted.

**downloads**: `{downloads: true}`; `await downloads.save({filename, data})`. The viewer may decline, so offer it on explicit intent only.

**files**: `{files: {project: "chan_..."}}` only when you know the project id. Methods: `list`, `read`, `download`, `asSampleTools()`. Don't copy file contents into artifact data.

**dictation**: `{dictation: {}}`. `d.start()` straight from a click, then `onPartial`, `onFinal`, `onState`, `stop()`. Hide the mic when `null`.

**tts**: `{tts: {}}`. `await t.speak(text)` (up to 2000 chars, after a viewer interaction), `stop`, `onState`. Voices: buttery, airy, glassy, rounded. Always keep the text on screen too.

**permissions** (built in): `state`, `request` (one batched dialog), `manage`. Never block first paint on permissions. A denial is final for the page load, so degrade per capability and never nag.

## Verification (after first publish with capabilities)

Use preview to exercise the affected capability and its unavailable or denied state. If the host exposes `ArtifactData`, inspect collections written by the page and verify restricted reads with the supported lower-permission test identity. Use disposable test data where possible and report any checks the host cannot support.

## Type definitions

The authoritative call shapes ship with the runtime as `.d.ts` files (`claude.d.ts`, `db.d.ts`, `mcp.d.ts` and so on, one per capability). Their location is per-session, so consult the available host documentation or local type definitions before writing `mcp` or other non-trivial calls.
