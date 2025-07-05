#!/usr/bin/env python3
"""
Simple startup script for the Sustainable Travel Route Finder application.
"""

import os
import sys
from app import create_app
from config import DevelopmentConfig

def main():
    """Main function to run the application."""
    try:
        # Create the Flask application
        app = create_app(DevelopmentConfig)
        
        # Get port from environment or use default
        port = int(os.environ.get('PORT', 5000))
        
        # Get debug mode from environment
        debug = os.environ.get('FLASK_ENV') == 'development'
        
        print(f"🚀 Starting Sustainable Travel Route Finder...")
        print(f"📍 Server will be available at: http://localhost:{port}")
        print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
        print(f"🌱 Environment: {os.environ.get('FLASK_ENV', 'development')}")
        print(f"🔑 API Key configured: {'Yes' if app.config.get('ORS_API_KEY') else 'No'}")
        print("\n" + "="*50)
        print("Press Ctrl+C to stop the server")
        print("="*50 + "\n")
        
        # Run the application
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            use_reloader=debug
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 