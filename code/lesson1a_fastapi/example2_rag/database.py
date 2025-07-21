import chromadb
from langchain_huggingface import HuggingFaceEmbeddings

DOCS_DIR = "sample_data"


# Initialize embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(DOCS_DIR)