---
name: frontend-unslop
description: Enforces high-craft frontend engineering and eliminates AI UI/React slop. Trigger whenever creating, refactoring, or styling React, Next.js, TypeScript, or Tailwind CSS components.
---

# Frontend Anti-Slop Protocol

Never output generic first-draft UI or unverified React boilerplate.

## 1. Visual & Tailwind (HARD BANS)
- **No "AI SaaS purple" gradients:** never default to `from-indigo-500 via-purple-500 to-pink-500` or neon glow backdrops unless defined in design tokens.
- **No generic 3-column icon cards:** no symmetric 3-card grids with an icon in a tinted circle unless requested. Use layouts that fit the data: bento, tables, dense lists.
- **No happy-path-only components:** every data-driven component implements `Loading` (skeleton matching layout geometry), `Empty` (actionable), and `Error` (retryable inline) states.
- **Token discipline:** prefer semantic tokens (`bg-background`, `text-foreground`, `border-border`) over arbitrary hex, **but only tokens that are defined** (see section 2).

## 2. Styles MUST load (HARD REQUIREMENT, especially one-shot prompts)
A page with unstyled markup is a failure. In a fresh or one-shot build, nothing is set up for you, so:
- **Wire the stylesheet:** ensure an entry CSS exists and is imported by the root (`import "./globals.css"` in the Next.js `app/layout.tsx`, or in `main.tsx`; `<link>`/`<style>` for plain HTML). Tailwind v4: `@import "tailwindcss";`. Tailwind v3: `@tailwind base; @tailwind components; @tailwind utilities;` plus `content` globs covering every source dir.
- **Define every token you use:** `bg-background`, `text-foreground`, `border-border`, `bg-primary`, etc. do not exist by default. Declare the CSS variables and register them (v4: `@theme inline { --color-background: var(--background); ... }`; v3: map in `tailwind.config`). If you will not define tokens, use real Tailwind colors (`bg-zinc-950`, `text-zinc-100`).
- **Never invent utilities or `@apply` undefined classes.** Dynamic class names (`bg-${color}-500`) are not generated; use complete literal class strings.
- **Create the config the stack needs** (`postcss.config.mjs` with `@tailwindcss/postcss` for v4; `tailwind.config` for v3) and install the packages in the same change.
- Include the stylesheet, config and layout edits in the same response as the components, never as a follow-up.

## 3. Images, motion & layout integrity (HARD RULES)
- **Never invent image URLs.** Do not write `images.unsplash.com/photo-...` IDs from memory; they resolve to wrong subjects (a burger on a water charity page) or 404. Call MCP tool `get_verified_images` with a descriptive `query` and use the returned URLs and `alt` verbatim. If it returns `PLACEHOLDER`, ship the SVG placeholders. Do not swap in guessed photos.
- **No frozen counters.** Never start a count-up at `useState(0)`; an SSR render or screenshot freezes it at nonsense like "23% Transparency". Render the real target value and animate with CSS, or initialise state with the target.
- **Safe scroll reveals.** No `initial={{ opacity: 0 }}` gated on `whileInView`. Content must be visible by default; use a subtle `y: 12 -> 0` or CSS keyframes, and respect `prefers-reduced-motion`.
- **Aligned cards.** Every card in a grid: wrapper `flex flex-col h-full`, body `flex-1`, footer/CTA/progress `mt-auto`, so buttons share one baseline whatever the title length.
- **Break grid monotony.** With 4+ items, do not render N identical cards: make the first a `col-span-2` featured card or give one a distinct ring/border treatment.
- **Grid slot math.** Before writing a grid, add up the column spans: the total MUST be a multiple of the column count, or the last row ends with an orphan. With `grid-cols-3` and one `col-span-2` featured card: render **5** cards (row 1: span-2 + span-1; row 2: three span-1), or **4** cards with the last one also `col-span-2` (2+1, 1+2). NEVER render 6 cards when one is `col-span-2` (7 slots leaves a lone card on row 3). The same arithmetic applies to any column count and any number of spanning cards.
- **Typography.** `text-balance` on every `h1`-`h3`, `text-pretty` on paragraphs. Left-align section headings; use full-bleed contrast bands instead of floating white cards on white.
- **No ambient `blur-2xl/3xl` corner blobs.** Use flat colour fields.
- **No hydration traps.** Never render `new Date()`, `Date.now()` or `Math.random()` directly in JSX.
- **Complete pages.** Include every requested section (for example "How it works"); do not silently skip one.

## 4. React & TypeScript (HARD BANS)
- **No `useEffect` for derived state:** compute during render or with `useMemo`.
- **No type escapes:** `: any`, `as unknown as`, `@ts-ignore`, `@ts-expect-error`, `eslint-disable`.
- **No silent error swallowing:** no empty `catch {}` or `catch (e) { console.log(e) }`.
- **No placeholder artifacts:** no `// TODO`, `Lorem ipsum`, `via.placeholder.com`, `John Doe`, `Acme Inc`.
- **Stable keys:** never `key={index}` (or `` key={`row-${i}`} ``); use the item's id.
- **No dynamic Tailwind classes:** `` `bg-${tone}-500` `` is never generated. Map values to complete literal strings (`const tone = { ok: "bg-emerald-600", bad: "bg-red-600" }`).
- **Real links:** no `href="#"`, empty `href` or `javascript:`. Use a route, or a `<button>` for actions.
- **Effects that fetch abort:** create an `AbortController` and abort in the cleanup, or use the framework's loader/query library.
- **No raw HTML injection** (`dangerouslySetInnerHTML`, `v-html`) without sanitising. JSON-LD via `JSON.stringify` is fine.

## 5. Mandatory verification loop
Before claiming a frontend task is complete:
1. Call MCP tool `audit_frontend_slop` with every modified file path.
2. Call MCP tool `verify_styles_wired` with the modified files. It confirms the stylesheet exists and is imported, and that every semantic token class is defined.
3. Call MCP tool `verify_typescript_compile`.
4. On `status: "FAIL"`, fix every reported violation and re-run until `PASS`. Omitting `files` audits the git working-tree changes.
5. A verified false positive may be suppressed with `{/* unslop-ignore RULE_ID -- reason */}` (or `// unslop-ignore ...`) on or above the line. A suppression without a reason is an ERROR.
6. `SKIPPED` means a tool could not run (e.g. TypeScript not installed): say so, never claim it passed.

For visual craft and accessibility (contrast, focus, alt text, token sprawl) also run `ui-unslop`; for user-facing text run `copy-unslop` if those servers are installed.
