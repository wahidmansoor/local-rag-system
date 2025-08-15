"""CLI script for querying the RAG system."""
import argparse
from src.config import PERSIST_DIR, TOP_K
from src.store import get_client, get_or_create_collection
from src.rag import retrieve_and_answer

def main():
    parser = argparse.ArgumentParser(description="Query the RAG system")
    parser.add_argument(
        "--q", "--question",
        dest="question",
        help="Question to ask"
    )
    
    args = parser.parse_args()
    
    try:
        # Get collection
        client = get_client(PERSIST_DIR)
        collection = get_or_create_collection(client)
        
        # Check if collection has any documents
        try:
            count = collection.count()
            if count == 0:
                print("❌ No documents found in the knowledge base.")
                print("💡 Run 'python ingest.py' first to add documents.")
                return
            else:
                print(f"📚 Knowledge base contains {count} document chunks")
        except:
            print("⚠️ Could not check document count, but proceeding...")
        
        # Get question
        question = args.question
        if not question:
            question = input("🤔 Enter your question: ").strip()
        
        if not question:
            print("❌ No question provided.")
            return
        
        print(f"❓ Question: {question}")
        print("-" * 60)
        
        answer, sources = retrieve_and_answer(question, collection, TOP_K)
        
        print("💭 Answer:")
        print(answer)
        print()
        
        if sources:
            print(f"📖 Sources ({len(sources)} found):")
            for i, source in enumerate(sources, 1):
                print(f"[{i}] 📄 {source['source']} (chunk {source['chunk']})")
                print(f"    💬 {source['text']}")
                print()
        else:
            print("📭 No sources found.")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure:")
        print("  - Ollama is running: ollama serve")
        print("  - Required models are installed: ollama pull nomic-embed-text")
        print("  - Documents have been ingested: python ingest.py")

if __name__ == "__main__":
    main()
