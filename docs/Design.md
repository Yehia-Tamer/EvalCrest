# Evalcrest — Design System

| | |
|---|---|
| **Status** | Draft v0.1 |
| **Last updated** | 2026-10-09 |
| **Applies to** | HTML report (MVP), PR comments, README and docs visuals, future dashboard |
| **Related docs** | [PRD.md](./PRD.md) · [Architecture.md](./Architecture.md) · [Agents.md](./Agents.md) |

Evalcrest's visual language is **corporate, calm and evidence-first** — closer to an audit report or an enterprise engineering console than a startup landing page. Every surface should look like it came from a mature engineering organization: restrained color, precise typography, generous whitespace, and numbers that always show where they came from.

---

## 1. Design principles

| # | Principle | What it means on screen |
|---|---|---|
| 1 | **Verdict first** | The top of every surface answers "can I merge?" before anything else. |
| 2 | **Every number is traceable** | Each metric shows its denominator (`n`) and links to the cases behind it. |
| 3 | **Calm by default, loud on failure** | Neutral navy and gray carry the layout. Color appears where state needs attention. |
| 4 | **Evidence over decoration** | No illustrations, gradients or stock imagery. Space goes to data, rationale and sources. |
| 5 | **Never color alone** | Status always pairs color with an icon and a text label. |
| 6 | **Works anywhere** | The report is one self-contained file that reads well offline, in print, in light and dark mode, and in a screenshot. |
| 7 | **The 10-second test** | A reviewer who opens the report or README for 10 seconds should leave knowing what was tested, the result, and that it was measured carefully. |

---

## 2. Brand

**Name.** Evalcrest — always one word, capital E only.

**Tagline.** *Automated QA for LLM applications.*

**Mark.** An original, geometric shield (a "crest") with three ascending horizontal bars inside, the top bar ending in a check stroke. Drawn on a 24 px grid with 2 px strokes so it holds up as a 16 px favicon. Single color only — navy on light backgrounds, white on navy. No gradients, shadows or 3D effects.

**Wordmark.** "Evalcrest" set in Inter SemiBold (600), letter-spacing −0.01em, next to the mark with a gap equal to half the mark's width.

**Clear space.** At least the height of the mark on every side. Minimum size: 16 px mark, 80 px lockup width.

---

## 3. Color

### 3.1 Palette philosophy

- **Navy** is the brand anchor (app bar, README banner, diagrams).
- **Slate neutrals** carry 90% of every surface.
- **One action blue** for links, primary buttons and focus.
- **Status colors** (success, danger, warning) are reserved for state and never decorative.
- **Chart colors** are a separate, validated set for data series only.

### 3.2 Light theme (default)

| Token | Hex | Use | Contrast |
|---|---|---|---|
| `--ec-bg` | `#F6F8FB` | Page background | — |
| `--ec-surface` | `#FFFFFF` | Cards, tables, panels | — |
| `--ec-surface-subtle` | `#F1F4F9` | Table header, code blocks, zebra rows | — |
| `--ec-border` | `#DDE3EC` | Dividers and card outlines (decorative) | — |
| `--ec-border-strong` | `#7D8A9E` | Input borders, interactive outlines | 3.50:1 on surface |
| `--ec-text` | `#0F1B2D` | Primary text | 17.3:1 on surface |
| `--ec-text-secondary` | `#46546A` | Secondary text, table body | 7.7:1 on surface |
| `--ec-text-muted` | `#5F6B7E` | Metadata, captions, axis labels | 5.4:1 on surface · 4.9:1 on subtle |
| `--ec-navy` | `#0B1F3A` | App bar, banner, brand surfaces | — |
| `--ec-on-navy` | `#FFFFFF` | Text on navy | 16.5:1 |
| `--ec-on-navy-secondary` | `#B9C6DA` | Secondary text on navy | 9.6:1 |
| `--ec-primary` | `#1D4FA8` | Primary buttons, links, selected states | 7.7:1 on surface |
| `--ec-primary-hover` | `#173F87` | Hover/pressed for primary | — |
| `--ec-on-primary` | `#FFFFFF` | Text on primary fill | 7.7:1 |
| `--ec-primary-subtle` | `#EAF1FB` | Selected row, info callout background | — |
| `--ec-focus` | `#2563C9` | Focus ring | 5.7:1 on surface |

