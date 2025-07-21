from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from database import collection, DOCS_DIR


def safe_load_markdown(filepath: str):
    """Attempt to load a markdown file with fallback encoding."""
    try:
        loader = TextLoader(filepath, encoding='utf-8')
        return loader.load()
    except UnicodeDecodeError:
        print(f"⚠️ UTF-8 failed for {filepath}. Retrying with latin-1...")
        loader = TextLoader(filepath, encoding='latin-1')
        return loader.load()
    except Exception as e:
        print(f"❌ Failed to load {filepath}: {e}")
        return []


def ingest_documents():
    """Load markdown documents into ChromaDB"""
    print(f"🔍 Looking for documents in: {os.path.abspath(DOCS_DIR)}")

    if not os.path.exists(DOCS_DIR):
        print(f"❌ Folder {DOCS_DIR} does not exist. Creating it...")
        os.makedirs(DOCS_DIR, exist_ok=True)
        return

    md_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]
    if not md_files:
        print("❌ No markdown (.md) files found.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    total_chunks = 0

    for filename in md_files:
        filepath = os.path.join(DOCS_DIR, filename)
        print(f"📄 Processing: {filepath}")

        try:
            documents = safe_load_markdown(filepath)
            if not documents:
                continue

            chunks = splitter.split_documents(documents)

            batch_docs = [chunk.page_content for chunk in chunks]
            batch_ids = [f"{filename}_{i}" for i in range(len(chunks))]
            batch_metadatas = [{"title": filename, "chunk": i} for i in range(len(chunks))]

            collection.add(
                documents=batch_docs,
                metadatas=batch_metadatas,
                ids=batch_ids
            )

            print(f"✅ Added {len(chunks)} chunks from {filename}")
            total_chunks += len(chunks)

        except Exception as e:
            print(f"⚠️ Error processing {filename}: {e}")

    print(f"\n🚀 Total chunks ingested: {total_chunks}")


def check_database():
    """Check what's in the ChromaDB collection"""
    count = collection.count()
    print(f"\n📦 Collection has {count} documents")

    if count > 0:
        results = collection.get(limit=3)
        print("🧪 Sample documents:")
        for i, doc in enumerate(results['documents']):
            print(f"Doc {i}: {doc[:100]}...")
            print(f"Metadata: {results['metadatas'][i]}")
            print("---")


if __name__ == "__main__":
    ingest_documents()
    check_database()
