// app.js
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatOutput = document.getElementById("chat-output");

// Listen for form submit
chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    // Get the user's message
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;

    // Add the user's message to the output
    addMessageToOutput("user", userMessage);
    chatInput.value = "";

    // Send only the user's message
    const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_message: userMessage }),
    });

    // Get the assistant's response
    const data = await response.json();
    addMessageToOutput("assistant", data);
});

// Add a message to the chat output
function addMessageToOutput(role, message) {
    const messageElement = document.createElement("div");
    messageElement.className = role;
    messageElement.textContent = message;
    chatOutput.appendChild(messageElement);
    chatOutput.scrollTop = chatOutput.scrollHeight;
}
