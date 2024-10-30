from flask import render_template, request, jsonify
from app import app, db
from models import Patient, Appointment
from utils import get_ai_response
from datetime import datetime

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/doctor-portal')
def doctor_portal():
    appointments = Appointment.query.order_by(Appointment.datetime).all()
    return render_template('doctor_portal.html', appointments=appointments)

@app.route('/patient-chat')
def patient_chat():
    return render_template('patient_chat.html')

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    patient = Patient.query.filter_by(email=data['email']).first()
    if not patient:
        patient = Patient(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        db.session.add(patient)
        
    appointment = Appointment(
        patient=patient,
        datetime=datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M'),
        procedure=data['procedure']
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/appointments/<int:appointment_id>/approve', methods=['POST'])
def approve_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'approved'
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/chat', methods=['POST'])
def chat():
    message = request.json['message']
    response = get_ai_response(message)
    return jsonify({'response': response})
