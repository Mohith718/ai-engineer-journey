# AI Engineer Journey

My 14-week journey from automation engineer to AI engineer, built entirely in public. Every project, every bug, every day logged here.

**Background:** B.Tech CSE 2025 graduate from Hyderabad with production automation experience (n8n, VAPI, webhook-based AI systems). Currently rebuilding those skills in raw Python and modern AI frameworks to move into AI Engineer and Agentic AI Engineer roles.

**Connect:** [LinkedIn](https://www.linkedin.com/in/mohith-srinivas/) · mohithsrinivassomaraju@gmail.com

---

## Projects

### Project 1 — Voice AI Receptionist
`n8n` `VAPI` `Google Calendar API` `CRM`

A fully autonomous inbound call handler. Identifies the caller via CRM lookup, books or reschedules appointments in real time, and logs every call outcome. Built and deployed for a real client before this repo existed.

### Project 2 — PDF RAG Chatbot
`Python` `ChromaDB` `Gemini Embeddings` `Groq LLaMA` `Streamlit` `LangChain` `FastAPI`

Upload any PDF, ask questions, get answers grounded in the document with zero hallucination. Built four ways to understand every layer of the stack:
- **From scratch** — manual chunking, embedding, and retrieval, no framework
- **LangChain rebuild** — same pipeline in a fraction of the code
- **Streamlit UI** — browser-based chat interface
- **FastAPI service** — `/upload` and `/ask` REST endpoints so any external app can use it

📁 [`project-2-rag-chatbot/`](./project-2-rag-chatbot)

### Project 3 — AI Research Agent
`LangGraph` `Tavily Search` `Groq LLaMA`

Give it a topic. It searches the web, judges whether it found enough information, loops back and searches again if not (capped at 3 attempts so it can't run forever), then writes a structured report — Executive Summary, Key Findings, Analysis, References — with real source URLs.

This is the project that proves agentic behavior: the graph itself decides what happens next based on what it finds, nothing is hardcoded.

📁 [`project-3-research-agent/`](./project-3-research-agent)

---

## Weekly Breakdown

| Week | Focus | Key Skills |
|---|---|---|
| 1 | Python Basics | Functions, file I/O, error handling, `.env` config |
| 2 | Python Intermediate | OOP, decorators, `async`/`await` |
| 3 | LLM APIs | Groq API, prompt engineering, tool/function calling, conversation memory |
| 4 | Advanced LLM | Streaming, token management, production system prompts |
| 5 | Embeddings + RAG | ChromaDB, cosine similarity, chunking, full RAG pipeline from scratch |
| 6 | LangChain | Chains, prompt templates, agents with `bind_tools` |
| 7 | LangGraph | State graphs, conditional edges, looping agents, RAG evaluation (RAGAS-style faithfulness scoring) |
| 8+ | FastAPI + Deployment | REST APIs, Docker, live deployment *(in progress)* |

---

## Tech Stack

**LLMs & Embeddings:** Groq (LLaMA 3.3), Google Gemini (embeddings)
**Frameworks:** LangChain, LangGraph, FastAPI, Streamlit
**Vector Store:** ChromaDB
**Automation background:** n8n, VAPI
**Tools:** Python, Git, `python-dotenv`, `tiktoken`

---

## Philosophy

Every project here was built manually first, then rebuilt with a framework. RAG from scratch before LangChain's RAG chain. A hand-rolled tool-calling loop before LangChain's `bind_tools`. The goal isn't just to use these tools, it's to know exactly what they're doing underneath, so I can debug them when they break in production.

This is a living repo. New folders get added weekly as the roadmap progresses.
