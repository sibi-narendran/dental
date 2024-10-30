from typing import Dict, List, Tuple
import re
from datetime import datetime, timedelta

# Dental procedures knowledge base
DENTAL_PROCEDURES = {
    'cleaning': {
        'name': 'Dental Cleaning',
        'duration': '30-60 minutes',
        'frequency': 'Every 6 months',
        'description': 'Professional cleaning to remove plaque and tartar, followed by polishing.',
        'preparation': 'No special preparation needed.',
        'cost_range': '$75-$200'
    },
    'filling': {
        'name': 'Dental Filling',
        'duration': '30-60 minutes',
        'frequency': 'As needed',
        'description': 'Restoration of decayed tooth using composite or amalgam material.',
        'preparation': 'Local anesthetic will be used.',
        'cost_range': '$150-$300 per filling'
    },
    'root canal': {
        'name': 'Root Canal',
        'duration': '90 minutes',
        'frequency': 'As needed',
        'description': 'Treatment of infected tooth pulp to save the natural tooth.',
        'preparation': 'X-rays needed beforehand.',
        'cost_range': '$700-$1,500'
    },
    'crown': {
        'name': 'Dental Crown',
        'duration': 'Two 60-minute visits',
        'frequency': 'As needed',
        'description': 'Cap placed over damaged tooth to restore shape and function.',
        'preparation': 'Temporary crown placed first.',
        'cost_range': '$800-$1,700'
    }
}

# Common dental symptoms and advice
DENTAL_SYMPTOMS = {
    'pain': 'Tooth pain could indicate decay, infection, or sensitivity. Schedule a check-up soon.',
    'bleeding': 'Bleeding gums may indicate gingivitis. Maintain good oral hygiene and schedule a cleaning.',
    'sensitivity': 'Tooth sensitivity could be from worn enamel or receding gums. Try sensitive toothpaste.',
    'swelling': 'Facial swelling could indicate infection. This requires immediate attention.',
    'bad breath': 'Bad breath might indicate gum disease or poor oral hygiene. Schedule a cleaning.',
}

def get_procedure_info(procedure: str) -> Dict:
    """Find the closest matching procedure from our knowledge base."""
    procedure = procedure.lower()
    for key in DENTAL_PROCEDURES:
        if key in procedure:
            return DENTAL_PROCEDURES[key]
    return None

def format_procedure_info(procedure_info: Dict) -> str:
    """Format procedure information into a readable response."""
    return f"""Here's what you need to know about {procedure_info['name']}:
• Duration: {procedure_info['duration']}
• Typical frequency: {procedure_info['frequency']}
• Description: {procedure_info['description']}
• Preparation: {procedure_info['preparation']}
• Estimated cost range: {procedure_info['cost_range']}

Would you like to schedule an appointment for this procedure?"""

def check_for_emergency(message: str) -> Tuple[bool, str]:
    """Check if the message indicates a dental emergency."""
    emergency_keywords = ['severe pain', 'extreme pain', 'swelling', 'bleeding', 'knocked out', 'broken tooth']
    is_emergency = any(keyword in message.lower() for keyword in emergency_keywords)
    
    if is_emergency:
        return True, """This sounds like a dental emergency. Please call our emergency line immediately at (555) 123-4567.
For severe pain or swelling, you can:
1. Apply a cold compress to reduce swelling
2. Rinse with warm salt water
3. Take over-the-counter pain medication
4. Keep the affected area clean

Would you like me to help you schedule an emergency appointment?"""
    return False, ""

def get_ai_response(message: str) -> str:
    """
    Enhanced AI response function that provides more engaging and context-aware responses
    """
    message = message.lower()
    
    # Check for emergencies first
    is_emergency, emergency_response = check_for_emergency(message)
    if is_emergency:
        return emergency_response
    
    # Appointment scheduling
    if 'appointment' in message:
        if 'schedule' in message or 'book' in message:
            return """I can help you schedule an appointment. To find the best time:
1. What type of appointment do you need? (Regular check-up, cleaning, or specific procedure)
2. Do you have a preferred day of the week?
3. Morning or afternoon preference?

Please provide these details, and I'll check our availability."""
        elif 'cancel' in message or 'reschedule' in message:
            return "I can help you modify your appointment. Please provide your name and the appointment date, and I'll assist with rescheduling."
    
    # Procedure information
    for procedure in DENTAL_PROCEDURES.keys():
        if procedure in message:
            procedure_info = get_procedure_info(procedure)
            if procedure_info:
                return format_procedure_info(procedure_info)
    
    # Symptom checking
    for symptom, advice in DENTAL_SYMPTOMS.items():
        if symptom in message:
            return f"{advice}\n\nWould you like to schedule an appointment to have this checked?"
    
    # Cost and insurance
    if any(word in message for word in ['cost', 'price', 'insurance', 'payment']):
        return """We offer various payment options and work with most insurance providers. The cost varies depending on the procedure and your insurance coverage. 

Some typical costs:
• Regular check-up and cleaning: $75-$200
• Fillings: $150-$300
• Root canals: $700-$1,500

Would you like specific pricing for a particular procedure?"""
    
    # Office information
    if any(word in message for word in ['hours', 'location', 'address', 'open']):
        return """Our office is open:
Monday-Friday: 9:00 AM - 6:00 PM
Saturday: 9:00 AM - 2:00 PM (by appointment)
Closed on Sundays

Address: 123 Dental Street, San Francisco, CA 94101

Would you like to schedule an appointment?"""
    
    # Default response with engagement
    return """I can help you with:
• Scheduling or modifying appointments
• Information about dental procedures
• Cost estimates and insurance
• Emergency dental care
• General dental advice

What would you like to know more about?"""
