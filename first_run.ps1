#!/usr/bin/env pwsh
param(
    [switch]$SkipVenv,
    [switch]$SkipOllama,
    [switch]$SkipIngest,
    [string]$DocsFolder = "docs"
)

Write-Host "🚀 RAG System First-Run Setup" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check if Python is available
Write-Host "📋 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Error "❌ Python not found. Please install Python 3.11+ and ensure it's in your PATH."
    exit 1
}

# Create virtual environment
if (-not $SkipVenv) {
    Write-Host "🐍 Setting up Python virtual environment..." -ForegroundColor Yellow
    
    if (-not (Test-Path ".venv")) {
        python -m venv .venv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Virtual environment created" -ForegroundColor Green
        } else {
            Write-Error "❌ Failed to create virtual environment"
            exit 1
        }
    } else {
        Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
    }
    
    # Activate virtual environment
    Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
    
    # Upgrade pip and install dependencies
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Error "❌ Failed to install dependencies"
        exit 1
    }
    
    # Download NLTK data
    Write-Host "📚 Downloading NLTK data..." -ForegroundColor Yellow
    python -c "import nltk; nltk.download('punkt', quiet=True); print('NLTK punkt data downloaded')"
}

# Check Ollama installation and pull models
if (-not $SkipOllama) {
    Write-Host "🤖 Checking Ollama setup..." -ForegroundColor Yellow
    
    # Check if Ollama is running
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method Get -TimeoutSec 5
        Write-Host "✅ Ollama is running" -ForegroundColor Green
        
        # Check for required models
        $models = $response.models | ForEach-Object { $_.name }
        
        if ($models -contains "nomic-embed-text:latest") {
            Write-Host "✅ Embedding model (nomic-embed-text) is available" -ForegroundColor Green
        } else {
            Write-Host "📥 Pulling embedding model..." -ForegroundColor Yellow
            & ollama pull nomic-embed-text
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Embedding model downloaded" -ForegroundColor Green
            } else {
                Write-Warning "⚠️ Failed to download embedding model. You may need to run 'ollama pull nomic-embed-text' manually."
            }
        }
        
        if ($models -contains "qwen2.5:latest") {
            Write-Host "✅ Chat model (qwen2.5) is available" -ForegroundColor Green
        } else {
            Write-Host "📥 Pulling chat model..." -ForegroundColor Yellow
            & ollama pull qwen2.5
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Chat model downloaded" -ForegroundColor Green
            } else {
                Write-Warning "⚠️ Failed to download chat model. You may need to run 'ollama pull qwen2.5' manually."
            }
        }
        
    } catch {
        Write-Warning "⚠️ Ollama not running or not accessible. Please:"
        Write-Host "   1. Install Ollama from https://ollama.ai" -ForegroundColor Cyan
        Write-Host "   2. Run 'ollama serve' in another terminal" -ForegroundColor Cyan
        Write-Host "   3. Pull required models:" -ForegroundColor Cyan
        Write-Host "      ollama pull nomic-embed-text" -ForegroundColor Cyan
        Write-Host "      ollama pull qwen2.5" -ForegroundColor Cyan
    }
}

# Create docs folder and add sample document
Write-Host "📁 Setting up documents folder..." -ForegroundColor Yellow
if (-not (Test-Path $DocsFolder)) {
    New-Item -ItemType Directory -Path $DocsFolder
    Write-Host "✅ Created $DocsFolder folder" -ForegroundColor Green
}

$sampleDoc = Join-Path $DocsFolder "sample.txt"
if (-not (Test-Path $sampleDoc)) {
    @"
# Sample Document for RAG System

This is a sample document to test your RAG (Retrieval-Augmented Generation) system.

## Key Features

1. **Document Ingestion**: The system can process PDF, TXT, and Markdown files
2. **Chunking**: Text is split into manageable chunks with overlap
3. **Embeddings**: Uses Ollama's nomic-embed-text model for vector embeddings
4. **Retrieval**: Finds relevant chunks using similarity search
5. **Generation**: Uses Ollama's chat models to generate responses

## Usage Instructions

1. Place your documents in the docs/ folder
2. Run ingestion: python ingest.py
3. Query the system: python query.py --q "Your question here"
4. Or use the web interface: .\run_api.ps1

## Models Supported

- Embedding: nomic-embed-text
- Chat: qwen2.5, tinyllama-1.1b, llama2

Enjoy using your local RAG system!
"@ | Out-File -FilePath $sampleDoc -Encoding UTF8
    Write-Host "✅ Created sample document" -ForegroundColor Green
}

# Run document ingestion
if (-not $SkipIngest) {
    Write-Host "📚 Ingesting documents..." -ForegroundColor Yellow
    python ingest.py --folder $DocsFolder
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Document ingestion completed" -ForegroundColor Green
    } else {
        Write-Warning "⚠️ Document ingestion failed. You can run 'python ingest.py' manually later."
    }
}

# Final instructions
Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. To start the web interface:" -ForegroundColor White
Write-Host "   .\run_api.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. To query via command line:" -ForegroundColor White
Write-Host "   python query.py --q `"Your question here`"" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. To add more documents:" -ForegroundColor White
Write-Host "   - Place files in the $DocsFolder/ folder" -ForegroundColor Yellow
Write-Host "   - Run: python ingest.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Access the web app at: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Happy RAG-ing! 🤖📚" -ForegroundColor Green
