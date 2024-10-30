from app import app, db
from models import Patient, Appointment
from utils import DEMO_PATIENTS
from datetime import datetime, timedelta
import random

def create_demo_data():
    with app.app_context():
        # Clear existing data
        Appointment.query.delete()
        Patient.query.delete()
        
        # Demo procedures
        procedures = ["Dental Cleaning", "Root Canal", "Filling", "Crown"]
        statuses = ["pending", "approved"]
        
        # Create patients
        patients = {}
        for name, data in DEMO_PATIENTS.items():
            patient = Patient(
                name=name,
                email=f"{name.lower().replace(' ', '.')}@demo.com",
                phone="555-0123"
            )
            db.session.add(patient)
            patients[name] = patient
        
        # Generate appointments for the next 7 days
        current_date = datetime.now()
        for day in range(1, 8):
            appointment_date = current_date + timedelta(days=day)
            
            # Only weekdays
            if appointment_date.weekday() < 5:
                # 2-3 appointments per day
                for hour in random.sample(range(9, 16), random.randint(2, 3)):
                    # Randomly select patient and procedure
                    patient = random.choice(list(patients.values()))
                    procedure = random.choice(procedures)
                    status = random.choice(statuses)
                    
                    appointment = Appointment(
                        patient=patient,
                        datetime=appointment_date.replace(hour=hour, minute=random.choice([0, 30])),
                        procedure=procedure,
                        status=status,
                        notes="Demo appointment"
                    )
                    db.session.add(appointment)
        
        db.session.commit()
        print("Demo data created successfully!")

if __name__ == "__main__":
    create_demo_data()
