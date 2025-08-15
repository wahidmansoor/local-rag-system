"""CLI script for ingesting documents into the vector store."""
import argparse
import os
from pathlib import Path

from src.config import PERSIST_DIR
from src.store import get_client, get_or_create_collection
from src.rag import ingest_path

def main():
    parser = argparse.ArgumentParser(description="Ingest documents into RAG vector store")
    parser.add_argument(
        "--folder",
        default="docs",
        help="Folder containing documents to ingest (default: docs)"
    )
    
    args = parser.parse_args()
    
    # Create docs folder if it doesn't exist
    docs_dir = Path(args.folder)
    docs_dir.mkdir(exist_ok=True)
    
    print(f"📁 Scanning folder: {docs_dir.absolute()}")
    
    try:
        # Get collection
        client = get_client(PERSIST_DIR)
        collection = get_or_create_collection(client)
        
        # Find files to ingest
        supported_extensions = ['.pdf', '.txt', '.md']
        files_to_ingest = []
        
        for ext in supported_extensions:
            files_to_ingest.extend(docs_dir.glob(f"*{ext}"))
            files_to_ingest.extend(docs_dir.glob(f"**/*{ext}"))
        
        if not files_to_ingest:
            print(f"❌ No supported files found in {args.folder}/")
            print(f"📋 Supported formats: {', '.join(supported_extensions)}")
            print("💡 Add some .pdf, .txt, or .md files to the docs/ folder and try again.")
            return
        
        # Ingest files
        total_chunks = 0
        processed_files = 0
        failed_files = 0
        
        print(f"🔍 Found {len(files_to_ingest)} files to process")
        print("-" * 60)
        
        for file_path in files_to_ingest:
            print(f"📄 Processing: {file_path.name}")
            try:
                chunks_added = ingest_path(str(file_path), collection)
                if chunks_added > 0:
                    total_chunks += chunks_added
                    processed_files += 1
                    print(f"  ✅ Added {chunks_added} chunks")
                else:
                    failed_files += 1
                    print(f"  ⚠️ No chunks added (empty or unsupported content)")
            except Exception as e:
                failed_files += 1
                print(f"  ❌ Error: {e}")
            print()
        
        print("-" * 60)
        print(f"🎉 Ingestion complete!")
        print(f"✅ Successfully processed: {processed_files} files")
        if failed_files > 0:
            print(f"⚠️ Failed to process: {failed_files} files")
        print(f"📊 Total chunks added: {total_chunks}")
        
        if total_chunks == 0:
            print("\n💡 Tips:")
            print("- Ensure your documents contain readable text")
            print("- Check that PDF files are not scanned images")
            print("- Verify file encoding for text files")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return 1

if __name__ == "__main__":
    main()
