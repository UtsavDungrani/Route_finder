# ========================================

# FILE: services/emissions_service.py
"""
Emissions service for calculating CO2 emissions for different transport modes.
Provides detailed emissions analysis and environmental impact calculations.
"""

import logging
from typing import Dict, Optional, Tuple, List
from config import Config

logger = logging.getLogger(__name__)

class EmissionsService:
    """Service for calculating CO2 emissions for different transport modes."""
    
    def __init__(self):
        """Initialize the emissions service with emission rates."""
        self.emission_rates = Config.get_emission_rates()
        self.vehicle_emissions = self._get_vehicle_emission_rates()
        logger.info("Emissions service initialized with rates: %s", self.emission_rates)
    
    def _get_vehicle_emission_rates(self) -> Dict[str, Dict[str, float]]:
        """Get detailed emission rates for different vehicle types."""
        return {
            'car': {
                'gasoline_small': 0.120,      # Small gasoline car
                'gasoline_medium': 0.180,     # Medium gasoline car
                'gasoline_large': 0.250,      # Large gasoline car/SUV
                'diesel_small': 0.140,        # Small diesel car
                'diesel_medium': 0.200,       # Medium diesel car
                'hybrid': 0.080,              # Hybrid vehicle
                'electric': 0.040,            # Electric vehicle (grid average)
                'electric_renewable': 0.010,  # Electric vehicle (renewable energy)
                'average': 0.120              # Average car
            },
            'motorcycle': {
                'small': 0.080,               # Small motorcycle (125cc)
                'medium': 0.120,              # Medium motorcycle (500cc)
                'large': 0.180,               # Large motorcycle (1000cc+)
                'electric': 0.020,            # Electric motorcycle
                'average': 0.120              # Average motorcycle
            },
            'transit': {
                'bus': 0.068,                 # Bus per passenger
                'train': 0.041,               # Train per passenger
                'subway': 0.035,              # Subway per passenger
                'tram': 0.030,                # Tram per passenger
                'average': 0.068              # Average transit
            },
            'truck': {
                'small': 0.200,               # Small delivery truck
                'medium': 0.350,              # Medium truck
                'large': 0.500,               # Large truck
                'average': 0.350              # Average truck
            }
        }
    
    def calculate_emission(self, distance_km: float, mode: str) -> float:
        """
        Calculate CO2 emissions for a given distance and transport mode.
        
        Args:
            distance_km: Distance in kilometers
            mode: Transport mode ('driving', 'transit', 'bicycling', 'walking')
            
        Returns:
            CO2 emissions in kilograms
        """
        if distance_km <= 0:
            return 0.0
        
        emission_rate = self.emission_rates.get(mode, 0.1)  # Default fallback rate
        emission = distance_km * emission_rate
        
        logger.debug(f"Calculated emission for {mode}: {emission:.3f} kg CO2 for {distance_km} km")
        return round(emission, 3)
    
    def calculate_vehicle_emission(self, distance_km: float, vehicle_type: str, vehicle_model: str = 'average') -> float:
        """
        Calculate CO2 emissions for a specific vehicle type and model.
        
        Args:
            distance_km: Distance in kilometers
            vehicle_type: Vehicle type ('car', 'motorcycle', 'transit', 'truck')
            vehicle_model: Specific vehicle model (e.g., 'hybrid', 'electric', 'small')
            
        Returns:
            CO2 emissions in kilograms
        """
        if distance_km <= 0:
            return 0.0
        
        vehicle_rates = self.vehicle_emissions.get(vehicle_type, {})
        emission_rate = vehicle_rates.get(vehicle_model, vehicle_rates.get('average', 0.120))
        emission = distance_km * emission_rate
        
        logger.debug(f"Calculated vehicle emission for {vehicle_type}/{vehicle_model}: {emission:.3f} kg CO2 for {distance_km} km")
        return round(emission, 3)
    
    def get_available_vehicles(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """
        Get all available vehicle options with descriptions.
        
        Returns:
            Dictionary of vehicle types and their models with descriptions
        """
        return {
            'car': {
                'gasoline_small': {
                    'name': 'Small Gasoline Car',
                    'description': 'Compact or subcompact gasoline vehicle',
                    'emission_rate': '0.120 kg CO₂/km',
                    'examples': 'Honda Civic, Toyota Corolla, Ford Focus'
                },
                'gasoline_medium': {
                    'name': 'Medium Gasoline Car',
                    'description': 'Mid-size gasoline sedan or hatchback',
                    'emission_rate': '0.180 kg CO₂/km',
                    'examples': 'Toyota Camry, Honda Accord, Volkswagen Passat'
                },
                'gasoline_large': {
                    'name': 'Large Gasoline Car/SUV',
                    'description': 'Large sedan, SUV, or pickup truck',
                    'emission_rate': '0.250 kg CO₂/km',
                    'examples': 'Ford F-150, Toyota Highlander, Chevrolet Tahoe'
                },
                'diesel_small': {
                    'name': 'Small Diesel Car',
                    'description': 'Compact diesel vehicle',
                    'emission_rate': '0.140 kg CO₂/km',
                    'examples': 'Volkswagen Golf TDI, BMW 320d'
                },
                'diesel_medium': {
                    'name': 'Medium Diesel Car',
                    'description': 'Mid-size diesel vehicle',
                    'emission_rate': '0.200 kg CO₂/km',
                    'examples': 'BMW 520d, Mercedes E220d'
                },
                'hybrid': {
                    'name': 'Hybrid Vehicle',
                    'description': 'Gasoline-electric hybrid',
                    'emission_rate': '0.080 kg CO₂/km',
                    'examples': 'Toyota Prius, Honda Insight, Ford Fusion Hybrid'
                },
                'electric': {
                    'name': 'Electric Vehicle',
                    'description': 'Battery electric vehicle (grid average)',
                    'emission_rate': '0.040 kg CO₂/km',
                    'examples': 'Tesla Model 3, Nissan Leaf, Chevrolet Bolt'
                },
                'electric_renewable': {
                    'name': 'Electric Vehicle (Renewable)',
                    'description': 'Battery electric vehicle with renewable energy',
                    'emission_rate': '0.010 kg CO₂/km',
                    'examples': 'Tesla with solar charging, any EV with green energy'
                }
            },
            'motorcycle': {
                'small': {
                    'name': 'Small Motorcycle',
                    'description': 'Small displacement motorcycle (125cc)',
                    'emission_rate': '0.080 kg CO₂/km',
                    'examples': 'Honda CB125F, Yamaha YBR125'
                },
                'medium': {
                    'name': 'Medium Motorcycle',
                    'description': 'Medium displacement motorcycle (500cc)',
                    'emission_rate': '0.120 kg CO₂/km',
                    'examples': 'Honda CB500F, Kawasaki Ninja 400'
                },
                'large': {
                    'name': 'Large Motorcycle',
                    'description': 'Large displacement motorcycle (1000cc+)',
                    'emission_rate': '0.180 kg CO₂/km',
                    'examples': 'Honda CBR1000RR, Yamaha R1, BMW S1000RR'
                },
                'electric': {
                    'name': 'Electric Motorcycle',
                    'description': 'Battery electric motorcycle',
                    'emission_rate': '0.020 kg CO₂/km',
                    'examples': 'Zero SR/F, Harley-Davidson LiveWire'
                }
            },
            'transit': {
                'bus': {
                    'name': 'Bus',
                    'description': 'Public bus transportation',
                    'emission_rate': '0.068 kg CO₂/km per passenger',
                    'examples': 'City buses, intercity coaches'
                },
                'train': {
                    'name': 'Train',
                    'description': 'Rail transportation',
                    'emission_rate': '0.041 kg CO₂/km per passenger',
                    'examples': 'Commuter trains, intercity rail'
                },
                'subway': {
                    'name': 'Subway/Metro',
                    'description': 'Underground rail transportation',
                    'emission_rate': '0.035 kg CO₂/km per passenger',
                    'examples': 'New York Subway, London Underground'
                },
                'tram': {
                    'name': 'Tram/Light Rail',
                    'description': 'Light rail or streetcar',
                    'emission_rate': '0.030 kg CO₂/km per passenger',
                    'examples': 'Portland Streetcar, San Francisco Muni'
                }
            },
            'truck': {
                'small': {
                    'name': 'Small Truck',
                    'description': 'Small delivery or pickup truck',
                    'emission_rate': '0.200 kg CO₂/km',
                    'examples': 'Ford Ranger, Toyota Tacoma'
                },
                'medium': {
                    'name': 'Medium Truck',
                    'description': 'Medium commercial truck',
                    'emission_rate': '0.350 kg CO₂/km',
                    'examples': 'Ford F-650, Freightliner M2'
                },
                'large': {
                    'name': 'Large Truck',
                    'description': 'Heavy commercial truck',
                    'emission_rate': '0.500 kg CO₂/km',
                    'examples': 'Freightliner Cascadia, Peterbilt 579'
                }
            }
        }
    
    def get_emission_comparison(self, distance_km: float) -> Dict[str, float]:
        """
        Get emissions comparison for all transport modes.
        
        Args:
            distance_km: Distance in kilometers
            
        Returns:
            Dictionary with emissions for each mode
        """
        comparison = {}
        for mode, rate in self.emission_rates.items():
            comparison[mode] = self.calculate_emission(distance_km, mode)
        
        return comparison
    
    def calculate_environmental_impact(self, emission_kg: float) -> Dict[str, float]:
        """
        Calculate environmental impact metrics from CO2 emissions.
        
        Args:
            emission_kg: CO2 emissions in kilograms
            
        Returns:
            Dictionary with various environmental impact metrics
        """
        # Environmental impact calculations based on EPA data
        return {
            'trees_needed': round(emission_kg / 21.77, 2),  # Trees needed to offset (kg CO2/year per tree)
            'car_miles_equivalent': round(emission_kg / 0.404, 2),  # Equivalent car miles
            'smartphone_charges': round(emission_kg / 0.0084, 0),  # Smartphone charges equivalent
            'light_bulb_hours': round(emission_kg / 0.0006, 0)  # 60W light bulb hours
        }
    
    def get_emission_rating(self, emission_kg: float, distance_km: float) -> Tuple[str, str]:
        """
        Get emission rating and description for a route.
        
        Args:
            emission_kg: CO2 emissions in kilograms
            distance_km: Distance in kilometers
            
        Returns:
            Tuple of (rating, description)
        """
        if distance_km <= 0:
            return 'N/A', 'No emissions data available'
        
        emission_per_km = emission_kg / distance_km
        
        if emission_per_km == 0:
            return 'A+', 'Zero emissions - excellent environmental choice!'
        elif emission_per_km < 0.05:
            return 'A', 'Very low emissions - great for the environment'
        elif emission_per_km < 0.1:
            return 'B', 'Low emissions - good environmental choice'
        elif emission_per_km < 0.15:
            return 'C', 'Moderate emissions - consider greener alternatives'
        elif emission_per_km < 0.2:
            return 'D', 'High emissions - better alternatives available'
        else:
            return 'E', 'Very high emissions - consider sustainable alternatives'
    
    def get_mode_info(self, mode: str) -> Dict[str, str]:
        """
        Get detailed information about a transport mode.
        
        Args:
            mode: Transport mode
            
        Returns:
            Dictionary with mode information
        """
        mode_info = {
            'driving': {
                'name': 'Driving',
                'icon': '🚗',
                'description': 'Personal vehicle transportation',
                'benefits': 'Fast and convenient',
                'drawbacks': 'High emissions and fuel costs'
            },
            'transit': {
                'name': 'Public Transit',
                'icon': '🚌',
                'description': 'Bus, train, or other public transport',
                'benefits': 'Lower emissions per person, cost-effective',
                'drawbacks': 'Limited routes and schedules'
            },
            'bicycling': {
                'name': 'Bicycling',
                'icon': '🚴',
                'description': 'Bicycle transportation',
                'benefits': 'Zero emissions, great exercise',
                'drawbacks': 'Weather dependent, limited range'
            },
            'walking': {
                'name': 'Walking',
                'icon': '🚶',
                'description': 'Walking transportation',
                'benefits': 'Zero emissions, excellent exercise',
                'drawbacks': 'Slow for long distances'
            }
        }
        
        return mode_info.get(mode, {
            'name': mode.title(),
            'icon': '🌍',
            'description': 'Alternative transport mode',
            'benefits': 'Varies by mode',
            'drawbacks': 'Varies by mode'
        })
    
    def get_sustainability_tips(self, best_mode: str) -> List[str]:
        """
        Get sustainability tips based on the best transport mode.
        
        Args:
            best_mode: The most sustainable transport mode for the route
            
        Returns:
            List of sustainability tips
        """
        tips = {
            'walking': [
                "Walking is the most sustainable option - zero emissions!",
                "Consider walking for short distances to improve your health",
                "Use walking apps to find pedestrian-friendly routes"
            ],
            'bicycling': [
                "Cycling is excellent for the environment and your health",
                "Consider bike-sharing programs if you don't own a bike",
                "Plan routes using dedicated bike paths for safety"
            ],
            'transit': [
                "Public transit significantly reduces per-person emissions",
                "Consider monthly passes for regular commuting",
                "Combine transit with walking/cycling for the last mile"
            ],
            'driving': [
                "Consider carpooling to reduce emissions per person",
                "Plan multiple errands in one trip to minimize driving",
                "Look into electric or hybrid vehicles for your next car"
            ]
        }
        
        return tips.get(best_mode, ["Choose the most sustainable option available"])
