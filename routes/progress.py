"""
Progress endpoint for tracking seizure logs and treatment progress.
Handles logging seizures and generating treatment trend analysis.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid

progress_bp = Blueprint('progress', __name__)

# In-memory storage for seizure logs (in production, use database)
seizure_logs_db = []

@progress_bp.route('/progress', methods=['POST'])
def log_seizure():
    """
    Log a seizure occurrence or non-occurrence.
    
    Expected input:
    {
        "date": "YYYY-MM-DD",
        "occurred": 0 or 1,
        "patient": "Patient Name",
        "notes": "Optional notes about the day"
    }
    
    Returns:
    {
        "status": "success",
        "message": "Seizure log recorded successfully",
        "log_id": "unique_id",
        "log": {...}
    }
    """
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['date', 'occurred', 'patient']
        for field in required_fields:
            if not data or field not in data:
                return jsonify({
                    "error": "Missing required field",
                    "message": f"Field '{field}' is required"
                }), 400
        
        date_str = data['date']
        occurred = data['occurred']
        patient = data['patient'].strip()
        notes = data.get('notes', '').strip()
        
        # Validate patient name
        if not patient:
            return jsonify({
                "error": "Invalid input",
                "message": "Patient name cannot be empty"
            }), 400
        
        # Validate occurred value
        if occurred not in [0, 1]:
            return jsonify({
                "error": "Invalid occurred value",
                "message": "Occurred must be 0 (no seizure) or 1 (seizure occurred)"
            }), 400
        
        # Validate date format
        try:
            log_date = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
            if log_date > today:
                return jsonify({
                    "error": "Invalid date",
                    "message": "Cannot log seizures for future dates"
                }), 400
        except ValueError:
            return jsonify({
                "error": "Invalid date format",
                "message": "Date must be in YYYY-MM-DD format"
            }), 400
        
        # Check if log already exists for this date and patient
        for log in seizure_logs_db:
            if log['date'] == date_str and log['patient'] == patient:
                return jsonify({
                    "error": "Duplicate log",
                    "message": f"Seizure log already exists for {patient} on {date_str}"
                }), 409
        
        # Create seizure log object
        log_id = str(uuid.uuid4())
        seizure_log = {
            "id": log_id,
            "patient": patient,
            "date": date_str,
            "occurred": occurred,
            "notes": notes,
            "created_at": datetime.now().isoformat()
        }
        
        # Store seizure log
        seizure_logs_db.append(seizure_log)
        
        return jsonify({
            "status": "success",
            "message": "Seizure log recorded successfully",
            "log_id": log_id,
            "log": seizure_log
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": "Logging failed",
            "message": f"An error occurred while logging seizure: {str(e)}"
        }), 500

@progress_bp.route('/progress', methods=['GET'])
def get_progress():
    """
    Get treatment progress summary.
    
    Optional query parameters:
    - patient: Filter by patient name
    - days: Number of days to analyze (default: 7)
    
    Returns:
    {
        "status": "success",
        "summary": {
            "total_seizures": count,
            "seven_day_trend": count,
            "progress": "Improving" | "Stable" | "Needs Attention",
            "seizure_rate": percentage
        },
        "logs": [...]
    }
    """
    
    try:
        # Get query parameters
        patient_filter = request.args.get('patient', '').strip()
        days = int(request.args.get('days', 7))
        
        # Filter logs by patient if specified
        filtered_logs = seizure_logs_db.copy()
        if patient_filter:
            filtered_logs = [
                log for log in filtered_logs
                if patient_filter.lower() in log['patient'].lower()
            ]
        
        if not filtered_logs:
            return jsonify({
                "status": "success",
                "summary": {
                    "total_seizures": 0,
                    "seven_day_trend": 0,
                    "progress": "No Data",
                    "seizure_rate": 0.0
                },
                "logs": []
            })
        
        # Calculate total seizures
        total_seizures = sum(log['occurred'] for log in filtered_logs)
        
        # Calculate 7-day trend (or specified days)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = today - timedelta(days=days)
        
        recent_logs = [
            log for log in filtered_logs
            if datetime.strptime(log['date'], '%Y-%m-%d') >= start_date
        ]
        
        recent_seizures = sum(log['occurred'] for log in recent_logs)
        
        # Calculate seizure rate
        total_days = len(filtered_logs)
        seizure_rate = (total_seizures / total_days * 100) if total_days > 0 else 0.0
        
        # Determine progress status
        if total_days < 7:
            progress = "Insufficient Data"
        elif recent_seizures == 0:
            progress = "Improving"
        elif recent_seizures <= total_seizures / total_days * days * 0.5:
            progress = "Improving"
        elif recent_seizures <= total_seizures / total_days * days * 1.2:
            progress = "Stable"
        else:
            progress = "Needs Attention"
        
        # Sort logs by date (newest first)
        filtered_logs.sort(key=lambda x: x['date'], reverse=True)
        
        return jsonify({
            "status": "success",
            "summary": {
                "total_seizures": total_seizures,
                "seven_day_trend": recent_seizures,
                "progress": progress,
                "seizure_rate": round(seizure_rate, 2),
                "total_days_logged": total_days,
                "analysis_period_days": days
            },
            "logs": filtered_logs
        })
        
    except ValueError as e:
        return jsonify({
            "error": "Invalid parameter",
            "message": "Days parameter must be a valid integer"
        }), 400
        
    except Exception as e:
        return jsonify({
            "error": "Analysis failed",
            "message": f"An error occurred while analyzing progress: {str(e)}"
        }), 500

@progress_bp.route('/progress/<log_id>', methods=['PUT'])
def update_seizure_log(log_id):
    """
    Update a seizure log entry.
    
    Expected input:
    {
        "occurred": 0 or 1,
        "notes": "Updated notes"
    }
    
    Returns:
    {
        "status": "success",
        "message": "Seizure log updated successfully",
        "log": {...}
    }
    """
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No data provided",
                "message": "Please provide data to update"
            }), 400
        
        # Find log
        log = None
        for seizure_log in seizure_logs_db:
            if seizure_log['id'] == log_id:
                log = seizure_log
                break
        
        if not log:
            return jsonify({
                "error": "Log not found",
                "message": f"No seizure log found with ID: {log_id}"
            }), 404
        
        # Update fields if provided
        if 'occurred' in data:
            occurred = data['occurred']
            if occurred not in [0, 1]:
                return jsonify({
                    "error": "Invalid occurred value",
                    "message": "Occurred must be 0 or 1"
                }), 400
            log['occurred'] = occurred
        
        if 'notes' in data:
            log['notes'] = data['notes'].strip()
        
        log['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            "status": "success",
            "message": "Seizure log updated successfully",
            "log": log
        })
        
    except Exception as e:
        return jsonify({
            "error": "Update failed",
            "message": f"An error occurred while updating seizure log: {str(e)}"
        }), 500

@progress_bp.route('/progress/<log_id>', methods=['DELETE'])
def delete_seizure_log(log_id):
    """
    Delete a seizure log entry.
    
    Returns:
    {
        "status": "success",
        "message": "Seizure log deleted successfully"
    }
    """
    
    try:
        # Find and remove log
        for i, log in enumerate(seizure_logs_db):
            if log['id'] == log_id:
                del seizure_logs_db[i]
                
                return jsonify({
                    "status": "success",
                    "message": "Seizure log deleted successfully"
                })
        
        return jsonify({
            "error": "Log not found",
            "message": f"No seizure log found with ID: {log_id}"
        }), 404
        
    except Exception as e:
        return jsonify({
            "error": "Deletion failed",
            "message": f"An error occurred while deleting seizure log: {str(e)}"
        }), 500 