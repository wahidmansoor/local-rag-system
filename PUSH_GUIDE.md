# 🚀 Git Repository Setup Guide

This guide will help you initialize this RAG project as a Git repository and push it to GitHub.

## Prerequisites

- Git installed on your system
- GitHub account
- GitHub CLI (optional but recommended) or GitHub web interface access

## Step 1: Initialize Local Repository

If you haven't already initialized Git:

```powershell
git init
```

## Step 2: Stage and Commit Files

Add all files to Git (the .gitignore will exclude unnecessary files):

```powershell
git add .
git commit -m "feat: initial RAG system with Ollama integration

- Local RAG system using ChromaDB and Ollama
- Support for PDF, TXT, and Markdown ingestion
- CLI tools for ingestion and querying
- FastAPI web interface
- Windows PowerShell setup scripts
- Comprehensive test suite
- GitHub Actions CI/CD"
```

## Step 3: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)

```powershell
# Install GitHub CLI if not already installed
# winget install GitHub.cli

# Login to GitHub
gh auth login

# Create repository (choose public or private)
gh repo create my-rag-system --public --description "Local RAG system with Ollama integration"

# Push to GitHub
git remote add origin https://github.com/YOUR-USERNAME/my-rag-system.git
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Web Interface

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `my-rag-system` (or your preferred name)
3. Description: `Local RAG system with Ollama integration`
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

Then run these commands:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git branch -M main
git push -u origin main
```

## Step 4: Verify Repository

Visit your repository on GitHub to confirm:

- ✅ All source code files are present
- ✅ README.md displays correctly
- ✅ GitHub Actions workflow is detected
- ✅ License is recognized
- ✅ .gitignore is working (no .venv/, vectorstore/, etc.)

## Step 5: Set Up Repository Settings (Optional)

### Branch Protection Rules

To protect your main branch:

1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable "Require status checks to pass before merging"
4. Select the CI workflow
5. Enable "Require pull request reviews before merging"

### Repository Topics

Add topics to make your repository discoverable:

1. Go to repository main page
2. Click the gear icon next to "About"
3. Add topics: `rag`, `ollama`, `python`, `vector-database`, `ai`, `fastapi`, `chromadb`

### Enable Discussions (Optional)

For community questions and feedback:

1. Go to Settings → General
2. Scroll to "Features"
3. Check "Discussions"

## Step 6: Create First Release

After confirming everything works:

```powershell
git tag -a v1.0.0 -m "Initial release of RAG system"
git push origin v1.0.0
```

Then create a release on GitHub:

1. Go to Releases → Create a new release
2. Tag: `v1.0.0`
3. Title: `Initial Release - Local RAG System v1.0.0`
4. Description:
```markdown
# 🎉 Initial Release

A complete local RAG (Retrieval-Augmented Generation) system using Ollama.

## Features
- 📚 PDF, TXT, and Markdown document ingestion
- 🔍 Semantic search with ChromaDB
- 🤖 Local AI with Ollama models
- 🌐 Web interface with FastAPI
- 💻 Windows PowerShell scripts
- 🧪 Comprehensive test suite

## Quick Start
```powershell
.\first_run.ps1
```

See README.md for detailed instructions.
```

## Next Steps

- ⭐ Star your own repository
- 📝 Update README.md with any specific setup notes
- 🐛 Open issues for any bugs or enhancements
- 🔄 Set up regular backups with `git push`
- 👥 Share with collaborators if needed

## Repository Maintenance

### Regular Updates

```powershell
# After making changes
git add .
git commit -m "feat: description of changes"
git push
```

### Sync with Remote

```powershell
# Pull latest changes (if collaborating)
git pull origin main
```

### Clean Up

```powershell
# Remove merged branches
git branch -d old-feature-branch

# Clean up remote references
git remote prune origin
```

Congratulations! Your RAG system is now version-controlled and ready for collaboration! 🎉
