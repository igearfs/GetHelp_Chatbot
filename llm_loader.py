#  Copyright (c) 2025. In-Game Event, A Red Flag Syndicate LLC.

import os
import logging
import psycopg2
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)

DOCS_DIR = "./docs"
SQL_DIR = "./sql"

logging.basicConfig(level=logging.INFO)

def load_documents_from_directory(directory: str) -> List[Document]:
    docs = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        ext = filename.lower().split(".")[-1]
        try:
            if ext == "pdf":
                loader = PyPDFLoader(path)
            elif ext in ["txt", "text", "md"]:
                loader = TextLoader(path)
            elif ext in ["docx", "doc"]:
                loader = UnstructuredWordDocumentLoader(path)
            else:
                logging.warning(f"Unsupported file type: {filename}")
                continue
            file_docs = loader.load()
            for doc in file_docs:
                doc.metadata["source"] = filename
            docs.extend(file_docs)
        except Exception as e:
            logging.error(f"Error loading {filename}: {e}")
    return docs

def load_documents_from_sql_dir(sql_dir: str) -> List[Document]:
    sql_docs = []
    for filename in os.listdir(sql_dir):
        if not filename.endswith(".sql"):
            continue
        path = os.path.join(sql_dir, filename)
        with open(path, "r") as f:
            lines = f.readlines()
        if len(lines) < 2:
            continue
        db_url = lines[0].strip()
        sql_query = "".join(lines[1:]).strip()
        try:
            conn = psycopg2.connect(db_url)
            cur = conn.cursor()
            cur.execute(sql_query)
            rows = cur.fetchall()
            colnames = [desc[0] for desc in cur.description]
            for row in rows:
                content = "\n".join([f"{col}: {val}" for col, val in zip(colnames, row)])
                sql_docs.append(Document(page_content=content, metadata={"source": filename}))
            cur.close()
            conn.close()
        except Exception as e:
            logging.error(f"SQL error in {filename}: {e}")
    return sql_docs

def load_all_documents() -> List[Document]:
    file_docs = load_documents_from_directory(DOCS_DIR)
    sql_docs = load_documents_from_sql_dir(SQL_DIR)
    return file_docs + sql_docs
