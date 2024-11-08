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

        // Handle Enter key press
        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });

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

    // Handle appointment approval (UI simulation only)
    const approveButtons = document.querySelectorAll('.approve-btn');
    approveButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const appointmentId = this.dataset.id;
            const parentTd = this.parentElement;
            const statusTd = parentTd.previousElementSibling;

            // Update UI only - no backend call needed
            statusTd.innerHTML = `
                <span class="badge rounded-pill bg-success px-3 py-2">
                    <i class="bi bi-check-circle-fill me-1"></i>
                    Approved
                </span>
            `;
            parentTd.innerHTML = `
                <button class="btn btn-outline-secondary btn-sm rounded-pill px-3" disabled>
                    <i class="bi bi-check2-all me-1"></i> Approved
                </button>
            `;
        });
    });
});
