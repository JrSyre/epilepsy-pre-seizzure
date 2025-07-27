"""
Appointments endpoint for managing doctor appointments.
Handles booking appointments and retrieving appointment history.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

appointments_bp = Blueprint('appointments', __name__)

# In-memory storage for appointments (in production, use database)
appointments_db = []

@appointments_bp.route('/appointments', methods=['POST'])
def book_appointment():
    """
    Book a new doctor appointment.
    
    Expected input:
    {
        "patient": "Patient Name",
        "doctor": "Doctor Name", 
        "date": "YYYY-MM-DD",
        "time": "HH:MM"
    }
    
    Returns:
    {
        "status": "success",
        "message": "Appointment booked successfully",
        "appointment_id": "unique_id",
        "appointment": {...}
    }
    """
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient', 'doctor', 'date', 'time']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    "error": "Missing required field",
                    "message": f"Field '{field}' is required"
                }), 400
        
        patient = data['patient'].strip()
        doctor = data['doctor'].strip()
        date_str = data['date']
        time_str = data['time']
        
        # Validate patient and doctor names
        if not patient or not doctor:
            return jsonify({
                "error": "Invalid input",
                "message": "Patient and doctor names cannot be empty"
            }), 400
        
        # Validate date format
        try:
            appointment_date = datetime.strptime(date_str, '%Y-%m-%d')
            if appointment_date < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                return jsonify({
                    "error": "Invalid date",
                    "message": "Appointment date cannot be in the past"
                }), 400
        except ValueError:
            return jsonify({
                "error": "Invalid date format",
                "message": "Date must be in YYYY-MM-DD format"
            }), 400
        
        # Validate time format
        try:
            datetime.strptime(time_str, '%H:%M')
        except ValueError:
            return jsonify({
                "error": "Invalid time format", 
                "message": "Time must be in HH:MM format (24-hour)"
            }), 400
        
        # Create appointment object
        appointment_id = str(uuid.uuid4())
        appointment = {
            "id": appointment_id,
            "patient": patient,
            "doctor": doctor,
            "date": date_str,
            "time": time_str,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        
        # Store appointment
        appointments_db.append(appointment)
        
        return jsonify({
            "status": "success",
            "message": "Appointment booked successfully",
            "appointment_id": appointment_id,
            "appointment": appointment
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": "Booking failed",
            "message": f"An error occurred while booking appointment: {str(e)}"
        }), 500

@appointments_bp.route('/appointments', methods=['GET'])
def get_appointments():
    """
    Retrieve all appointments.
    
    Optional query parameters:
    - patient: Filter by patient name
    - doctor: Filter by doctor name
    - status: Filter by appointment status
    
    Returns:
    {
        "status": "success",
        "appointments": [...],
        "total": count
    }
    """
    
    try:
        # Get filter parameters
        patient_filter = request.args.get('patient', '').strip()
        doctor_filter = request.args.get('doctor', '').strip()
        status_filter = request.args.get('status', '').strip()
        
        # Filter appointments
        filtered_appointments = appointments_db.copy()
        
        if patient_filter:
            filtered_appointments = [
                apt for apt in filtered_appointments 
                if patient_filter.lower() in apt['patient'].lower()
            ]
        
        if doctor_filter:
            filtered_appointments = [
                apt for apt in filtered_appointments
                if doctor_filter.lower() in apt['doctor'].lower()
            ]
        
        if status_filter:
            filtered_appointments = [
                apt for apt in filtered_appointments
                if status_filter.lower() == apt['status'].lower()
            ]
        
        # Sort by date and time
        filtered_appointments.sort(key=lambda x: (x['date'], x['time']))
        
        return jsonify({
            "status": "success",
            "appointments": filtered_appointments,
            "total": len(filtered_appointments)
        })
        
    except Exception as e:
        return jsonify({
            "error": "Retrieval failed",
            "message": f"An error occurred while retrieving appointments: {str(e)}"
        }), 500

@appointments_bp.route('/appointments/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """
    Update appointment status.
    
    Expected input:
    {
        "status": "completed" | "cancelled" | "rescheduled"
    }
    
    Returns:
    {
        "status": "success",
        "message": "Appointment updated successfully",
        "appointment": {...}
    }
    """
    
    try:
        data = request.get_json()
        
        if not data or 'status' not in data:
            return jsonify({
                "error": "Missing status",
                "message": "Status field is required"
            }), 400
        
        new_status = data['status'].lower()
        valid_statuses = ['scheduled', 'completed', 'cancelled', 'rescheduled']
        
        if new_status not in valid_statuses:
            return jsonify({
                "error": "Invalid status",
                "message": f"Status must be one of: {', '.join(valid_statuses)}"
            }), 400
        
        # Find and update appointment
        for appointment in appointments_db:
            if appointment['id'] == appointment_id:
                appointment['status'] = new_status
                appointment['updated_at'] = datetime.now().isoformat()
                
                return jsonify({
                    "status": "success",
                    "message": "Appointment updated successfully",
                    "appointment": appointment
                })
        
        return jsonify({
            "error": "Appointment not found",
            "message": f"No appointment found with ID: {appointment_id}"
        }), 404
        
    except Exception as e:
        return jsonify({
            "error": "Update failed",
            "message": f"An error occurred while updating appointment: {str(e)}"
        }), 500 