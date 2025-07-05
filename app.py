# FILE: app.py
"""
Sustainable Travel Route Finder
A Flask web application for finding eco-friendly travel routes with emissions calculation.
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.exceptions import BadRequest
from config import DevelopmentConfig
from services.route_service import RouteService
from services.emissions_service import EmissionsService
from utils.validators import validate_location_input
from utils.exceptions import RouteFinderException, ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_class=DevelopmentConfig):
    """Application factory pattern for creating Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize services
    route_service = RouteService(app.config['ORS_API_KEY'])
    emissions_service = EmissionsService()
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(RouteFinderException)
    def handle_route_finder_exception(error):
        logger.warning(f"Route finder exception: {error}")
        return render_template('error.html', error=str(error)), 400
    
    @app.route('/')
    def home():
        """Render the home page with route finder form."""
        return render_template('index.html')
    
    @app.route('/api/routes', methods=['POST'])
    def api_routes():
        """API endpoint for getting route data as JSON."""
        try:
            data = request.get_json()
            if not data:
                raise BadRequest("No JSON data provided")
            
            origin = data.get('origin', '').strip()
            destination = data.get('destination', '').strip()
            
            # Validate inputs
            validate_location_input(origin, 'origin')
            validate_location_input(destination, 'destination')
            
            # Get routes and calculate emissions
            routes = route_service.get_routes(origin, destination)
            processed_routes = []
            
            for route in routes:
                emission = emissions_service.calculate_emission(
                    route['distance'], route['mode']
                )
                processed_routes.append({
                    **route,
                    'emission': emission,
                    'emission_per_km': round(emission / route['distance'], 3) if route['distance'] > 0 else 0
                })
            
            # Sort by emission (lowest first)
            processed_routes.sort(key=lambda x: x['emission'])
            
            return jsonify({
                'success': True,
                'routes': processed_routes,
                'origin': origin,
                'destination': destination,
                'best_route': processed_routes[0] if processed_routes else None
            })
            
        except ValidationError as e:
            return jsonify({'success': False, 'error': str(e)}), 400
        except RouteFinderException as e:
            return jsonify({'success': False, 'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error in API route: {e}")
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    @app.route('/result', methods=['POST'])
    def result():
        """Handle form submission and display route results."""
        try:
            origin = request.form.get('origin', '').strip()
            destination = request.form.get('destination', '').strip()
            vehicle_type = request.form.get('vehicle_type', '').strip()
            vehicle_model = request.form.get('vehicle_model', '').strip()
            
            # Validate inputs
            validate_location_input(origin, 'origin')
            validate_location_input(destination, 'destination')
            
            # Get routes and calculate emissions
            routes = route_service.get_routes(origin, destination)
            
            if not routes:
                flash('No routes found between the specified locations. Please try different locations.', 'warning')
                return render_template('result.html', 
                                     no_routes=True, 
                                     origin=origin, 
                                     destination=destination)
            
            # Process routes with emissions
            processed_routes = []
            for route in routes:
                # Use vehicle-specific calculation if vehicle is selected
                if vehicle_type and vehicle_model and route['mode'] == 'driving':
                    emission = emissions_service.calculate_vehicle_emission(
                        route['distance'], vehicle_type, vehicle_model
                    )
                    vehicle_info = emissions_service.get_available_vehicles().get(vehicle_type, {}).get(vehicle_model, {})
                    route['vehicle_name'] = vehicle_info.get('name', 'Custom Vehicle')
                    route['vehicle_emission_rate'] = vehicle_info.get('emission_rate', 'Custom rate')
                else:
                    emission = emissions_service.calculate_emission(
                        route['distance'], route['mode']
                    )
                    route['vehicle_name'] = None
                    route['vehicle_emission_rate'] = None
                
                processed_routes.append({
                    **route,
                    'emission': emission,
                    'emission_per_km': round(emission / route['distance'], 3) if route['distance'] > 0 else 0,
                    'origin': origin,
                    'destination': destination,
                    'vehicle_type': vehicle_type,
                    'vehicle_model': vehicle_model
                })
            
            # Sort by emission (lowest first)
            processed_routes.sort(key=lambda x: x['emission'])
            best_route = processed_routes[0]
            
            # Calculate savings compared to driving
            driving_route = next((r for r in processed_routes if r['mode'] == 'driving'), None)
            if driving_route and best_route['mode'] != 'driving':
                savings = driving_route['emission'] - best_route['emission']
                best_route['emission_savings'] = round(savings, 3)
            
            return render_template('result.html',
                                 route=best_route,
                                 all_routes=processed_routes,
                                 origin=origin,
                                 destination=destination,
                                 no_routes=False,
                                 route_geometry=best_route.get('geometry'))
            
        except ValidationError as e:
            flash(str(e), 'error')
            return redirect(url_for('home'))
        except RouteFinderException as e:
            flash(str(e), 'error')
            return redirect(url_for('home'))
        except Exception as e:
            logger.error(f"Unexpected error in result route: {e}")
            flash('An unexpected error occurred. Please try again.', 'error')
            return redirect(url_for('home'))
    
    @app.route('/about')
    def about():
        """Display information about the application."""
        return render_template('about.html')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring."""
        return jsonify({'status': 'healthy', 'version': '1.0.0'})
    
    @app.route('/api/vehicles')
    def api_vehicles():
        """API endpoint for getting vehicle information."""
        try:
            vehicles = emissions_service.get_available_vehicles()
            return jsonify({
                'success': True,
                'vehicles': vehicles
            })
        except Exception as e:
            logger.error(f"Error getting vehicle information: {e}")
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)