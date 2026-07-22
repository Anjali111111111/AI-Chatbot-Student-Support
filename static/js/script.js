// script.js
// Handles the chatbot's AJAX interaction with the Flask backend.

document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chatForm");
    if (!chatForm) return; // Only run this logic on the chatbot page

    const chatWindow = document.getElementById("chatWindow");
    const userMessageInput = document.getElementById("userMessage");

    // Human-readable labels for the AI pipeline stage that produced a reply
    const SOURCE_LABELS = {
        llm_with_retrieval: "LLM + FAQ Retrieval",
        llm: "Gemini LLM",
        faq_retrieval: "FAQ Retrieval (TF-IDF)",
        faq_retrieval_fallback: "FAQ Retrieval (Fallback)",
        rule_based_fallback: "Rule-based Fallback",
    };

    // Appends a chat bubble to the chat window. `meta` (optional) carries
    // AI pipeline info { source, intent, similarity } shown as a small tag.
    function appendMessage(text, sender, meta) {
        const messageDiv = document.createElement("div");
        messageDiv.className = "chat-message " + (sender === "user" ? "user-message" : "bot-message");

        const icon = document.createElement("i");
        icon.className = sender === "user" ? "bi bi-person-fill" : "bi bi-robot";

        const contentWrap = document.createElement("div");

        const span = document.createElement("span");
        span.textContent = text;
        contentWrap.appendChild(span);

        if (meta && meta.source && SOURCE_LABELS[meta.source]) {
            const tag = document.createElement("div");
            tag.className = "ai-source-tag";
            tag.innerHTML = '<i class="bi bi-cpu"></i> ' + SOURCE_LABELS[meta.source];
            contentWrap.appendChild(tag);
        }

        messageDiv.appendChild(icon);
        messageDiv.appendChild(contentWrap);
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
            appendMessage(data.reply || "Sorry, something went wrong. Please try again.", "bot", data);
        } catch (error) {
            removeTypingIndicator();
            appendMessage("Network error: could not reach the server. Please try again.", "bot");
            console.error("Chatbot request failed:", error);
        }
    });
});
