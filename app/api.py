import requests
from fastapi import FastAPI, HTTPException, Body
import re
import json
from utils.transpiler import PythonToWTranspiler

prompt = """ Wykonaj to zadanie w języku Python, nie importuj żadnych bibliotek, nie używaj funkcji def, nie komplikuj kodu, nie dodawaj typów np. int, użyj jak najprostszych metod programowania, w najprostszej strukturze kodu jaką tylko się da. Wynik podaj w postaci tylko i wyłącznie kodu w jednej komórce bez żadnych komentarzy, nie używaj funkcji (def), oraz f-stringów, oraz innych wbudowanych funkcji pythona. Zadanie: """
app = FastAPI(
    title="Maszyna W API",
    description="Tu jakiś opis",
    version="0.1.0"
)

@app.post("/chat_llm/", summary="Chat with a language model")
async def chat(text: str = Body(..., embed=True)):
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "gemma3:4b",
        "messages": [
            {"role": "user", "content": f"{prompt}\n{text}"},
        ],
        "stream": False,
        "max_length": 2048
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        transpiler = PythonToWTranspiler()
        
        if "message" in result and "content" in result["message"]:
            match = re.search(r'```(?:python)?\s*(.*?)```', result["message"]["content"], re.DOTALL)
            if match:
                code_inside = match.group(1).strip()
                w_code = transpiler.transpile(code_inside)
                print(w_code)  
            return {"response": w_code}
        else:
            raise HTTPException(status_code=500, detail="Invalid response format from LLM")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error connecting to LLM: {str(e)}")
   
    return result["message"]["content"]
