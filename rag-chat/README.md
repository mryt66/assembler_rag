# W-RAG-CHAT-APP

RAG-CHAT-APP is a lightweight, containerized Retrieval-Augmented Generation (RAG) system that uses FAISS for semantic search and integrates with Google’s Gemini API for content generation. It includes a FastAPI backend with persistent conversation logging using SQLite.

## 📦 Features

- ✅ Dockerized API server for easy deployment

- 🔍 FAISS-based semantic search for relevant context retrieval

- 🧠 RAG pipeline with Gemini API integration

- 💬 FastAPI endpoint for interactive chat sessions

- 🗃️ Conversation logging using SQLite

- 🚀 Simple shell scripts to manage system lifecycle (start_system.sh, stop_system.sh)

- 🌐 Ngrok integration for external access

## 📁 Project Structure
```bash
W-RAG-CHAT-APP/
│
├── data/                            # Persistent volume for database and files
│
├── Dockerfile                       # Docker image specification
├── main.py                          # FastAPI app with RAG logic
├── request.py                       # example request 
├── output_chunks.jsonl              # Text chunks for semantic search
├── rag_prompt_config.jsonl          # Base/system prompt definitions
├── faiss_index.index                # Saved FAISS index (auto-generated)
│
├── start_system.sh                  # Start the app + ngrok
├── stop_system.sh                   # Stop everything
```
## 🚀 Getting Started

### Prerequisites

- Docker
- Ngrok (installed and accessible via CLI)
- .jsonl config and chunk files placed in root (as seen above)
- A valid Gemini API Key

### 1. Build the Docker Image
```bash
docker build -t rag-chat .
```

### 2. Run the System
```bash
export GEMINI_API_KEY=your_api_key_here
./start_system.sh
```
### 💡 This:
> - Starts the container and exposes it on port `10000`  
> - Mounts the `data/` folder for persistent database storage  
> - Launches an ngrok tunnel in a background `tmux` session

### 3. Stop the System
```bash
./stop_system.sh
```

## 🧠 API Usage

### Endpoint
```bash
POST /chat
```
### Request Body
```json
{
          "history": [
            {
                "role": "user",
                "message": "Jak działa maszyna W?"
            },
            {
                "role": "assistant",
                "message": "Maszyna W jest symulowanym procesorem, dla którego pisze się programy w języku asemblera. Program składa się z instrukcji (rozkazów) i danych. Każda linia programu zawiera etykietę (opcjonalną)..."
            },
            {
                "role": "user",
                "message": "Napisz program w języku W, który oblicza sumę liczb od 1 do 10."
            },
  ]
}
```
### Response
```json
{
  "response": "```assembly\n Program oblicza sumę liczb od 1 do 10\n\n SUMA RPA ; Rezerwacja miejsca na zmienną SUMA (wynik)\n LICZNIK RST 1 ;\n licznika wartością 1\n LIMIT RST 10 ; Ustawienie górnej granicy pętli\n\n POCZATEK:\n..."
}
```
## 🧬 How It Works

### Startup:

- Loads output_chunks.jsonl and rag_prompt_config.jsonl
- Initializes or loads FAISS index
- Sets up SQLite DB
- Request Handling:
- Builds a concatenated prompt using semantic search via FAISS
- Sends this prompt to Gemini API
- Logs the full interaction in the database
- Returns the assistant's response

## 🛠 Developer Notes
- Default port: 10000
- DB file: data/conversations.db
- If faiss_index.index does not exist, it is built at runtime