"""
Medication endpoint for managing medication schedules.
Handles setting up medication reminders and schedules for patients.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

medication_bp = Blueprint('medication', __name__)

# In-memory storage for medication schedules (in production, use database)
medication_db = []

@medication_bp.route('/medication', methods=['POST'])
def schedule_medication():
    """
    Schedule medication for a patient.
    
    Expected input:
    {
        "patient": "Patient Name",
        "drug_name": "Medication Name",
        "times": ["08:00", "20:00"],
        "dosage": "10mg",
        "instructions": "Take with food"
    }
    
    Returns:
    {
        "status": "success",
        "message": "Medication scheduled successfully",
        "medication_id": "unique_id",
        "medication": {...}
    }
    """
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient', 'drug_name', 'times']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    "error": "Missing required field",
                    "message": f"Field '{field}' is required"
                }), 400
        
        patient = data['patient'].strip()
        drug_name = data['drug_name'].strip()
        times = data['times']
        dosage = data.get('dosage', '').strip()
        instructions = data.get('instructions', '').strip()
        
        # Validate patient and drug names
        if not patient or not drug_name:
            return jsonify({
                "error": "Invalid input",
                "message": "Patient and drug names cannot be empty"
            }), 400
        
        # Validate times array
        if not isinstance(times, list) or len(times) == 0:
            return jsonify({
                "error": "Invalid times",
                "message": "Times must be a non-empty array of time strings"
            }), 400
        
        # Validate time format for each time
        for time_str in times:
            try:
                datetime.strptime(time_str, '%H:%M')
            except ValueError:
                return jsonify({
                    "error": "Invalid time format",
                    "message": f"Time '{time_str}' must be in HH:MM format (24-hour)"
                }), 400
        
        # Sort times chronologically
        times.sort()
        
        # Create medication schedule object
        medication_id = str(uuid.uuid4())
        medication = {
            "id": medication_id,
            "patient": patient,
            "drug_name": drug_name,
            "times": times,
            "dosage": dosage,
            "instructions": instructions,
            "status": "active",
            "created_at": datetime.now().isoformat()
        }
        
        # Store medication schedule
        medication_db.append(medication)
        
        return jsonify({
            "status": "success",
            "message": "Medication scheduled successfully",
            "medication_id": medication_id,
            "medication": medication
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": "Scheduling failed",
            "message": f"An error occurred while scheduling medication: {str(e)}"
        }), 500

@medication_bp.route('/medication', methods=['GET'])
def get_medications():
    """
    Retrieve medication schedules.
    
    Optional query parameters:
    - patient: Filter by patient name
    - status: Filter by medication status
    
    Returns:
    {
        "status": "success",
        "medications": [...],
        "total": count
    }
    """
    
    try:
        # Get filter parameters
        patient_filter = request.args.get('patient', '').strip()
        status_filter = request.args.get('status', '').strip()
        
        # Filter medications
        filtered_medications = medication_db.copy()
        
        if patient_filter:
            filtered_medications = [
                med for med in filtered_medications
                if patient_filter.lower() in med['patient'].lower()
            ]
        
        if status_filter:
            filtered_medications = [
                med for med in filtered_medications
                if status_filter.lower() == med['status'].lower()
            ]
        
        # Sort by patient name and drug name
        filtered_medications.sort(key=lambda x: (x['patient'], x['drug_name']))
        
        return jsonify({
            "status": "success",
            "medications": filtered_medications,
            "total": len(filtered_medications)
        })
        
    except Exception as e:
        return jsonify({
            "error": "Retrieval failed",
            "message": f"An error occurred while retrieving medications: {str(e)}"
        }), 500

@medication_bp.route('/medication/<medication_id>', methods=['PUT'])
def update_medication(medication_id):
    """
    Update medication schedule.
    
    Expected input:
    {
        "times": ["new_time1", "new_time2"],
        "dosage": "new_dosage",
        "instructions": "new_instructions",
        "status": "active" | "paused" | "discontinued"
    }
    
    Returns:
    {
        "status": "success",
        "message": "Medication updated successfully",
        "medication": {...}
    }
    """
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No data provided",
                "message": "Please provide data to update"
            }), 400
        
        # Find medication
        medication = None
        for med in medication_db:
            if med['id'] == medication_id:
                medication = med
                break
        
        if not medication:
            return jsonify({
                "error": "Medication not found",
                "message": f"No medication found with ID: {medication_id}"
            }), 404
        
        # Update fields if provided
        if 'times' in data:
            times = data['times']
            if not isinstance(times, list) or len(times) == 0:
                return jsonify({
                    "error": "Invalid times",
                    "message": "Times must be a non-empty array"
                }), 400
            
            # Validate time format
            for time_str in times:
                try:
                    datetime.strptime(time_str, '%H:%M')
                except ValueError:
                    return jsonify({
                        "error": "Invalid time format",
                        "message": f"Time '{time_str}' must be in HH:MM format"
                    }), 400
            
            medication['times'] = sorted(times)
        
        if 'dosage' in data:
            medication['dosage'] = data['dosage'].strip()
        
        if 'instructions' in data:
            medication['instructions'] = data['instructions'].strip()
        
        if 'status' in data:
            new_status = data['status'].lower()
            valid_statuses = ['active', 'paused', 'discontinued']
            
            if new_status not in valid_statuses:
                return jsonify({
                    "error": "Invalid status",
                    "message": f"Status must be one of: {', '.join(valid_statuses)}"
                }), 400
            
            medication['status'] = new_status
        
        medication['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            "status": "success",
            "message": "Medication updated successfully",
            "medication": medication
        })
        
    except Exception as e:
        return jsonify({
            "error": "Update failed",
            "message": f"An error occurred while updating medication: {str(e)}"
        }), 500

@medication_bp.route('/medication/<medication_id>', methods=['DELETE'])
def delete_medication(medication_id):
    """
    Delete medication schedule.
    
    Returns:
    {
        "status": "success",
        "message": "Medication deleted successfully"
    }
    """
    
    try:
        # Find and remove medication
        for i, medication in enumerate(medication_db):
            if medication['id'] == medication_id:
                del medication_db[i]
                
                return jsonify({
                    "status": "success",
                    "message": "Medication deleted successfully"
                })
        
        return jsonify({
            "error": "Medication not found",
            "message": f"No medication found with ID: {medication_id}"
        }), 404
        
    except Exception as e:
        return jsonify({
            "error": "Deletion failed",
            "message": f"An error occurred while deleting medication: {str(e)}"
        }), 500 