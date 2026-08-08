import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from src.aircraft import Aircraft


class BaseStorageConnector(ABC):
    """ Абстрактный класс для хранения данных о самолетах """

    @abstractmethod
    def add_aircraft(self, aircraft: Aircraft):
        """ Добавить информацию об одном самолете в хранилище """
        pass

    @abstractmethod
    def add_aircraft_batch(self, aircraft_list):
        """ Пакетное добавление списка самолетов """
        pass

    @abstractmethod
    def get_aircraft(self, criteria):
        """ Получить список самолетов по критериям """
        pass

    @abstractmethod
    def delete_aircraft(self, criteria):
        """ Удалить информацию о самолетах по указанным критериям """
        pass


class JsonConnector(BaseStorageConnector):
    """ Реализация хранилища данных о самолетах в формате JSON-файла """

    def __init__(self, file_path: str = "coursework2/data/planes.json") -> None:
        self.file_path = file_path

    def _read_file(self) -> List[Dict[str, Any]]:
        """ Чтение из файла JSON """
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """ Запись в файл JSON """
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _aircraft_to_dict(self, aircraft: Aircraft) -> Dict[str, Any]:
        """ Преобразование объекта Aircraft в словарь """
        return {
            "icao24": aircraft.icao24,
            "callsign": aircraft.callsign,
            "origin_country": aircraft.origin_country,
            "velocity": aircraft.velocity,
            "geo_altitude": aircraft.geo_altitude
        }

    def add_aircraft(self, aircraft: Aircraft) -> bool:
        data = self._read_file()
        data.append(self._aircraft_to_dict(aircraft))
        self._write_file(data)
        return True

    def add_aircraft_batch(self, aircraft_list: List[Aircraft]) -> int:
        data = self._read_file()
        for aircraft in aircraft_list:
            data.append(self._aircraft_to_dict(aircraft))
        self._write_file(data)
        return len(aircraft_list)

    def get_aircraft(self, criteria: Dict[str, Any]) -> List[Aircraft]:
        raw_data = self._read_file()
        result: List[Aircraft] = []

        for item in raw_data:
            match = True
            for key, value in criteria.items():
                if key == "min_velocity" and item.get("velocity", 0) < value:
                    match = False
                elif key == "max_velocity" and item.get("velocity", 0) > value:
                    match = False
                elif key == "min_altitude" and item.get("geo_altitude", 0) < value:
                    match = False
                elif key == "max_altitude" and item.get("geo_altitude", 0) > value:
                    match = False
                elif key in item and item[key] != value:
                    match = False

            if match:
                result.append(Aircraft(
                    icao24=item["icao24"],
                    callsign=item["callsign"],
                    origin_country=item["origin_country"],
                    velocity=item["velocity"],
                    geo_altitude=item["geo_altitude"]
                ))
        return result

    def delete_aircraft(self, criteria: Dict[str, Any]) -> int:
        raw_data = self._read_file()
        updated_data: List[Dict[str, Any]] = []
        deleted_count = 0

        for item in raw_data:
            match = True
            for key, value in criteria.items():
                if key in item and item[key] != value:
                    match = False

            if match and criteria:
                deleted_count += 1
            else:
                updated_data.append(item)

        if deleted_count > 0:
            self._write_file(updated_data)
        return deleted_count
