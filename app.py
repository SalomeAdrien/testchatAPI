from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Configurez votre clé OpenAI à partir de la variable d'environnement

API_KEY = "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" # os.getenv("OPENAI_API_KEY")
client = OpenAI(
  api_key=API_KEY
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Obtenir le message de l'utilisateur depuis le formulaire
        user_input = request.json.get("message", "")
        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        # Appeler l'API OpenAI
        completion = client.chat.completions.create(
          model="gpt-4o-mini",
          store=True,
          messages=[
            {"role": "user", "content": user_input}
          ]
        )
        # Extraire et retourner la réponse
        reply = completion.choices[0].message.content
        return jsonify({"reply": reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Obtenir le port dynamique pour Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
