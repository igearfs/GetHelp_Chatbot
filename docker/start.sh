#!/bin/bash

# Start Ollama server in a background screen session
echo "Starting Ollama server..."
screen -dmS ollama_screen ollama serve

# Wait for Ollama server to be ready
echo "Waiting for Ollama server to be ready..."
until curl -s http://localhost:11434 > /dev/null; do
    sleep 2
done

# Only pull model + run indexer the first time (based on chroma_db existence)
CHROMA_DB_DIR="/app/chroma_db"  # Update path if needed

if [ ! -d "$CHROMA_DB_DIR" ]; then
    echo "First-time setup: chroma_db not found."

    echo "Pulling mistral:7b..."
    if ! ollama pull mistral:7b; then
        echo "Model pull failed. Exiting."
        exit 1
    fi

    echo "Running indexer..."
    if python llm_indexer.py; then
        echo "Indexing complete."
    else
        echo "Indexer failed. Exiting."
        exit 1
    fi
else
    echo "Startup: chroma_db found. Skipping model pull and indexing..."
fi

# Start Streamlit
echo "Starting Streamlit app..."
exec streamlit run app.py \
    --server.enableCORS=false \
    --server.headless=true \
    --server.port=8501
