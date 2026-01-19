#  Copyright (c) 2025. In-Game Event, A Red Flag Syndicate LLC.

import os
import shutil
import logging  # <-- Make sure logging is imported

# Import OllamaEmbeddings from the new package
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document  # <-- Needed for wrapping chunks
from llm_loader import load_all_documents  # This should be your own loader

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def build_vectorstore(documents, model_name="mistral", persist_directory="./data/chroma_db"):
    """
    Build a Chroma vectorstore from the provided documents.
    """

    logging.info("Building new Chroma vectorstore...")

    # Chunk the documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = []
    for doc in documents:
        text_chunks = splitter.split_text(doc.page_content)  # Split based on page_content
        for chunk in text_chunks:
            chunks.append(Document(page_content=chunk, metadata=doc.metadata))  # Wrap each chunk in Document
    logging.info(f"Split into {len(chunks)} chunks.")

    # Build embeddings and save to Chroma
    embeddings = OllamaEmbeddings(model=model_name)
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=persist_directory)

    logging.info(f"✅ Vectorstore built and saved to: {persist_directory}")


if __name__ == "__main__":
    persist_directory = "./data/chroma_db"
    if os.path.exists(persist_directory):
        logging.info("Removing existing Chroma store...")
        shutil.rmtree(persist_directory)
    logging.info("📁 Loading documents...")
    documents = load_all_documents()
    build_vectorstore(documents)
