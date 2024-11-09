import os
from openai import OpenAI
from typing import Dict, Optional
from datetime import datetime, timedelta
import random
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client with error handling
try:
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key is not set in environment variables")

    client = OpenAI(api_key=api_key)
    # Test the API key with a minimal request
    client.models.list()
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Error initializing OpenAI client: {str(e)}")
    client = None

# Keep demo patient data for reference
DEMO_PATIENTS = {
    "Emily Thompson": {
        "id":
        "P1001",
        "history": [{
            "date":
            "2024-09-15",
            "procedure":
            "Teeth Whitening",
            "notes":
            "Professional whitening completed, excellent results"
        }, {
            "date": "2024-03-20",
            "procedure": "Routine Checkup",
            "notes": "No cavities, good oral hygiene"
        }]
    },
    "Michael Chen": {
        "id":
        "P1002",
        "history": [{
            "date": "2024-10-01",
            "procedure": "Dental Implant",
            "tooth": "#30",
            "notes": "Implant placement successful"
        }, {
            "date": "2024-08-12",
            "procedure": "Dental Bridge",
            "tooth": "#18-20",
            "notes": "Bridge fitted and adjusted"
        }]
    },
    "Sofia Rodriguez": {
        "id":
        "P1003",
        "history": [{
            "date": "2024-09-20",
            "procedure": "Orthodontic Consultation",
            "notes": "Treatment plan discussed for braces"
        }, {
            "date": "2024-07-15",
            "procedure": "Gum Treatment",
            "notes": "Deep cleaning completed"
        }]
    },
    "James Wilson": {
        "id":
        "P1004",
        "history": [{
            "date": "2024-10-05",
            "procedure": "Wisdom Tooth Extraction",
            "tooth": "#1,16,17,32",
            "notes": "All wisdom teeth removed"
        }, {
            "date": "2024-06-30",
            "procedure": "Emergency Dental Care",
            "notes": "Treated severe tooth pain"
        }]
    },
    "Aisha Patel": {
        "id":
        "P1005",
        "history": [{
            "date": "2024-09-25",
            "procedure": "Dental Bridge",
            "tooth": "#13-15",
            "notes": "Bridge preparation completed"
        }, {
            "date": "2024-08-01",
            "procedure": "Gum Treatment",
            "notes": "Periodontal maintenance"
        }]
    },
    "David Kim": {
        "id":
        "P1006",
        "history": [{
            "date": "2024-10-10",
            "procedure": "Dental Implant",
            "tooth": "#19",
            "notes": "Initial implant consultation"
        }, {
            "date": "2024-07-20",
            "procedure": "Routine Checkup",
            "notes": "Minor plaque buildup noted"
        }]
    },
    "Rachel Foster": {
        "id":
        "P1007",
        "history": [{
            "date": "2024-09-30",
            "procedure": "Teeth Whitening",
            "notes": "Take-home whitening kit provided"
        }, {
            "date": "2024-08-15",
            "procedure": "Orthodontic Consultation",
            "notes": "Invisalign treatment discussed"
        }]
    },
    "Omar Hassan": {
        "id":
        "P1008",
        "history": [{
            "date": "2024-10-15",
            "procedure": "Emergency Dental Care",
            "notes": "Treated chipped tooth"
        }, {
            "date": "2024-07-01",
            "procedure": "Wisdom Tooth Extraction",
            "tooth": "#16",
            "notes": "Single wisdom tooth removal"
        }]
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
    return """lets play a role play game im a dentist dr thiyagu you are my assiatant u have access to all my documents and data, and u have to assist me, just assume everything there and answer , if i ask any documents just pretend u have send them, if any query assume and answer, pretent you can do anything i ask u to, and you done it.."""


def get_patient_system_prompt() -> str:
    """Get the system prompt for patient interactions"""
    return """lets play a roleplay game you are a dental receptionist, and u are talking to customers, book appointments, answer questions, get customer details, and follow up 

Keep responses simple and u  pretend u can do anything they ask, and u have already done it, try to upsell products , your dental office name is dr thiyagu dental clinic."""


def get_ai_response(message: str, is_doctor: bool = False) -> str:
    """Get response from OpenAI ChatGPT based on role"""
    try:
        if not client:
            logger.error("OpenAI client is not initialized")
            return "I apologize, but the AI service is currently unavailable. Please try again later."

        # Log the incoming request
        logger.info(
            f"Processing {'doctor' if is_doctor else 'patient'} chat request")

        # Get patient context if available
        patient_context = get_patient_context(message)

        # Generate available slots for appointment-related queries
        slots = generate_available_slots(
            7) if 'appointment' in message.lower() else []

        # Create system message based on role
        system_message = get_doctor_system_prompt(
        ) if is_doctor else get_patient_system_prompt()

        # Create messages array for the chat
        messages = [{
            "role": "system",
            "content": system_message
        }, {
            "role": "user",
            "content": message
        }]

        # Add patient context if available
        if patient_context:
            messages.insert(
                1, {
                    "role": "system",
                    "content": f"Current patient context:\n{patient_context}"
                })

        # Add available slots if appointment-related
        if slots:
            slot_text = "\n".join(f"• {slot}" for slot in slots[:3])
            messages.insert(
                1, {
                    "role": "system",
                    "content": f"Available appointment slots:\n{slot_text}"
                })

        # Get response from OpenAI
        response = client.chat.completions.create(model="gpt-4",
                                                  messages=messages,
                                                  temperature=0.7,
                                                  max_tokens=500)

        # Log successful response
        logger.info(
            f"Successfully generated response for {'doctor' if is_doctor else 'patient'} chat"
        )
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Error in get_ai_response: {str(e)}")
        return "I apologize, but I'm having trouble processing your request at the moment. Please try again later or contact our office directly."
