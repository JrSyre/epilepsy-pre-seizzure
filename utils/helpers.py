"""
Helper utility functions for the Seizure Prediction API.
Provides common validation and utility functions used across endpoints.
"""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional

def validate_date_format(date_str: str) -> bool:
    """
    Validate if a date string is in YYYY-MM-DD format.
    
    Args:
        date_str: Date string to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_time_format(time_str: str) -> bool:
    """
    Validate if a time string is in HH:MM format (24-hour).
    
    Args:
        time_str: Time string to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def validate_patient_name(name: str) -> bool:
    """
    Validate patient name format.
    
    Args:
        name: Patient name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not name or not name.strip():
        return False
    
    # Allow letters, spaces, hyphens, and apostrophes
    pattern = r'^[a-zA-Z\s\-\']+$'
    return bool(re.match(pattern, name.strip()))

def validate_medication_name(name: str) -> bool:
    """
    Validate medication name format.
    
    Args:
        name: Medication name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not name or not name.strip():
        return False
    
    # Allow letters, numbers, spaces, hyphens, and parentheses
    pattern = r'^[a-zA-Z0-9\s\-\()]+$'
    return bool(re.match(pattern, name.strip()))

def generate_error_response(message: str, error_type: str = "validation_error") -> Dict[str, Any]:
    """
    Generate a standardized error response.
    
    Args:
        message: Error message
        error_type: Type of error
        
    Returns:
        dict: Standardized error response
    """
    return {
        "error": error_type,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

def generate_success_response(data: Dict[str, Any], message: str = "Operation completed successfully") -> Dict[str, Any]:
    """
    Generate a standardized success response.
    
    Args:
        data: Response data
        message: Success message
        
    Returns:
        dict: Standardized success response
    """
    return {
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Input text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', text.strip())
    return sanitized

def format_datetime_for_display(dt: datetime) -> str:
    """
    Format datetime for user-friendly display.
    
    Args:
        dt: Datetime object
        
    Returns:
        str: Formatted datetime string
    """
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def calculate_age_from_date(birth_date: str) -> Optional[int]:
    """
    Calculate age from birth date.
    
    Args:
        birth_date: Birth date in YYYY-MM-DD format
        
    Returns:
        int: Age in years, or None if invalid date
    """
    try:
        birth_dt = datetime.strptime(birth_date, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_dt.year
        
        # Adjust if birthday hasn't occurred this year
        if today.month < birth_dt.month or (today.month == birth_dt.month and today.day < birth_dt.day):
            age -= 1
            
        return age
    except ValueError:
        return None

def validate_eeg_features(features: List[float]) -> bool:
    """
    Validate EEG feature array.
    
    Args:
        features: List of EEG feature values
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(features, list):
        return False
    
    if len(features) != 115:
        return False
    
    # Check if all values are numeric
    try:
        for feature in features:
            float(feature)
        return True
    except (ValueError, TypeError):
        return False

def normalize_feature_values(features: List[float]) -> List[float]:
    """
    Normalize feature values to prevent extreme outliers.
    
    Args:
        features: List of feature values
        
    Returns:
        List[float]: Normalized feature values
    """
    if not features:
        return []
    
    # Simple min-max normalization to [0, 1] range
    min_val = min(features)
    max_val = max(features)
    
    if max_val == min_val:
        return [0.5] * len(features)
    
    normalized = [(x - min_val) / (max_val - min_val) for x in features]
    return normalized 