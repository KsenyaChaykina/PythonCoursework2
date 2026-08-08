from src.apiadapter import FlightRadarAPIAdapter
from src.storage import JsonConnector

if __name__ == "__main__":
    api = FlightRadarAPIAdapter()
    print("Ввести название страны для запроса информации о самолетах:")
    aircraft_list = api.get_aeroplanes(input())
    print(f"Найдено самолетов: {len(aircraft_list)}")
    print("Получить топ самолетов по высоте полета, введите количество:")
    user_input = int(input())
    sorted_planes = sorted(aircraft_list, key=lambda x: x)
    for p in sorted_planes[:user_input]:
        print(p)
    print('Получить самолеты по стране их регистрации, введите страну:')
    country_input = input()
    storage = JsonConnector("coursework2/data/planes.json")
    search_criteria = {"origin_country": country_input}
    found_aircrafts = storage.get_aircraft(search_criteria)
    print(f"Найдено самолетов: {len(found_aircrafts)}")