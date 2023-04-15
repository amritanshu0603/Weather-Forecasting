import datetime as dt
import requests
import tkinter as tk

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "6b01e4260c1df19b7c854b0e40dd0f0b"

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius* (9/5) + 32
    return celsius, fahrenheit

def get_weather_data(city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()
    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
    return temp_celsius, humidity, wind_speed, description, sunrise_time, sunset_time

def show_weather_data():
    city = city_entry.get()
    temp_celsius, humidity, wind_speed, description, sunrise_time, sunset_time = get_weather_data(city)
    temp_label.config(text=f"Temperature: {temp_celsius:.2f} C")
    humidity_label.config(text=f"Humidity: {humidity}%")
    wind_label.config(text=f"Wind Speed: {wind_speed}m/s")
    weather_label.config(text=f"Weather: {description}")
    sunrise_label.config(text=f"Sun Rises at: {sunrise_time}")
    sunset_label.config(text=f"Sun Sets at: {sunset_time}")

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
