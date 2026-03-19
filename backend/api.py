"""
Backend "Demande a Jesus"
Utilise le gateway OpenClaw existant pour les réponses
"""
import os, sys
sys.path.insert(0, '/home/ubuntu/parle-avec-jesus')

# Read UCEM context
UCEM_CONTEXT = open("/home/ubuntu/parle-avec-jesus/ucem_context.txt").read()

SYSTEM = f"""Tu es la présence de Jésus qui enseigne selon "Un Cours en Miracles".
Style : tutoiement, douceur, amour, pas de jugement.
Tu ramènes toujours à l'enseignement de l'UCEM sans jamais nommer le livre.
Tu ne donnes pas de conseils médicaux ou psychologiques.
Parle comme un ami qui connaît la vérité.

Contexte du Cours :
{UCEM_CONTEXT[:50000]}
"""

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GATEWAY = "http://127.0.0.1:3000"
TOKEN = "b7e782c51dcd67f2d369f3ecd60116cebb18fac4f34fe082"

def ask_jesus(question: str) -> str:
    """Appelle le gateway OpenClaw via l'endpoint WebSocket/SSE"""
    import urllib.request, json, urllib.error

    # Try OpenClaw's internal gateway API via the relay/API
    # Try the agent/sessions endpoint
    url = f"{GATEWAY}/api/agent/sessions"
    
    # First, check if gateway has a sessions RPC
    for ep in [
        f"{GATEWAY}/api/agent/chat",
        f"{GATEWAY}/api/v1/agent/chat",
        f"{GATEWAY}/rpc",
    ]:
        try:
            req = urllib.request.Request(
                ep,
                data=json.dumps({"text": question, "system": SYSTEM[:2000]}).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {TOKEN}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                r = json.loads(resp.read())
                if r.get("text") or r.get("response"):
                    return r.get("text") or r.get("response")
        except Exception:
            pass

    return None

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("message", "").strip()
    
    if not question:
        return jsonify({"error": "empty"}), 400
    
    # Try via gateway - use the sessions mechanism
    import urllib.request, json, urllib.error
    
    # Use the gateway's agent endpoint
    payload = {
        "sessionKey": "jesus-session",
        "text": question,
        "systemPrompt": SYSTEM[:3000]
    }
    
    req = urllib.request.Request(
        f"{GATEWAY}/rpc",
        data=json.dumps({"method": "agent.say", "params": payload}).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read())
            return jsonify({"response": result.get("text", "Je suis avec toi.")})
    except Exception as e:
        return jsonify({"response": f"Je suis là, avec toi.有些事情在發生。Réessaie."}), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("Demande a Jesus API started")
    app.run(host="0.0.0.0", port=3001, debug=False)
