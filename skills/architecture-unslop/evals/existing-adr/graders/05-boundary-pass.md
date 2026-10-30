---
type: llm
focus: trace
weight: 1
---

The run checks that the new code keeps dependencies pointing inward (no domain import of an adapter or database package, no import of another module's internals), by running a tool or searching the imports, and reports the result
