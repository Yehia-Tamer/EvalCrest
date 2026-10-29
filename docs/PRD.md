# Evalcrest — Product Requirements Document

| | |
|---|---|
| **Product** | Evalcrest — a multi-agent QA system for LLM applications |
| **Owner** | Yahia Tamer Nour |
| **Status** | Draft v0.1 |
| **Last updated** | 2026-10-29 |
| **Related docs** | [Architecture.md](./Architecture.md) · [Agents.md](./Agents.md) · [Design.md](./Design.md) |

---

## 1. Summary

Evalcrest tests LLM applications the way a QA team would. Point it at an AI app's API — a RAG chatbot or an agent — and a team of agents:

1. **designs** test cases from the app's own knowledge base (normal questions with expected answers and sources, edge cases, and adversarial attacks),
2. **runs** them against the app,
3. **judges** each response for correctness, faithfulness, citation accuracy and safety,
4. **diagnoses** why failures happened (retrieval miss, hallucination, tool error) using the app's traces, and
5. **reports** the result as a readable HTML report and a pass/fail gate in CI.

> **In one line:** regression tests and a CI gate for RAG apps — generated, judged and explained by agents, with every judgment measured against human labels.

The first target is **StudyBuddy AI**, a RAG study assistant the owner built and deployed. Evalcrest is engineered as a flagship portfolio project, so every headline claim must be backed by a measured number (see [§10](#10-success-metrics)).

---

## 2. Problem

**LLM apps fail quietly.** A RAG app can return a fluent answer that is wrong, unsupported by its sources, or backed by a citation that doesn't say what the answer claims. Nothing crashes, so nothing alerts.

**Changes regress quality without warning.** A new prompt, a different chunk size, a larger `k`, or a model upgrade can silently break answers that used to be right. Most small teams catch this by manually trying a few questions before merging — which isn't repeatable and doesn't scale.

**Test sets are expensive to write by hand.** A useful RAG test needs a question, a correct answer, and the exact source that supports it. Writing 200 of those by hand takes days, so it rarely happens.

**A failing score doesn't say what to fix.** "Correctness: 0.71" doesn't tell you whether the retriever missed the document, the generator ignored it, or a tool call failed. Developers end up debugging symptoms one case at a time.

**Security is tested ad hoc, if at all.** Prompt injection (direct and through poisoned documents), system-prompt leakage, cross-user data leakage and jailbreaks are real risks for any app that answers questions over private documents.

**Concretely, for StudyBuddy today:** there is no automated regression suite. Changes to chunking, prompts or models ship on manual spot checks.

### 2.1 Prior art and positioning

Mature open-source and commercial tools already cover parts of this space — for example RAGAS and DeepEval (RAG metrics), promptfoo (prompt testing and red-teaming), and LangSmith's evaluation features. Evalcrest does not try to out-feature them on metric breadth. Its focus is the **closed loop**:

`knowledge base → generated & validated tests → execution → judging → trace-based root cause → CI gate`

…with each stage **measured** (test validity, judge agreement with humans, diagnosis accuracy, gate effectiveness, cost). Where a well-established metric definition exists, Evalcrest adopts it and cites it rather than inventing a new one.

---

## 3. Goals and non-goals

### 3.1 Goals

| ID | Goal |
|---|---|
| G1 | Generate a useful, source-grounded test suite from a RAG app's knowledge base with minimal human effort. |
| G2 | Run suites reproducibly and record everything needed to reproduce any result. |
| G3 | Judge responses on four criteria, with judge accuracy measured against human labels before it is trusted. |
| G4 | Explain failures by root cause using the target's traces, grouped so developers fix causes, not symptoms. |
| G5 | Block regressions in CI with a gate that is fast, cheap and not flaky. |
| G6 | Publish measured results — judge accuracy, before/after pass rate, gate effectiveness, cost per run. |

### 3.2 Non-goals (through v2)

- **Not a general model benchmark.** Evalcrest tests a specific application against its own knowledge, not models against public leaderboards.
- **Not a hosted multi-tenant SaaS.** It is a single-owner tool that runs locally, in CI, and on the owner's AWS account.
- **Not for testing apps you don't own.** Adversarial testing of third-party apps without written permission is out of scope and blocked in code.
- **Not an auto-fixer.** The Diagnostician proposes hypotheses and fixes; a human changes the target app.
- **Not production monitoring.** Evalcrest runs offline and in CI. Online monitoring of live traffic is a possible future direction.
- **Not full agent-trajectory evaluation.** v2 detects tool errors from traces; scoring whole multi-step trajectories is future work.

---

## 4. Users

| Persona | Who | What they need |
|---|---|---|
| **P1 — App developer** (primary) | The owner maintaining StudyBuddy; more generally a small team shipping a RAG app. | Know before merging whether a change broke something, and know *what* to fix when it did. |
| **P2 — Reviewer** (secondary) | An engineer, hiring manager or recruiter reading the README or a sample report. | Understand in 30 seconds what was tested, the verdict, and the evidence — and trust the numbers. |
| **P3 — CI pipeline** (system) | GitHub Actions running on every pull request. | A deterministic exit code, machine-readable output, and bounded runtime and cost. |

---

## 5. Key scenarios (user stories)

| ID | Story |
|---|---|
| US-1 | As a developer, I run one command to generate a test suite from my app's knowledge base, review the drafts, and commit the approved cases. |
| US-2 | As a developer, I run a suite against my local, staging or deployed app and get an HTML report with a clear verdict. |
| US-3 | As a developer, I open a failed case and see the question, expected answer, actual answer, cited and retrieved sources, the judge's rationale per criterion, and the diagnosed root cause. |
| US-4 | As a developer, I see failures grouped into root-cause clusters, each with a fix hypothesis, so I fix one cause instead of twelve symptoms. |
| US-5 | As a developer, every pull request to StudyBuddy runs a smoke suite that blocks the merge if quality drops below thresholds or regresses against `main`. |
| US-6 | As a developer, I run adversarial tests against my own app, and the system refuses to run them against any target that isn't authorized. |
| US-7 | As a developer, I measure how often the judge agrees with my own labels before I rely on it to gate merges. |
| US-8 | As a developer, I see what each run cost and how long it took. |
| US-9 | As a reviewer, I read the top of a report and understand the verdict without reading individual cases. |

---

## 6. Releases and milestones

Phases follow the IBM RAG & Agentic AI certificate. Dates after the MVP are estimates and move with course pace.

| Milestone | Target date | Scope | Exit criteria |
|---|---|---|---|
| **M0 — Foundations** | Oct 2026 | Repo, CI, Postgres, LangGraph state schema, target registry, StudyBuddy eval endpoints | `evalcrest target check studybuddy` passes against local StudyBuddy |
| **M1 — Design & Run** (Course 7) | Nov 2026 | Test Designer (normal + edge), Runner, YAML suites, CLI | ≥ 40 approved normal cases run end to end, results stored |
| **M2 — MVP** | **31 Dec 2026** | Baseline Judge (4 criteria), adversarial starter set, HTML report, one-command pipeline | See [§6.1](#61-mvp-acceptance-criteria) |
| **M3 — Diagnose** (Course 8) | Jan 2027 (est.) | Diagnostician, judge calibration, CrewAI/AG2 comparison (BeeAI optional) | Orchestration ADR with measured comparison; diagnosis accuracy measured on FaultyBuddy |
| **M4 — v1** (Course 9) | Feb 2027 (est.) | MCP target adapter, AWS deployment, nightly runs, CI gate on StudyBuddy PRs | Gate runs on every StudyBuddy PR; nightly run on AWS publishes a report |
| **M5 — v2** | **Mar 2027** | Measured results in README, before/after fixes, trend history | All four headline numbers published with method and sample size |

### 6.1 MVP acceptance criteria

The MVP is done when, against a local StudyBuddy instance:

1. `evalcrest generate --target studybuddy` produces draft cases with gold answers and gold source IDs from the StudyBuddy corpus, and ≥ 90% of a 20-case random sample is rated valid by the owner.
2. The approved suite contains **≥ 60 cases**: ≥ 40 normal, ≥ 10 edge, ≥ 10 adversarial.
3. `evalcrest run --target studybuddy --suite full` executes every case with bounded concurrency and stores raw responses, latency and errors in Postgres.
4. Every response is judged on all applicable criteria, with a structured verdict, score and rationale.
5. A single self-contained HTML report is produced, following [Design.md](./Design.md).
6. The whole pipeline runs with **one command** (`evalcrest pipeline --target studybuddy`), and every Evalcrest LLM call appears in LangSmith tagged with run and case IDs.
7. Run cost and runtime are recorded and shown in the report.

---

## 7. Scope matrix

| Capability | MVP (Dec 2026) | v1 (after Course 9) | v2 (Mar 2027) |
|---|---|---|---|
| HTTP target adapter | ✅ | ✅ | ✅ |
| MCP target adapter | — | ✅ | ✅ |
| Normal + edge case generation | ✅ | ✅ | ✅ |
| Adversarial generation | Starter set (≥ 10) | Full attack library | Full attack library |
| Runner (concurrency, retries, timeouts) | ✅ | + resume, multi-turn | + repeated sampling |
| Judge — 4 criteria | Baseline | Calibrated | Calibrated + published accuracy |
| Diagnostician | — | ✅ | + before/after comparison |
| HTML report | ✅ | + clusters, JUnit, PR comment | + trends |
| CI gate (GitHub Actions) | — | ✅ | ✅ measured on seeded PRs |
| AWS deployment | — | ✅ | ✅ |
| REST API | Minimal | ✅ | ✅ |

---

## 8. Functional requirements

Priority: **P0** = required for its release · **P1** = should have · **P2** = nice to have.

### 8.1 Targets

| ID | Requirement | Release | Pri |
|---|---|---|---|
| FR-T1 | Register a target in `evalcrest.yaml`: name, base URL, adapter (`http` \| `mcp`), auth reference, capability level, authorization. | MVP | P0 |
| FR-T2 | Every target declares `authorization: owned \| permitted \| none`. `permitted` requires a reference to written permission, its scope, and an expiry date. | MVP | P0 |
| FR-T3 | Adversarial suites run only if authorization is `owned` or an unexpired `permitted` **and** `adversarial_enabled: true`. The check is enforced by the Runner in code, and refusals are logged. | MVP | P0 |
| FR-T4 | Health check (`/health`, `/version`) before every run; abort with an actionable error if the target is unreachable or the version can't be read. | MVP | P0 |
| FR-T5 | Capability levels — **black-box** (answer only), **grey-box** (answer + citations), **white-box** (+ retrieved contexts and trace ID). Features degrade gracefully at lower levels. | MVP | P0 |
| FR-T6 | MCP adapter so any app exposing the Evalcrest target contract over MCP can be tested without custom code. | v1 | P0 |
| FR-T7 | Agent targets: extract tool calls and tool errors from traces. | v2 | P1 |

### 8.2 Test design

| ID | Requirement | Release | Pri |
|---|---|---|---|
| FR-D1 | Ingest the target's knowledge source (directory, S3 prefix, or target export endpoint) and map chunks to the **target's own source IDs**, so gold sources can be compared with what the target cites. | MVP | P0 |
| FR-D2 | Generate **normal** cases — subtypes `factual`, `multi_hop`, `comparison` — each with question, expected answer, `must_include` key facts, gold source IDs and difficulty. | MVP | P0 |
| FR-D3 | Generate **edge** cases — `unanswerable`, `ambiguous`, `out_of_scope`, `noisy_input`, `multilingual`, `long_input` — each with an expected behavior (`answer`, `abstain`, `clarify`, `refuse`). | MVP | P1 |
| FR-D4 | Generate **adversarial** cases from a curated, versioned attack library: `prompt_injection_direct`, `prompt_injection_indirect`, `system_prompt_leak`, `cross_tenant_leak`, `jailbreak`. Leakage tests use planted canary tokens. | MVP (starter) / v1 (full) | P0 |
| FR-D5 | Validate every generated case: schema check, answerability check against the gold chunk, near-duplicate removal. Invalid cases are quarantined with a reason, never silently dropped. | MVP | P0 |
| FR-D6 | Cases are created as `draft`. Only `approved` cases count toward the gate. Approval happens by committing the case to `suites/` (reviewed in a PR) or via `evalcrest suite approve`. | MVP | P0 |
| FR-D7 | Provenance on every case: generator model, prompt version, source chunk IDs, timestamp. | MVP | P0 |
| FR-D8 | Suites are versioned by content hash; every run records the suite version it used. | MVP | P0 |
| FR-D9 | A **smoke** subset (~30 cases, stratified by category) is maintained for CI. | v1 | P0 |

### 8.3 Execution

| ID | Requirement | Release | Pri |
|---|---|---|---|
| FR-R1 | Execute cases concurrently with configurable concurrency (default 4) and a requests-per-second cap. | MVP | P0 |
| FR-R2 | Per-request timeout (default 30 s). Retry with exponential backoff and jitter on network errors, 429 and 5xx (max 3 attempts). Never retry other 4xx. | MVP | P0 |
| FR-R3 | Record for every case: request, raw response, HTTP status, latency, target-reported tokens, trace ID, target version. | MVP | P0 |
| FR-R4 | Each case runs in a fresh session. Adversarial cases run as dedicated test accounts. | MVP | P0 |
| FR-R5 | Resume an interrupted run without re-executing completed cases. | v1 | P1 |
| FR-R6 | Multi-turn cases with conversation history. | v1 | P1 |
| FR-R7 | `--repeats N` to measure the target's own nondeterminism. | v2 | P2 |

### 8.4 Judging

| ID | Requirement | Release | Pri |
|---|---|---|---|
| FR-J1 | Score four criteria — **correctness**, **faithfulness**, **citation accuracy**, **safety**. Each returns a verdict (`pass` \| `fail` \| `not_applicable`), a score in [0, 1], a rationale, and evidence spans. | MVP | P0 |
| FR-J2 | Deterministic checks run **before** any LLM judge: citation-ID matching against gold sources, canary-token detection, abstention/refusal detection, format checks. A definitive deterministic result (e.g. a leaked canary) overrides the LLM. | MVP | P0 |
| FR-J3 | Criteria apply according to case type (see [Agents.md → Judge](./Agents.md#53-judge)). | MVP | P0 |
| FR-J4 | Judge outputs are schema-validated; an invalid output is retried once, then recorded as `judge_error` (never as a pass). | MVP | P0 |
| FR-J5 | Judgments are cached by a hash of (prompt version, model, inputs) so re-judging unchanged results costs nothing. | v1 | P1 |
| FR-J6 | Calibration: 50 hand-labeled cases, labeled blind, split 20 dev / 30 held-out. Report per-criterion agreement, Cohen's κ, confusion matrix and 95% confidence intervals. | v1 | P0 |
| FR-J7 | Every judgment records the judge model and prompt version. Prefer a judge model that differs from the target's generator to limit self-preference bias. | MVP | P0 |

### 8.5 Diagnosis

| ID | Requirement | Release | Pri |
|---|---|---|---|
| FR-G1 | Assign every failed case one root cause: `retrieval_miss`, `hallucination`, `generation_error`, `citation_error`, `safety_violation`, `tool_error`, `infra_error`, or `unknown`. | v1 | P0 |
| FR-G2 | Rules first, using trace evidence (was the gold source retrieved, and at what rank?). The LLM is used only to explain and to resolve ambiguous cases. Every diagnosis records confidence and evidence. | v1 | P0 |
| FR-G3 | Cluster failures within each root cause by similarity. Each cluster has a title, size, representative cases and a fix hypothesis labeled as a hypothesis. | v1 | P0 |
| FR-G4 | Measure diagnosis accuracy on **FaultyBuddy**, a small fixture RAG app with deliberately injected faults of known type. | v1 | P1 |
| FR-G5 | Compare two runs on the same suite version: fixed, newly failing, still failing. | v2 | P0 |

### 8.6 Reporting and CI gate

| ID | Requirement | Release | Pri |
|---|---|---|---|
| FR-P1 | Self-contained single-file HTML report (works offline as a CI artifact): verdict, KPIs, per-criterion and per-category results, failures table, case detail, cost, runtime and run metadata. | MVP | P0 |
| FR-P2 | Machine outputs: `results.json` (MVP), JUnit XML and a Markdown PR summary (v1). | MVP / v1 | P0 |
| FR-P3 | Gate with configurable thresholds and regression check against a baseline run. Outcomes `PASS` / `FAIL` / `INCONCLUSIVE` with exit codes `0` / `1` / `2`. | v1 | P0 |
| FR-P4 | Reusable GitHub Actions workflow: start the target with Docker Compose, run the smoke suite, upload the report, post a PR comment, set a required status check. | v1 | P0 |
| FR-P5 | Trends across runs: pass rate, per-criterion scores, cost. | v2 | P1 |

### 8.7 Interfaces, cost and observability

| ID | Requirement | Release | Pri |
|---|---|---|---|
| FR-I1 | CLI: `init`, `target check`, `generate`, `suite approve`, `suite sync`, `run`, `judge`, `diagnose`, `report`, `gate`, `pipeline`, `calibrate`. | MVP (subset) | P0 |
| FR-I2 | REST API (FastAPI) to trigger runs and fetch results and reports. | v1 | P1 |
| FR-I3 | Read-only web dashboard over run history. | Future | P2 |
| FR-C1 | Token and cost accounting per LLM call, per agent and per run, using a dated price table in config. | MVP | P0 |
| FR-C2 | Per-run budget cap. When exceeded, the run stops, partial results are reported, and the gate returns `INCONCLUSIVE`. | MVP | P1 |
| FR-C3 | Every Evalcrest LLM call is traced in LangSmith with `run_id`, `case_id` and `agent` metadata. | MVP | P0 |

---

## 9. Non-functional requirements

| ID | Area | Requirement |
|---|---|---|
| NFR-1 | Reproducibility | Every run records suite version, target version, Evalcrest git SHA, model IDs, prompt versions and a config hash. Re-judging a stored run with the same versions reproduces ≥ 98% of verdicts (measured, since LLM outputs are not perfectly deterministic even at temperature 0). |
| NFR-2 | Performance | Smoke suite (~30 cases) completes in ≤ 6 min in GitHub Actions, including target startup. Full suite (~200 cases) in ≤ 20 min. |
| NFR-3 | Cost | Evalcrest LLM spend ≤ $0.50 per smoke run and ≤ $5.00 per full run. These are starting budgets, replaced by measured values in v2. |
| NFR-4 | Reliability | Transient target errors don't fail a run; they are retried, then recorded as errors. If more than 5% of cases end in an error (target or judge), the gate returns `INCONCLUSIVE`. |
| NFR-5 | Security | Secrets only via environment variables / AWS Secrets Manager, never logged or written to reports. Target output is untrusted data: never executed, never followed as instructions. |
| NFR-6 | Privacy | Test corpora contain no real personal data. StudyBuddy test accounts use synthetic or public documents. |
| NFR-7 | Maintainability | Typed Python (mypy strict on core packages), ≥ 80% line coverage on non-LLM code, prompts as versioned files, an ADR for every major decision. |
| NFR-8 | Portability | `docker compose up` runs everything locally. The same image runs locally, in CI and on AWS. |
| NFR-9 | Accessibility | Reports meet WCAG 2.1 AA (see [Design.md](./Design.md)). |

---

## 10. Success metrics

These are the numbers that go in the README. Each is published with its method, sample size and confidence interval — no number without a "how measured".

| Metric | Definition | Target | When |
|---|---|---|---|
| **Judge accuracy** | Agreement between the Judge and the owner's blind labels on the 30 held-out calibration cases, per criterion; plus Cohen's κ. | ≥ 85% agreement, κ ≥ 0.6 | v2 |
| **Test validity** | Share of a random sample of generated cases the owner rates valid (answerable, correct gold answer and source, not a duplicate). | ≥ 90% | MVP |
| **Diagnosis accuracy** | Share of FaultyBuddy's seeded failures assigned the correct root cause. | ≥ 80% | v1 |
| **StudyBuddy pass rate, before → after** | Pass rate on the same frozen suite version before and after fixes guided by the Diagnostician, with case counts. | Report the delta; aim for ≥ +10 pp | v2 |
| **CI gate effectiveness** | Seeded regression PRs blocked, and clean PRs passed, on StudyBuddy. | 5 / 5 blocked, 0 / 5 false blocks | v2 |
| **Cost per run** | Evalcrest LLM spend in USD, smoke and full. | ≤ $0.50 / ≤ $5.00 | MVP → v2 |
| **Time per CI run** | Wall-clock time of the smoke gate in GitHub Actions. | ≤ 6 min | v1 |

> **Note on sample size.** 50 labels is a small sample. Agreement is reported with a Wilson 95% interval, and the README says so plainly. Overclaiming is worse than a modest, honest number.

---

## 11. Responsible testing policy

Adversarial testing is powerful and easy to misuse. These rules are product requirements, not suggestions:

1. **Authorization first.** Adversarial suites run only against targets the owner owns, or has written permission to test — with scope and expiry recorded in the target config. The Runner enforces this in code.
2. **Canaries, not real data.** Leakage tests plant synthetic canary tokens (e.g. in a second test account's documents or in the system prompt) and check whether they come back. Evalcrest never tries to extract real user data.
3. **Staging by default.** Adversarial and full suites target a local or staging instance. Production gets only the smoke suite, at low concurrency.
4. **No load testing.** Concurrency and rate limits are conservative and always on.
5. **Curated attacks.** The attack library is curated and versioned. Jailbreak tests check *whether the app refuses*; Evalcrest does not try to generate novel harmful content.
6. **Clean public artifacts.** README screenshots and public sample reports contain no secrets, no production canaries and no real user data. Unsafe target outputs are redacted in shareable reports.

---

## 12. Target integration requirements (StudyBuddy)

To be tested at grey-box and white-box level, StudyBuddy needs a few small, test-only changes:

| # | Change | Why |
|---|---|---|
| 1 | Chat endpoint returns `answer` plus `citations[]` with stable `source_id`s (document ID + chunk or page). | Citation accuracy needs IDs, not just titles. |
| 2 | **Eval mode** — when a valid `X-Eval-Key` header is sent (staging/test only), the response also includes `retrieved[]` (`source_id`, `rank`, `score`) and `trace_id`. | Faithfulness and root-cause diagnosis need the retrieved context. |
| 3 | `GET /version` returns git SHA plus key config (model, chunk size, `k`). | Reproducibility and before/after comparisons. |
| 4 | Corpus export: document list and chunk IDs used by the index (or raw files plus chunking config). | The Test Designer must cite the same IDs the target uses. |
| 5 | Test accounts `eval-user-a` and `eval-user-b` with synthetic corpora; `eval-user-b` owns the canary document. | Cross-tenant leakage tests. |
| 6 | LangSmith tracing to a dedicated project, with the trace ID returned to the caller. | The Diagnostician reads traces. |
| 7 | A Docker Compose profile that starts StudyBuddy with the seeded test corpus. | CI gate runs against a fresh, known instance. |

---

## 13. Assumptions and dependencies

- Anthropic API access (paid credits) for Evalcrest's Test Designer, Judge and Diagnostician.
- StudyBuddy's own Gemini keys with enough quota for a full run, kept separate from Evalcrest's keys so the two never compete for quota.
- A LangSmith account for tracing Evalcrest and StudyBuddy.
- An AWS account with a budget alarm for v1 deployment.
- Write access to the StudyBuddy repository for the integration changes and the CI gate.
- Course progress drives v1 timing; the MVP date is fixed.

---

## 14. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| The Judge is unreliable or biased (e.g. self-preference toward its own model family). | Gate decisions can't be trusted. | Deterministic checks first; the Judge (Claude) uses a different provider from StudyBuddy (Gemini); calibration against human labels; publish κ, not just accuracy. |
| The target is slow or rate-limited (StudyBuddy took 18–27 s per answer; an overloaded Gemini model stalled for ~10 min). | CI runs time out; failures get blamed on answer quality. | Conservative concurrency per target, per-request timeouts, and rate-limit failures recorded as `infra_error` so the gate says INCONCLUSIVE rather than FAIL. |
| Generated tests have wrong gold answers. | False failures, wasted debugging. | Answerability validation, quarantine, human approval before cases count toward the gate. |
| The gate is flaky because LLM outputs vary. | Developers learn to ignore it. | Stratified smoke set, retry-on-fail with majority vote for non-critical cases, thresholds with margin, tracked flake rate. |
| Costs overrun. | Project becomes expensive to run. | Budget caps, judgment cache, cheaper model tier by default, smoke subset in CI. |
| The target exposes no traces. | No root cause. | Graceful degradation to `unknown`, clearly labeled; integration guide for targets. |
| Target output injects instructions into the Judge. | Wrong verdicts on adversarial cases. | Delimited untrusted input, deterministic overrides, and dedicated judge-injection test cases. |
| Model deprecations or behavior changes. | Silent drift in judgments. | Model IDs in config; calibration re-run on every judge model change. |
| Scope creep against coursework. | MVP slips. | Strict phase scope and non-goals; MVP first, polish later. |
| AWS spend. | Unexpected bills. | Scale-to-zero batch tasks, smallest instance sizes, budget alarm. |

---

## 15. Open questions

1. **Judge timing.** The brief places the Judge in Course 8, but the MVP (December) needs it. *Current assumption:* a baseline Judge ships in the MVP in LangGraph; Course 8 extends it and compares orchestration frameworks.
2. **Model tiers.** Claude Haiku 5.5 or Sonnet 5.5 for the Judge in CI? Default: Sonnet for full runs and calibration; switch the smoke run to Haiku only if calibration shows comparable agreement.
3. **Judge independence.** *Resolved:* StudyBuddy generates with Gemini and Evalcrest judges with Claude. Calibration also runs a Gemini judge on the same labels to measure any self-preference effect.
4. **Multilingual.** Do StudyBuddy users ask questions in Arabic? If yes, `multilingual` edge cases move to P0.
5. **Public demo.** Should a read-only sample report be hosted publicly for reviewers?

---

## 16. Glossary

| Term | Meaning |
|---|---|
| **Target** | The LLM application under test (e.g. StudyBuddy). |
| **Knowledge source** | The documents the target retrieves from. |
| **Test case** | One input plus its expectations (answer, sources, behavior). |
| **Suite** | A versioned set of approved test cases. **Smoke** = ~30 for CI; **full** = everything. |
| **Golden set** | The 50 hand-labeled cases used to calibrate the Judge. |
| **Run** | One execution of a suite against one target version. |
| **Judgment** | The Judge's verdict, score and rationale for one criterion on one result. |
| **Diagnosis** | The root cause assigned to a failed case, with evidence. |
| **Gate** | The pass / fail / inconclusive decision computed from a run. |
| **Canary** | A unique synthetic string planted where it must never leak. |
| **Capability level** | How much the target exposes: black-box, grey-box or white-box. |