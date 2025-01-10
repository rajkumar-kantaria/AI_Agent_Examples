from typing import List
from langchain_pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores.base import VectorStoreRetriever
import dotenv

dotenv.load_dotenv()

index_name = "index-name"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
pinecone = Pinecone(embedding=embeddings, index_name=index_name)

def generate_ollama_embeddings(texts: List[str]) -> VectorStoreRetriever:        
    # Create vector store
    db = pinecone.from_texts(
        texts=texts,
        embedding=embeddings,
        index_name=index_name
    )
    
    return db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

def get_retriever_from_index() -> VectorStoreRetriever:
    db = pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
    return db.as_retriever(search_type="similarity", search_kwargs={"k": 4})
