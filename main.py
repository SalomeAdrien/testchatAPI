# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 22:52:27 2025

@author: PC
"""

from openai import OpenAI
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

# Remplacez par votre propre clé API OpenAI
API_KEY = "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"

client = OpenAI(
  api_key=API_KEY
)
def envoyer_requete():
    """Envoie une requête à l'API OpenAI et affiche la réponse."""
    question = entree.get("1.0", tk.END).strip()
    if not question:
        afficher_message("Vous", "Veuillez entrer une question.")
        return

    afficher_message("Vous", question)
    entree.delete("1.0", tk.END)

    try:
        reponse_var.set("En cours de traitement...")
        completion = client.chat.completions.create(
          model="gpt-4o-mini",
          store=True,
          messages=[
            {"role": "user", "content": question}
          ]
        )
        reponse = completion.choices[0].message.content
        afficher_message("ChatGPT", reponse)
        reponse_var.set("")
    except Exception as e:
        afficher_message("ChatGPT", f"Erreur : {str(e)}")

def afficher_message(auteur, message):
    """Affiche un message dans la zone de chat."""
    zone_texte.configure(state="normal")
    zone_texte.insert(tk.END, f"{auteur} : {message}\n", auteur)
    zone_texte.configure(state="disabled")
    zone_texte.yview(tk.END)

# Création de la fenêtre principalehell
fenetre = tk.Tk()
fenetre.title("ChatGPT Interface Moderne")
fenetre.geometry("600x500")
fenetre.configure(bg="#f5f5f5")

# Styles pour la zone de chat
style = ttk.Style()
style.configure("User.TLabel", foreground="blue", background="#f5f5f5")
style.configure("ChatGPT.TLabel", foreground="green", background="#f5f5f5")

# Zone pour afficher la conversation
zone_texte = scrolledtext.ScrolledText(fenetre, wrap=tk.WORD, state="disabled", height=20, width=70, bg="#ffffff", fg="#000000", font=("Arial", 10))
zone_texte.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Champ d'entrée pour la question
entree = tk.Text(fenetre, height=3, width=50, bg="#e8e8e8", fg="#000000", font=("Arial", 10))
entree.grid(row=1, column=0, padx=10, pady=10)

# Bouton pour envoyer la requête
bouton_envoyer = tk.Button(fenetre, text="Envoyer", command=envoyer_requete, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
bouton_envoyer.grid(row=1, column=1, padx=10, pady=10)

# Variable pour afficher les messages de traitement ou erreurs
reponse_var = tk.StringVar()
label_reponse = tk.Label(fenetre, textvariable=reponse_var, bg="#f5f5f5", fg="red", font=("Arial", 10))
label_reponse.grid(row=2, column=0, columnspan=2, pady=10)

# Lancement de la boucle principale
fenetre.mainloop()
