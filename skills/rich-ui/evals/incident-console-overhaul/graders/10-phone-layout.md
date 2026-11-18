---
type: llm
focus: trace
weight: 1
---

At 390px the layout works: the sidebar collapses into a menu/bar or a bottom/top nav (not a 190px column eating half the screen), the stats stack or wrap into 2 columns, the two-column grid becomes one column, filters wrap or scroll, and the table either scrolls inside its own container or reflows into stacked rows. There is a real @media rule (or container query) in the final CSS, and the viewport meta is kept. No fixed 100vh app shell that traps content; uses dvh/min-height or normal flow.
