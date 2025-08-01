from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Load your OpenRouter API key (put it in a .env or directly paste here)
API_KEY = os.getenv("OPENROUTER_API_KEY") or "YOUR_API_KEY_HERE"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    payload = {
        "model": "openai/gpt-3.5-turbo",  # or any model listed on openrouter.ai
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        return jsonify({"reply": f"(Error {response.status_code}) {response.text}"})

    reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