### 3.3 Status colors (light)

| State | Text / icon | Background | Border | Text contrast on its background |
|---|---|---|---|---|
| **Success** — pass, gate PASS | `#11713A` | `#E7F4EC` | `#A9D8BA` | 5.4:1 |
| **Danger** — fail, gate FAIL | `#B42318` | `#FDECEB` | `#F3B4AE` | 5.8:1 |
| **Warning** — error, gate INCONCLUSIVE, flaky | `#8A5100` | `#FEF4E1` | `#F2CF8D` | 5.9:1 |
| **Info** | `#1D4FA8` | `#EAF1FB` | `#B7CCEE` | 6.8:1 |
| **Neutral** — skipped, not applicable | `#46546A` | `#EEF1F5` | `#DDE3EC` | 6.8:1 |

### 3.4 Dark theme

Dark mode is a designed theme, not an automatic inversion. The report follows the viewer's system setting and offers a toggle.

| Token | Hex | Contrast |
|---|---|---|
| `--ec-bg` | `#0B1220` | — |
| `--ec-surface` | `#111A2B` | — |
| `--ec-surface-subtle` | `#172238` | — |
| `--ec-border` | `#26324A` | — |
| `--ec-border-strong` | `#5E6C86` | 3.3:1 on surface |
| `--ec-text` | `#E8EDF5` | 14.8:1 on surface |
| `--ec-text-secondary` | `#A9B6CA` | 8.5:1 |
| `--ec-text-muted` | `#8C99AE` | 6.0:1 |
| `--ec-navy` (app bar) | `#0B1220` + bottom border `#26324A` | — |
| `--ec-primary` / links | `#7AA5F2` | 7.0:1 on surface |
| `--ec-on-primary` | `#0B1220` | 7.6:1 on primary |
| `--ec-primary-subtle` | `#14264A` | — |
| Success text / bg | `#5BC995` / `#0F2A1F` | 7.5:1 |
| Danger text / bg | `#F28B80` / `#3A1715` | 6.7:1 |
| Warning text / bg | `#E9B355` / `#33260C` | 7.8:1 |

All text pairs above meet WCAG 2.1 AA (4.5:1 for body text); interactive borders meet 3:1. Ratios were computed, not estimated — re-run the check whenever a token changes.

### 3.5 Chart colors

Chart series use a separate categorical palette, assigned **in fixed order and never cycled**. It was validated for lightness, chroma, color-vision-deficiency (CVD) separation and contrast against each theme's surface.

| Slot | Hue | Light | Dark | Default meaning in Evalcrest |
|---|---|---|---|---|
| 1 | Blue | `#2563C9` | `#4A82E0` | `normal` cases · "current run" |
| 2 | Orange | `#D9761A` | `#CF6E17` | `edge` cases |
| 3 | Teal | `#0F9488` | `#12998C` | `adversarial` cases |
| 4 | Violet | `#7A52D1` | `#8E73E6` | 4th series (line/bar charts only) |
| 5 | Magenta | `#C2407F` | `#D4558F` | 5th series (line/bar charts only) |

**Validation results**

- Slots 1–5, adjacent pairs (bars, lines): pass in both themes — worst CVD ΔE 12.5 light / 13.6 dark; worst normal-vision ΔE 18.4 / 17.6; all ≥ 3:1 on surface.
- Slots 1–3, all pairs (scatter, maps, small multiples): pass in both themes.
- Slots 1–4 under all pairs **fail** (blue and violet are too close for some readers). Charts where every pair can sit side by side are therefore **capped at three series**; fold the rest into "Other" or split into small multiples.

**Chart rules for color**

- **Color follows the entity, not its rank.** `edge` is always orange, in every chart, in every filter state.
- **One hue for nominal bars.** A bar chart of root causes or agents uses slot 1 for every bar — the labels carry identity.
- **Status meaning wears status colors.** Pass/fail counts use success/danger tokens, never chart slots. One chart never mixes the two.
- **Comparisons:** baseline = `--ec-text-muted` gray, current = slot 1.
- **Sequential** (heatmaps, confusion matrices): one blue ramp, light → dark. **Never** a rainbow.
- **Ink:** values, labels and legends use text tokens, never the series color.
- **Grid** `#E6EAF0` light / `#1F2A40` dark; axis labels `--ec-text-muted`.

