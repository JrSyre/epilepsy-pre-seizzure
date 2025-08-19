"""
Database models for Seizure Prediction Web App
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Appointment(db.Model):
    """Appointment model for doctor visits."""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient = db.Column(db.String(100), nullable=False)
    doctor = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert appointment to dictionary."""
        return {
            'id': self.id,
            'patient': self.patient,
            'doctor': self.doctor,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'time': self.time.strftime('%H:%M') if self.time else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Medication(db.Model):
    """Medication model for treatment schedules."""
    __tablename__ = 'medications'
    
    id = db.Column(db.Integer, primary_key=True)
    patient = db.Column(db.String(100), nullable=False)
    drug_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    times = db.Column(db.JSON, nullable=False)  # Store as JSON array
    instructions = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert medication to dictionary."""
        return {
            'id': self.id,
            'patient': self.patient,
            'drug_name': self.drug_name,
            'dosage': self.dosage,
            'times': self.times,
            'instructions': self.instructions,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class SeizureLog(db.Model):
    """Seizure log model for progress tracking."""
    __tablename__ = 'seizure_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    patient = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    occurred = db.Column(db.Boolean, nullable=False)
    notes = db.Column(db.Text)
    severity = db.Column(db.String(20))  # mild, moderate, severe
    duration = db.Column(db.Integer)  # duration in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert seizure log to dictionary."""
        return {
            'id': self.id,
            'patient': self.patient,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'occurred': self.occurred,
            'notes': self.notes,
            'severity': self.severity,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def init_db(app):
    """Initialize database with Flask app."""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
