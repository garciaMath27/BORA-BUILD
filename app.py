from flask import Flask, request, jsonify, render_template
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Garante que a chave da API foi configurada
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("A variável de ambiente OPENAI_API_KEY não está definida.")

openai.api_key = api_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
