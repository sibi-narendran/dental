document.addEventListener('DOMContentLoaded', function() {
    // Handle appointment approval
    document.querySelectorAll('.approve-btn').forEach(button => {
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

    // Handle AI queries for doctors
    const aiQueryForm = document.getElementById('aiQueryForm');
    const aiResponse = document.getElementById('aiResponse');
    const queryInput = document.getElementById('query');

    aiQueryForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const query = queryInput.value.trim();
        if (!query) return;

        aiResponse.innerHTML = '<div class="alert alert-info">Processing your request...</div>';
        
        try {
            const response = await fetch('/api/chat/doctor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: query })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            aiResponse.innerHTML = `<div class="alert alert-info">${data.response}</div>`;
            queryInput.value = '';
        } catch (error) {
            console.error('Error querying AI:', error);
            aiResponse.innerHTML = '<div class="alert alert-danger">Failed to process your request. Please try again.</div>';
        }
    });
});
