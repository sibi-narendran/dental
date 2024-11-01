"""In-memory data storage for the dental practice CRM"""
from datetime import datetime
from typing import Dict, List, Optional

# In-memory storage
patients: Dict[int, dict] = {}
appointments: Dict[int, dict] = {}
patient_id_counter = 1
appointment_id_counter = 1

def add_patient(name: str, email: str, phone: str) -> dict:
    """Add a new patient to storage"""
    global patient_id_counter
    patient = {
        'id': patient_id_counter,
        'name': name,
        'email': email,
        'phone': phone
    }
    patients[patient_id_counter] = patient
    patient_id_counter += 1
    return patient

def get_patient(patient_id: int) -> Optional[dict]:
    """Get patient by ID"""
    return patients.get(patient_id)

def get_patient_by_email(email: str) -> Optional[dict]:
    """Get patient by email"""
    for patient in patients.values():
        if patient['email'] == email:
            return patient
    return None

def add_appointment(patient_id: int, datetime_obj: datetime, procedure: str, status: str = 'pending', notes: str = '') -> dict:
    """Add a new appointment to storage"""
    global appointment_id_counter
    patient = get_patient(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID {patient_id} not found")
        
    appointment = {
        'id': appointment_id_counter,
        'patient_id': patient_id,
        'patient': patient,
        'datetime': datetime_obj,
        'procedure': procedure,
        'status': status,
        'notes': notes,
        'created_at': datetime.now()
    }
    appointments[appointment_id_counter] = appointment
    appointment_id_counter += 1
    return appointment

def get_appointment(appointment_id: int) -> Optional[dict]:
    """Get appointment by ID"""
    return appointments.get(appointment_id)

def get_all_appointments() -> List[dict]:
    """Get all appointments sorted by datetime"""
    return sorted(appointments.values(), key=lambda x: x['datetime'])

def clear_storage():
    """Clear all data from storage"""
    global patient_id_counter, appointment_id_counter
    patients.clear()
    appointments.clear()
    patient_id_counter = 1
    appointment_id_counter = 1
