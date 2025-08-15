You are GitHub Copilot in VS Code. Create a local RAG project that works with Ollama models on Windows (PowerShell commands provided). Use Python 3.11+. Deliver a minimal, clean codebase that I can run immediately.

🎯 Objectives

Ingest PDFs/TXT/Markdown from a docs/ folder, chunk them, embed with Ollama embeddings, store in a persistent ChromaDB.

Query the store with a question, retrieve top chunks, build a grounded prompt (with citations), call Ollama Chat (e.g., qwen2.5 / tinyllama-1.1b), and return an answer + sources.

Provide CLI scripts (ingest.py, query.py) and a tiny FastAPI server (app.py) with a simple chat UI (HTML) for convenience.

Everything must be portable and run offline, assuming Ollama app is installed.

🗂️ Project Structure (create all)
rag-local/
├─ docs/                              # user drops PDFs/TXT/MD here
├─ vectorstore/                       # Chroma persistent dir (created at runtime)
├─ app/                               # FastAPI web app
│  ├─ app.py
│  ├─ templates/
│  │  └─ index.html
│  └─ static/
│     └─ styles.css
├─ src/
│  ├─ config.py
│  ├─ chunking.py
│  ├─ embeddings.py
│  ├─ store.py
│  ├─ llm.py
│  ├─ prompt.py
│  └─ rag.py                          # high-level ingest/query orchestration
├─ tests/
│  └─ test_chunking.py
├─ .env.example
├─ requirements.txt
├─ ingest.py
├─ query.py
├─ run_api.ps1
├─ README.md
└─ LICENSE

🔧 Tech Choices

Embeddings: nomic-embed-text (Ollama embeddings endpoint).

Chat LLM: default qwen2.5; allow swapping to tinyllama-1.1b via .env.

DB: Chroma persistent client in vectorstore/.

Chunking: sentence-aware (NLTK/Punkt), ~1100 chars with 200 overlap.

Prompting: system + user template with numbered citations [1], [2], … inserted from retrieved chunks.

⚙️ Configuration

Create src/config.py to read:

OLLAMA_URL (default http://127.0.0.1:11434)

EMBED_MODEL (default nomic-embed-text)

CHAT_MODEL (default qwen2.5)

PERSIST_DIR (default vectorstore)

TOP_K (default 5)

MAX_CHARS (1100) and OVERLAP (200)

Provide .env.example with those keys and comments. Use python-dotenv to load.

🧱 Core Modules (implement)
src/chunking.py

split_into_chunks(text: str, max_chars: int, overlap: int) -> list[str]

Sentence-aware using nltk.sent_tokenize with fallback to raw slicing.

src/embeddings.py

embed_texts(texts: list[str]) -> list[list[float]] calling POST {OLLAMA_URL}/api/embeddings with {"model": EMBED_MODEL, "input": texts}.

Handle both embedding and embeddings response shapes. Raise helpful errors.

src/store.py

get_client(persist_dir) -> chromadb.PersistentClient

get_or_create_collection(client, name="rag_docs")

add_texts(collection, ids, docs, metadatas, embeddings)

query(collection, query_text: str, k: int) -> list[tuple[str, dict]]

src/llm.py

chat(messages: list[dict]) -> str via POST {OLLAMA_URL}/api/chat with {"model": CHAT_MODEL, "messages": [...], "stream": false}.

Messages follow roles: system, user, assistant.

src/prompt.py

build_system_prompt() → concise safety/grounding instruction to cite sources only from context.

build_user_prompt(question: str, contexts: list[tuple[text, meta]]) → render a block:

Question: ...
Context:
[1] From: path (chunk n)
    text...
[2] ...


render_messages(system, user) -> list[dict] convenient wrapper.

src/rag.py

ingest_path(path, collection, max_chars, overlap):

Read PDF via pypdf, or text for .txt/.md.

Chunk → embed (batching) → add to store.

retrieve_and_answer(question, collection):

Query → build messages → call LLM → return answer + used sources.

🧰 CLI Scripts
ingest.py

Parse --folder docs/ (default), env vars from src/config.py.

Walk PDFs/TXT/MD; call rag.ingest_path.

Print counts and total chunks; nice progress logs.

query.py

Parse --q "question" (or interactive prompt if not given).

Load collection; call rag.retrieve_and_answer.

Print Answer and Sources neatly.

🌐 FastAPI Minimal UI
app/app.py

Endpoints:

GET / → render simple HTML with a question box.

POST /ask → JSON {question} → returns {answer, sources:[{source,chunk}]}.

Use the same src/rag.py logic.

Serve templates/index.html and static/styles.css.

templates/index.html

Minimal single-page form + results area; no frontend framework needed.

🧪 Testing

tests/test_chunking.py with 2–3 tests: sentence split, overlap behavior, fallback slicing.

📦 requirements.txt

Include:

chromadb==0.5.*
pypdf
python-dotenv
requests
nltk
fastapi
uvicorn
jinja2

🖥️ PowerShell helpers

Create run_api.ps1:

param(
  [string]$Host = "127.0.0.1",
  [int]$Port = 8000
)
$env:UVICORN_WORKERS="1"
uvicorn app.app:app --host $Host --port $Port --reload

📘 README.md (write clearly)

Prereqs: Python 3.11+, Ollama installed, models already created (qwen2.5 / tinyllama-1.1b), and nomic-embed-text pulled:

"C:\Users\MWAHID\AppData\Local\Programs\Ollama\ollama.exe" pull nomic-embed-text


Setup:

py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -c "import nltk; import nltk; nltk.download('punkt')"
Copy .env.example to .env and adjust if needed


Ingest & query:

python ingest.py
python query.py --q "Summarize neutropenic fever management"


Run API:

.\run_api.ps1
# open http://127.0.0.1:8000


Switching models: edit .env (CHAT_MODEL=tinyllama-1.1b).

Troubleshooting: Ollama not running → ollama serve; Chroma reset → delete vectorstore/.

✅ Acceptance Criteria

Running python ingest.py after dropping a PDF into docs/ prints “Ingestion complete” with chunk counts.

python query.py --q "…" returns an answer and at least 1 source.

Hitting POST /ask with JSON returns {answer, sources} in <2 steps.

Code is modular; swapping the chat model requires no code changes (only .env).

🚀 Stretch Goals (scaffold TODOs)

Add rerank stage (BM25 or small cross-encoder).

Add source dedup + max_tokens per chunk to control prompt size.

Add CSV export of answers with citations.

Add JWT-protected API key gate (simple bearer).

Add local PDF OCR fallback (pytesseract) for scans.

Create all files above with clean, commented code. Then stop.