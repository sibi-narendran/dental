import os
from openai import OpenAI
from typing import Dict
from datetime import datetime, timedelta
import random

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Keep demo patient data for reference
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

def generate_available_slots(days_ahead: int = 7) -> list:
    """Generate demo available appointment slots"""
    slots = []
    current_date = datetime.now()
    for day in range(1, days_ahead + 1):
        date = current_date + timedelta(days=day)
        if date.weekday() < 5:  # Monday to Friday
            times = ["9:00 AM", "10:30 AM", "2:00 PM", "3:30 PM", "4:45 PM"]
        else:  # Saturday
            times = ["9:00 AM", "10:30 AM", "11:45 AM"]
        
        for time in random.sample(times, min(3, len(times))):
            slots.append(f"{date.strftime('%A, %B %d')}, {time}")
    return slots

def get_patient_context(message: str) -> str:
    """Get patient context if available"""
    for patient_name, data in DEMO_PATIENTS.items():
        if patient_name.lower() in message.lower():
            history = data['history']
            return f"""Patient Record for {patient_name} (ID: {data['id']}):
Last visits:
{chr(10).join(f"• {visit['date']}: {visit['procedure']} - {visit['notes']}" for visit in history)}"""
    return ""

def get_doctor_system_prompt() -> str:
    """Get the system prompt for doctor interactions"""
    return """You are an AI assistant for dental professionals. Your role is to:
1. Help analyze patient records and provide insights
2. Assist with treatment planning and procedure recommendations
3. Provide evidence-based answers to clinical questions
4. Help manage appointments and schedules
5. Offer guidance on best practices and protocols

Use medical terminology when appropriate but maintain clarity. This is a demo system, so prefix any specific medical advice, diagnoses, or treatment plans with [DEMO]. Always encourage consulting with colleagues for complex cases."""

def get_patient_system_prompt() -> str:
    """Get the system prompt for patient interactions"""
    return """You are a friendly and professional dental office AI assistant. 
Your role is to help patients with:
1. Scheduling and managing appointments
2. Providing general information about dental procedures
3. Answering questions about services and costs
4. Addressing basic dental concerns
5. Offering oral hygiene guidance

Keep responses simple and patient-friendly. Avoid technical medical terminology unless necessary.
This is a demo system, so prefix any specific appointment times, costs, or contact details with [DEMO]."""

def get_ai_response(message: str, is_doctor: bool = False) -> str:
    """Get response from OpenAI ChatGPT based on role"""
    try:
        # Get patient context if available
        patient_context = get_patient_context(message)
        
        # Generate available slots for appointment-related queries
        slots = generate_available_slots(7) if 'appointment' in message.lower() else []
        
        # Create system message based on role
        system_message = get_doctor_system_prompt() if is_doctor else get_patient_system_prompt()
        
        # Create messages array for the chat
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": message}
        ]

        # Add patient context if available
        if patient_context:
            messages.insert(1, {"role": "system", "content": f"Current patient context:\n{patient_context}"})

        # Add available slots if appointment-related
        if slots:
            slot_text = "\n".join(f"• {slot}" for slot in slots[:3])
            messages.insert(1, {"role": "system", "content": f"Available appointment slots:\n{slot_text}"})

        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"I apologize, but I'm having trouble processing your request at the moment. Please try again later or contact our office directly."
