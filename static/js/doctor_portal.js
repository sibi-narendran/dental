document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Chat elements
    const chatButton = document.querySelector('#chatButton');
    const chatOverlay = document.querySelector('#chatOverlay');
    const minimizeChat = document.querySelector('#minimizeChat');
    const chatMessages = document.querySelector('#chatMessages');
    const chatForm = document.querySelector('#chatForm');
    const chatInput = document.querySelector('#chatInput');
    const sendButton = document.querySelector('#sendButton');
    const typingIndicator = document.querySelector('.typing-indicator');

    // Search and filter elements
    const searchInput = document.querySelector('#searchInput');
    const statusFilter = document.querySelector('#statusFilter');
    const sortOrder = document.querySelector('#sortOrder');
    const appointmentsTableBody = document.querySelector('#appointmentsTableBody');
    const noResults = document.querySelector('#noResults');

    // Current time display
    const currentTimeElement = document.querySelector('#currentTime');
    function updateCurrentTime() {
        const now = new Date();
        currentTimeElement.textContent = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    updateCurrentTime();
    setInterval(updateCurrentTime, 60000);

    // Initialize chat functionality
    if (chatButton && chatOverlay && minimizeChat && chatMessages && chatForm && chatInput) {
        function toggleChatOverlay() {
            chatOverlay.classList.toggle('active');
            if (chatOverlay.classList.contains('active')) {
                chatInput.focus();
                scrollToBottom();
            }
        }

        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function addMessage(message, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'ai'} mb-3`;
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            scrollToBottom();
        }

        function showTypingIndicator() {
            typingIndicator.classList.remove('d-none');
            scrollToBottom();
        }

        function hideTypingIndicator() {
            typingIndicator.classList.add('d-none');
        }

        chatButton.addEventListener('click', toggleChatOverlay);
        minimizeChat.addEventListener('click', toggleChatOverlay);

        chatInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });

        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            chatInput.value = '';
            chatInput.disabled = true;
            sendButton.disabled = true;
            showTypingIndicator();

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
                hideTypingIndicator();
                addMessage(data.response);
            } catch (error) {
                console.error('Error in chat:', error);
                hideTypingIndicator();
                addMessage('Sorry, I encountered an error. Please try again.', false);
            } finally {
                chatInput.disabled = false;
                sendButton.disabled = false;
                chatInput.focus();
            }
        });
    }

    // Search and filter functionality
    function filterAndSortAppointments() {
        const searchTerm = searchInput.value.toLowerCase();
        const statusValue = statusFilter.value;
        const sortValue = sortOrder.value;
        
        const rows = Array.from(appointmentsTableBody.getElementsByTagName('tr'));
        let visibleRows = 0;

        rows.forEach(row => {
            const patientName = row.getAttribute('data-patient');
            const status = row.getAttribute('data-status');
            const time = row.getAttribute('data-time');
            
            const matchesSearch = patientName.includes(searchTerm);
            const matchesStatus = !statusValue || status === statusValue;
            
            if (matchesSearch && matchesStatus) {
                row.style.display = '';
                visibleRows++;
            } else {
                row.style.display = 'none';
            }
        });

        // Sort visible rows
        const sortedRows = rows
            .filter(row => row.style.display !== 'none')
            .sort((a, b) => {
                switch(sortValue) {
                    case 'time-asc':
                        return a.getAttribute('data-time').localeCompare(b.getAttribute('data-time'));
                    case 'time-desc':
                        return b.getAttribute('data-time').localeCompare(a.getAttribute('data-time'));
                    case 'name-asc':
                        return a.getAttribute('data-patient').localeCompare(b.getAttribute('data-patient'));
                    case 'name-desc':
                        return b.getAttribute('data-patient').localeCompare(a.getAttribute('data-patient'));
                    default:
                        return 0;
                }
            });

        // Reorder the table
        sortedRows.forEach(row => appointmentsTableBody.appendChild(row));

        // Toggle no results message
        noResults.classList.toggle('d-none', visibleRows > 0);
    }

    // Add event listeners for search and filters
    searchInput.addEventListener('input', filterAndSortAppointments);
    statusFilter.addEventListener('change', filterAndSortAppointments);
    sortOrder.addEventListener('change', filterAndSortAppointments);

    // Handle appointment approval
    const approveButtons = document.querySelectorAll('.approve-btn');
    approveButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const appointmentId = this.dataset.id;
            const parentTd = this.parentElement;
            const statusTd = parentTd.previousElementSibling;

            // Update UI
            statusTd.innerHTML = `
                <span class="badge rounded-pill bg-success px-3 py-2">
                    <i class="bi bi-check-circle-fill me-1"></i>
                    Approved
                </span>
            `;
            parentTd.innerHTML = `
                <button class="btn btn-outline-secondary btn-sm rounded-pill px-3" disabled>
                    <i class="bi bi-check2-all me-1"></i>Approved
                </button>
            `;

            // Update row data attribute
            const row = parentTd.closest('tr');
            row.setAttribute('data-status', 'approved');

            // Refresh filters
            filterAndSortAppointments();
        });
    });
});
