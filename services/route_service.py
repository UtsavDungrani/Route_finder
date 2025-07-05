# ========================================

# FILE: services/route_service.py
"""
Route service for handling route calculations and geocoding.
Provides a clean interface for the OpenRouteService API.
"""

import logging
from typing import List, Dict, Tuple, Optional
import openrouteservice
from openrouteservice.exceptions import ApiError
from config import Config
from utils.exceptions import RouteFinderException, GeocodingError

logger = logging.getLogger(__name__)

class RouteService:
    """Service for handling route calculations and geocoding."""
    
    def __init__(self, api_key: str):
        """Initialize the route service with API key."""
        self.api_key = api_key
        self.client = openrouteservice.Client(key=api_key)
        self.supported_modes = Config.get_supported_modes()
    
    def geocode_location(self, location: str) -> Tuple[float, float]:
        """
        Geocode a location string to coordinates.
        
        Args:
            location: Location string to geocode
            
        Returns:
            Tuple of (longitude, latitude)
            
        Raises:
            GeocodingError: If geocoding fails
        """
        try:
            logger.info(f"Geocoding location: {location}")
            result = self.client.pelias_search(text=location, size=1)
            
            if not result.get('features'):
                raise GeocodingError(f"Location not found: {location}")
            
            coordinates = result['features'][0]['geometry']['coordinates']
            return tuple(coordinates)
            
        except ApiError as e:
            logger.error(f"API error during geocoding: {e}")
            raise GeocodingError(f"Failed to geocode location: {location}")
        except Exception as e:
            logger.error(f"Unexpected error during geocoding: {e}")
            raise GeocodingError(f"Geocoding service unavailable")
    
    def get_route_for_mode(self, origin_coords: Tuple[float, float], 
                          destination_coords: Tuple[float, float], 
                          ors_mode: str, mode_name: str) -> Optional[Dict]:
        """
        Get route information for a specific transport mode.
        
        Args:
            origin_coords: Origin coordinates (longitude, latitude)
            destination_coords: Destination coordinates (longitude, latitude)
            ors_mode: OpenRouteService mode string
            mode_name: Display name for the mode
            
        Returns:
            Dictionary with route information or None if route not found
        """
        try:
            logger.info(f"Getting route for mode: {mode_name}")
            
            route = self.client.directions(
                coordinates=(origin_coords, destination_coords),
                profile=ors_mode,
                format='geojson'
            )
            
            if not route.get('features'):
                logger.warning(f"No route found for mode: {mode_name}")
                return None
            
            feature = route['features'][0]
            properties = feature['properties']
            
            # Extract route information
            distance_meters = properties['segments'][0]['distance']
            distance_km = round(distance_meters / 1000, 2)
            duration_seconds = properties['segments'][0]['duration']
            
            # Convert geometry from [lon, lat] to [lat, lon] for Leaflet
            geometry = feature['geometry']['coordinates']
            geometry_latlon = [[coord[1], coord[0]] for coord in geometry]
            
            return {
                'mode': mode_name,
                'distance': distance_km,
                'duration': duration_seconds,
                'duration_formatted': self._format_duration(duration_seconds),
                'geometry': geometry_latlon
            }
            
        except ApiError as e:
            logger.warning(f"API error for mode {mode_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for mode {mode_name}: {e}")
            return None
    
    def get_routes(self, origin: str, destination: str) -> List[Dict]:
        """
        Get all available routes between origin and destination.
        
        Args:
            origin: Origin location string
            destination: Destination location string
            
        Returns:
            List of route dictionaries
            
        Raises:
            RouteFinderException: If no routes can be found
        """
        try:
            # Geocode locations
            origin_coords = self.geocode_location(origin)
            destination_coords = self.geocode_location(destination)
            
            logger.info(f"Finding routes from {origin} to {destination}")
            
            routes = []
            
            # Get routes for each supported mode
            for ors_mode, mode_name in self.supported_modes.items():
                route = self.get_route_for_mode(
                    origin_coords, destination_coords, ors_mode, mode_name
                )
                if route:
                    routes.append(route)
            
            if not routes:
                raise RouteFinderException(
                    f"No routes found between {origin} and {destination}. "
                    "Please check the locations and try again."
                )
            
            logger.info(f"Found {len(routes)} routes")
            return routes
            
        except GeocodingError:
            # Re-raise geocoding errors as-is
            raise
        except RouteFinderException:
            # Re-raise route finder errors as-is
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting routes: {e}")
            raise RouteFinderException("Service temporarily unavailable. Please try again later.")
    
    def _format_duration(self, seconds: int) -> str:
        """Format duration in seconds to human-readable string."""
        if seconds < 60:
            return f"{seconds} seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes == 0:
                return f"{hours} hour{'s' if hours != 1 else ''}"
            else:
                return f"{hours}h {minutes}m"