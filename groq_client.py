import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def groq_generate(prompt: str, model: str = "llama-3.3-70b-versatile"):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in .env")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role":"user","content":prompt}],
        "temperature": 0.3,
        "max_tokens": 512
    }

    r = requests.post(url, json=payload, headers=headers, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]
