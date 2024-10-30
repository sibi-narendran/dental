from app import app, db
from models import Patient, Appointment
from utils import DEMO_PATIENTS
from datetime import datetime, timedelta
import random

def create_demo_data():
    with app.app_context():
        # Set fixed seed for consistent data
        random.seed(42)

        # Clear existing data
        Appointment.query.delete()
        Patient.query.delete()
        
        # Fixed time slots for appointments
        time_slots = [
            (9, 30),   # 9:30 AM
            (10, 30),  # 10:30 AM
            (11, 30),  # 11:30 AM
            (14, 30),  # 2:30 PM
            (15, 30),  # 3:30 PM
            (16, 30)   # 4:30 PM
        ]
        
        # Fixed patient-procedure assignments
        appointments_data = [
            # Day 1 appointments
            ("Michael Chen", "Dental Bridge", "approved", 0, "Bridge adjustment follow-up"),
            ("James Wilson", "Wisdom Tooth Extraction", "approved", 1, "Pre-surgery consultation"),
            ("Sofia Rodriguez", "Routine Checkup", "approved", 2, "Annual checkup"),
            ("Aisha Patel", "Emergency Dental Care", "approved", 3, "Severe tooth pain"),
            
            # Day 2 appointments
            ("Omar Hassan", "Wisdom Tooth Extraction", "pending", 0, "Initial consultation"),
            ("David Kim", "Dental Implant", "pending", 1, "Implant planning"),
            ("Rachel Foster", "Teeth Whitening", "pending", 2, "Professional whitening session"),
            ("Emily Thompson", "Routine Checkup", "pending", 3, "6-month checkup"),
            
            # Day 3 appointments
            ("Michael Chen", "Dental Implant", "pending", 0, "Consultation for missing tooth"),
            ("Aisha Patel", "Dental Bridge", "pending", 1, "Bridge preparation"),
            ("Sofia Rodriguez", "Orthodontic Consultation", "pending", 2, "Braces discussion")
        ]

        # Create patients with consistent data
        patients = {}
        for name, data in DEMO_PATIENTS.items():
            patient = Patient(
                name=name,
                email=f"{name.lower().replace(' ', '.')}@demo.com",
                phone=f"555-{random.randint(1000,9999)}"  # Using random seed for consistent numbers
            )
            db.session.add(patient)
            patients[name] = patient
        
        # Create appointments with fixed assignments
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for day_offset in range(3):  # Create appointments for next 3 days
            appointment_date = current_date + timedelta(days=day_offset + 1)
            
            # Skip weekends
            if appointment_date.weekday() >= 5:
                continue
                
            # Get appointments for this day
            day_appointments = [appt for appt in appointments_data 
                              if (appointments_data.index(appt) // 4) == day_offset]
            
            for patient_name, procedure, status, time_slot_idx, notes in day_appointments:
                hour, minute = time_slots[time_slot_idx]
                appointment = Appointment(
                    patient=patients[patient_name],
                    datetime=appointment_date.replace(hour=hour, minute=minute),
                    procedure=procedure,
                    status=status,
                    notes=notes
                )
                db.session.add(appointment)
        
        db.session.commit()
        print("Demo data created successfully!")

if __name__ == "__main__":
    create_demo_data()
