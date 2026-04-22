import requests
import streamlit as st

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


st.set_page_config(page_title="Погода", page_icon="🌤", layout="centered")

st.title("🌤 Погодное приложение")
st.write("Введи название города и получи текущую температуру.")

city = st.text_input("Введите город", placeholder="Например: Washington") # cities: USA(15 cities)(washington, new york, losangeles, chicago, houston,
                                                                          # phoenix, philadelphia, san antonio, san diego, dallas, san jose, austin,
                                                                          # jacksonville, fort worth, columbus)

if st.button("Показать погоду"):
    if not city.strip():
        st.warning("Введите название города.")
    else:
        try:
            city_data = get_city_coordinates(city.strip())

            if not city_data:
                st.error("Город не найден.")
            else:
                weather = get_current_weather(
                    city_data["latitude"],
                    city_data["longitude"]
                )

                st.success("Данные успешно получены")
                st.write(f"**Город:** {city_data['name']}")
                st.write(f"**Страна:** {city_data['country']}")
                st.write(f"**Температура:** {weather['temperature']} °C")
                st.write(f"**Время измерения:** {weather['time']}")

        except requests.exceptions.RequestException as e:
            st.error(f"Ошибка сети: {e}")
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")