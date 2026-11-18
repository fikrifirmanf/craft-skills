---
tags: [skill-creator]
max_turns: 80
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---
Build the front end for "Tidewell", a scheduling and billing tool used by front-desk staff at small physiotherapy clinics. Plain HTML, CSS and a little vanilla JS only, no build step, no external network resources. Put it in the current directory with index.html as the entry point, linking the other screens.

Screens (separate HTML files sharing one stylesheet):
1. Week schedule: a Mon-Sun calendar grid with 30-minute rows, 3 practitioners filterable, appointments as blocks (some overlapping, some with long patient names), a "now" line, a mini-month picker, and a New appointment button.
2. Patient record: header with name, age, allergies flag and insurer; tabs for Visits, Notes, Billing; a visits table; a notes composer; an outstanding-balance summary.
3. New appointment form: patient search, service type, practitioner, date, time, duration, recurrence, reminders (SMS/email), notes; with inline validation errors shown for at least two fields, and a sticky save bar.
4. Billing: an invoices table with statuses (draft, sent, overdue, paid), amounts in two currencies (NZD and AUD), a filter bar, a bulk-select toolbar, and a designed empty state variant for "no overdue invoices".

Requirements: a light and a dark theme (follow the system setting, plus a visible toggle), usable at 1440px and 390px, keyboard and screen-reader friendly, realistic sample data (invent plausible names and amounts; this is a prototype), and visible loading, empty and error states for at least the schedule and billing screens. Do not use a UI framework or icon font; inline SVG icons are fine.
