# Comparing skill revisions

Keep historical results unchanged. The saved iteration-2 timing files measure resumed segments after rate limits, so they cannot establish a full-run speed improvement. Earlier outputs were reused and models were not recorded. Treat those results as exploratory.

For the next comparison:

1. Freeze the prompts, input projects, graders, model version, tools, and environment. Record the skill revision or content hash. Compare baseline, previous skill, and revised skill using fresh outputs and separate contexts.
2. Run each case multiple times per configuration. Record all failures and interruptions. Separate executor tokens from grading tokens; record input, output, cached tokens, and any available reasoning-token counts rather than inventing a total from incomplete fields.
3. Measure elapsed time from the original start through completion, including retries. Record interrupted or incomplete runs separately and do not compare partial timings with completed runs.
4. Run the same behavior and accessibility checks for each configuration. Have visual reviewers compare anonymized screenshots at matching viewports against the brief. Do not award points merely for adding illustrations, extra fonts, charts, or design.md.
5. Add efficiency cases alongside the three full-build cases: a small spacing fix, a new screen using an existing theme, and a review-only request. Check that these do not trigger a new full design document, unrelated redesign, or unnecessary reference reads.
6. Report per-case results, variation, visual preference, scope regressions, and token cost. Do not infer total-run savings from the character reduction of SKILL.md. Compare total cost only when token accounting is consistent across configurations.

The local regression suite checks script behavior independently:

```bash
python3 -B -m unittest discover -s tests -v
```

Run from the rich-ui skill directory. These checks do not measure UI quality or model token usage.
