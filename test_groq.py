import os, requests

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_API_KEY}"}
payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": "Tu es Jesus."}, {"role": "user", "content": "Bonjour"}], "temperature": 0.8, "max_tokens": 30}

try:
    r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=10)
    print("Status:", r.status_code)
    print("Response:", r.json()["choices"][0]["message"]["content"])
except Exception as e:
    print("Error:", type(e).__name__, str(e))
