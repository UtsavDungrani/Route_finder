#!/usr/bin/env python3
"""
Basic tests for the Sustainable Travel Route Finder application.
"""

import unittest
import json
from app import create_app
from config import DevelopmentConfig


class TestSustainableTravelApp(unittest.TestCase):
    """Test cases for the Flask application."""

    def setUp(self):
        """Set up test client and configuration."""
        self.app = create_app(DevelopmentConfig)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home_page(self):
        """Test that the home page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'EcoRoute Finder', response.data)

    def test_about_page(self):
        """Test that the about page loads correctly."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About EcoRoute Finder', response.data)

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_api_routes_missing_data(self):
        """Test API endpoint with missing data."""
        response = self.client.post('/api/routes', 
                                  data=json.dumps({}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_api_routes_invalid_data(self):
        """Test API endpoint with invalid data."""
        response = self.client.post('/api/routes',
                                  data=json.dumps({
                                      'origin': '',
                                      'destination': 'Test'
                                  }),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_404_error(self):
        """Test 404 error handling."""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)

    def test_form_submission_missing_data(self):
        """Test form submission with missing data."""
        response = self.client.post('/result', data={})
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_form_submission_same_locations(self):
        """Test form submission with same origin and destination."""
        response = self.client.post('/result', data={
            'origin': 'New York',
            'destination': 'New York'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home


class TestConfig(unittest.TestCase):
    """Test configuration settings."""

    def test_emission_rates(self):
        """Test emission rates configuration."""
        rates = DevelopmentConfig.get_emission_rates()
        self.assertIn('driving', rates)
        self.assertIn('transit', rates)
        self.assertIn('bicycling', rates)
        self.assertIn('walking', rates)
        self.assertEqual(rates['walking'], 0.0)
        self.assertEqual(rates['bicycling'], 0.0)

    def test_supported_modes(self):
        """Test supported transportation modes."""
        modes = DevelopmentConfig.get_supported_modes()
        self.assertIn('driving-car', modes)
        self.assertIn('cycling-regular', modes)
        self.assertIn('foot-walking', modes)


if __name__ == '__main__':
    unittest.main() 