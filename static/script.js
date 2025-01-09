document.getElementById("chat-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    // Désactiver le champ d'entrée et le bouton
    const inputField = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    inputField.disabled = true;
    sendButton.disabled = true;

    // Afficher le message utilisateur
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    try {
        // Envoyer la requête à l'API Flask
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userInput }),
        });

        const data = await response.json();

        // Afficher la réponse ou un message d'erreur
        if (response.ok && data.reply) {
            chatBox.innerHTML += `<p><strong>Assistant virtuel 21-22:</strong> ${data.reply}</p>`;
        } else if (response.status === 429) {
            chatBox.innerHTML += `<p><strong>Warning:</strong> A run is already active. Please wait and try again.</p>`;
        } else {
            chatBox.innerHTML += `<p><strong>Error:</strong> ${data.error}</p>`;
        }
    } catch (error) {
        // Gérer les erreurs réseau ou autres
        chatBox.innerHTML += `<p><strong>Error:</strong> Unable to connect to the server. Please try again later.</p>`;
        console.error("Error:", error);
    } finally {
        // Réactiver le champ d'entrée et le bouton
        inputField.disabled = false;
        sendButton.disabled = false;

        // Effacer le champ utilisateur et faire défiler vers le bas
        inputField.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
