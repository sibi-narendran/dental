import random
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import json

# Mock patient data for demo purposes
DEMO_PATIENTS = {
    "John Smith": {
        "id": "P1001",
        "history": [
            {"date": "2024-09-15", "procedure": "Dental Cleaning", "notes": "Regular checkup, good oral hygiene"},
            {"date": "2024-03-20", "procedure": "Filling", "tooth": "#18", "notes": "Composite filling"}
        ]
    },
    "Sarah Johnson": {
        "id": "P1002",
        "history": [
            {"date": "2024-10-01", "procedure": "Root Canal", "tooth": "#30", "notes": "Post-procedure recovery excellent"},
            {"date": "2024-08-12", "procedure": "Crown", "tooth": "#19", "notes": "Permanent crown placed"}
        ]
    }
}

def generate_available_slots(days_ahead: int = 7) -> List[str]:
    slots = []
    current_date = datetime.now()
    for day in range(1, days_ahead + 1):
        date = current_date + timedelta(days=day)
        if date.weekday() < 5:  # Monday to Friday
            times = ["9:00 AM", "10:30 AM", "2:00 PM", "3:30 PM", "4:45 PM"]
        else:  # Saturday
            times = ["9:00 AM", "10:30 AM", "11:45 AM"]
        
        for time in random.sample(times, min(3, len(times))):  # Randomly select 3 slots
            slots.append(f"{date.strftime('%A, %B %d')}, {time}")
    return slots

DENTAL_PROCEDURES = {
    'cleaning': {
        'name': 'Dental Cleaning',
        'duration': '30-60 minutes',
        'frequency': 'Every 6 months',
        'description': [
            'Professional cleaning to remove plaque and tartar, followed by polishing.',
            'Comprehensive cleaning that includes scaling, polishing, and fluoride treatment.',
            'Deep cleaning procedure to maintain optimal oral health and prevent gum disease.'
        ],
        'preparation': [
            'No special preparation needed.',
            'Brush and floss as usual before your appointment.',
            'Eat normally, but try to brush after your last meal before the appointment.'
        ],
        'cost_range': '$75-$200'
    },
    'filling': {
        'name': 'Dental Filling',
        'duration': '30-60 minutes',
        'frequency': 'As needed',
        'description': [
            'Restoration of decayed tooth using composite or amalgam material.',
            'Modern tooth-colored composite filling to restore damaged teeth.',
            'Minimally invasive procedure to treat cavities and prevent further decay.'
        ],
        'preparation': [
            'Local anesthetic will be used.',
            'No eating for 2-3 hours before the procedure.',
            'Inform us about any medications you\'re currently taking.'
        ],
        'cost_range': '$150-$300 per filling'
    }
}

DENTAL_SYMPTOMS = {
    'pain': [
        'Tooth pain could indicate decay, infection, or sensitivity. Schedule a check-up soon.',
        'Dental pain might be a sign of a cavity or deeper infection. Let\'s get you checked out.',
        'Pain in your teeth shouldn\'t be ignored. We should examine this to prevent it from getting worse.'
    ],
    'bleeding': [
        'Bleeding gums may indicate gingivitis. Maintain good oral hygiene and schedule a cleaning.',
        'Gum bleeding often suggests early-stage gum disease. A professional cleaning could help.',
        'If your gums bleed while brushing, it\'s time for a dental check-up to assess your gum health.'
    ]
}

class ConversationContext:
    def __init__(self):
        self.history = []
        self.current_topic = None
        self.last_response_type = None

    def add_message(self, message: str, response: str):
        self.history.append({"message": message, "response": response})
        if len(self.history) > 5:  # Keep last 5 messages for context
            self.history.pop(0)

    def get_context(self) -> Dict:
        return {
            "history": self.history,
            "current_topic": self.current_topic,
            "last_response_type": self.last_response_type
        }

conversation_context = ConversationContext()

def get_procedure_info(procedure: str) -> Dict:
    """Find the closest matching procedure from our knowledge base."""
    procedure = procedure.lower()
    for key in DENTAL_PROCEDURES:
        if key in procedure:
            return DENTAL_PROCEDURES[key]
    return None

def format_procedure_info(procedure_info: Dict) -> str:
    """Format procedure information into a readable response with randomized variations."""
    description = random.choice(procedure_info['description'])
    preparation = random.choice(procedure_info['preparation'])
    
    return f"""Here's what you need to know about {procedure_info['name']}:
• Duration: {procedure_info['duration']}
• Typical frequency: {procedure_info['frequency']}
• Description: {description}
• Preparation: {preparation}
• Estimated cost range: {procedure_info['cost_range']}

[DEMO] Would you like to schedule an appointment? Here are some available slots:
{chr(10).join('• ' + slot for slot in generate_available_slots(5)[:3])}"""

def get_mock_patient_info(patient_name: str = None) -> str:
    """Generate mock patient information for demo purposes."""
    if patient_name and patient_name in DEMO_PATIENTS:
        patient = DEMO_PATIENTS[patient_name]
        history = patient['history']
        return f"""[DEMO] Patient Record for {patient_name} (ID: {patient['id']}):
Last visits:
{chr(10).join(f"• {visit['date']}: {visit['procedure']} - {visit['notes']}" for visit in history)}"""
    return None

