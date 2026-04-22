import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_city_coordinates(city_name: str):
    params = {
        "name": city_name,
        "count": 5,
        "language": "ru",
        "format": "json"
    }

    response = requests.get(GEOCODING_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    results = data.get("results")
    if not results:
        return None

    first = results[0]
    return {
        "name": first.get("name"),
        "country": first.get("country"),
        "latitude": first.get("latitude"),
        "longitude": first.get("longitude"),
    }


def get_current_weather(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
        "timezone": "auto"
    }

    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data.get("current", {})
    return {
        "temperature": current.get("temperature_2m"),
        "time": current.get("time")
    }


def main():
    city = input("Введите город: ").strip()

    if not city:
        print("Город не введен.")
        return

    city_data = get_city_coordinates(city)
    if not city_data:
        print("Город не найден.")
        return

    weather = get_current_weather(
        city_data["latitude"],
        city_data["longitude"]
    )

    print("\nРезультат:")
    print(f"Город: {city_data['name']}")
    print(f"Страна: {city_data['country']}")
    print(f"Широта: {city_data['latitude']}")
    print(f"Долгота: {city_data['longitude']}")
    print(f"Температура: {weather['temperature']} °C")
    print(f"Время измерения: {weather['time']}")


if __name__ == "__main__":
    main()