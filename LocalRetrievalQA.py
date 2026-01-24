#  Copyright (c) 2025. In-Game Event, A Red Flag Syndicate LLC.

import logging
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from chromadb.config import Settings

CHROMA_DIR = "./data/chroma_db"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class LocalRetrievalQA:
    def __init__(self, model_name="mistral", persist_directory=CHROMA_DIR):
        logging.info("🔍 Initializing retriever and LLM...")

        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            client_settings=Settings(anonymized_telemetry=False),
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

        prompt_template = """
You are a helpful assistant that ONLY uses the provided context to answer questions.
If the context does not contain the answer, just say "I don't know based on the documents."

CONTEXT:
{context}

QUESTION:
{question}

HELPFUL ANSWER:
"""
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=prompt_template,
        )

        self.qa = RetrievalQA.from_chain_type(
            llm=OllamaLLM(model=model_name, temperature=0),
            retriever=self.retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True,
        )

    def ask(self, question: str) -> str:
        result = self.qa.invoke({"query": question})
        return result["result"]


if __name__ == "__main__":
    qa = LocalRetrievalQA()

    print("📚 Ask a question based only on your documents.")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("❓ Question: ")
        if question.lower() in ["exit", "quit"]:
            break
        answer = qa.ask(question)
        print(f"💬 Answer: {answer}\n")
