import os
import json
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session

# Determine the absolute path of the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data") # For the database and potentially other data

# Construct absolute paths for data files
OUTPUT_CHUNKS_FILE = os.path.join(SCRIPT_DIR, "output_chunks.jsonl")
RAG_CONFIG_FILE = os.path.join(SCRIPT_DIR, "rag_prompt_config.jsonl")
FAISS_INDEX_FILE = os.path.join(SCRIPT_DIR, "faiss_index.index")

DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'conversations.db')}"

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text)
    response = Column(Text)
    context = Column(Text)
    base_context = Column(Text)
    system_prompt = Column(Text)
    full_prompt = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

origins = ["http://localhost:5173", "https://wmaszyna.netlify.app/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

chunks = None
base_chunk = None
system_prompt = None
API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def load_chunks(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def retrieve_relevant_chunks(query, chunks, model, top_k=3):
    texts = [chunk['content'] for chunk in chunks]
    chunk_embeddings = model.encode(texts, convert_to_numpy=True).astype('float32')
    faiss.normalize_L2(chunk_embeddings)

    embedding_dim = chunk_embeddings.shape[1]
    index_file = FAISS_INDEX_FILE # Use absolute path
    if not os.path.exists(index_file):
        index = faiss.IndexFlatIP(embedding_dim)
        index.add(chunk_embeddings)
        faiss.write_index(index, index_file)
    else:
        index = faiss.read_index(index_file)

    query_embedding = model.encode([query], convert_to_numpy=True).astype('float32')
    faiss.normalize_L2(query_embedding)
    _, indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0]]

def construct_prompt(chunks, model, base_chunk, system_prompt, query):
    relevant_chunks = retrieve_relevant_chunks(query, chunks, model)
    context = "".join([chunk['content'] + "\n" for chunk in relevant_chunks])
    full_prompt = f"System prompt:\n{system_prompt['content']}\nContext:\n{context}\n{base_chunk['content']}\nQuery:\n{query}"

    return full_prompt,context

def get_answer(prompt):
    prompt_data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(
        URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(prompt_data)
    )

    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return None

class ChatRequest(BaseModel):
    history: list

@app.on_event("startup")
def load_configs():
    global chunks, base_chunk, system_prompt
    chunks = load_chunks(OUTPUT_CHUNKS_FILE) # Use absolute path
    config = load_chunks(RAG_CONFIG_FILE)[0] # Use absolute path
    base_chunk = config['base_chunk']
    system_prompt = config['system_prompt']

    Base.metadata.create_all(bind=engine)


@app.post("/chat")
def chat(req: ChatRequest,db: Session = Depends(get_db)):
    query = ""
    for item in req.history:
        if item["role"] == "user":
            query += f"User query: {item['message']}\n"
        elif item["role"] == "assistant":
            query += f"Gemini response: {item['message']}\n"

    full_prompt,context = construct_prompt(chunks, model, base_chunk, system_prompt, query)
    answer = get_answer(full_prompt)
    if answer is None:
        answer = "Failed to get a response from Gemini"
    
    db.add(Conversation(
        query=query,
        response=answer,
        context=context,
        base_context=base_chunk['content'],
        system_prompt=system_prompt['content'],
        full_prompt=full_prompt
    ))
    db.commit()

    return {"response": answer}

if __name__ == "__main__":
    import uvicorn
    # Ensure the data directory exists, as DATABASE_URL points to it.
    if not os.path.exists(DATA_DIR): # Use absolute path for data directory
        os.makedirs(DATA_DIR)
    # The load_configs function is called at startup by FastAPI's @app.on_event("startup")
    # so no need to call it explicitly here before uvicorn.run
    uvicorn.run(app, host="127.0.0.1", port=8000)
