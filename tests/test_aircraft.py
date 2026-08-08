import unittest
from src.aircraft import Aircraft


class TestAircraft(unittest.TestCase):

    def test_successful_initialization(self):
        """ Тест успешного создания объекта """
        plane = Aircraft("c01122", "ACA123", "Canada", 240.5, 10500.0)
        self.assertEqual(plane.icao24, "c01122")
        self.assertEqual(plane.callsign, "ACA123")
        self.assertEqual(plane.origin_country, "Canada")
        self.assertEqual(plane.velocity, 240.5)
        self.assertEqual(plane.geo_altitude, 10500.0)

    def test_validation_none_handling_for_floats(self):
        """ Тест None преобразуется в 0.0 """
        plane = Aircraft("c01122", "ACA123", "Canada", None, None)
        self.assertEqual(plane.velocity, 0.0)
        self.assertEqual(plane.geo_altitude, 0.0)

    def test_from_opensky_list(self):
        """ Тест метода создания объекта из списка OpenSky """
        mock_state = [None] * 15
        mock_state[0] = "c01122"
        mock_state[1] = "ACA123  "
        mock_state[2] = "Canada"
        mock_state[5] = 250.0
        mock_state[13] = 11000.0

        plane = Aircraft.from_opensky_list(mock_state)
        self.assertEqual(plane.icao24, "c01122")
        self.assertEqual(plane.callsign, "ACA123")
        self.assertEqual(plane.velocity, 250.0)

    def test_aircraft_comparison_by_velocity(self):
        """ Тест сравнения самолетов по скорости """
        plane_slow = Aircraft("1", "P1", "Country", 150.0, 5000.0)
        plane_fast = Aircraft("2", "P2", "Country", 250.0, 5000.0)

        self.assertTrue(plane_slow < plane_fast)
        self.assertTrue(plane_fast > plane_slow)
        self.assertFalse(plane_slow == plane_fast)

    def test_aircraft_comparison_by_altitude_fallback(self):
        """ Тест сравнения по высоте, если скорости одинаковы """
        plane_low = Aircraft("1", "P1", "Country", 200.0, 4000.0)
        plane_high = Aircraft("2", "P2", "Country", 200.0, 9000.0)

        self.assertTrue(plane_low < plane_high)
        self.assertTrue(plane_high > plane_low)

    def test_aircraft_equality(self):
        """ Тест равенства самолетов при совпадении скорости и высоты """
        plane1 = Aircraft("1", "P1", "Country", 200.0, 5000.0)
        plane2 = Aircraft("2", "P2", "Country", 200.0, 5000.0)

        self.assertTrue(plane1 == plane2)
        self.assertTrue(plane1 <= plane2)
        self.assertTrue(plane1 >= plane2)
