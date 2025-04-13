# About This Project

While navigating through various documentation to find the help I needed, I realized there was so much information to sift through.
Many times, I found myself overwhelmed by the abundance of content, trying to pinpoint exactly what was relevant to me. 
I wanted a solution that could help me quickly find answers without diving through pages and pages of documentation.

So, I decided to build a generic chatbot that could search and retrieve relevant information from any documents. 
The goal was to simplify the process of accessing information, especially when dealing with a large volume of documents. 
In this case, I started with documents to help people like myself to *Get Help* while being unemployed, specifically focusing on resources
available in Williamson County and the Texas Workforce.

This project demonstrates how to take your local documents (such as PDFs, Word docs, and even SQL-based data) and quickly
build a chatbot to answer questions based on their content. You can drop in any documents you want to ask questions to the chatbot,
and it will retrieve relevant answers from them. But feel free to experiment with any other helpful documents
to expand and test the chatbot's capabilities!

Please check with your local government for latest documents. The Samples added may be out of date.

# Donate

If you find this project helpful and would like to support its development, you can donate via Ko-Fi: [Donate on Ko-Fi](https://ko-fi.com/igearfs)


🤖 Ethical Use of AI

This project is designed with the intention of responsibly using AI to help people access information more efficiently. Users are encouraged to:

    Respect privacy: Only upload and process documents you have the right to use.

    Avoid harmful use: Do not use this chatbot to spread misinformation or generate misleading content.

    Promote fairness: Remember that AI reflects the data it's given — be mindful of bias and context.

As with any tool, please use it ethically and responsibly.

```markdown
# 📚 Local Document Q&A System

This project enables you to build a **Question-Answering system** using documents in your local storage. It uses **LangChain**, **Ollama**, and **Chroma** for efficient document storage and retrieval. The system is designed to process and extract information from various file types like PDF, DOCX, SQL, and text files, allowing you to ask questions based on the documents you upload.

---

## Testing.

** Still needs SQL testing I have only done documents so far. **
This is the basics of how the SQL should be formatted and TEXT should be returned for processing:

## Example: SQL-based Documents

You can also add SQL-based documents to the chatbot. Here’s an example:

### SQL File Structure:

Suppose you have a file called `help_docs.sql` that contains the following data:

```sql
postgres://user:password@localhost:5432/mydatabase # Database URL (first line of the file)
SELECT * FROM help_resources WHERE category = 'Unemployment';  # SQL Query (subsequent lines) One Query per SQL file

## 🛠️ Features

- Load documents from local directories (`PDF`, `DOCX`, `TXT`, `SQL`, etc.)
- Use **Ollama** and **Chroma** for document embedding and storage
- Build a **local vector store** for fast document retrieval
- Ask natural language questions based on the loaded documents
- Local processing (No external API calls for retrieval)
  
## 🚀 Quick Start

How to run Ollama in windows. Good article below.
https://medium.com/@Tanzim/how-to-run-ollama-in-windows-via-wsl-8ace765cee12

if in windows you will also need python:
https://www.python.org/downloads/windows/

### Prerequisites

1. **Python 3.11+**
2. **C++14** (required by some dependencies)
3. **OpenOffice** (for document processing)
4. **Chroma DB** for vector storage

You can install required Python dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### Installation

1. Clone the repository:
   
   ```bash
   git clone https://github.com/igearfs/gethelp_chatbot.git
   cd local-document-qa
   ```

2. Install the dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have **C++14** and **OpenOffice** installed for document processing (see instructions below for your OS).

### Usage

1. Run the `llm_loader.py` to load documents into the Chroma DB:

    ```bash
    python llm_loader.py
    ```

    This will process all files in the `/docs` and `/sql` directories and build the Chroma vector store at `./data/chroma_db`.

2. Start the Streamlit app to interact with the Q&A system:

    ```bash
    streamlit run app.py
    ```

    This will start the app on your local server. You can open the app in your browser by navigating to the following URL:
   
    ```text
    http://localhost:8501
    ```

    Once the app is running, you can start asking questions based on the documents you loaded into the vector store.

---

## 📚 Supported File Types

- **PDF** (.pdf)
- **Text Files** (.txt, .md)
- **Word Documents** (.docx, .doc)
- **SQL files** (.sql)

The system supports loading these documents and extracting relevant information to create a searchable index.

---

## 🧩 Components

1. **llm_loader.py**: Loads documents from a specified directory, processes them, and stores them in Chroma for fast retrieval.
2. **localretrievalqa.py**: The core logic for querying the Chroma vector store to return relevant answers based on the documents.
3. **app.py**: Streamlit-based UI for interacting with the Q&A system.

---

## 📑 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 🖥️ Running on Windows

1. Ensure you have **C++14** installed (needed by some dependencies).
2. Install **OpenOffice** for document processing.
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the `llm_loader.py` to load documents into the Chroma DB:

   ```bash
   python llm_loader.py
   ```

5. Start the Streamlit app:

   ```bash
   streamlit run app.py
   ```

6. Open your browser and visit:

   ```text
   http://localhost:8501
   ```

---

## 🖥️ Running on macOS/Linux

1. Ensure you have **C++14** and **OpenOffice** installed:
   - macOS/Linux: Use package managers like `brew` or `apt-get` to install OpenOffice.
   - C++14: Ensure your C++ toolchain supports C++14 (e.g., `g++` 5+).

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the `llm_loader.py` to load documents into Chroma DB:

   ```bash
   python llm_loader.py
   ```

4. Start the Streamlit app:

   ```bash
   streamlit run app.py
   ```

5. Open your browser and visit:

   ```text
   http://localhost:8501
   ```

---

## 🤝 Contributing

Feel free to submit issues, pull requests, or suggestions! This is an open-source project, and contributions are welcome.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

```
⚠️ Disclaimer

While this chatbot uses AI to provide helpful responses based on the content of your documents, it is important to understand that no system is perfect. The AI may occasionally miss relevant information, misinterpret context, or provide incomplete answers.

Please verify any critical information against the original source documents and consult official resources or experts when in doubt. This tool is intended to assist, not replace, careful reading or professional advice.