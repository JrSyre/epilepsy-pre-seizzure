from . import frontend_bp
from flask import render_template, request
import requests

API_BASE = 'http://localhost:5000/api'

@frontend_bp.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@frontend_bp.route('/predict', methods=['GET', 'POST'])
def predict():
    result = None
    error = None
    if request.method == 'POST':
        features = request.form.get('features', '')
        try:
            features_list = [float(x.strip()) for x in features.split(',')]
            resp = requests.post(f'{API_BASE}/predict', json={'features': features_list})
            if resp.ok:
                result = resp.json()
            else:
                error = resp.json().get('message', 'Prediction failed.')
        except Exception as e:
            error = str(e)
    return render_template('predict.html', result=result, error=error)

@frontend_bp.route('/appointments', methods=['GET', 'POST'])
def appointments():
    result = None
    error = None
    appointments = []
    if request.method == 'POST':
        data = {k: request.form[k] for k in ['patient', 'doctor', 'date', 'time']}
        try:
            resp = requests.post(f'{API_BASE}/appointments', json=data)
            if resp.ok:
                result = 'Appointment booked!'
            else:
                error = resp.json().get('message', 'Booking failed.')
        except Exception as e:
            error = str(e)
    try:
        resp = requests.get(f'{API_BASE}/appointments')
        if resp.ok:
            appointments = resp.json()
    except Exception:
        pass
    return render_template('appointments.html', result=result, error=error, appointments=appointments)

@frontend_bp.route('/medication', methods=['GET', 'POST'])
def medication():
    result = None
    error = None
    medications = []
    if request.method == 'POST':
        data = {k: request.form.get(k, '') for k in ['patient', 'drug_name', 'dosage', 'instructions', 'times']}
        if data['times']:
            data['times'] = [t.strip() for t in data['times'].split(',')]
        try:
            resp = requests.post(f'{API_BASE}/medication', json=data)
            if resp.ok:
                result = 'Medication scheduled!'
            else:
                error = resp.json().get('message', 'Scheduling failed.')
        except Exception as e:
            error = str(e)
    try:
        resp = requests.get(f'{API_BASE}/medication')
        if resp.ok:
            medications = resp.json()
    except Exception:
        pass
    return render_template('medication.html', result=result, error=error, medications=medications)

@frontend_bp.route('/progress', methods=['GET', 'POST'])
def progress():
    result = None
    error = None
    progress_logs = []
    if request.method == 'POST':
        data = {k: request.form.get(k, '') for k in ['date', 'patient', 'occurred', 'notes']}
        try:
            data['occurred'] = int(data['occurred'])
            resp = requests.post(f'{API_BASE}/progress', json=data)
            if resp.ok:
                result = 'Progress logged!'
            else:
                error = resp.json().get('message', 'Logging failed.')
        except Exception as e:
            error = str(e)
    try:
        resp = requests.get(f'{API_BASE}/progress')
        if resp.ok:
            progress_logs = resp.json()
    except Exception:
        pass
    return render_template('progress.html', result=result, error=error, progress_logs=progress_logs)