document.getElementById("chat-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    // Afficher le message utilisateur
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    // Envoyer la requête à l'API Flask
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
    });

    const data = await response.json();
    if (data.reply) {
        chatBox.innerHTML += `<p><strong>Assitant virtuel:</strong> ${data.reply}</p>`;
    } else {
        chatBox.innerHTML += `<p><strong>Error:</strong> ${data.error}</p>`;
    }

    // Effacer le champ utilisateur
    document.getElementById("user-input").value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
});
