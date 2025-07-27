"""
Main Flask application for Seizure Prediction Web App
A patient-centered web application for predicting seizures using ML models.
"""

from flask import Flask
from flask_cors import CORS
import os

# Import blueprints
from routes.predict import predict_bp
from routes.appointments import appointments_bp
from routes.medication import medication_bp
from routes.progress import progress_bp

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Enable CORS for frontend integration
    CORS(app)
    
    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # Register blueprints
    app.register_blueprint(predict_bp, url_prefix='/api')
    app.register_blueprint(appointments_bp, url_prefix='/api')
    app.register_blueprint(medication_bp, url_prefix='/api')
    app.register_blueprint(progress_bp, url_prefix='/api')
    
    @app.route('/')
    def health_check():
        """Health check endpoint for deployment verification."""
        return {
            "status": "healthy",
            "message": "Seizure Prediction API is running",
            "version": "1.0.0"
        }
    
    @app.route('/api/health')
    def api_health():
        """API health check endpoint."""
        return {
            "status": "success",
            "message": "API endpoints are available",
            "endpoints": [
                "/api/predict",
                "/api/appointments",
                "/api/medication", 
                "/api/progress"
            ]
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 