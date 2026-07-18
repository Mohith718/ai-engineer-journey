# AI Support Ticket Triage Agent

A production-style AI agent that reads a support ticket, classifies it, searches a company knowledge base for a relevant answer, and either resolves it automatically or escalates it to the correct human team, with a full reasoning trail at every step.

**Live demo:** [ai-engineer-journey-production-4b12.up.railway.app](https://ai-engineer-journey-production-4b12.up.railway.app)

---

## Why this project exists

Most portfolio "AI agent" projects are a chatbot with extra steps, one LLM call, one answer, no real decision-making. This project is built around a single, deliberate constraint: **the agent must be able to say "I don't know" and hand off to a human, instead of guessing.**

That constraint is what turns a demo into something closer to a real internal support tool. A system that auto-resolves everything, including things it shouldn't, is a liability, not a feature. This one is designed to fail safely.

---

## Architecture

```
User submits ticket (browser)
        │
        ▼
┌───────────────────┐
│   classify_node    │  → category, urgency, sentiment (LLM, structured JSON)
└─────────┬─────────┘
          ▼
┌───────────────────┐
│   retrieve_node    │  → searches knowledge_base.txt via ChromaDB + Gemini embeddings
└─────────┬─────────┘
          ▼
┌───────────────────┐
│    resolve_node     │  → LLM judges: is retrieved context sufficient to answer?
└─────────┬─────────┘
          ▼
┌───────────────────┐
│  route_output_node  │  → formats response differently depending on outcome
└─────────┬─────────┘
          ▼
   auto_resolved  OR  escalated (with assigned team + priority)
```

All four steps run inside a single **LangGraph** `StateGraph`. State is a `TypedDict` that accumulates fields as it passes through each node, the same mechanic as a linear pipeline, but built as a graph specifically so branching logic (add later: retry loops, team-specific routing) can be introduced without restructuring the whole flow.

### Why a graph instead of a straight function chain

Every node in this version happens to lead to exactly one next node, no node currently branches to two different next-node destinations. That means, strictly speaking, this graph does not yet require LangGraph's conditional-edge feature, plain sequential function calls would produce an identical result today.

It's built as a graph anyway for one reason: the decision logic (auto-resolve vs. escalate) already exists inside `route_output_node`. The natural next iteration of this project is routing escalated tickets to team-specific handler nodes (a real conditional edge, multiple possible destinations), and building on a graph from day one means that extension doesn't require re-architecting anything, only adding nodes and one `add_conditional_edges` call.

---

## Tech stack

| Layer | Tool | Purpose |
|---|---|---|
| Orchestration | LangGraph | State machine connecting the four processing nodes |
| LLM | Groq (LLaMA 3.3 70B) | Classification, resolution judgment, response drafting |
| Embeddings | Google Gemini (`gemini-embedding-001`) | Converts knowledge base + ticket text into vectors |
| Vector store | ChromaDB | Stores and searches knowledge base chunks |
| Backend | FastAPI | Exposes the pipeline as a `/ticket` POST endpoint |
| Frontend | Static HTML/CSS/JS | Calls the API directly via `fetch()`, no framework |
| Containerization | Docker | Single image bundling backend + frontend |
| Deployment | Railway | Public hosting, environment variable management |

---

## Project structure

```
project-4-support-agent/
├── knowledge_base.txt      # Synthetic FAQ/policy corpus (34 entries)
├── support_agent.py        # LangGraph pipeline: state, 4 nodes, graph assembly
├── support_agent_api.py    # FastAPI wrapper: /ticket endpoint, CORS, static file serving
├── index.html              # Frontend: form, styled result card, fetch() call
├── requirements.txt        # Pinned dependency versions
├── Dockerfile              # Container build instructions
└── .env                    # GROQ_API_KEY, GEMINI_API_KEY (local only, never committed)
```

---

## The pipeline in detail

### 1. `classify_node`

Takes the raw ticket text. Sends it to the LLM with a system prompt constrained to return only JSON:

```json
{"category": "billing" | "technical" | "security" | "account" | "feature_request",
 "urgency": "low" | "medium" | "high" | "critical",
 "sentiment": "frustrated" | "neutral" | "positive"}
```

Parsed defensively with a two-level fallback JSON parser (`safe_parse_json`): try a direct `json.loads`, then try extracting the substring between the first `{` and last `}` if the LLM added any stray text around the JSON, then fall back to an explicit error object rather than crashing the pipeline.

### 2. `retrieve_node`

Embeds the original ticket text with Gemini and searches a ChromaDB vector store built once, at import time, from `knowledge_base.txt` (chunked with `RecursiveCharacterTextSplitter`, 500 chars, 50 overlap). Returns the top 3 matching chunks concatenated as `retrieved_context`.

The vector store is built **outside** any node function, at module load time, and read from, never rebuilt or reassigned, inside a request. This avoids a real bug class encountered earlier in this project's sibling API (Project 2's RAG chatbot): reassigning a shared object inside a function without the `global` keyword silently creates a function-local copy that vanishes after the request completes, leaving the "shared" state untouched. Because retrieval here never *writes* to `vectorstore` or `retriever`, that failure mode doesn't apply, this is documented as a deliberate design choice, not an oversight.

### 3. `resolve_node`

The core judgment call. Given the ticket and the retrieved context, the LLM is asked one question: *is this context actually sufficient to answer the ticket, or does it need a human?* It does not simply check "did retrieval return something", it checks whether what was returned is actually relevant to what was asked.

Returns `resolution_type: "auto_resolved" | "escalated"` and either a customer-facing answer or an internal note explaining the gap.

