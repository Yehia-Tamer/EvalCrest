# StudyBuddy API contract (as observed)

| | |
|---|---|
| **Captured** | 2026-10-26 |
| **StudyBuddy commit** | `main @ <0d43f7a>` |
| **Pre-fix commit (for the "before" baseline)** | `<last commit before fix/pdf-source-type>` |
| **Primary LLM** | `gemini-3.6-flash` (fallbacks: `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`; `gemini-3.8-flash` removed after 503/504 on all keys) |
| **Retrieval** | hybrid (vector + BM25, k=8) → cross-encoder rerank, top_n=5 |
| **Chunking** | RecursiveCharacterTextSplitter, chunk_size=800, overlap=150 |
| **Corpus** | `physics_notes.pdf` (PHYS 201 Lecture 4, 5 pages, 7 chunks) |
| **Base URL** | `http://localhost:8000` (uvicorn) · `http://localhost/api` (full docker compose) |

## Request flow

| # | Request | Body | Returns |
|---|---|---|---|
| 1 | `POST /auth/register` | JSON `{username, email, password}` | `201`, or `409` if the user exists |
| 2 | `POST /auth/login` | **form fields** `username`, `password` | `{access_token, token_type: "bearer"}` (expires after 30 min) |
| 3 | `POST /documents/pdf` | multipart `file` | `DocumentResponse` |
| 4 | `POST /conversations/` | JSON `{document_id}` | `{id, document_id, created_at}` |
| 5 | `POST /conversations/{id}/messages` | JSON `{content}` | `MessageResponse` (below) |

All requests after login send `Authorization: Bearer <token>`.

## Response shape: `MessageResponse`

```json
{
  "id": 0,
  "role": "assistant",
  "content": "string (Markdown, may contain LaTeX)",
  "timestamp": "ISO 8601",
  "sources": [
    {
      "source_type": "pdf | pptx | web | youtube | audio",
      "filename": "string | null",
      "page": "int, 1-based | null",
      "slide": "int | null",
      "source_url": "string | null",
      "link": "string | null",
      "timestamp_seconds": "int | null",
      "timestamp_delay": "string | null"
    }
  ]
}
```

No `/health`, `/version`, source IDs, retrieved chunk text or trace ID yet.

## Sample 1: answerable question

**Question:** "What is Newton's second law?" · document 6 · **18.3 s**

```json
{
  "id": 9,
  "role": "assistant",
  "content": "According to the document context, **Newton's Second Law** states that the net force acting on an object is equal to the rate of change of its momentum. \n\nFor an object with constant mass, it is expressed by the formula:\n\n$$\\mathbf{F = ma}$$\n\nWhere:\n* $\\mathbf{F}$ is the net force (measured in Newtons, $\\text{N}$)\n* $\\mathbf{m}$ is the mass of the object (measured in kilograms, $\\text{kg}$)\n* $\\mathbf{a}$ is the acceleration (measured in meters per second squared, $\\text{m/s}^2$)",
  "timestamp": "2026-10-26T08:09:15.769638",
  "sources": [
    {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 2},
    {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 5},
    {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 1},
    {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 4},
    {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 3}
  ]
}
```

## Sample 2: unanswerable question

**Question:** "What does the lecture say about Maxwell's equations?" · document 7 · **26.5 s**

```json
{
  "id": 11,
  "role": "assistant",
  "content": "Based on the provided lecture notes, **Maxwell's equations are not mentioned**. \n\nThe lecture focuses entirely on classical mechanics topics, specifically:\n* Newton's Three Laws of Motion\n* Conservation of Momentum and Collisions (Elastic vs. Inelastic)\n* Potential and Kinetic Energy, and the Conservation of Mechanical Energy",
  "timestamp": "2026-10-26T08:10:00.508750",
  "sources": [
    {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 1},
    {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 2},
    {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 5},
    {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 4}
  ]
}
```

Null fields (`source_url`, `timestamp_seconds`, `timestamp_delay`, `link`, `slide`) are omitted from the samples for readability. The API returns them as `null`.

## Observations

| # | Observation | Implication for Evalcrest |
|---|---|---|
| 1 | Sample 1 is correct, but `sources` lists all 5 pages of the PDF | `sources` = everything retrieved, not what the answer used, so the answer can't be traced to its evidence. Citation accuracy will fail. |
| 2 | Sample 2 correctly abstains | Grounding held in this case; the edge-case suite will test it properly. |
| 3 | Sample 2 still lists 4 sources | An abstention shouldn't cite anything. Another citation-accuracy failure. |
| 4 | 4 sources instead of 5 in Sample 2 | Either two chunks were on the same page (merged), or a BM25-only chunk was dropped (`Metadata: {}` bug). |
| 5 | Answers use Markdown + LaTeX (`$$\mathbf{F = ma}$$`) | Correctness must be judged by meaning, not string match. |
| 6 | 18–27 s per question | Smoke suite of ~30 cases at concurrency 2 ≈ 5 min. Size the CI suite accordingly. |

## Known StudyBuddy bugs (keep for the before/after comparison)

| Bug | Location | Status |
|---|---|---|
| PDF chunks had no `source_type`, so every PDF answer returned `sources: []` | `rag/loaders/pdf_loader.py` | Fixed on `fix/pdf-source-type` (now in `main`) |
| BM25-only hits lose all metadata and are dropped from `sources` | `rag/retrievers.py` (`BM25Retriever.from_texts` without metadata) | Open |
| `sources` lists all retrieved chunks, not the ones the answer used | `rag/chains/chat_chain.py` (`build_sources(docs)`) | Open |
| PPTX sources have no filename; dedupe key `(total_slides, slide)` collides across decks | `rag/chains/chat_chain.py` | Open |
| Web-search answers still list document chunks as sources | `rag/chains/chat_chain.py` | Open |
| `page_count` stores the chunk count, not the page count | `repository/documents.py` | Open |
| Key rotation catches `ResourceExhausted`, but the SDK raises `google.genai.errors.APIError` | all chains | Fix on `fix/key-rotation` |
| No LLM timeout; a stalled model (`gemini-3.8-flash`) blocked calls for ~10 min | `rag/config.py` | Fix on `fix/key-rotation` |