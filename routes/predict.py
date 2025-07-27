"""
Prediction endpoint for seizure risk assessment.
Handles ML model loading, feature scaling, and prediction with natural language responses.
"""

from flask import Blueprint, request, jsonify
import joblib
import numpy as np
import random
import os

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

def load_model():
    """Load the trained ML model and scaler from joblib files."""
    global model, scaler
    
    try:
        model_path = os.path.join('models', 'best_mlp_model.joblib')
        scaler_path = os.path.join('models', 'mlp_scaler.joblib')
        
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
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({
                "error": "Invalid input",
                "message": "Please provide 'features' array with 115 EEG values"
            }), 400
        
        features = data['features']
        
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