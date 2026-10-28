---
name: copy-unslop
description: Enforces specific, human copywriting and eliminates AI-sounding text in landing pages, product UI, microcopy, onboarding, emails, docs, READMEs, app-store listings and social posts, in English and Bahasa Indonesia. Trigger whenever writing, rewriting or reviewing any user-facing words, including headlines, CTAs, error messages, metadata and i18n strings.
---

# Copywriting Anti-Slop Protocol

AI copy is easy to spot: it promises to "unlock potential" and "seamlessly empower" without saying what the product does. Good copy is specific, plain and believable.

## 1. Say the specific thing
- **Lead with the outcome in the reader's words:** what changes for them, with a number, time, or concrete noun. "Close the books in two days", not "Revolutionize your finance workflow".
- **Every claim needs a fact.** Replace adjectives (cutting-edge, robust, innovative, world-class, seamless) with the detail that earns them ("search returns in 40 ms", "works offline on the train").
- **Never invent proof.** No "Trusted by 10,000+ teams", "#1", "10x faster" or star ratings unless the user gave you the real figure and source. Ask, or leave the claim out.
- **No placeholders:** no Lorem ipsum, "Feature 1", "[Your Company]", "John Doe", "Acme".

## 2. Banned AI tells (HARD BANS)
- Phrases: *delve, tapestry, testament to, unlock the power/potential, unleash, supercharge, seamless, game-changer, revolutionize, harness the power, in today's fast-paced world, ever-evolving, look no further, take it to the next level, navigate the complexities, embark on a journey, it's important to note, elevate your, dive into, whether you're an X or a Y*.
- Cadences: "It's not just X, it's Y"; "More than just a ___"; three-item adjective lists; a rhetorical question as the opening line.
- Punctuation: em dashes in every paragraph (most should be periods); exclamation marks to fake excitement.
- Bahasa Indonesia: *di era digital saat ini, mari kita selami/jelajahi, ke level berikutnya, bukan sekadar X melainkan Y, tidak hanya X tetapi juga Y, solusi terbaik/terpercaya untuk, revolusioner, dalam lanskap*.
- Emoji as bullets or headings in docs and READMEs.

## 3. Plain style
- Short sentences (12-18 words on average), active voice, "you" and "we".
- Cut filler: "in order to" becomes "to", "due to the fact that" becomes "because". Drop *very, really, basically, actually*.
- Sentence case for headings and buttons.
- Match the brand voice and the reader: consumer copy around grade 7, B2B around 9, technical docs up to 11.

## 4. Microcopy
- **Buttons name the action and its object:** "Create invoice", "Download report", "Book a 15-min demo", not "Submit", "Get Started", "Learn More".
- **Links describe their destination:** never "click here" or "read more".
- **Errors** say what happened, why, and what to do next, without blame: "Card declined by your bank. Try another card or contact your bank."
- **Empty states** explain what will appear here and offer the first action.
- **Length budgets:** title <= 60 chars, meta description 70-160, button <= 4 words, email subject <= 50, push <= 110, App Store subtitle <= 30, Play short description <= 80.

## 5. Mandatory verification loop
Before claiming a copy task is complete:
1. Call `audit_copy_slop` with every modified file containing copy (md/mdx, html, components, i18n JSON), or omit `files` to audit git changes.
2. Call `analyze_readability` on the new copy (`text` or `files`) and revise anything it flags.
3. Call `check_copy_length` for titles, meta descriptions, CTAs, subject lines and store listings (pass `files` to auto-extract page metadata).
4. On `FAIL`, rewrite every ERROR and re-run until `PASS`. A quotation or a brand name that trips a rule may be suppressed with `unslop-ignore RULE_ID -- reason`.
