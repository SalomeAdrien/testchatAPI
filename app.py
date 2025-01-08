from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Configurez votre clé OpenAI à partir de la variable d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Ou "gpt-4" si vous y avez accès
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ]
        )

        # Extraire et retourner la réponse
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Obtenir le port dynamique pour Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