**Verified behavior, both branches:**
- *"I forgot my password"* → matched an exact knowledge base entry → `auto_resolved`
- *"I was charged twice this month and I'm furious"* → knowledge base had refund/overage/failed-payment entries, none addressing duplicate charges specifically → correctly `escalated` rather than guessing

### 4. `route_output_node`

Pure Python, no LLM call. Formats the final payload differently depending on `resolution_type`:
- **Auto-resolved:** `response_text` is passed through as-is, ready for a customer.
- **Escalated:** looks up `assigned_team` from `category` via a static dictionary (billing → Billing Team, technical → Technical Support, etc.), and builds an internal summary that leads with `urgency` and `sentiment`, the two fields a human triager needs first.

This node exists specifically so `category`, `urgency`, and `sentiment` are actually used downstream rather than computed and discarded, every classified field feeds into the final output.

---

## API

### `POST /ticket`

**Request:**
```json
{ "ticket_text": "I was charged twice this month and I'm furious, fix this now!" }
```

**Response:**
```json
{
  "ticket_text": "...",
  "category": "billing",
  "urgency": "high",
  "sentiment": "frustrated",
  "retrieved_context": "...",
  "resolution_type": "escalated",
  "response_text": "...",
  "assigned_team": "Billing Team",
  "final_output": "[HIGH priority, customer sentiment: frustrated] ..."
}
```

CORS is fully open (`allow_origins=["*"]`) for this demo; a production deployment would restrict this to known frontend origins.

---

## Frontend

Deliberately built as plain HTML/CSS/JS rather than a Python-only tool like Streamlit, specifically to demonstrate the ability to build and wire a real browser frontend to a REST API, not just a data-science notebook UI.

Design direction: dark, editorial, operational, closer to an internal ops dashboard than a marketing page. `Fraunces` (serif) for the headline and the AI's response text; `IBM Plex Mono` for labels, badges, and metadata, pairing warmth in the answer with precision in the surrounding chrome. Urgency is color-coded on a semantic scale (green → gold → orange → red). The escalated/resolved states get visually distinct treatment (a colored status strip with a dot, not just a border color), the same pattern used in tools like Linear or Intercom.

The frontend is served by the same FastAPI process that serves the API (`StaticFiles` mounted at `/`), so in production the JavaScript calls a **relative** path (`/ticket`), not a hardcoded `localhost` address, the same code works identically locally and once deployed.

---

## Deployment

Single Docker image containing the backend, the pipeline, and the frontend. Built with `python:3.11-slim`, dependencies pinned in `requirements.txt`, run via `uvicorn support_agent_api:api --host 0.0.0.0 --port 8000`.

Deployed on Railway, connected directly to this GitHub repository with **Root Directory** set to `project-4-support-agent`, so Railway builds only this project's `Dockerfile`, independent of the other projects living in the same monorepo. Environment variables (`GROQ_API_KEY`, `GEMINI_API_KEY`) are set through Railway's dashboard, never committed to source control.

---

## A real incident, documented honestly

During deployment, a `GEMINI_API_KEY` was briefly present in a Git commit before `.gitignore` was correctly applied. Google's automated leak-detection scanner found it in the public commit history and permanently revoked the key within hours, deleting the file in a later commit did not undo this; historical commits remain readable regardless of what the latest commit shows.

**Diagnosis:** the container built and started successfully, but crashed specifically inside `Chroma.from_documents()`, the underlying Gemini embeddings call returned `403 PERMISSION_DENIED: Your API key was reported as leaked`. Traced through the Railway deployment logs to the exact line and exact cause rather than assuming.

**Fix:** generated a new key at Google AI Studio, updated it in both the local `.env` and Railway's Variables tab, confirmed `.gitignore` correctly excludes `.env` going forward, redeployed, verified the fix by submitting a real ticket against the live URL rather than assuming a clean deploy log meant the app actually worked end to end.

This is included here deliberately. It's a real production security scenario, not a hypothetical, and the correct response (rotate the key, don't try to "fix" the old one, verify functionally rather than by log absence) is itself a demonstration of production judgment.

---

## Known limitations / next steps

- **Escalation is a label, not an action.** `assigned_team` is computed but nothing currently notifies that team (no email, Slack, or ticketing system integration). The natural next step is team-specific handler nodes with a real `add_conditional_edges` call, genuine branching to different destination nodes, not just internal `if/else` logic inside one node.
- **No retry/self-correction loop.** Unlike the Research Agent project, this pipeline doesn't re-query the knowledge base with refined terms if the first retrieval is weak, it escalates immediately. Worth adding a bounded retry (same pattern as the Research Agent's `attempts` counter) before escalating.
- **No automated evaluation.** Tested manually against two representative cases (one auto-resolve, one escalate). A proper ground-truth eval set with faithfulness/precision scoring, the same pattern built for the PDF RAG chatbot project, hasn't been applied here yet.
- **CORS is wide open.** Fine for a demo; would be scoped to specific origins in a real deployment.
- **Knowledge base is synthetic**, generated with an AI tool to simulate realistic product documentation for a fictional SaaS company, not sourced from a real company's actual support corpus.

---

## What this project demonstrates

- Multi-step LangGraph state machine design, with an honest explanation of why conditional edges weren't needed *yet*, not just that they were used
- Retrieval-augmented decision-making that can correctly decline to answer when context is insufficient
- Full-stack delivery: Python backend, hand-built frontend, Docker, live cloud deployment
- Real production debugging: a genuine security incident, diagnosed from raw logs and resolved correctly
