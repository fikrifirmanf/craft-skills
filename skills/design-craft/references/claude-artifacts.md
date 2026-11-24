# Claude Artifact HTML delivery

Use this reference when the requested destination is Claude Artifacts and the available publishing tool confirms these behaviors. The tool schema and preview determine the actual document format, supported features, and limits.

- Some publishing tools wrap an HTML fragment in the document shell. Supply a fragment only when the tool expects one. If the tool accepts title, description, or icon metadata, populate the fields supported by that tool.
- If the host supports `<meta name="claude:viewport-fit-sides" content="cover">`, pair it with safe-area padding on both sides. Use `max(16px, env(safe-area-inset-left, 0px))` and the corresponding right inset on the body or outer wrapper. Preserve host-provided vertical safe-area padding and account for insets on fixed or sticky elements.
- Verify the publisher’s allowed hosts for scripts and fonts, inline asset support, and payload limits before choosing dependencies. Where a script must expose a browser global, use the documented browser build and load it before the code that calls it.
- Use `<pre class="mermaid">` only when preview confirms a native Mermaid renderer. Inline SVG can carry the same diagram without a script.
- The sandbox can block native dialogs, printing, browser downloads, device permissions, iframes, and protocol links. Use in-page confirmations, selectable contact details, or a download capability where supported.
- Verify permitted fragment identifiers before using hash navigation. Shell-reserved hashes can collide with in-page routes.
- For live updates to a page with unsaved state, use a host snapshot and restore API only if the live runtime documents it. Exercise update and reload behavior in preview.
