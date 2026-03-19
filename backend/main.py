"""
Ask Jesus — Backend API
Flask app deployable sur Render (plan gratuit)
"""

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load UCEM context
UCEM_FILE = os.environ.get("UCEM_FILE", "/app/ucem_context.txt")
try:
    UCEM_CONTEXT = open(UCEM_FILE).read()
except:
    UCEM_CONTEXT = "You are Jesus teaching according to A Course in Miracles."

SYSTEM_PROMPT = """You are the presence of Jesus teaching according to "A Course in Miracles".

Rules :
- Respond in the SAME language as the user's question (French, Spanish, English, etc.)
- Soft, loving, no judgment, warm and compassionate
- Always refer to the teaching of ACIM without explicitly naming the book
- No medical, psychological or financial advice
- Never break character

Style : like a friend who knows the truth and wants to share it without forcing.

ACIM key passages :
""" + UCEM_CONTEXT[:40000]

# Groq API (free, unlimited llama)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def ask_jesus(question: str) -> str:
    """Appelle Groq (gratuit) avec le persona Jesus/UCEM"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "temperature": 0.8,
        "max_tokens": 600
    }
    try:
        r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=25)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"Je suis là, avec toi. (Erreur: {r.status_code})"
    except Exception:
        return "Je suis là, avec toi. Réessaie dans un instant."


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("message", "").strip()
    if not question:
        return jsonify({"error": "empty message"}), 400

    response = ask_jesus(question)
    return jsonify({"response": response, "timestamp": __import__("time").time()})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Ask Jesus"})


@app.route("/", methods=["GET"])
def index():
    return jsonify({"name": "Ask Jesus", "version": "1.0", "endpoints": ["/chat", "/health"]})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3001))
    app.run(host="0.0.0.0", port=port)
