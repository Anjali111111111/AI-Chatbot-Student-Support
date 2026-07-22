// script.js
// Handles the chatbot's AJAX interaction with the Flask backend.

document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chatForm");
    if (!chatForm) return; // Only run this logic on the chatbot page

    const chatWindow = document.getElementById("chatWindow");
    const userMessageInput = document.getElementById("userMessage");

    // Appends a chat bubble to the chat window
    function appendMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.className = "chat-message " + (sender === "user" ? "user-message" : "bot-message");

        const icon = document.createElement("i");
        icon.className = sender === "user" ? "bi bi-person-fill" : "bi bi-robot";

        const span = document.createElement("span");
        span.textContent = text;

        messageDiv.appendChild(icon);
        messageDiv.appendChild(span);
        chatWindow.appendChild(messageDiv);

        // Auto-scroll to the latest message
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return messageDiv;
    }

    // Shows a temporary "typing..." indicator while waiting for the AI reply
    function showTypingIndicator() {
        const typingDiv = document.createElement("div");
        typingDiv.className = "chat-message bot-message typing-indicator";
        typingDiv.id = "typingIndicator";
        typingDiv.innerHTML = '<i class="bi bi-robot"></i><span>Campus Assist is typing...</span>';
        chatWindow.appendChild(typingDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingDiv = document.getElementById("typingIndicator");
        if (typingDiv) typingDiv.remove();
    }

    chatForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const message = userMessageInput.value.trim();
        if (!message) return;

        // Show the user's message immediately
        appendMessage(message, "user");
        userMessageInput.value = "";
        userMessageInput.focus();

        showTypingIndicator();

        try {
            const response = await fetch("/chatbot/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();
            removeTypingIndicator();
            appendMessage(data.reply || "Sorry, something went wrong. Please try again.", "bot");
        } catch (error) {
            removeTypingIndicator();
            appendMessage("Network error: could not reach the server. Please try again.", "bot");
            console.error("Chatbot request failed:", error);
        }
    });
});
