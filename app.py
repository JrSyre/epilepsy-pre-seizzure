"""
Main Flask application for Seizure Prediction Web App
A patient-centered web application for predicting seizures using ML models.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Import configuration
from config import config

# Import database
from models.database import init_db

# Import blueprints
from routes.predict import predict_bp
from routes.appointments import appointments_bp
from routes.medication import medication_bp
from routes.progress import progress_bp
from routes.payments import payments_bp

def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__, static_folder='frontend-ui/assets')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(predict_bp, url_prefix='/api')
    app.register_blueprint(appointments_bp, url_prefix='/api')
    app.register_blueprint(medication_bp, url_prefix='/api')
    app.register_blueprint(progress_bp, url_prefix='/api')
    app.register_blueprint(payments_bp, url_prefix='/api')
    
    return app

# Create app instance
app = create_app()

# Health check endpoints
@app.route('/api/health')
def api_health():
    return {
        "status": "success",
        "message": "API endpoints are available",
        "endpoints": [
            "/api/predict",
            "/api/appointments",
            "/api/medication",
            "/api/progress",
            "/api/payments/config",
            "/api/payments/create-intent"
        ]
    }

# Serve static HTML pages
@app.route('/')
def serve_index():
    return send_from_directory('frontend-ui', 'index.html')

@app.route('/appointments')
def serve_appointments():
    return send_from_directory('frontend-ui', 'appointments.html')

@app.route('/medication')
def serve_medication():
    return send_from_directory('frontend-ui', 'medication.html')

@app.route('/progress')
def serve_progress():
    return send_from_directory('frontend-ui', 'progress.html')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('frontend-ui/assets', filename)

# Redirect .html URLs to the correct route (optional, for user convenience)
@app.route('/<page>.html')
def redirect_html(page):
    from flask import redirect
    if page in ['index', 'predict', 'appointments', 'medication', 'progress']:
        return redirect('/' if page == 'index' else f'/{page}')
    return '', 404

# Handle /predict route to serve the predict page
@app.route('/predict')
def serve_predict():
    return send_from_directory('frontend-ui', 'predict.html')

# Print all registered routes for debugging
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(debug=True) 