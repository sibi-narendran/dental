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
        
        # Demo procedures with approximate durations
        procedures = [
            "Teeth Whitening",
            "Dental Implant",
            "Wisdom Tooth Extraction",
            "Dental Bridge",
            "Orthodontic Consultation",
            "Gum Treatment",
            "Routine Checkup",
            "Emergency Dental Care"
        ]
        
        statuses = ["pending", "approved"]
        
        # Create patients
        patients = {}
        for name, data in DEMO_PATIENTS.items():
            patient = Patient(
                name=name,
                email=f"{name.lower().replace(' ', '.')}@demo.com",
                phone=f"555-{random.randint(1000,9999)}"
            )
            db.session.add(patient)
            patients[name] = patient
        
        # Generate appointments for the next 7 days
        current_date = datetime.now()
        
        # Assign procedures to specific time slots based on complexity
        morning_slots = [9, 10, 11]  # Morning appointments
        afternoon_slots = [14, 15, 16]  # Afternoon appointments
        
        for day in range(1, 8):
            appointment_date = current_date + timedelta(days=day)
            
            # Only weekdays
            if appointment_date.weekday() < 5:
                # Create 4-5 appointments per day
                num_appointments = random.randint(4, 5)
                available_slots = morning_slots + afternoon_slots
                selected_slots = random.sample(available_slots, num_appointments)
                
                for hour in selected_slots:
                    # Randomly select patient and procedure
                    patient = random.choice(list(patients.values()))
                    
                    # Select procedure based on time of day
                    if hour in morning_slots:
                        # More complex procedures in the morning
                        procedure = random.choice([
                            "Dental Implant",
                            "Wisdom Tooth Extraction",
                            "Dental Bridge",
                            "Gum Treatment"
                        ])
                    else:
                        # Simpler procedures in the afternoon
                        procedure = random.choice([
                            "Teeth Whitening",
                            "Orthodontic Consultation",
                            "Routine Checkup",
                            "Emergency Dental Care"
                        ])
                    
                    status = random.choice(statuses)
                    
                    appointment = Appointment(
                        patient=patient,
                        datetime=appointment_date.replace(hour=hour, minute=random.choice([0, 15, 30, 45])),
                        procedure=procedure,
                        status=status,
                        notes=f"Demo appointment for {procedure}"
                    )
                    db.session.add(appointment)
        
        db.session.commit()
        print("Demo data created successfully!")

if __name__ == "__main__":
    create_demo_data()
