#!/usr/bin/env python3
"""
Test vehicle emission calculations for the Sustainable Travel Route Finder.
"""

import unittest
from services.emissions_service import EmissionsService


class TestVehicleEmissions(unittest.TestCase):
    """Test vehicle-specific emission calculations."""

    def setUp(self):
        """Set up the emissions service."""
        self.emissions_service = EmissionsService()

    def test_vehicle_emission_calculation(self):
        """Test vehicle-specific emission calculations."""
        # Test electric car
        emission = self.emissions_service.calculate_vehicle_emission(
            100, 'car', 'electric'
        )
        self.assertEqual(emission, 4.0)  # 100 km * 0.040 kg/km
        
        # Test hybrid car
        emission = self.emissions_service.calculate_vehicle_emission(
            50, 'car', 'hybrid'
        )
        self.assertEqual(emission, 4.0)  # 50 km * 0.080 kg/km
        
        # Test large gasoline car
        emission = self.emissions_service.calculate_vehicle_emission(
            20, 'car', 'gasoline_large'
        )
        self.assertEqual(emission, 5.0)  # 20 km * 0.250 kg/km

    def test_available_vehicles(self):
        """Test that vehicle information is available."""
        vehicles = self.emissions_service.get_available_vehicles()
        
        # Check that all vehicle types are present
        self.assertIn('car', vehicles)
        self.assertIn('motorcycle', vehicles)
        self.assertIn('transit', vehicles)
        self.assertIn('truck', vehicles)
        
        # Check that car models are present
        car_models = vehicles['car']
        self.assertIn('electric', car_models)
        self.assertIn('hybrid', car_models)
        self.assertIn('gasoline_small', car_models)
        
        # Check that vehicle information is complete
        electric_car = car_models['electric']
        self.assertIn('name', electric_car)
        self.assertIn('description', electric_car)
        self.assertIn('emission_rate', electric_car)
        self.assertIn('examples', electric_car)

    def test_emission_comparison(self):
        """Test emission comparison between different vehicles."""
        distance = 100  # 100 km
        
        # Calculate emissions for different vehicles
        electric_emission = self.emissions_service.calculate_vehicle_emission(
            distance, 'car', 'electric'
        )
        hybrid_emission = self.emissions_service.calculate_vehicle_emission(
            distance, 'car', 'hybrid'
        )
        large_gas_emission = self.emissions_service.calculate_vehicle_emission(
            distance, 'car', 'gasoline_large'
        )
        
        # Electric should have lowest emissions
        self.assertLess(electric_emission, hybrid_emission)
        self.assertLess(hybrid_emission, large_gas_emission)
        
        # Verify specific values
        self.assertEqual(electric_emission, 4.0)   # 100 * 0.040
        self.assertEqual(hybrid_emission, 8.0)     # 100 * 0.080
        self.assertEqual(large_gas_emission, 25.0) # 100 * 0.250

    def test_transit_emissions(self):
        """Test transit emission calculations."""
        distance = 50  # 50 km
        
        # Test different transit modes
        bus_emission = self.emissions_service.calculate_vehicle_emission(
            distance, 'transit', 'bus'
        )
        train_emission = self.emissions_service.calculate_vehicle_emission(
            distance, 'transit', 'train'
        )
        subway_emission = self.emissions_service.calculate_vehicle_emission(
            distance, 'transit', 'subway'
        )
        
        # Subway should have lowest emissions
        self.assertLess(subway_emission, train_emission)
        self.assertLess(train_emission, bus_emission)
        
        # Verify specific values
        self.assertEqual(bus_emission, 3.4)    # 50 * 0.068
        self.assertEqual(train_emission, 2.05)  # 50 * 0.041
        self.assertEqual(subway_emission, 1.75) # 50 * 0.035

    def test_motorcycle_emissions(self):
        """Test motorcycle emission calculations."""
        distance = 30  # 30 km
        
        # Test different motorcycle types
        small_emission = self.emissions_service.calculate_vehicle_emission(
            distance, 'motorcycle', 'small'
        )
        electric_emission = self.emissions_service.calculate_vehicle_emission(
            distance, 'motorcycle', 'electric'
        )
        large_emission = self.emissions_service.calculate_vehicle_emission(
            distance, 'motorcycle', 'large'
        )
        
        # Electric should have lowest emissions
        self.assertLess(electric_emission, small_emission)
        self.assertLess(small_emission, large_emission)
        
        # Verify specific values
        self.assertEqual(small_emission, 2.4)   # 30 * 0.080
        self.assertEqual(electric_emission, 0.6) # 30 * 0.020
        self.assertEqual(large_emission, 5.4)    # 30 * 0.180

    def test_invalid_vehicle(self):
        """Test handling of invalid vehicle types."""
        # Test with invalid vehicle type
        emission = self.emissions_service.calculate_vehicle_emission(
            100, 'invalid_type', 'invalid_model'
        )
        # Should fall back to average car rate (0.120)
        self.assertEqual(emission, 12.0)  # 100 * 0.120

    def test_zero_distance(self):
        """Test that zero distance returns zero emissions."""
        emission = self.emissions_service.calculate_vehicle_emission(
            0, 'car', 'electric'
        )
        self.assertEqual(emission, 0.0)


if __name__ == '__main__':
    unittest.main() 