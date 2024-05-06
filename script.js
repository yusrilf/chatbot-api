function toggleChat() {
    var chatContainer = document.getElementById("chat-container");
    chatContainer.style.display = (chatContainer.style.display === "none" || chatContainer.style.display === "") ? "block" : "none";
}

function sendMessage() {
    var userMessage = document.getElementById("user-message").value;
    displayMessage("user", userMessage);

    // Call API and display bot's response
    callApiStreaming(userMessage);

    document.getElementById("user-message").value = "";
}

async function callApiStreaming(message) {
    try {
        var response = await fetch('http://localhost:8000/stream_chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: message })
        });

        var reader = response.body.getReader();
        var decoder = new TextDecoder('utf-8');
        var partialMessage = '';  // Menyimpan pesan sebagian sebelum ditampilkan

        while (true) {
            const { done, value } = await reader.read();

            if (done) {
                // Jika pembacaan selesai, tampilkan sisa pesan yang belum ditampilkan
                if (partialMessage.trim() !== '') {
                    displayMessage("bot", partialMessage);
                }
                break; // Keluar dari loop
            }

            let token = decoder.decode(value);

            // Periksa apakah token merupakan bagian dari satu pesan yang lebih besar
            if (token.endsWith('.') || token.endsWith('!') || token.endsWith('?')) {
                // Jika token berakhir dengan tanda baca, anggap sebagai akhir pesan
                partialMessage += token;
                displayMessage("bot", partialMessage);
                partialMessage = '';  // Reset untuk pesan berikutnya
            } else {
                // Jika tidak, tambahkan token ke pesan sebagian
                partialMessage += token;
            }
        }
    } catch (error) {
        console.error('Error calling API:', error);
    }
}



// Existing displayMessage function remains the same
function displayMessage(sender, message) {
    var chatMessages = document.getElementById("chat-messages");
    var messageContainer = document.createElement("div");
    messageContainer.className = 'message-container';

    // Create image element for user or bot
    var image = document.createElement("img");
    image.src = sender === 'user' ? 'user-image.png' : 'bot-image.png';
    image.alt = sender === 'user' ? 'User Image' : 'Bot Image';
    image.className = 'message-image';

    // Create message element
    var messageDiv = document.createElement("div");
    messageDiv.className = sender;
    messageDiv.innerHTML = message;

    // Append image and message to message container
    messageContainer.appendChild(image);
    messageContainer.appendChild(messageDiv);

    // Append message container to chat messages
    chatMessages.appendChild(messageContainer);

    // Scroll to the bottom of the chat messages
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
