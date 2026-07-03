# AI Engineer Journey

I'm an automation engineer learning to build AI systems in code instead of drag-and-drop tools.

Before this repo, I built real things for real clients: a Voice AI Receptionist that handles inbound calls end-to-end, a WhatsApp order system processing 50+ daily orders, B2B sales pipelines with automated lead scoring. All in n8n and VAPI. All running in production.

The problem: I couldn't explain what was happening under the hood, and I couldn't build any of it without a visual workflow builder. This repo is me fixing that, one day at a time.

---

## What I've built so far

### Project 2: PDF RAG Chatbot
`Python` `ChromaDB` `Gemini Embeddings` `Groq LLaMA` `Streamlit` `LangChain` `FastAPI`

Upload a PDF. Ask questions about it. Get answers pulled from the actual document, not the model's imagination.

I built this four separate times on purpose:
- From scratch in raw Python (manual chunking, embedding, vector search)
- Rebuilt with LangChain (same thing, way less code, now I know what it hides)
- Wrapped in Streamlit (browser UI instead of terminal)
- Wrapped in FastAPI (`/upload` and `/ask` endpoints, any app can call it)

### Project 3: AI Research Agent
`LangGraph` `Tavily Search` `Groq LLaMA`

Give it a topic. It searches the web, reads what it finds, decides whether that's enough to write a decent report. If not, it searches again with different terms. If yes, it writes the report. Caps out at 3 search attempts so it can't loop forever and burn through API credits.

Output is always the same structure: Executive Summary, Key Findings, Analysis, References with actual URLs.

The interesting part isn't the report. It's that the agent decides its own next step based on what it found. Nothing is hardcoded. The graph routes itself.

### Project 1: Voice AI Receptionist
`n8n` `VAPI` `Google Calendar API` `Google Sheets CRM`

Built before this repo. Handles inbound calls for a business: identifies the caller, checks the calendar, books or reschedules appointments, logs everything. No human needed. This is what got me interested in building AI systems properly instead of just wiring nodes together.

---

## What I covered each week

| Week | What I did |
|---|---|
| 1 | Python from scratch. Functions, file I/O, error handling, `.env` secrets |
| 2 | OOP, decorators, async/await, cross-file imports |
| 3 | Groq LLM API, prompt engineering, tool calling, chatbot with conversation memory |
| 4 | Streaming, token management, production system prompts |
| 5 | Embeddings, ChromaDB, cosine similarity, full RAG pipeline built manually |
| 6 | LangChain (chains, agents, `bind_tools`), LangChain RAG rebuild |
| 7 | LangGraph (state, nodes, conditional edges, looping), RAG evaluation with LLM-as-a-Judge |
| 8+ | FastAPI, Docker, deployment *(in progress)* |

---

## Stack

**LLMs:** Groq (LLaMA 3.3 70B, free tier)
**Embeddings:** Google Gemini (gemini-embedding-001, 3072-dim, free tier)
**Vector DB:** ChromaDB
**Frameworks:** LangChain, LangGraph, FastAPI, Streamlit
**Automation:** n8n, VAPI
**Other:** Python, Git, tiktoken, python-dotenv

---

## Why I built everything twice

Every major concept in this repo, I built manually first, then rebuilt with a framework. RAG from scratch before LangChain's retrieval chain. A hand-rolled tool-calling loop before `bind_tools`. The Groq API directly before `ChatGroq`.

The reason is interviews. When someone asks "what does LangChain's retrieval chain actually do under the hood?" I can answer because I wrote every piece of it myself before I ever imported it. Most people who start with the framework can't do that.

---

## Contact

[LinkedIn](https://www.linkedin.com/in/mohith-srinivas/) · [GitHub](https://github.com/Mohith718) · mohithsrinivassomaraju@gmail.com · Hyderabad, India
