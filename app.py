#  Copyright (c) 2025. In-Game Event, A Red Flag Syndicate LLC.

import streamlit as st
from LocalRetrievalQA import LocalRetrievalQA

st.set_page_config(page_title="📚 Local Document Q&A", layout="centered")
# Initialize once
@st.cache_resource

def get_qa():
    return LocalRetrievalQA()

qa = get_qa()

# App layout
from chromadb.config import Settings
client = chromadb.Client(Settings(anonymized_telemetry=False))
# or if using PersistentClient
client = chromadb.PersistentClient(path=".", settings=Settings(anonymized_telemetry=False))

st.title("📚 Ask Questions About Your Documents")
st.markdown("Powered by Ollama + LangChain + Streamlit")

# Input
question = st.text_input("❓ Ask a question:")

# Handle query
if question:
    with st.spinner("Searching..."):
        answer = qa.ask(question)
    st.success("💬 Answer:")
    st.write(answer)
