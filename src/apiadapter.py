from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import requests
from src.aircraft import Aircraft


class BaseAPIAdapter(ABC):
    """ Абстрактный класс для работы с API """

    @abstractmethod
    def get_aeroplanes(self, country: str) -> List[Aircraft]:
        """ Получает информацию о самолетах в воздушном пространстве страны """
        pass


class FlightRadarAPIAdapter(BaseAPIAdapter):
    """ Реализация """

    def __init__(self) -> None:
        """ Инициализация """
        self._openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self._opensky_url = 'https://opensky-network.org/api/states/all'
        self.aeroplanes: List[Aircraft] = []

    def _make_request(self, url: str, params: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Any:
        """ Выполнение HTTP-запросов """
        response = requests.get(url=url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_aeroplanes(self, country: str) -> List[Aircraft]:
        # Headers с user-agent - обязательный параметр при запросе к nominatim.openstreetmap.
        # Вы можете использовать любое название вместо test-app/1.0, например просто test-app.
        self.aeroplanes = []
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }

        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }

        geo_data = self._make_request(
            url=self._openstreetmap_url,
            params=params_nominatim,
            headers=headers_nominatim
        )

        # Пример ответа от nominatim.openstreetmap можно посмотреть в задании курсовой.
        geo_coordinates = geo_data[0].get('boundingbox')
        if not geo_coordinates or len(geo_coordinates) < 4:
            print("Неверный формат гео-данных")
            return None

        # Параметры для фильтрации самолетов по их географическим координатам.
        params_opensky = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }

        raw_data = self._make_request(
            url=self._opensky_url,
            params=params_opensky
        )

        for state in raw_data['states']:
            aircraft_obj = Aircraft.from_opensky_list(state)
            self.aeroplanes.append(aircraft_obj)

        return self.aeroplanes
