from functools import total_ordering
from typing import Any, List


@total_ordering
class Aircraft:
    """ Класс для сравнения информации о самолете """

    def __init__(self, icao24: str, callsign: str, origin_country: str, velocity: float, geo_altitude: float) -> None:
        self.icao24 = self._validate_str(icao24, "icao24")
        self.callsign = self._validate_str(callsign, "позывной").strip()
        self.origin_country = self._validate_str(origin_country, "страна регистрации")
        self.velocity = self._validate_float(velocity, "скорость полета")
        self.geo_altitude = self._validate_float(geo_altitude, "высота полета")

    @staticmethod
    def _validate_str(value: Any, field_name: str) -> str:
        """ Проверка строковых полей """
        return value

    @staticmethod
    def _validate_float(value: Any, field_name: str):
        """ Проверка числовых полей. Допускает None, преобразуя в 0.0 """
        if value is None:
            return 0.0
        if not isinstance(value, (int, float)):
            raise TypeError(f"Поле '{field_name}' должно быть числом, получено {type(value)}")
        return float(value)

    @classmethod
    def from_opensky_list(cls, state_vector: List[Any]) -> "Aircraft":
        # Индексы: 0: icao24, 1: callsign, 2: origin_country, 7: velocity, 13: geo_altitude
        try:
            return cls(
                icao24=state_vector[0],
                callsign=state_vector[1] or "UNKNOWN",
                origin_country=state_vector[2],
                velocity=state_vector[5],
                geo_altitude=state_vector[13]
            )
        except (IndexError, TypeError) as e:
            raise ValueError(f"Ошибка: {e}")

    def __eq__(self, other):
        """ Самолеты равны, если равны их скорость и высота одновременно """
        return (self.velocity == other.velocity) and (self.geo_altitude == other.geo_altitude)

    def __lt__(self, other):
        """ Сравнение меньше. Сначала сравниваем по скорости. Если скорость равна - сравниваем по высоте полета """
        if not isinstance(other, Aircraft):
            return NotImplemented
        if self.velocity == other.velocity:
            return self.geo_altitude < other.geo_altitude
        return self.velocity < other.velocity

    def __repr__(self) -> str:
        return (
            f"Aircraft(ICAO: {self.icao24}, Позывной: '{self.callsign}', "
            f"Страна: {self.origin_country}, Скорость: {self.velocity} м/с, "
            f"Высота: {self.geo_altitude} м)"
        )
