from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import time
import logging
from datetime import datetime

app = Flask(__name__)

# Configurez votre clé OpenAI à partir de la variable d'environnement
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# === Hardcode our ids ===
assistant_id = "asst_AB8UZivPRzzlqbD51AH5cApv"
thread_id = "thread_7AmKxWVK6uXbnIT6zQoYtcoR"

logging.basicConfig(level=logging.INFO)

def is_run_active(client, thread_id):
    """
    Vérifie si un run est actif dans le thread.
    """
    try:
        runs = client.beta.threads.runs.list(thread_id=thread_id)
        for run in runs.data:
            if not run.completed_at:  # Si un run n'est pas terminé
                return True
        return False
    except Exception as e:
        logging.error(f"Erreur lors de la vérification des runs : {e}")
        return False

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Attends qu'un run se termine et retourne le temps écoulé.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                the_return = f"Run completed in {formatted_elapsed_time}"
                # Récupération des messages une fois le run terminé
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = ''.join(
                    segment.text.value for segment in last_message.content
                )
                the_return += f" Assistant Response: {response}"
                return the_return
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du run : {e}")
            return f"Erreur: {str(e)}"
        logging.info("En attente de la fin du run...")
        time.sleep(sleep_interval)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        # Vérifiez si un run est actif
        if is_run_active(client, thread_id):
            return jsonify({"error": "A previous run is still active. Please wait."}), 429

        # Ajouter le message utilisateur au thread
        message = client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=user_input
        )

        # Démarrer une nouvelle exécution
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # Attendre la fin de l'exécution
        the_return = wait_for_run_completion(client, thread_id, run.id)
        return jsonify({"reply": the_return})

    except Exception as e:
        logging.error(f"Erreur lors du traitement du chat : {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Obtenir le port dynamique pour Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