def check_for_emergency(message: str) -> Tuple[bool, str]:
    """Check if the message indicates a dental emergency with randomized urgent care slots."""
    emergency_keywords = ['severe pain', 'extreme pain', 'swelling', 'bleeding', 'knocked out', 'broken tooth']
    is_emergency = any(keyword in message.lower() for keyword in emergency_keywords)
    
    if is_emergency:
        urgent_slots = [
            f"{(datetime.now() + timedelta(hours=h)).strftime('%I:%M %p')} TODAY"
            for h in range(1, 4)
        ]
        
        return True, f"""[DEMO] This sounds like a dental emergency. Our emergency line is available 24/7 at (555) 123-4567.

Urgent care slots available:
{chr(10).join('• ' + slot for slot in urgent_slots)}

While waiting for your emergency appointment:
1. {random.choice([
    'Apply a cold compress to reduce swelling',
    'Use an ice pack on the affected area',
    'Place a cold towel on your face near the pain'
])}
2. {random.choice([
    'Rinse with warm salt water',
    'Gently clean the affected area',
    'Use an antiseptic mouthwash if available'
])}
3. {random.choice([
    'Take over-the-counter pain medication',
    'Use acetaminophen for pain relief',
    'Consider taking ibuprofen for pain and swelling'
])}

Would you like me to schedule an emergency appointment for you?"""
    return False, ""

def get_ai_response(message: str) -> str:
    """Enhanced AI response function with context awareness and response variations"""
    message = message.lower()
    context = conversation_context.get_context()
    
    patient_info = None
    for patient_name in DEMO_PATIENTS.keys():
        if patient_name.lower() in message:
            patient_info = get_mock_patient_info(patient_name)
            if patient_info:
                conversation_context.current_topic = "patient_history"
                conversation_context.add_message(message, patient_info)
                return patient_info
    
    is_emergency, emergency_response = check_for_emergency(message)
    if is_emergency:
        conversation_context.current_topic = "emergency"
        conversation_context.add_message(message, emergency_response)
        return emergency_response
    
    if 'appointment' in message:
        available_slots = generate_available_slots(7)
        if 'schedule' in message or 'book' in message:
            response = random.choice([
                f"I'd be happy to help you schedule an appointment! Here are some available slots:\n{chr(10).join('• ' + slot for slot in available_slots[:3])}",
                f"I can help you find the perfect time for your visit. These slots are currently open:\n{chr(10).join('• ' + slot for slot in available_slots[:3])}",
                f"Let's get you scheduled! Here are our next available appointments:\n{chr(10).join('• ' + slot for slot in available_slots[:3])}"
            ])
            conversation_context.current_topic = "scheduling"
            conversation_context.add_message(message, response)
            return response
        elif 'cancel' in message or 'reschedule' in message:
            response = random.choice([
                "I can help you modify your appointment. Could you provide your name and current appointment date?",
                "I'll assist you with rescheduling. What's your name and when was your original appointment?",
                "Sure, I can help you with that. Please share your name and appointment details."
            ])
            conversation_context.current_topic = "rescheduling"
            conversation_context.add_message(message, response)
            return response
    
    for procedure in DENTAL_PROCEDURES.keys():
        if procedure in message:
            procedure_info = DENTAL_PROCEDURES[procedure]
            response = format_procedure_info(procedure_info)
            conversation_context.current_topic = "procedure_info"
            conversation_context.add_message(message, response)
            return response
    
    for symptom, responses in DENTAL_SYMPTOMS.items():
        if symptom in message:
            response = f"{random.choice(responses)}\n\n[DEMO] Would you like me to check our next available appointments?"
            conversation_context.current_topic = "symptoms"
            conversation_context.add_message(message, response)
            return response
    
    if any(word in message for word in ['cost', 'price', 'insurance', 'payment']):
        cost_responses = [
            """[DEMO] We offer flexible payment options and work with most insurance providers. Here's a general price guide:
• Check-up and cleaning: $75-$200
• Fillings: $150-$300
• Root canals: $700-$1,500

Would you like to discuss a specific procedure?""",
            """[DEMO] Our prices are competitive, and we accept most insurance plans. Some typical costs:
• Routine cleaning: Starting at $75
• Composite fillings: From $150
• Crown procedure: $800-$1,700

Can I provide specific pricing for any procedure?""",
        ]
        response = random.choice(cost_responses)
        conversation_context.current_topic = "costs"
        conversation_context.add_message(message, response)
        return response
    
    if any(word in message for word in ['hours', 'location', 'address', 'open']):
        office_responses = [
            """[DEMO] We're conveniently located at 123 Dental Street, San Francisco, CA 94101

Hours of Operation:
• Monday-Friday: 9:00 AM - 6:00 PM
• Saturday: 9:00 AM - 2:00 PM (by appointment)
• Sunday: Closed

Would you like to schedule a visit?""",
            """[DEMO] You can find us at:
123 Dental Street
San Francisco, CA 94101

We're open:
• Weekdays: 9:00 AM - 6:00 PM
• Saturdays: 9:00 AM - 2:00 PM
• Sundays: Closed

Can I help you book an appointment?"""
        ]
        response = random.choice(office_responses)
        conversation_context.current_topic = "office_info"
        conversation_context.add_message(message, response)
        return response
    
    default_responses = [
        """I can assist you with:
• Scheduling or modifying appointments
• Information about dental procedures
• Cost estimates and insurance
• Emergency dental care
• General dental advice

What would you like to know more about?""",
        """I'm here to help! I can provide information about:
• Booking appointments
• Our dental services
• Treatment costs and insurance
• Urgent dental care
• Oral health advice

How can I assist you today?""",
    ]
    
    response = random.choice(default_responses)
    conversation_context.current_topic = "general"
    conversation_context.add_message(message, response)
    return response