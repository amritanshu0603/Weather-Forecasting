import datetime as dt
import requests
import tkinter as tk
from tkinter import messagebox

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "889836504f124ae43e24093292d22cd9"  # Replace with your actual API key


def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit


def get_weather_data(city):
    url = f"{BASE_URL}appid={API_KEY}&q={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        temp_kelvin = data['main']['temp']
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = data['main']['feels_like']
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        timezone_offset = data['timezone']
        sunrise_time = dt.datetime.utcfromtimestamp(data['sys']['sunrise'] + timezone_offset)
        sunset_time = dt.datetime.utcfromtimestamp(data['sys']['sunset'] + timezone_offset)

        return temp_celsius, humidity, wind_speed, description, sunrise_time, sunset_time
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")
    except Exception as err:
        messagebox.showerror("Error", f"An error occurred: {err}")
    return None


def show_weather_data():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    weather_data = get_weather_data(city)
    if weather_data:
        temp_celsius, humidity, wind_speed, description, sunrise_time, sunset_time = weather_data
        temp_label.config(text=f"Temperature: {temp_celsius:.2f} °C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
        weather_label.config(text=f"Weather: {description}")
        sunrise_label.config(text=f"Sun Rises at: {sunrise_time.strftime('%Y-%m-%d %H:%M:%S')}")
        sunset_label.config(text=f"Sun Sets at: {sunset_time.strftime('%Y-%m-%d %H:%M:%S')}")


root = tk.Tk()
root.title("Weather App")

city_label = tk.Label(root, text="Enter city name:")
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

submit_button = tk.Button(root, text="Get Weather", command=show_weather_data)
submit_button.pack()

temp_label = tk.Label(root, text="")
temp_label.pack()

humidity_label = tk.Label(root, text="")
humidity_label.pack()

wind_label = tk.Label(root, text="")
wind_label.pack()

weather_label = tk.Label(root, text="")
weather_label.pack()

sunrise_label = tk.Label(root, text="")
sunrise_label.pack()

sunset_label = tk.Label(root, text="")
sunset_label.pack()

root.mainloop()
