
# ========================================

# FILE: utils/validators.py
"""
Validation utilities for input validation and data sanitization.
"""

import re
from typing import Any
from utils.exceptions import ValidationError

def validate_location_input(location: str, field_name: str = 'location') -> str:
    """
    Validate location input string.
    
    Args:
        location: Location string to validate
        field_name: Name of the field for error messages
        
    Returns:
        Cleaned location string
        
    Raises:
        ValidationError: If validation fails
    """
    if not location:
        raise ValidationError(f"{field_name.title()} is required")
    
    if not isinstance(location, str):
        raise ValidationError(f"{field_name.title()} must be a string")
    
    # Remove extra whitespace
    location = location.strip()
    
    if len(location) < 2:
        raise ValidationError(f"{field_name.title()} must be at least 2 characters long")
    
    if len(location) > 200:
        raise ValidationError(f"{field_name.title()} must be less than 200 characters")
    
    # Check for potentially harmful characters
    if re.search(r'[<>"\']', location):
        raise ValidationError(f"{field_name.title()} contains invalid characters")
    
    # Check for SQL injection patterns (basic)
    suspicious_patterns = [
        r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|SCRIPT)\b',
        r'[;\'"]',
        r'--',
        r'/\*',
        r'\*/'
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, location, re.IGNORECASE):
            raise ValidationError(f"{field_name.title()} contains invalid content")
    
    return location

def validate_coordinates(lat: float, lon: float) -> tuple:
    """
    Validate latitude and longitude coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        Tuple of validated coordinates
        
    Raises:
        ValidationError: If coordinates are invalid
    """
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        raise ValidationError("Coordinates must be numeric")
    
    if not (-90 <= lat <= 90):
        raise ValidationError("Latitude must be between -90 and 90")
    
    if not (-180 <= lon <= 180):
        raise ValidationError("Longitude must be between -180 and 180")
    
    return float(lat), float(lon)

def validate_transport_mode(mode: str) -> str:
    """
    Validate transport mode.
    
    Args:
        mode: Transport mode string
        
    Returns:
        Validated mode string
        
    Raises:
        ValidationError: If mode is invalid
    """
    valid_modes = ['driving', 'transit', 'bicycling', 'walking']
    
    if not mode or mode not in valid_modes:
        raise ValidationError(f"Invalid transport mode. Must be one of: {', '.join(valid_modes)}")
    
    return mode

def sanitize_string(value: str, max_length: int = 255) -> str:
    """
    Sanitize string input by removing potentially harmful content.
    
    Args:
        value: String to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return str(value)
    
    # Remove HTML tags
    value = re.sub(r'<[^>]+>', '', value)
    
    # Remove extra whitespace
    value = re.sub(r'\s+', ' ', value).strip()
    
    # Truncate if too long
    if len(value) > max_length:
        value = value[:max_length]
    
    return value