# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8+
- pip package manager

## Installation Steps

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add ML model files** (optional for testing)
   - Place `best_mlp_model.joblib` in `models/` directory
   - Place `mlp_scaler.joblib` in `models/` directory
   - If you don't have these files, the prediction endpoint will return an error but other endpoints will work

3. **Run the Flask application**
   ```bash
   python app.py
   ```

4. **Test the API**
   ```bash
   python test_api.py
   ```

## Quick Test with curl

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Book an Appointment
```bash
curl -X POST http://localhost:5000/api/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "patient": "John Doe",
    "doctor": "Dr. Smith", 
    "date": "2024-01-15",
    "time": "14:30"
  }'
```

### Schedule Medication
```bash
curl -X POST http://localhost:5000/api/medication \
  -H "Content-Type: application/json" \
  -d '{
    "patient": "John Doe",
    "drug_name": "Levetiracetam",
    "times": ["08:00", "20:00"],
    "dosage": "500mg"
  }'
```

### Log Seizure Progress
```bash
curl -X POST http://localhost:5000/api/progress \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-01-10",
    "occurred": 0,
    "patient": "John Doe",
    "notes": "No seizures today"
  }'
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/api/health` | API status |
| POST | `/api/predict` | Seizure prediction |
| POST | `/api/appointments` | Book appointment |
| GET | `/api/appointments` | Get appointments |
| POST | `/api/medication` | Schedule medication |
| GET | `/api/medication` | Get medications |
| POST | `/api/progress` | Log seizure |
| GET | `/api/progress` | Get progress summary |

## Troubleshooting

### Connection Error
- Make sure Flask app is running: `python app.py`
- Check if port 5000 is available

### Model Loading Error
- Ensure `best_mlp_model.joblib` and `mlp_scaler.joblib` are in `models/` directory
- Check file permissions

### Import Errors
- Install all dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

## Next Steps

1. Test all endpoints with the provided test script
2. Add your ML model files for full functionality
3. Deploy to production (Render.com recommended)
4. Build the frontend (Phase 2) 