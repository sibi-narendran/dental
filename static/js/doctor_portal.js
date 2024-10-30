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
                }
            } catch (error) {
                console.error('Error approving appointment:', error);
            }
        });
    });

    // Handle AI queries for doctors
    const aiQueryForm = document.getElementById('aiQueryForm');
    const aiResponse = document.getElementById('aiResponse');

    aiQueryForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const query = document.getElementById('query').value;
        
        try {
            const response = await fetch('/api/chat/doctor', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: query })
            });
            
            const data = await response.json();
            aiResponse.innerHTML = `<div class="alert alert-info">${data.response}</div>`;
        } catch (error) {
            console.error('Error querying AI:', error);
            aiResponse.innerHTML = '<div class="alert alert-danger">Error processing your request</div>';
        }
    });
});
