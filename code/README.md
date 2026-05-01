# Multi-Domain Support Triage Agent

A terminal-based AI agent that triages support tickets across **HackerRank**, **Claude (Anthropic)**, and **Visa** using retrieval-augmented generation (RAG) grounded exclusively in the official support corpora.

---

## Architecture

```
code/
├── agent.py       CLI entry point — argument parsing, Rich terminal UI, CSV I/O, log wiring
├── corpus.py      Pre-built knowledge base (35 documents scraped from the 3 support sites)
├── retriever.py   BM25 retrieval — domain-filtered first, full-corpus fallback
├── triage.py      Core pipeline — safety gate → retrieval → LLM call → normalise → log
└── requirements.txt  Pinned dependencies

support_tickets/
├── support_tickets.csv   Input (provided)
└── output.csv            Agent predictions (generated)

log.txt            Full prompt/response trace for every ticket processed
```

### Design decisions

| Decision | Rationale |
|---|---|
| **Hybrid BM25 + TF-IDF retrieval** | BM25 handles exact keyword matches (doc IDs, commands, product names). TF-IDF cosine catches paraphrase/synonym matches (e.g. "block crawler" ↔ "stop crawling website"). Combined `0.6 × normalised_BM25 + 0.4 × TF-IDF` improves recall without losing precision. Domain-filtered index first; full-corpus fallback when company is None or best score < 1.5. |
| **Confidence-based auto-escalation** | Before calling the LLM, `compute_confidence()` scores the top retrieved doc (raw BM25 / 8.0, clamped to 1.0). If confidence < 0.15, the ticket is auto-escalated without an LLM call — preventing hallucinated answers when no corpus match exists. |
| **Corpus citations in output** | System prompt instructs the LLM to list every `[DOC_ID]` it used. The `citations` field in the JSON output (and CSV) makes answers traceable and auditable. |
| **Urgency scoring (1–5)** | LLM rates each ticket's urgency on a 1–5 scale (1=general how-to, 5=active fraud/outage). Surfaces time-sensitive tickets for faster human review. |
| **Groq + Llama-3.3-70B** | Free tier, deterministic at `temperature=0`, highly capable for structured JSON output. |
| **Safety gate before LLM** | Malicious/injection tickets are caught by regex patterns and never hit the model — saves cost and prevents misuse. |
| **Structured JSON output** | System prompt demands JSON only; output is validated and clamped to allowed enum values regardless of model variance. |
| **Corpus-only grounding** | System prompt explicitly forbids the model from using parametric knowledge; all facts must come from the retrieved context block. |
| **Escalation-by-rule + LLM** | Escalation keywords are checked as a secondary signal, but the LLM makes the final call based on the corpus policy docs. |

---

## Setup

**Requirements:** Python 3.10+

```bash
# 1. Install dependencies (exact versions pinned)
pip install -r code/requirements.txt

# 2. Set your free Groq API key (get one at console.groq.com — no credit card needed)
export GROQ_API_KEY=gsk_...
# OR create a .env file in the project root:
echo "GROQ_API_KEY=gsk_..." > .env
```

---

## Running the agent

```bash
# Process support_tickets/support_tickets.csv → support_tickets/output.csv
python code/agent.py

# Custom paths
python code/agent.py --input support_tickets/support_tickets.csv \
                     --output support_tickets/output.csv

# Demo mode (runs sample_support_tickets.csv)
python code/agent.py --demo

# Quiet mode (summary table only, no per-ticket panels)
python code/agent.py --quiet

# Interactive single-ticket mode
python code/agent.py --interactive
```

---

## Output columns

| Column | Allowed values | Description |
|---|---|---|
| `status` | `replied` / `escalated` | Whether the agent answers directly or routes to a human |
| `product_area` | free string | Most relevant support category / domain area |
| `response` | free string | User-facing answer, grounded in the support corpus |
| `justification` | free string | Internal reasoning traceable to corpus evidence |
| `request_type` | `product_issue` / `feature_request` / `bug` / `invalid` | Best-fit classification |
| `urgency` | integer 1–5 | Urgency score (1=general how-to, 5=critical/active fraud/outage) |
| `confidence` | float 0.0–1.0 | Retrieval confidence from corpus (below 0.15 triggers auto-escalation) |
| `citations` | semicolon-separated doc IDs | Corpus documents cited by the LLM in its answer |

---

## Chat transcript logging

Every time the agent runs, it appends a full trace to **`log.txt`** in the project root. Each entry records:

- The ticket number, timestamp, company, subject, and issue text
- The corpus documents retrieved (with BM25 scores)
- The exact prompt sent to the LLM
- The raw LLM response
- The final normalised decision

This log is generated automatically — no manual step required.

To inspect a specific run:
```bash
cat log.txt          # full trace
grep "TICKET #" log.txt   # list all ticket headers
```

The log lets evaluators verify that:
1. Responses are traceable to specific retrieved corpus documents
2. No hallucinated policies or phone numbers were generated
3. Malicious tickets (e.g., prompt injection, harmful code requests) were caught by the safety gate before reaching the LLM

---

## Escalation logic

The agent escalates when corpus documentation indicates the issue requires a human team:

| Trigger | Reason |
|---|---|
| Billing / refund / payment | Requires finance team |
| Fraud / identity theft / stolen card | Requires security team |
| Security vulnerabilities / bug bounty | Requires security team |
| Workspace access lost / seat removed | Requires admin/IT action |
| Score modifications / hiring decisions | Policy: not possible |
| Platform-wide outage / critical bug | Requires engineering |
| Subscription pause/cancel | Requires account management |
| Certificate name update | Requires identity verification |
| Third-party action required (bank, AWS, recruiter) | Outside support scope |

Out-of-scope, invalid, or malicious tickets are replied to directly with an appropriate message.

---

## Improvements over baseline

| Improvement | Implementation |
|---|---|
| **Hybrid BM25 + TF-IDF retrieval** | `retriever.py` — `HybridRetriever` combines BM25 (0.6×) and TF-IDF cosine (0.4×); better recall on paraphrased queries |
| **Corpus citations** | System prompt asks LLM to list `DOC_ID`s used; `citations` column in output CSV for auditability |
| **Urgency scoring** | LLM assigns urgency 1–5 per ticket; `urgency` column in output CSV |
| **Confidence-based auto-escalation** | `compute_confidence()` gates every ticket before the LLM; tickets with no strong corpus match are safely escalated |

## Reproducibility

- **Model:** `llama-3.3-70b-versatile` (pinned in `triage.py`)
- **Temperature:** `0` (deterministic output)
- **Dependencies:** exact versions in `requirements.txt`
- **Corpus:** fully embedded in `corpus.py` — no live scraping at runtime