---

## 4. Typography

**Typefaces**

| Role | Family | Fallback stack |
|---|---|---|
| UI and text | **Inter** (variable) | `system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` |
| Code, IDs, hashes | **JetBrains Mono** | `ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace` |

Both are open-source (SIL OFL). The self-contained HTML report uses the fallback stacks by default to stay small and offline; the layout must never depend on a specific font's metrics.

**Type scale** (px / line height / weight)

| Token | Size | Line | Weight | Use |
|---|---|---|---|---|
| `display` | 32 | 40 | 600 | Report title, README banner |
| `h1` | 24 | 32 | 600 | Page title |
| `h2` | 20 | 28 | 600 | Section titles |
| `h3` | 16 | 24 | 600 | Card and panel titles |
| `kpi` | 28 | 36 | 600 | KPI tile values |
| `body` | 14 | 22 | 400 | Default UI and tables (data-dense) |
| `body-lg` | 16 | 26 | 400 | Long-form prose (docs, rationale panels) |
| `label` | 12 | 16 | 600 | Form labels, section eyebrows (uppercase, +0.06em) |
| `caption` | 12 | 16 | 400 | Metadata, footnotes, `n =` counts |
| `mono` | 13 | 20 | 400 | Case IDs, source IDs, hashes, JSON |

**Rules**

- Sentence case for all headings, buttons and labels. Uppercase only for `label` eyebrows.
- 12 px is the minimum size anywhere.
- `font-variant-numeric: tabular-nums` in tables, axis ticks and anything that aligns vertically.
- Line length for prose: 60–80 characters.
- Two weights in practice: 400 and 600. No light or black weights.

---

## 5. Layout and spacing

**Spacing scale** (4 px base): `4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64` → tokens `--ec-space-1` … `--ec-space-10`.

- Inside components: 8–16. Between components: 24. Between page sections: 48.

**Grid.** 12 columns, max content width **1200 px**, gutters 24 px (16 px under 768 px). Side padding 32 px desktop, 16 px mobile.

| Breakpoint | Width | Layout change |
|---|---|---|
| `sm` | ≥ 640 px | KPI tiles 2-up |
| `md` | ≥ 768 px | Case detail opens as a side panel instead of full screen |
| `lg` | ≥ 1024 px | KPI tiles 4-up; charts side by side |
| `xl` | ≥ 1280 px | Content stays capped at 1200 px |

**Shape**

| Token | Value | Use |
|---|---|---|
| `--ec-radius-sm` | 4 px | Badges, tags, inputs |
| `--ec-radius-md` | 6 px | Buttons, tooltips |
| `--ec-radius-lg` | 8 px | Cards, panels, banners |

**Elevation.** Prefer borders to shadows.

| Level | Shadow | Use |
|---|---|---|
| 0 | none, 1 px `--ec-border` | Cards, tables |
| 1 | `0 1px 2px rgba(15,27,45,.06), 0 1px 3px rgba(15,27,45,.08)` | Sticky table header, app bar |
| 2 | `0 8px 24px rgba(15,27,45,.12)` | Tooltips, popovers, side panel |

**Motion.** 120–200 ms, ease-out, only for state changes (expanding a row, opening a panel, showing a tooltip). No decorative animation. Respect `prefers-reduced-motion` by removing transitions.

**Icons.** Lucide (ISC license), outline style, 1.75 px stroke. 16 px inline and in badges, 20 px in headers. Icons always sit beside a text label, except icon-only buttons, which require an `aria-label` and a tooltip.

---

## 6. Components

### 6.1 App bar

Navy (`--ec-navy`), 56 px tall, full width. Left: mark + wordmark. Center-left: breadcrumb — `Target · Suite · Run`, e.g. `StudyBuddy · smoke · 2026-12-14 09:41 UTC`. Right: theme toggle and "Download JSON". Text in `--ec-on-navy` / `--ec-on-navy-secondary`.

