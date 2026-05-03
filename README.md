# Simple RAG — Resume Analyzer

Ever wished you could just *talk* to a resume instead of reading through it line by line? That's exactly what this project does. Upload any resume as a PDF, ask questions in plain English, and get instant answers pulled directly from the document — no guessing, no hallucinations.

Built as a final year BTech project to explore how modern AI actually works under the hood.

---

## What it does

You upload a resume. You ask things like:

- *"What programming languages does this person know?"*
- *"How many years of experience do they have?"*
- *"Did they do any internships?"*
- *"What's their educational background?"*

And it answers — based purely on what's written in that resume.

---

## How it works (The Pipeline)

This project is built on a technique called **RAG — Retrieval Augmented Generation**. Instead of asking an AI to guess from memory, we feed it the exact relevant parts of the document before it answers. Think of it like an open book exam.

```
                        YOUR RESUME (PDF)
                               │
                               ▼
                    ┌─────────────────────┐
                    │   1. EXTRACT TEXT    │
                    │   Read every page,   │
                    │   split into small   │
                    │   200-word chunks    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   2. EMBED CHUNKS    │
                    │   Convert each chunk │
                    │   into a vector      │
                    │   (list of numbers)  │
                    │   using a free local │
                    │   AI model           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  3. STORE IN FAISS   │
                    │  A vector database   │
                    │  that can search     │
                    │  by meaning, not     │
                    │  just keywords       │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │   YOU ASK A QUESTION │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  4. EMBED QUESTION   │
                    │  Same model converts │
                    │  your question into  │
                    │  a vector too        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  5. FIND CLOSEST     │
                    │     CHUNKS           │
                    │  FAISS finds the 3   │
                    │  most relevant parts │
                    │  of the resume       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  6. ASK THE LLM      │
                    │  Send question +     │
                    │  those 3 chunks to   │
                    │  Groq's LLaMA model  │
                    │  and get an answer   │
                    └──────────┬──────────┘
                               │
                               ▼
                         YOUR ANSWER
```

The key insight here is step 5 — we never send the whole resume to the AI. We only send the *most relevant* parts. This keeps it fast, accurate and cheap.

---

## Project Structure

```
Simple RAG/
├── app.py              ← Streamlit web UI
├── main.py             ← CLI version (terminal)
├── requirements.txt    ← all dependencies
├── .env                ← your API key lives here
└── src/
    ├── config.py       ← settings (model names, chunk size etc.)
    ├── loader.py       ← reads the PDF and splits into chunks
    ├── embedder.py     ← converts chunks to vectors using AI
    ├── retriever.py    ← finds the most relevant chunks
    └── generator.py    ← sends to LLM and gets the final answer
```

Each file has exactly one job. If something breaks, you know exactly where to look.

---

## Models Used

### Embedding Model — BAAI/bge-small-en-v1.5
This is the model that converts text into vectors (numbers).

- Made by **Beijing Academy of AI (BAAI)**
- Hosted free on **HuggingFace**
- Runs entirely on your **local machine** — no internet needed after first download
- Downloads automatically on first run (~67MB)
- Chosen because it's lightweight, fast, and surprisingly accurate for its size

This is what makes the semantic search possible. When you ask *"what are their skills?"* it understands that's similar to *"Python, Java, Machine Learning"* even though the words are different.

### LLM — LLaMA 3.1 8B (via Groq)
This is the model that reads the retrieved chunks and forms a proper answer.

- Built by **Meta (Facebook AI)**
- Running on **Groq's hardware** — insanely fast inference
- **Free tier available** — no credit card needed to start
- 8 billion parameters — small enough to be fast, big enough to be smart

Groq's hardware (LPU chips) makes LLaMA run about 10x faster than a normal GPU setup. Responses come back in under a second which makes the demo feel alive.

---

## Setup

**1. Clone or download the project**

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Get a free Groq API key**
- Go to [console.groq.com](https://console.groq.com)
- Sign up → API Keys → Create API Key
- Copy the key

**4. Add your key to `.env`**
```
GROQ_API_KEY=gsk_your_key_here
```

**5. Run the web UI**
```bash
python -m streamlit run app.py
```

Or if you prefer the terminal version:
```bash
python main.py
```

---

## Why this is useful for Resume Analysis

Recruiters go through hundreds of resumes. Reading each one fully takes time. This tool lets you:

- **Screen faster** — ask the same question across multiple resumes
- **Dig deeper** — ask follow up questions a keyword search would miss
- **Stay honest** — answers come only from the document, no AI making things up
- **Save time** — what takes 5 minutes of reading takes 5 seconds here

It's not replacing human judgment — it's handling the boring part so humans can focus on the interesting parts.

---

## Requirements

```
Python        3.10 or above
groq          LLM API client
fastembed     local embedding model
faiss-cpu     vector similarity search
pypdf         PDF text extraction
streamlit     web UI
python-dotenv environment variable loader
```

---

## Limitations (being honest)

- Works best with text-based PDFs. Scanned image PDFs won't extract well.
- Very short resumes (under 1 page) might return fewer chunks than expected.
- Answers are only as good as what's written in the resume — it won't infer things that aren't there.

---

*Built with curiosity, a lot of debugging, and way too many terminal errors.*
