document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const templateButtons = document.querySelectorAll('.template-btn');

    // Initialize chat functionality if elements exist
    if (chatMessages && chatForm && messageInput) {
        function addMessage(message, isUser = false, isError = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : isError ? 'system' : 'ai'} mb-2`;
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Handle template button clicks
        templateButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const message = button.dataset.message;
                messageInput.value = message;
                messageInput.focus();
            });
        });

        // Handle Enter key press
        messageInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });

        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            messageInput.value = '';
            messageInput.disabled = true;

            try {
                const response = await fetch('/api/chat/patient', {
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
                console.error('Error sending message:', error);
                addMessage('Sorry, I encountered an error. Please try again.', false, true);
            } finally {
                messageInput.disabled = false;
                messageInput.focus();
            }
        });
    } else {
        console.warn('Some chat elements not found, chat functionality disabled');
    }
});
