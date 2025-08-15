# Local RAG System

A minimal, offline RAG (Retrieval-Augmented Generation) system that works with Ollama models on Windows. Ingest PDFs, TXT, and Markdown files, then query them using local AI models.

## 🚀 Quick Start

**Automated Setup (Recommended):**
```powershell
.\first_run.ps1
```

This script will automatically:
- Create Python virtual environment
- Install all dependencies
- Download NLTK data
- Pull required Ollama models
- Create sample documents
- Run initial ingestion
- Start the web server

**Manual Setup:** See [Manual Setup](#manual-setup) section below.

## Prerequisites

- **Python 3.11+**
- **Ollama installed** and running
  - Download from: https://ollama.ai
  - Start with: `ollama serve`
- **Required Ollama models:**
  ```powershell
  ollama pull qwen2.5
  ollama pull nomic-embed-text
  ```

## Manual Setup

1. **Create virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Download NLTK data:**
   ```powershell
   python -c "import nltk; nltk.download('punkt')"
   ```

4. **Configure environment:**
   ```powershell
   Copy-Item .env.example .env
   # Edit .env if needed to change models or settings
   ```

## Usage

### 1. Ingest Documents

Place your PDF, TXT, or Markdown files in the `docs/` folder, then run:

```powershell
python ingest.py
```

To specify a different folder:
```powershell
python ingest.py --folder "my_documents"
```

### 2. Query via CLI

Ask questions about your documents:

```powershell
python query.py --q "Summarize neutropenic fever management"
```

Or run interactively:
```powershell
python query.py
```

### 3. Web Interface

Start the FastAPI server:
```powershell
.\run_api.ps1
```

Then open http://127.0.0.1:8000 in your browser.

## Configuration

Edit `.env` to customize:

- `CHAT_MODEL`: Switch between `qwen2.5` and `tinyllama-1.1b`
- `EMBED_MODEL`: Embedding model (default: `nomic-embed-text`)
- `TOP_K`: Number of chunks to retrieve (default: 5)
- `MAX_CHARS`: Maximum characters per chunk (default: 1100)
- `OVERLAP`: Overlap between chunks (default: 200)

## Health Checks

**Check Ollama status:**
```powershell
# Check if Ollama is running
curl http://127.0.0.1:11434/api/tags

# List installed models
ollama list

# Test embedding model
ollama run nomic-embed-text "test"

# Test chat model
ollama run qwen2.5 "Hello, how are you?"
```

**Check Python environment:**
```powershell
# Verify Python version
python --version

# Check installed packages
pip list

# Test imports
python -c "from src import config, rag; print('✅ All modules imported')"
```

**Check vector store:**
```powershell
# List vector store contents
dir vectorstore/

# Check if documents are ingested
python -c "from src.store import get_client, get_or_create_collection; from src.config import PERSIST_DIR; client = get_client(PERSIST_DIR); collection = get_or_create_collection(client); print(f'Documents: {collection.count()}')"
```

## Troubleshooting

**Ollama not running:**
```powershell
ollama serve
```

**Reset vector store:**
```powershell
Remove-Item -Recurse -Force vectorstore/
```

**Model not found:**
```powershell
ollama list
# Pull missing models as shown in Prerequisites
```

## Project Structure

```
rag-local/
├── docs/                     # Drop your documents here
├── vectorstore/             # ChromaDB storage (auto-created)
├── app/                     # FastAPI web interface
├── src/                     # Core RAG modules
├── tests/                   # Unit tests
├── ingest.py               # CLI ingestion script
├── query.py                # CLI query script
├── run_api.ps1            # Start web server
└── requirements.txt        # Python dependencies
```

## API Endpoints

- `GET /` - Web chat interface
- `POST /ask` - Query endpoint (JSON: `{"question": "..."}`)
- `GET /health` - Health check

## Testing

Run tests:
```powershell
python -m pytest tests/
```

Or run specific test:
```powershell
python tests/test_chunking.py
```
