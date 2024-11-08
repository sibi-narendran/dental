from flask import render_template, request, jsonify
from app import app
from utils import get_ai_response
from datetime import datetime
import storage

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/portal-selection')
def portal_selection():
    return render_template('portal_selection.html')

@app.route('/doctor-portal')
def doctor_portal():
    appointments = storage.get_all_appointments()
    return render_template('doctor_portal.html', appointments=appointments)

@app.route('/patient-chat')
def patient_chat():
    return render_template('patient_chat.html')

@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    patient = storage.get_patient_by_email(data['email'])
    if not patient:
        patient = storage.add_patient(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        
    appointment = storage.add_appointment(
        patient_id=patient['id'],
        datetime_obj=datetime.strptime(data['datetime'], '%Y-%m-%dT%H:%M'),
        procedure=data['procedure']
    )
    return jsonify({'success': True})

@app.route('/api/appointments/<int:appointment_id>/approve', methods=['POST'])
def approve_appointment(appointment_id):
    # Demo mode: No storage updates, just return success
    # Updates are simulated in the UI and reset on page reload
    return jsonify({'success': True})

@app.route('/api/chat/doctor', methods=['POST'])
def doctor_chat():
    message = request.json['message']
    response = get_ai_response(message, is_doctor=True)
    return jsonify({'response': response})

@app.route('/api/chat/patient', methods=['POST'])
def patient_chat_api():
    message = request.json['message']
    response = get_ai_response(message, is_doctor=False)
    return jsonify({'response': response})
