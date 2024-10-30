def get_ai_response(message: str) -> str:
    """
    Simple AI response function that returns predefined responses based on keywords
    """
    message = message.lower()
    
    if 'appointment' in message and ('book' in message or 'schedule' in message):
        return "I can help you book an appointment. Please provide your preferred date and time, and I'll check availability."
    
    if 'opening hours' in message or 'business hours' in message:
        return "Our dental practice is open Monday to Friday, 9:00 AM to 6:00 PM."
    
    if 'emergency' in message:
        return "For dental emergencies, please call our emergency hotline at (555) 123-4567."
    
    if 'procedure' in message or 'treatment' in message:
        return "I can provide general information about our dental procedures. Please specify which treatment you're interested in."
    
    return "I'm here to help with appointments, general inquiries, and information about our dental services. How can I assist you today?"
