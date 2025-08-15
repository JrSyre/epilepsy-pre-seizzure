"""
Main Flask application for Seizure Prediction Web App
A patient-centered web application for predicting seizures using ML models.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Import blueprints
from routes.predict import predict_bp
from routes.appointments import appointments_bp
from routes.medication import medication_bp
from routes.progress import progress_bp
from frontend import frontend_bp

# Top-level app for static HTML and assets
app = Flask(__name__, static_folder='frontend-ui/assets')

# Serve static HTML pages
@app.route('/')
def serve_index():
    return send_from_directory('frontend-ui', 'index.html')

@app.route('/predict')
def serve_predict():
    return send_from_directory('frontend-ui', 'predict.html')

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

# Factory for API endpoints and blueprints

def create_app():
    api_app = app  # Use the top-level app for both static and API
    CORS(api_app)
    api_app.config['JSON_SORT_KEYS'] = False
    api_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    # Register API blueprints
    api_app.register_blueprint(predict_bp, url_prefix='/api')
    api_app.register_blueprint(appointments_bp, url_prefix='/api')
    api_app.register_blueprint(medication_bp, url_prefix='/api')
    api_app.register_blueprint(progress_bp, url_prefix='/api')
    api_app.register_blueprint(frontend_bp)
    # Health check endpoints
    @api_app.route('/api/health')
    def api_health():
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
    return api_app

# Print all registered routes for debugging
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 