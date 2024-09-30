#!/bin/bash

# Start the Ollama server in the background
ollama serve &

# Wait for the server to start up (give it enough time)
sleep 10

# Pull the LLaMA model
ollama pull llama3.1

# Run the model after it's pulled
ollama run llama3.1

# Keep the container running to avoid it from exiting
wait
