---
name: runtime-craft
description: Plan and implement runtime behavior for web pages and interactive artifacts that need input, persistence, live data, integrations, model calls, or file and media access. Use when choosing how those features work in the target browser or host.
---

# Runtime Craft

Identify where the page runs and what it needs to do. Start with the existing app's runtime, data services, and deployment model. For a standalone page, use standard browser APIs where they meet the requirement. For an embedded or hosted artifact, check the host's sandbox, supported APIs, and persistence guarantees before promising an interaction. Verify actual schemas and return types before using an integration.

| Need | Implementation |
|---|---|
| Input, preview, filter, or calculation in the current session | In-memory state |
| Draft or preferences on the same browser and origin | Browser storage where available. Handle failure and make reset possible. |
| User-controlled transfer between sessions or devices | Import and export a documented, validated format where the target supports file access. |
| Shared state, durable records, or private per-user data | An existing backend or a documented host data service with the required authentication and access controls. Treat the service as the source of truth. |
| Live updates or presence | The project's subscription mechanism or a documented host API. Unsubscribe on teardown and distinguish transient presence from persisted data. |
| Model calls, connectors, privileged file access, or voice | A documented host capability or authorized service integration. Use a server boundary for credentials and privileged actions. |

## Behavior at the runtime boundary

- Render a usable first frame before permissions, storage, or network calls resolve. Show an empty state for a real empty dataset. Label example data clearly.
- Handle loading, denial, unsupported features, timeouts, and service errors where they affect the interaction. Request permissions and start gesture-gated APIs from the relevant viewer action. If a requested integration is unavailable, use a fallback that still serves the task and state which behavior depends on the integration.
- Validate data from users and integrations at the boundary. Insert untrusted strings as text and validate URL schemes before creating links. Keep credentials out of page source, browser storage, and URLs. Enforce identity and access controls in the service that owns the data.
- Respect existing deployment and permissions. Request only the capabilities and scopes the feature needs. Check how a deployment updates permissions before redeploying a page with an existing configuration.
- Attach readers and subscriptions once per active view or query. Disable duplicate submissions while a write is pending. For shared edits, use the service's conflict handling and keep unsaved input available if a write is rejected. Retry only operations that are safe to repeat.
- Use separate test data or an authorized test identity for mutations. When preview is available, exercise the main action and a relevant failure or denial. Verify reload behavior for saved data, a second session for shared data, and read/write boundaries for restricted data. Report checks that require a live integration you cannot exercise.

## Optional host reference

For a Claude Artifact destination that exposes the corresponding runtime, read [Claude Artifact capabilities](references/claude-artifacts.md). For other targets, use the project or host's documented interfaces. The browser-only workflow needs no publishing tool or companion skill.