### 6.2 Gate verdict banner

The first thing below the app bar. Full content width, `--ec-radius-lg`, 4 px left border in the status color, status-subtle background.

| Decision | Icon | Title | Color |
|---|---|---|---|
| PASS | `circle-check` | Gate passed | Success |
| FAIL | `octagon-x` | Gate failed | Danger |
| INCONCLUSIVE | `triangle-alert` | Gate inconclusive | Warning |

Body: one bullet per reason, each specific and quantified — for example *"Pass rate 81.3% is below the 85.0% threshold (26 of 32 cases)"*. Right side: baseline reference (`vs main @ 3f2a91c`). On PASS, a single line confirms which checks ran.

### 6.3 KPI tile

Surface card, 16 px padding. Structure: `label` eyebrow → `kpi` value → caption with the denominator and delta vs baseline.

- Delta shows direction with an arrow icon **and** a sign (`▲ +2.1 pp`, `▼ −4.1 pp`). Color the delta with success/danger only when "up" has an unambiguous meaning (pass rate up = good, cost up = bad).
- Default tiles: **Pass rate**, **Critical failures**, **Weakest criterion**, **Cost · duration**.

### 6.4 Criterion bar (bullet chart)

One row per criterion: name (left, 160 px) → horizontal bar of the mean score on a 0–1 scale → a 2 px vertical threshold tick → value and `n` (right, tabular). The bar uses slot 1; a criterion below its threshold switches the value text to danger and adds a `circle-x` icon. The threshold tick is labeled in the tooltip and in the legend line under the chart.

### 6.5 Status badge

Inline, 20 px tall, `--ec-radius-sm`, 12 px `label`-weight text, 14 px icon, status-subtle background with status border.

| Badge | Icon | Tokens |
|---|---|---|
| Pass | `check` | Success |
| Fail | `x` | Danger |
| Error | `triangle-alert` | Warning |
| Skipped | `minus` | Neutral |
| N/A | — | Neutral, text only |
| Flaky (modifier) | `shuffle` | Warning outline, shown next to the outcome badge |

### 6.6 Tags and chips

- **Category tag** (`Normal` / `Edge` / `Adversarial`): neutral chip with an 8 px dot in the category's chart color, so it matches the charts.
- **Subtype tag** (`multi_hop`, `cross_tenant_leak`): mono, neutral, no color.
- **Root-cause chip** (`Retrieval miss`, `Hallucination`, `Tool error`, …): neutral chip with an icon per cause — `search-x` (retrieval miss), `message-square-warning` (hallucination), `pen-off` (generation error), `quote` (citation error), `shield-alert` (safety violation), `wrench` (tool error), `server-crash` (infra error), `circle-help` (unknown). Root causes are never color-coded; there are too many to stay distinguishable, and none of them is "good".
- **Critical marker**: small danger-outline tag `Critical` on cases that block the gate.

### 6.7 Results table

The workhorse of the report.

- Columns: Outcome · Case ID (mono) · Category · Subtype · Question (truncated to one line) · Criteria (four mini-badges) · Root cause · Latency.
- Default sort: failures first, then errors, then by case ID. Every column sortable.
- Filter bar above, in one row: search, Outcome, Category, Root cause, "Critical only". Active filters show as removable chips and a result count (`Showing 6 of 32`).
- 44 px rows, zebra striping with `--ec-surface-subtle`, sticky header (elevation 1), horizontal scroll inside the card on small screens.
- Row click or `Enter` opens the case detail. Focus is visible on rows.

### 6.8 Case detail panel

Side panel (≥ 768 px) or full screen (< 768 px). Sections in this order:

1. **Header** — case ID, outcome badge, category and subtype tags, critical marker.
2. **Question** — the exact input, with test account and turn history if any.
3. **Expected** — behavior, expected answer, key facts.
4. **Actual answer** — target output rendered **as plain text**. Claims the Judge marked *unsupported* get a dotted danger underline; *contradicted* claims get a danger-subtle highlight. Each highlight carries an icon and a tooltip, so meaning never depends on color alone.
5. **Sources** — cited vs gold comparison: `✓ cited and gold`, `✕ gold but not cited`, `! cited but not gold` (with support-check result). For white-box targets, retrieved chunks with rank and score.
6. **Judgments** — one row per criterion: badge, score, method (`deterministic` / `llm` / `hybrid`), rationale, evidence.
7. **Diagnosis** — root-cause chip, confidence, the rule that fired and its evidence, explanation. Hypotheses are labeled "Hypothesis".
8. **Links** — target trace, judge trace (LangSmith), raw JSON.

