
#  Copyright (c) 2025. In-Game Event, A Red Flag Syndicate LLC.

import os
import shutil
import logging

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.config import Settings

from llm_loader import load_all_documents

CHROMA_DIR = "./data/chroma_db"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def build_vectorstore(
    persist_directory: str = CHROMA_DIR,
    embedding_model: str = "nomic-embed-text",
):
    logging.info("📁 Loading documents...")
    documents = load_all_documents()
    if not documents:
        logging.warning("⚠️ No documents found. Aborting.")
        return

    logging.info(f"📄 Loaded {len(documents)} documents")

    logging.info("✂️ Chunking documents...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_documents(documents)
    logging.info(f"🧩 Created {len(chunks)} chunks")

    logging.info("🧠 Initializing embeddings...")
    embeddings = OllamaEmbeddings(model=embedding_model)

    logging.info("📦 Writing Chroma vectorstore...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        client_settings=Settings(anonymized_telemetry=False)
    )

    logging.info(f"✅ Vectorstore built at: {persist_directory}")


if __name__ == "__main__":
    if os.path.exists(CHROMA_DIR):
        logging.info("🗑️ Removing existing Chroma store...")
        shutil.rmtree(CHROMA_DIR)

    build_vectorstore()
