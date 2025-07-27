#!/usr/bin/env python3
"""
Test script for the Seizure Prediction API.
Tests all endpoints with sample data to verify functionality.
"""

import requests
import json
import random
import time
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_endpoints():
    """Test health check endpoints."""
    print("🔍 Testing health endpoints...")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    
    # Test API health endpoint
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"API health endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    
    print()

def test_prediction_endpoint():
    """Test seizure prediction endpoint."""
    print("🧠 Testing prediction endpoint...")
    
    # Generate random EEG features (115 values)
    features = [random.uniform(0, 1) for _ in range(115)]
    
    data = {
        "features": features
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/predict",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Prediction endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {result.get('status')}")
            print(f"Confidence: {result.get('confidence')}")
            print(f"Message: {result.get('message')}")
        else:
            print(f"Error: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the Flask app is running")
    
    print()

def test_appointments_endpoints():
    """Test appointment management endpoints."""
    print("📅 Testing appointment endpoints...")
    
    # Test booking appointment
    appointment_data = {
        "patient": "John Doe",
        "doctor": "Dr. Smith",
        "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "time": "14:30"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/appointments",
            json=appointment_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Book appointment: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            appointment_id = result.get('appointment_id')
            print(f"Appointment ID: {appointment_id}")
            
            # Test getting appointments
            response = requests.get(f"{BASE_URL}/api/appointments")
            print(f"Get appointments: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Total appointments: {result.get('total')}")
        else:
            print(f"Error: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the Flask app is running")
    
    print()

def test_medication_endpoints():
    """Test medication scheduling endpoints."""
    print("💊 Testing medication endpoints...")
    
    # Test scheduling medication
    medication_data = {
        "patient": "John Doe",
        "drug_name": "Levetiracetam",
        "times": ["08:00", "20:00"],
        "dosage": "500mg",
        "instructions": "Take with food"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/medication",
            json=medication_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Schedule medication: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            medication_id = result.get('medication_id')
            print(f"Medication ID: {medication_id}")
            
            # Test getting medications
            response = requests.get(f"{BASE_URL}/api/medication")
            print(f"Get medications: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Total medications: {result.get('total')}")
        else:
            print(f"Error: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the Flask app is running")
    
    print()

def test_progress_endpoints():
    """Test progress tracking endpoints."""
    print("📊 Testing progress endpoints...")
    
    # Test logging seizure
    progress_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "occurred": 0,
        "patient": "John Doe",
        "notes": "No seizures today"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/progress",
            json=progress_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Log seizure: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            log_id = result.get('log_id')
            print(f"Log ID: {log_id}")
            
            # Test getting progress
            response = requests.get(f"{BASE_URL}/api/progress")
            print(f"Get progress: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                summary = result.get('summary', {})
                print(f"Total seizures: {summary.get('total_seizures')}")
                print(f"Progress: {summary.get('progress')}")
        else:
            print(f"Error: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the Flask app is running")
    
    print()

def main():
    """Run all API tests."""
    print("🧪 Starting API Tests...")
    print("=" * 50)
    
    # Wait a moment for the server to start
    time.sleep(1)
    
    test_health_endpoints()
    test_prediction_endpoint()
    test_appointments_endpoints()
    test_medication_endpoints()
    test_progress_endpoints()
    
    print("✅ API tests completed!")
    print("\n📝 Note: Some tests may fail if the ML model files are not present.")
    print("   Place your 'best_mlp_model.joblib' and 'mlp_scaler.joblib' files")
    print("   in the 'models/' directory for full functionality.")

if __name__ == "__main__":
    main() 