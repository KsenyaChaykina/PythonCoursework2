import unittest
from unittest.mock import patch
from src.apiadapter import FlightRadarAPIAdapter
from src.aircraft import Aircraft


class TestFlightRadarAPIAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = FlightRadarAPIAdapter()

    @patch('requests.get')
    def test_get_aeroplanes_success(self, mock_get):
        mock_nominatim_response = unittest.mock.Mock()
        mock_nominatim_response.raise_for_status = unittest.mock.Mock()
        mock_nominatim_response.json.return_value = [{"boundingbox": ["45.0", "46.0", "-75.0", "-74.0"]}]
        mock_opensky_response = unittest.mock.Mock()
        mock_opensky_response.raise_for_status = unittest.mock.Mock()

        mock_state_vector = [None] * 15
        mock_state_vector[0] = "c01122"
        mock_state_vector[1] = "ACA123"
        mock_state_vector[2] = "Canada"
        mock_state_vector[5] = 220.0  # Скорость
        mock_state_vector[13] = 10000.0  # Высота

        mock_opensky_response.json.return_value = {
            "time": 123456789,
            "states": [mock_state_vector]
        }

        mock_get.side_effect = [mock_nominatim_response, mock_opensky_response]

        result = self.adapter.get_aeroplanes("Canada")

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Aircraft)
        self.assertEqual(result[0].icao24, "c01122")
        self.assertEqual(result[0].velocity, 220.0)
