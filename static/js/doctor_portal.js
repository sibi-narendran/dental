document.addEventListener('DOMContentLoaded', function() {
    // Chat overlay elements
    const chatElements = {
        button: document.getElementById('chatButton'),
        overlay: document.getElementById('chatOverlay'),
        minimize: document.getElementById('minimizeChat'),
        messages: document.getElementById('chatMessages'),
        form: document.getElementById('chatForm'),
        input: document.getElementById('chatInput')
    };

    // Check if all required chat elements are present
    const hasChatElements = Object.entries(chatElements).every(([key, element]) => {
        if (!element) {
            console.error(`Chat element not found: ${key}`);
            return false;
        }
        return true;
    });

    // Chat history storage
    let chatHistory = [];

    if (hasChatElements) {
        // Initialize chat functionality
        function toggleChatOverlay() {
            chatElements.overlay.classList.toggle('active');
            if (chatElements.overlay.classList.contains('active')) {
                chatElements.input.focus();
            }
        }

        // Add event listeners
        chatElements.button.addEventListener('click', toggleChatOverlay);
        chatElements.minimize.addEventListener('click', toggleChatOverlay);

        // Add message to chat
        function addMessage(message, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'ai'} mb-2`;
            messageDiv.textContent = message;
            chatElements.messages.appendChild(messageDiv);
            chatElements.messages.scrollTop = chatElements.messages.scrollHeight;
            
            // Store message in history
            chatHistory.push({ message, isUser });
        }

        // Restore chat history
        function restoreChatHistory() {
            chatElements.messages.innerHTML = '';
            chatHistory.forEach(msg => addMessage(msg.message, msg.isUser));
        }

        // Handle chat form submission
        chatElements.form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const message = chatElements.input.value.trim();
            if (!message) return;

            addMessage(message, true);
            chatElements.input.value = '';
            chatElements.input.disabled = true;

            try {
                const response = await fetch('/api/chat/doctor', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                addMessage(data.response);
            } catch (error) {
                console.error('Error in chat:', error);
                addMessage('Sorry, I encountered an error. Please try again.', false);
            } finally {
                chatElements.input.disabled = false;
                chatElements.input.focus();
            }
        });
    }

    // Handle appointment approval (separate functionality)
    const approveButtons = document.querySelectorAll('.approve-btn');
    if (approveButtons.length > 0) {
        approveButtons.forEach(button => {
            button.addEventListener('click', async function() {
                const appointmentId = this.dataset.id;
                try {
                    const response = await fetch(`/api/appointments/${appointmentId}/approve`, {
                        method: 'POST'
                    });
                    if (response.ok) {
                        this.parentElement.innerHTML = 'Approved';
                        this.remove();
                    } else {
                        throw new Error('Failed to approve appointment');
                    }
                } catch (error) {
                    console.error('Error approving appointment:', error);
                    alert('Failed to approve appointment. Please try again.');
                }
            });
        });
    }
});