### 6.9 Failure cluster card

Card per cluster, sorted by size. Header: root-cause chip + cluster title + count (`7 cases`). Body: fix hypothesis (labeled), up to three representative case IDs as links, and "View all 7" which filters the results table.

### 6.10 Run metadata panel

Definition list in two columns at the bottom of the report: run ID, trigger, git ref, target version, suite version, Evalcrest version, models, prompt versions, config hash, started/finished (ISO 8601, UTC), duration, cost by agent. Values in mono with a copy button.

### 6.11 Buttons and controls

| Variant | Fill | Text | Use |
|---|---|---|---|
| Primary | `--ec-primary` | `--ec-on-primary` | One per view at most |
| Secondary | `--ec-surface`, 1 px `--ec-border-strong` | `--ec-text` | Most actions |
| Ghost | transparent | `--ec-primary` | Low-emphasis, inline |
| Danger | Danger text color as fill | White (light) / `#0B1220` (dark) | Destructive actions (dashboard only) |

Heights: 28 px (small), 36 px (default). Minimum target 24 × 24 px. States: default, hover, active, focus (2 px `--ec-focus` ring with 2 px offset), disabled (40% opacity, no pointer).

Inputs and selects: 36 px, `--ec-radius-sm`, 1 px `--ec-border-strong`, label above in `label` style, helper or error text below. Error state uses danger border plus an icon and message.

### 6.12 Feedback states

| State | Pattern | Example copy |
|---|---|---|
| Empty — no failures | Success callout | "No failures in this run. 32 of 32 cases passed." |
| Empty — filters | Neutral text + reset link | "No cases match these filters. Clear filters" |
| Partial run | Warning callout at top | "Run stopped at the $0.50 budget. 24 of 32 cases were judged; the gate is inconclusive." |
| Target unreachable | Danger callout with next step | "Couldn't reach StudyBuddy at localhost:8000 (timed out after 30 s). Start the target, then run `evalcrest run --resume <run_id>`." |
| Loading (dashboard) | Skeleton rows, no spinners over 300 ms | — |

### 6.13 Code and JSON blocks

`--ec-surface-subtle` background, 1 px border, `mono` text, 12 px padding, copy button top-right, horizontal scroll (no wrapping for JSON). Long payloads collapse after 20 lines with "Show all".

---

## 7. Report anatomy

```text
┌───────────────────────────────────────────────────────────────────────┐
│ ▣ Evalcrest     StudyBuddy · smoke · 2026-12-14 09:41 UTC      ◐  ⤓ │  App bar (navy)
├───────────────────────────────────────────────────────────────────────┤
│ ✕ Gate failed                                     vs main @ 3f2a91c  │  Verdict banner
│   • Pass rate 81.3% is below the 85.0% threshold (26 of 32 cases)     │
│   • 1 critical safety case failed: sb-adv-0007                        │
├─────────────────┬─────────────────┬─────────────────┬─────────────────┤
│ PASS RATE       │ CRITICAL FAILS  │ WEAKEST         │ COST · TIME     │  KPI tiles
│ 81.3%           │ 1               │ Citation 0.76   │ $0.31 · 4m 12s  │
│ ▼ −4.1 pp, n=32 │ of 6 critical   │ min 0.80, n=22  │ 192 LLM calls   │
├─────────────────┴─────────────────┴─────────────────┴─────────────────┤
│ Quality by criterion           │ Pass rate by category                │  Charts
│ Correctness   ███████████▏|    │ Normal       ███████████  85.0%      │
│ Faithfulness  ████████████|▏   │ Edge         ████████     66.7%      │
│ Citation      █████████▏  |    │ Adversarial  ██████████   83.3%      │
│ Safety        ██████████████   │                                       │
├───────────────────────────────────────────────────────────────────────┤
│ Failure clusters (v1)                                                 │  Cluster cards
│ [Retrieval miss · Lecture 7 formulas · 3]  [Hallucination · … · 2]    │
├───────────────────────────────────────────────────────────────────────┤
│ Results   [Search] [Outcome ▾] [Category ▾] [Root cause ▾] Showing 32 │  Results table
│ ✕ Fail  sb-normal-0042  Normal  multi_hop  Which sorting algorithm…   │
│ …                                                                     │
├───────────────────────────────────────────────────────────────────────┤
│ Run metadata · versions · models · config hash · cost by agent        │  Metadata
└───────────────────────────────────────────────────────────────────────┘
```

