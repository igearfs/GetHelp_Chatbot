#  Copyright (c) 2025. In-Game Event, A Red Flag Syndicate LLC.

import logging
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class LocalRetrievalQA:
    def __init__(self, model_name="mistral", persist_directory="./data/chroma_db"):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        logging.info("🔍 Initializing retriever and LLM...")

        self.embeddings = OllamaEmbeddings(model=model_name)
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever()

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
            llm=OllamaLLM(model=model_name),
            retriever=self.retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True,
        )

    def ask(self, question: str) -> str:
        # Get the relevant documents
        context = self.retriever.get_relevant_documents(question)
        if not context:
            logging.info(f"No relevant documents found for the question: {question}")
        else:
            logging.info(f"Context retrieved: {context}")

        result = self.qa.invoke({"query": question})
        # result = self.qa({"query": question})
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
