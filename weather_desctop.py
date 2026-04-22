import requests
import tkinter as tk
from tkinter import messagebox

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


def show_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Предупреждение", "Введите название города.")
        return

    try:
        city_data = get_city_coordinates(city)

        if not city_data:
            result_label.config(text="Город не найден.")
            return

        weather = get_current_weather(
            city_data["latitude"],
            city_data["longitude"]
        )

        result_text = (
            f"Город: {city_data['name']}\n"
            f"Страна: {city_data['country']}\n"
            f"Температура: {weather['temperature']} °C\n"
            f"Время измерения: {weather['time']}"
        )

        result_label.config(text=result_text)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка сети", f"Не удалось получить данные:\n{e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка:\n{e}")


root = tk.Tk()
root.title("Погода по городам")
root.geometry("400x300")
root.resizable(False, False)

title_label = tk.Label(root, text="Погодное приложение", font=("Arial", 16))
title_label.pack(pady=10)

city_label = tk.Label(root, text="Введите город:")
city_label.pack()

city_entry = tk.Entry(root, width=30, font=("Arial", 12))
city_entry.pack(pady=5)

search_button = tk.Button(root, text="Показать погоду", command=show_weather)
search_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 11), justify="left")
result_label.pack(pady=10)

root.mainloop()