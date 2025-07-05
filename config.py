# ========================================

# FILE: config.py
"""
Configuration module for the Flask application.
Handles environment variables and application settings.
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # API Keys
    ORS_API_KEY = os.environ.get('ORS_API_KEY') or '5b3ce3597851110001cf62485ebda0a63ac84eec83b45932b9626273'
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Rate limiting
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '100 per hour')
    
    # Cache settings
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', '300'))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def get_emission_rates() -> Dict[str, float]:
        """Get CO2 emission rates per km for different transport modes."""
        return {
            'driving': float(os.environ.get('EMISSION_RATE_DRIVING', '0.120')),
            'transit': float(os.environ.get('EMISSION_RATE_TRANSIT', '0.068')),
            'bicycling': float(os.environ.get('EMISSION_RATE_BICYCLING', '0.0')),
            'walking': float(os.environ.get('EMISSION_RATE_WALKING', '0.0'))
        }
    
    @staticmethod
    def get_supported_modes() -> Dict[str, str]:
        """Get mapping of OpenRouteService modes to display names."""
        return {
            'driving-car': 'driving',
            'cycling-regular': 'bicycling',
            'foot-walking': 'walking'
        }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Override with more secure defaults for production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    def __init__(self):
        super().__init__()
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable must be set in production")

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    
    # Use mock API key for testing
    ORS_API_KEY = 'test-api-key'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}