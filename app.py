from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Configurez votre clé OpenAI à partir de la variable d'environnement

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(
  api_key=API_KEY
)

# Identifiant de l'assistant personnalisé
ASSISTANT_ID = "asst_AB8UZivPRzzlqbD51AH5cApv"

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
          model="gpt-4o",
          store=True,
          messages=[
            {"role": "system", "content": f"This conversation is with the assistant ID: {ASSISTANT_ID}"},
            {"role": "user", "content": user_input}
          ],
          assistant_id="asst_AB8UZivPRzzlqbD51AH5cApv"
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
