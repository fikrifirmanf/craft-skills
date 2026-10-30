---
type: llm
focus: trace
weight: 1
---

Domain tests that need no database are written, and the run checks that the domain and application code import no database, HTTP or framework package (by running a tool or searching the imports); running go test is not required if Go is not installed, but the run must say it was not run
