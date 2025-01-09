from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import time
import logging
from datetime import datetime




app = Flask(__name__)

# Configurez votre clé OpenAI à partir de la variable d'environnement

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(
  api_key=API_KEY
)

# === Hardcode our ids ===
asistant_id = "asst_AB8UZivPRzzlqbD51AH5cApv"
thread_id = "thread_7AmKxWVK6uXbnIT6zQoYtcoR"


def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
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
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                the_return +=f"Assistant Response: {response}"
                return the_return
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

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
        message = client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=user_input
        )
        
        # === Run our Assistant ===
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=asistant_id,
        )
        
        # === Run ===
        the_return = wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

        # ==== Steps --- Logs ==
        run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
        
        return jsonify({"reply": the_return})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Obtenir le port dynamique pour Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
