#!/bin/bash

# Start Ollama server in a background screen session
echo "Starting Ollama server..."
screen -dmS ollama_screen ollama serve

# Wait for Ollama server to be ready
echo "Waiting for Ollama server to be ready..."
until curl -s http://localhost:11434 > /dev/null; do
    sleep 2
done

# Only pull model + run indexer the first time
if [ ! -f /root/indexer_done.txt ]; then
    echo "First-time setup: Pulling mistral:7b..."
    if ! ollama pull mistral:7b; then
        echo "Model pull failed. Exiting."
        exit 1
    fi

    echo "Launching mistral:7b in background..."
    screen -dmS mistral_7b_session ollama run mistral

    echo "Running indexer..."
    if python llm_indexer.py; then
        touch /root/indexer_done.txt
    else
        echo "Indexer failed. Exiting."
        exit 1
    fi
else
    echo "Startup: Model already pulled and indexer completed. Skipping setup..."
    echo "Launching mistral:7b in background..."
    screen -dmS mistral_7b_session ollama run mistral
fi

# Start Streamlit hopefully...
echo "Starting Streamlit app..."
exec streamlit run app.py \
    --server.enableCORS=false \
    --server.headless=true \
    --server.port=8501
