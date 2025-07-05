# ========================================

# FILE: utils/exceptions.py
"""
Custom exception classes for the route finder application.
"""

class RouteFinderException(Exception):
    """Base exception for route finder errors."""
    pass

class ValidationError(RouteFinderException):
    """Exception raised for input validation errors."""
    pass

class GeocodingError(RouteFinderException):
    """Exception raised for geocoding errors."""
    pass

class RouteCalculationError(RouteFinderException):
    """Exception raised for route calculation errors."""
    pass

class ApiError(RouteFinderException):
    """Exception raised for external API errors."""
    pass

class ConfigurationError(RouteFinderException):
    """Exception raised for configuration errors."""
    pass