The sketch is illustrative but internally consistent (20 normal, 6 edge and 6 adversarial cases; 26 of 32 pass). Real reports compute every number from stored results.

**Order is fixed:** verdict → KPIs → charts → clusters → results → metadata. A reviewer can stop reading at any point and still have the most important information.

**Print.** A print stylesheet removes the theme toggle and filters, expands all failed cases inline, keeps charts in color with patterns as backup, and adds page breaks before Results and Metadata.

---

## 8. Data visualization

| Question the reader has | Form | Notes |
|---|---|---|
| Did the gate pass? | Verdict banner | Not a chart |
| What are the headline numbers? | KPI tiles | Value + `n` + delta |
| Is each criterion above its threshold? | Bullet bars ([§6.4](#64-criterion-bar-bullet-chart)) | 0–1 scale, threshold tick |
| How does each category or subtype perform? | Horizontal bars, sorted descending | Slot colors for categories; one hue for subtypes |
| What is breaking? | Root causes as horizontal bars, sorted by count | One hue; **never a pie** |
| Are we improving across runs? | Line chart of pass rate | Dashed threshold line; baseline marker |
| Did the fixes work? | Dumbbell chart, before → after per category | Before gray, after slot 1 |
| Can the Judge be trusted? | 2 × 2 confusion matrix per criterion | Sequential blue; agreement, κ and 95% CI under each |
| What did it cost? | Horizontal bars by agent | One hue; total in a KPI tile |

**Mark specifications**

- Bars: 4 px rounded data end, square at the baseline; 2 px surface gap between adjacent bars; bars start at zero.
- Lines: 2 px; point markers ≥ 8 px with a 2 px surface ring where marks overlap.
- One y-axis per chart. Two measures of different scale get two charts.
- Legend for two or more series; up to four series are also labeled directly at the line end. A single series needs no legend — the title names it.
- Gridlines are hairlines and horizontal only. No 3D, no shadows on marks, no gradients.
- Label values selectively (end of bar, last point) — never a number on every point.
- Every chart has a title stating the takeaway in plain words when possible, a caption with `n` and the data source, and a "View as table" toggle.

**Implementation.** Charts in the report are inline SVG rendered at build time (Python), so they work offline, print cleanly and need no JavaScript library. Each chart includes `<title>` and `<desc>`, and hover tooltips are a small progressive enhancement.

---

## 9. Content and voice

**Voice:** precise, neutral, specific. Write like a senior QA engineer summarizing a test run for a release meeting.

| Do | Don't |
|---|---|
| "Pass rate 81.3% (26 of 32), below the 85.0% threshold." | "Quality looks a bit low!" |
| "Likely cause (hypothesis): chunk boundary splits the formula." | "The chunking is broken." |
| "Couldn't reach the target. Start it, then resume the run." | "Oops! Something went wrong 😕" |
| "Gate inconclusive: 3 of 32 cases errored (9.4% > 5.0%)." | "Unknown error." |

**Formats**

| Value | Format | Example |
|---|---|---|
| Percentages | 1 decimal | `81.3%` |
| Percentage change | percentage points | `−4.1 pp` |
| Scores | 2 decimals, 0–1 | `0.76` |
| Cost | USD, 2 decimals (4 below $0.01) | `$0.31`, `$0.0042` |
| Duration | largest two units | `4m 12s` |
| Timestamps | ISO 8601, UTC in metadata | `2026-12-14 09:41 UTC` |
| Counts | always with the denominator | `26 of 32` |
| IDs and hashes | mono, short SHA (7 characters) | `3f2a91c` |

Terminology follows the PRD glossary. Use "case", not "test" or "sample"; "run", not "execution"; "target", not "app under test".

---

## 10. Accessibility

Target: **WCAG 2.1 AA** for every surface.

- Text contrast ≥ 4.5:1 (≥ 3:1 for text ≥ 18.66 px bold); interactive borders and chart marks ≥ 3:1 against their background. All tokens in §3 meet this.
- Status, outcome and verdict always use color **+ icon + text**.
- Full keyboard use: skip link to results, logical tab order, `Enter`/`Space` to open a case, `Esc` to close the panel and return focus to the row.
- Visible 2 px focus ring on everything focusable; never `outline: none` without a replacement.
- Landmarks (`header`, `main`, `nav`, `footer`) and one `h1` per page; table headers with `scope`; sortable columns expose `aria-sort`.
- Charts: `<title>` + `<desc>` and a data-table alternative.
- Respect `prefers-reduced-motion`, `prefers-color-scheme` and `forced-colors` (in forced colors, chart bars fall back to patterns).
- Minimum target size 24 × 24 px.
- Target output is rendered as escaped plain text — accessibility and security agree here.

---

## 11. Recruiter-facing surfaces

The README and a sample report are the first things a reviewer sees. They follow the same system.

### 11.1 README structure

1. **Banner** — navy, 1280 × 320, mark + wordmark + tagline. No imagery.
2. **Badge row** — CI status, Evalcrest gate status, Python version, license, test coverage.
3. **One-paragraph pitch** — what it is, who it's for, the first target.
4. **Results** — a table with the four measured numbers (judge accuracy with κ and CI, StudyBuddy before → after, gate effectiveness, cost per run), each linking to its method.
5. **Report screenshot** — light theme, 1440 px wide, cropped to verdict + KPIs + charts; plus a link to the hosted sample report.
6. **Architecture diagram** — the Mermaid system-context diagram styled with house colors.
7. **Demo** — a 60–90 second clip: a PR is blocked by the gate, the Diagnostician points to a retrieval miss, the fix lands, the gate passes.
8. **Quick start** — three commands.
9. **Design decisions** — links to the ADRs.

Rules: no emoji in headings, no stock images, no "revolutionary" language, and no number without its method.

### 11.2 Diagram style

Mermaid diagrams use house colors so they look like one family:

```text
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#FFFFFF','primaryBorderColor':'#7D8A9E','primaryTextColor':'#0F1B2D',
  'lineColor':'#46546A','fontFamily':'Inter, system-ui, sans-serif'}}}%%
classDef core fill:#0B1F3A,stroke:#0B1F3A,color:#FFFFFF;
classDef external fill:#F1F4F9,stroke:#7D8A9E,color:#0F1B2D;
classDef store fill:#EAF1FB,stroke:#1D4FA8,color:#0F1B2D;
```

Evalcrest components use `core`, third-party systems `external`, databases and storage `store`. Arrows are labeled with what flows, not with verbs like "uses".

### 11.3 PR comment

GitHub-flavored Markdown, in this order: verdict line with an icon (`✅ Evalcrest gate passed` / `❌ Evalcrest gate failed` / `⚠️ Evalcrest gate inconclusive`), the reasons, a compact table (pass rate, each criterion vs threshold, critical failures, cost, duration, delta vs `main`), up to five failing cases with links, and a link to the full report artifact. Updated in place on every push.

---

## 12. Design tokens (CSS)

```css
:root {
  color-scheme: light;
  /* surfaces */
  --ec-bg: #F6F8FB;  --ec-surface: #FFFFFF;  --ec-surface-subtle: #F1F4F9;
  --ec-border: #DDE3EC;  --ec-border-strong: #7D8A9E;
  /* text */
  --ec-text: #0F1B2D;  --ec-text-secondary: #46546A;  --ec-text-muted: #5F6B7E;
  /* brand and action */
  --ec-navy: #0B1F3A;  --ec-on-navy: #FFFFFF;  --ec-on-navy-secondary: #B9C6DA;
  --ec-primary: #1D4FA8;  --ec-primary-hover: #173F87;  --ec-on-primary: #FFFFFF;
  --ec-primary-subtle: #EAF1FB;  --ec-focus: #2563C9;
  /* status */
  --ec-success: #11713A;  --ec-success-subtle: #E7F4EC;  --ec-success-border: #A9D8BA;
  --ec-danger: #B42318;   --ec-danger-subtle: #FDECEB;   --ec-danger-border: #F3B4AE;
  --ec-warning: #8A5100;  --ec-warning-subtle: #FEF4E1;  --ec-warning-border: #F2CF8D;
  --ec-neutral-subtle: #EEF1F5;
  /* charts */
  --ec-chart-1: #2563C9;  --ec-chart-2: #D9761A;  --ec-chart-3: #0F9488;
  --ec-chart-4: #7A52D1;  --ec-chart-5: #C2407F;
  --ec-chart-grid: #E6EAF0;
  /* type */
  --ec-font-sans: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --ec-font-mono: "JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  /* shape and space */
  --ec-radius-sm: 4px;  --ec-radius-md: 6px;  --ec-radius-lg: 8px;
  --ec-space-1: 4px;  --ec-space-2: 8px;  --ec-space-3: 12px;  --ec-space-4: 16px;  --ec-space-5: 20px;
  --ec-space-6: 24px; --ec-space-7: 32px; --ec-space-8: 40px;  --ec-space-9: 48px;  --ec-space-10: 64px;
  --ec-shadow-1: 0 1px 2px rgba(15,27,45,.06), 0 1px 3px rgba(15,27,45,.08);
  --ec-shadow-2: 0 8px 24px rgba(15,27,45,.12);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --ec-bg: #0B1220;  --ec-surface: #111A2B;  --ec-surface-subtle: #172238;
    --ec-border: #26324A;  --ec-border-strong: #5E6C86;
    --ec-text: #E8EDF5;  --ec-text-secondary: #A9B6CA;  --ec-text-muted: #8C99AE;
    --ec-navy: #0B1220;
    --ec-primary: #7AA5F2;  --ec-primary-hover: #9BBCF6;  --ec-on-primary: #0B1220;
    --ec-primary-subtle: #14264A;  --ec-focus: #7AA5F2;
    --ec-success: #5BC995;  --ec-success-subtle: #0F2A1F;  --ec-success-border: #1E5A3E;
    --ec-danger: #F28B80;   --ec-danger-subtle: #3A1715;   --ec-danger-border: #7A2E27;
    --ec-warning: #E9B355;  --ec-warning-subtle: #33260C;  --ec-warning-border: #6B4E12;
    --ec-neutral-subtle: #1C2740;
    --ec-chart-1: #4A82E0;  --ec-chart-2: #CF6E17;  --ec-chart-3: #12998C;
    --ec-chart-4: #8E73E6;  --ec-chart-5: #D4558F;
    --ec-chart-grid: #1F2A40;
    --ec-shadow-1: 0 1px 2px rgba(0,0,0,.4);
    --ec-shadow-2: 0 8px 24px rgba(0,0,0,.5);
  }
}

/* Theme toggle: the same dark values under [data-theme="dark"] */
:root[data-theme="dark"] { /* …identical to the dark block above… */ }

body { background: var(--ec-bg); color: var(--ec-text); font: 400 14px/22px var(--ec-font-sans); }
```

Tokens are the only place raw hex values appear. Components reference tokens, never hex.

---

## 13. Do and don't

| Do | Don't |
|---|---|
| Lead with the verdict and its reasons | Lead with charts or a logo hero |
| Show `n` next to every percentage | Show a percentage without its count |
| Use neutral surfaces and let status color mark what needs attention | Color whole sections, rows or headers for decoration |
| Pair every status color with an icon and a word | Rely on red/green alone |
| Use horizontal bars for categories and root causes | Use pies, donuts, 3D or dual-axis charts |
| Render target output as escaped text | Render target HTML or Markdown as live content |
| Keep one primary button per view | Put several competing primary actions side by side |
| Label hypotheses as hypotheses | Present a guessed root cause as fact |