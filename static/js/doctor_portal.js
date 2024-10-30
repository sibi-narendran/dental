document.addEventListener('DOMContentLoaded', function() {
    // Chat overlay elements
    const chatButton = document.querySelector('#chatButton');
    const chatOverlay = document.querySelector('#chatOverlay');
    const minimizeChat = document.querySelector('#minimizeChat');
    const chatMessages = document.querySelector('#chatMessages');
    const chatForm = document.querySelector('#chatForm');
    const chatInput = document.querySelector('#chatInput');

    // Initialize chat functionality if elements exist
    if (chatButton && chatOverlay && minimizeChat && chatMessages && chatForm && chatInput) {
        // Toggle chat overlay
        function toggleChatOverlay() {
            chatOverlay.classList.toggle('active');
            if (chatOverlay.classList.contains('active')) {
                chatInput.focus();
            }
        }

        // Add event listeners
        chatButton.addEventListener('click', toggleChatOverlay);
        minimizeChat.addEventListener('click', toggleChatOverlay);

        // Add message to chat
        function addMessage(message, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'ai'} mb-2`;
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Handle chat form submission
        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            chatInput.value = '';
            chatInput.disabled = true;

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
                chatInput.disabled = false;
                chatInput.focus();
            }
        });
    } else {
        console.warn('Some chat elements not found, chat functionality disabled');
    }

    // Handle appointment approval (separate functionality)
    const approveButtons = document.querySelectorAll('.approve-btn');
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
});
