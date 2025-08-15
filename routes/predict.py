"""
Prediction endpoint for seizure risk assessment.
Handles ML model loading, feature scaling, and prediction with natural language responses.
"""

from flask import Blueprint, request, jsonify
import joblib
import numpy as np
import random
import os
import json
import re

predict_bp = Blueprint('predict', __name__)

# Natural language messages for different prediction outcomes
SEIZURE_RISK_MESSAGES = [
    "Warning: Seizure may occur soon. Stay safe and alert.",
    "High seizure probability. Alert your caregiver if possible.",
    "Critical: Seizure risk detected. Please take immediate precautions.",
    "Danger: Brain activity indicates potential seizure. Seek medical attention.",
    "Alert: Seizure warning active. Avoid dangerous activities.",
    "Urgent: Seizure probability elevated. Contact your healthcare provider.",
    "Warning: Abnormal brain patterns detected. Stay in safe environment.",
    "High risk: Seizure indicators present. Take prescribed medication if available.",
    "Critical alert: Seizure may be imminent. Lie down in safe area.",
    "Emergency: Seizure risk confirmed. Call emergency services if needed."
]

NORMAL_EEG_MESSAGES = [
    "Your brain activity looks stable.",
    "No seizure indicators present at the moment.",
    "EEG patterns appear normal and healthy.",
    "Brain activity is within safe parameters.",
    "No seizure risk detected in current readings.",
    "Your neurological activity is stable.",
    "EEG shows normal brain wave patterns.",
    "No concerning brain activity detected.",
    "Brain function appears to be normal.",
    "Seizure risk assessment: Low probability."
]

# Global variables for model and scaler
model = None
scaler = None
MODEL_PATH = None
SCALER_PATH = None

def _resolve_model_paths():
    """Resolve absolute filesystem paths for model and scaler."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    default_model = os.path.join(base_dir, 'models', 'best_mlp_model.joblib')
    default_scaler = os.path.join(base_dir, 'models', 'mlp_scaler.joblib')
    model_path = os.environ.get('MODEL_PATH', default_model)
    scaler_path = os.environ.get('SCALER_PATH', default_scaler)
    return model_path, scaler_path

def load_model():
    """Load the trained ML model and scaler from joblib files."""
    global model, scaler, MODEL_PATH, SCALER_PATH

    try:
        model_path, scaler_path = _resolve_model_paths()
        MODEL_PATH, SCALER_PATH = model_path, scaler_path

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            return True
        else:
            print(f"Model files not found. Expected: {model_path}, {scaler_path}")
            return False
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False

@predict_bp.route('/predict/model/status', methods=['GET'])
def model_status():
    """Return model loading status and file information for diagnostics."""
    model_path, scaler_path = _resolve_model_paths()
    model_exists = os.path.exists(model_path)
    scaler_exists = os.path.exists(scaler_path)
    return jsonify({
        "loaded": model is not None and scaler is not None,
        "model_path": model_path,
        "scaler_path": scaler_path,
        "model_exists": model_exists,
        "scaler_exists": scaler_exists,
        "model_mtime": os.path.getmtime(model_path) if model_exists else None,
        "scaler_mtime": os.path.getmtime(scaler_path) if scaler_exists else None
    })

@predict_bp.route('/predict', methods=['POST'])
def predict_seizure():
    """
    Predict seizure risk based on EEG features.
    
    Expected input:
    {
        "features": [115 float values representing EEG features]
    }
    
    Returns:
    {
        "status": "High seizure risk" or "Normal EEG pattern",
        "confidence": float (0.0-1.0),
        "message": "Natural language prediction message"
    }
    """
    
    # Load model if not already loaded
    if model is None or scaler is None:
        if not load_model():
            return jsonify({
                "error": "Model not available",
                "message": "ML model files could not be loaded"
            }), 500
    
    try:
        # Attempt to extract features from either a file upload or JSON body
        features = None

        # 1) Multipart/form-data with a file
        if 'file' in request.files:
            uploaded_file = request.files['file']
            try:
                raw_text = uploaded_file.read().decode('utf-8', errors='ignore')
            except Exception:
                return jsonify({
                    "error": "Invalid file encoding",
                    "message": "Could not decode uploaded file as UTF-8"
                }), 400

            # Try JSON array first
            parsed = None
            try:
                parsed_json = json.loads(raw_text)
                if isinstance(parsed_json, list):
                    parsed = parsed_json
            except Exception:
                parsed = None

            if parsed is None:
                # Fallback: parse as CSV/whitespace separated numbers
                tokens = re.split(r'[\s,;]+', raw_text.strip()) if raw_text.strip() else []
                try:
                    parsed = [float(t) for t in tokens if t != '']
                except ValueError:
                    return jsonify({
                        "error": "Invalid file content",
                        "message": "File must contain 115 numeric values (CSV, whitespace, or JSON array)"
                    }), 400

            features = parsed

        else:
            # 2) JSON body { "features": [...] }
            data = request.get_json(silent=True)
            if data and 'features' in data:
                features = data['features']
            else:
                return jsonify({
                    "error": "Invalid input",
                    "message": "Provide 'features' JSON array or upload a file under field name 'file'"
                }), 400
        
        # Validate input
        if not isinstance(features, list) or len(features) != 115:
            return jsonify({
                "error": "Invalid features",
                "message": "Features must be an array of exactly 115 float values"
            }), 400
        
        # Convert to numpy array and reshape
        features_array = np.array(features, dtype=float).reshape(1, -1)
        
        # Scale features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        confidence = model.predict_proba(features_scaled)[0].max()
        
        # Generate response
        if prediction == 1:  # Seizure risk detected
            status = "High seizure risk"
            message = random.choice(SEIZURE_RISK_MESSAGES)
        else:  # Normal EEG
            status = "Normal EEG pattern"
            message = random.choice(NORMAL_EEG_MESSAGES)
        
        return jsonify({
            "status": status,
            "confidence": float(confidence),
            "message": message,
            "prediction": int(prediction)
        })
        
    except ValueError as e:
        return jsonify({
            "error": "Invalid data format",
            "message": "Features must contain valid numeric values"
        }), 400
        
    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "message": f"An error occurred during prediction: {str(e)}"
        }), 500

# Load model on module import
load_model() 