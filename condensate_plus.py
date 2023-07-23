import random
import time
import csv
import requests
from datetime import datetime

# Function to get weather data from OpenWeatherMap API
def get_weather_data(api_key, latitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        temperature = data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
        humidity = data["main"]["humidity"]
        return temperature, humidity
    else:
        print("Failed to fetch weather data.")
        return None

# Function to estimate AC condensate production
def estimate_condensate_production(temperature, humidity, ac_size, room_square_footage):
    # Constants for the condensate production formula (simplified for the example)
    condensate_per_btuh = 0.005  # Gallons of water produced per BTU per hour
    efficiency_factor = 0.8     # Efficiency factor of the AC unit

    # Calculate the BTUs needed for the room based on square footage
    btus_needed = room_square_footage * 20  # 20 BTUs per square foot

    # Calculate the estimated condensate production
    condensate_production = (
        btus_needed
        * condensate_per_btuh
        * efficiency_factor
        * (1 + (humidity - 50) / 100)  # Adjust for humidity (humidity deviation from 50%)
    )

    return condensate_production

def main():
    # Room and AC configuration (you can change these values as needed)
    room_square_footage = 200    # Replace with your room's square footage
    ac_size_btuh = 10000         # Replace with your AC's cooling capacity in BTU/h

    # Your OpenWeatherMap API key
    #api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your API key
    api_key = '06cefde2fb9735b6a48aedd072a74dc7'

    # Exact geographical location (latitude and longitude)
    latitude = 37.7749   # Replace with your latitude
    longitude = -122.4194  # Replace with your longitude

    # CSV file setup
    csv_file = "ac_data.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Temperature (C)", "Humidity (%)", "Condensate Production (gallons/hour)"])

    # Print location information and current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Location (Latitude, Longitude): {latitude}, {longitude}")
    print(f"Current Date and Time: {current_time}")
    print("-" * 30)

    while True:
        weather_data = get_weather_data(api_key, latitude, longitude)
        if weather_data:
            temperature, humidity = weather_data
            condensate_production = estimate_condensate_production(
                temperature, humidity, ac_size_btuh, room_square_footage
            )

            print(f"Current Temperature: {temperature:.1f}°C")
            print(f"Current Humidity: {humidity:.1f}%")
            print(f"Estimated Condensate Production: {condensate_production:.2f} gallons/hour")
            print("-" * 30)

            # Append data to CSV file
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([temperature, humidity, condensate_production])

        time.sleep(5)  # Simulate data refresh every 5 seconds

if __name__ == "__main__":
    main()
