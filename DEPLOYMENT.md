# Deployment Guide for Render

This guide explains how to deploy the Seizure Prediction Web App to Render.

## Prerequisites

- A Render account (free tier available)
- Your GitHub repository connected to Render
- ML model files in the `models/` directory

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository contains:
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render configuration (optional)
- `Procfile` - Web server configuration
- `models/best_mlp_model.joblib` - Trained ML model
- `models/mlp_scaler.joblib` - Feature scaler

### 2. Connect to Render

1. Go to [render.com](https://render.com)
2. Sign up/Login with your GitHub account
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository

### 3. Configure the Service

**Service Settings:**
- **Name**: `seizure-prediction-app` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `master` (or your main branch)
- **Root Directory**: Leave empty (if app is in root)

**Build & Deploy Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

**Environment Variables:**
- `FLASK_ENV`: `production`
- `FLASK_DEBUG`: `false`
- `PYTHON_VERSION`: `3.9.16`

### 4. Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your app
3. Monitor the build logs for any issues
4. Once deployed, you'll get a URL like: `https://your-app-name.onrender.com`

## Health Check

The app includes a health check endpoint at `/api/health` that Render can use to verify the service is running.

## Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check that `requirements.txt` is in the root directory
   - Ensure all dependencies are listed
   - Verify Python version compatibility

2. **Model Loading Errors**
   - Ensure model files are in the `models/` directory
   - Check file permissions
   - Verify model file names match the code

3. **Port Issues**
   - Render automatically sets the `PORT` environment variable
   - The app uses `gunicorn` to bind to `0.0.0.0:$PORT`

4. **Memory Issues**
   - Free tier has memory limits
   - Consider upgrading if you experience timeouts

### Debugging:

1. Check build logs in Render dashboard
2. Monitor application logs
3. Test endpoints using the provided URL
4. Verify environment variables are set correctly

## Production Considerations

1. **Security**: Ensure `FLASK_DEBUG=false` in production
2. **Performance**: Consider upgrading from free tier for better performance
3. **Monitoring**: Set up logging and monitoring
4. **Backup**: Regularly backup your model files and data

## API Endpoints

Once deployed, your API will be available at:
- Health Check: `https://your-app.onrender.com/api/health`
- Prediction: `https://your-app.onrender.com/api/predict`
- Appointments: `https://your-app.onrender.com/api/appointments`
- Medication: `https://your-app.onrender.com/api/medication`
- Progress: `https://your-app.onrender.com/api/progress`

## Frontend Integration

The frontend is served by the same Flask app and will be available at:
- Home: `https://your-app.onrender.com/`
- Predict: `https://your-app.onrender.com/predict`
- Appointments: `https://your-app.onrender.com/appointments`
- Medication: `https://your-app.onrender.com/medication`
- Progress: `https://your-app.onrender.com/progress`
