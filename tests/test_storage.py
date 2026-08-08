import os
import unittest
from src.aircraft import Aircraft
from src.storage import JsonConnector


class TestJsonConnector(unittest.TestCase):

    def setUp(self):
        """ Временный файл """
        self.test_filename = "test_aircrafts_db.json"
        self.storage = JsonConnector(self.test_filename)
        self.plane1 = Aircraft("a1b2c3", "ACA1", "Canada", 220.0, 10000.0)
        self.plane2 = Aircraft("d4e5f6", "AFR2", "France", 180.0, 8000.0)

    def tearDown(self):
        """ Зачистка временного файла """
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_and_get_aircraft(self):
        """ Тест добавления одного объекта """
        self.storage.add_aircraft(self.plane1)

        all_records = self.storage.get_aircraft({})
        self.assertEqual(len(all_records), 1)
        self.assertEqual(all_records[0].icao24, "a1b2c3")

    def test_batch_insertion(self):
        """ Тест добавления нескольких объектов """
        count = self.storage.add_aircraft_batch([self.plane1, self.plane2])
        self.assertEqual(count, 2)
        self.assertEqual(len(self.storage.get_aircraft({})), 2)

    def test_filtering_by_country(self):
        """ Тест фильтрации по стране """
        self.storage.add_aircraft_batch([self.plane1, self.plane2])

        france_planes = self.storage.get_aircraft({"origin_country": "France"})
        self.assertEqual(len(france_planes), 1)
        self.assertEqual(france_planes[0].callsign, "AFR2")

    def test_filtering_by_velocity_range(self):
        """ Тест фильтрации по скорости """
        self.storage.add_aircraft_batch([self.plane1, self.plane2])

        fast_planes = self.storage.get_aircraft({"min_velocity": 200.0})
        self.assertEqual(len(fast_planes), 1)
        self.assertEqual(fast_planes[0].icao24, "a1b2c3")

    def test_delete_aircraft(self):
        """ Тест удаления по точному критерию """
        self.storage.add_aircraft_batch([self.plane1, self.plane2])

        deleted = self.storage.delete_aircraft({"icao24": "a1b2c3"})
        self.assertEqual(deleted, 1)

        remaining = self.storage.get_aircraft({})
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].icao24, "d4e5f6")
