var socket = io.connect("http://127.0.0.1:5000");

function sendMessage() {
    let message = document.getElementById("message").value;
    if (message.trim() !== "") {
        socket.emit("send_message", { message: message });
        document.getElementById("message").value = "";
    }
}

function displayMessage(response) {
    let chatBox = document.getElementById("chat-box");

    if (response.type === "text") {
        chatBox.innerHTML += `<p class="bot-message">${response.message}</p>`;
    } 
    else if (response.type === "image") {
        let imgElement = document.createElement("img");
        imgElement.src = "data:image/png;base64," + response.image_data;
        imgElement.classList.add("generated-image");
        chatBox.appendChild(imgElement);
    }

    chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to the latest message
}


socket.on("receive_message", function(data) {
    let chatBox = document.getElementById("chat-box");
    let messageDiv = document.createElement("div");

    if (data.type === "text") {
        messageDiv.className = "message " + (data.sender === "You" ? "user-message" : "bot-message");
        messageDiv.textContent = data.message;
    } else if (data.type === "image") {
        messageDiv.className = "message bot-message";
        messageDiv.innerHTML = `<img src="${data.message}" alt="Generated Image">`;
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
});
