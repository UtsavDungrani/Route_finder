# ========================================

# FILE: wsgi.py
"""
WSGI entry point for production deployment.
"""

import os
from app import create_app
from config import config

# Get configuration from environment
config_name = os.environ.get('FLASK_ENV', 'production')
app = create_app(config[config_name])

if __name__ == "__main__":
    app.run()