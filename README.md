# 🧠 Seizure Prediction Web App - Backend API

A patient-centered Flask backend for predicting seizures using machine learning models. This API provides endpoints for seizure prediction, appointment management, medication scheduling, and progress tracking.

## 🚀 Features

- **Seizure Prediction**: ML-powered EEG analysis with natural language responses
- **Appointment Management**: Book and manage doctor appointments
- **Medication Scheduling**: Set up medication reminders and schedules
- **Progress Tracking**: Monitor treatment progress and seizure trends
- **RESTful API**: Clean JSON-based endpoints with comprehensive error handling

## 📁 Project Structure

```
phil/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── routes/               # API route blueprints
│   ├── __init__.py
│   ├── predict.py        # Seizure prediction endpoint
│   ├── appointments.py   # Appointment management
│   ├── medication.py     # Medication scheduling
│   └── progress.py       # Progress tracking
├── models/               # ML model files
│   ├── __init__.py
│   ├── README.md         # Model documentation
│   ├── best_mlp_model.joblib    # Trained ML model (required)
│   └── mlp_scaler.joblib        # Feature scaler (required)
└── utils/                # Helper utilities
    ├── __init__.py
    └── helpers.py        # Common utility functions
```

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd phil
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add ML model files**
   - Place your trained `best_mlp_model.joblib` in the `models/` directory
   - Place your `mlp_scaler.joblib` in the `models/` directory
   - See `models/README.md` for model requirements

4. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## 🔗 API Endpoints

### Health Check
- **GET** `/` - Application health status
- **GET** `/api/health` - API health check

### Seizure Prediction
- **POST** `/api/predict` - Predict seizure risk from EEG features

**Request:**
```json
{
  "features": [0.1, 0.2, 0.3, ...] // 115 EEG feature values
}
```

**Response:**
```json
{
  "status": "High seizure risk",
  "confidence": 0.9123,
  "message": "Warning: Seizure may occur soon. Stay safe and alert.",
  "prediction": 1
}
```

### Appointments
- **POST** `/api/appointments` - Book new appointment
- **GET** `/api/appointments` - Get all appointments
- **PUT** `/api/appointments/{id}` - Update appointment status

**Book Appointment:**
```json
{
  "patient": "John Doe",
  "doctor": "Dr. Smith",
  "date": "2024-01-15",
  "time": "14:30"
}
```

### Medication
- **POST** `/api/medication` - Schedule medication
- **GET** `/api/medication` - Get medication schedules
- **PUT** `/api/medication/{id}` - Update medication
- **DELETE** `/api/medication/{id}` - Delete medication

**Schedule Medication:**
```json
{
  "patient": "John Doe",
  "drug_name": "Levetiracetam",
  "times": ["08:00", "20:00"],
  "dosage": "500mg",
  "instructions": "Take with food"
}
```

### Progress Tracking
- **POST** `/api/progress` - Log seizure occurrence
- **GET** `/api/progress` - Get treatment progress summary
- **PUT** `/api/progress/{id}` - Update seizure log
- **DELETE** `/api/progress/{id}` - Delete seizure log

**Log Seizure:**
```json
{
  "date": "2024-01-10",
  "occurred": 1,
  "patient": "John Doe",
  "notes": "Seizure occurred in the morning"
}
```

## 🧪 Testing the API

### Using curl

1. **Health Check**
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Seizure Prediction**
   ```bash
   curl -X POST http://localhost:5000/api/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [0.1, 0.2, 0.3, ...]}'
   ```

3. **Book Appointment**
   ```bash
   curl -X POST http://localhost:5000/api/appointments \
     -H "Content-Type: application/json" \
     -d '{"patient": "John Doe", "doctor": "Dr. Smith", "date": "2024-01-15", "time": "14:30"}'
   ```

### Using Postman

1. Import the API endpoints into Postman
2. Set base URL to `http://localhost:5000`
3. Use the JSON examples above for request bodies

## 🔧 Configuration

### Environment Variables

Create a `.env` file for environment-specific configuration:

```env
FLASK_ENV=development
PORT=5000
DEBUG=True
```

### Production Deployment

For production deployment on Render.com:

1. **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Command:**
   ```bash
   gunicorn app:create_app()
   ```

3. **Environment Variables:**
   - `PORT`: Set by Render
   - `FLASK_ENV`: production

## 📊 ML Model Requirements

The API expects the following ML model setup:

- **Input**: 115 EEG feature values (float array)
- **Output**: Binary classification (0 = no seizure, 1 = seizure risk)
- **Format**: joblib serialized files
- **Files**: `best_mlp_model.joblib` and `mlp_scaler.joblib`

## 🚨 Error Handling

All endpoints return standardized error responses:

```json
{
  "error": "error_type",
  "message": "Human-readable error message",
  "timestamp": "2024-01-10T10:30:00Z"
}
```

Common HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

## 🔒 Security Considerations

- Input validation on all endpoints
- SQL injection prevention (when using database)
- CORS enabled for frontend integration
- Input sanitization for user-provided data

## 📝 Development

### Adding New Endpoints

1. Create a new blueprint in `routes/`
2. Register the blueprint in `app.py`
3. Add comprehensive error handling
4. Update this README with endpoint documentation

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions
- Use type hints where appropriate
- Include comprehensive error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support or questions:
- Check the API documentation
- Review error messages in the response
- Ensure ML model files are properly placed
- Verify all dependencies are installed

---

**Note**: This is Phase 1 (Backend) of the Seizure Prediction Web App. The frontend will be built in Phase 2. 