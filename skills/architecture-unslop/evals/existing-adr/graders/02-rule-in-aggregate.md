---
type: llm
focus: trace
weight: 1
---

The cancellation rule is enforced by a method on the Order aggregate that rejects orders not in the placed state, not by a status check in a handler or the repository
