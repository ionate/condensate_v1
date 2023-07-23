import random
import time
import csv
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Function to get historical weather data from OpenWeatherMap API
def get_historical_weather_data(api_key, latitude, longitude, start_date, end_date):
    url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={latitude}&lon={longitude}&dt="
    historical_data = []

    current_date = start_date
    while current_date <= end_date:
        timestamp = int(current_date.timestamp())
        response = requests.get(url + str(timestamp) + f"&appid={api_key}")
        data = response.json()

        if response.status_code == 200:
            temperature_celsius = data["current"]["temp"] - 273.15  # Convert Kelvin to Celsius
            humidity = data["current"]["humidity"]
            historical_data.append((current_date, temperature_celsius, humidity))
        else:
            print(f"Failed to fetch historical weather data for {current_date.date()}.")
        
        current_date += timedelta(days=1)
    
    return historical_data

# Function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

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
    api_key = '06cefde2fb9735b6a48aedd072a74dc7' # Replace with your API key

    # Exact geographical location (latitude and longitude)
    latitude = 30.31196722699356   # Replace with your latitude
    longitude = -97.91632949879643  # Replace with your longitude
    #30.31196722699356, -97.91632949879643

    # Date range for historical weather data
    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    end_date_str = input("Enter the end date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # CSV file setup
    csv_file = "ac_data.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Temperature (F)", "Humidity (%)", "Condensate Production (gallons/hour)"])

    # Print location information and current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Location (Latitude, Longitude): {latitude}, {longitude}")
    print(f"Current Date and Time: {current_time}")
    print("-" * 30)

    # Fetch historical weather data
    historical_data = get_historical_weather_data(api_key, latitude, longitude, start_date, end_date)
    
    # Plotting and saving to disk
    plot_data = {"Temperature (F)": [], "Humidity (%)": [], "Condensate Production (gallons/hour)": []}
    for date, temperature_celsius, humidity in historical_data:
        temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)
        condensate_production = estimate_condensate_production(
            temperature_celsius, humidity, ac_size_btuh, room_square_footage
        )

        # Print data for the current date
        print(f"Date: {date.date()}")
        print(f"Temperature: {temperature_fahrenheit:.1f}°F")
        print(f"Humidity: {humidity:.1f}%")
        print(f"Estimated Condensate Production: {condensate_production:.2f} gallons/hour")
        print("-" * 30)

        # Append data to CSV file
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date.date(), temperature_fahrenheit, humidity, condensate_production])
        
        # Add data to plot_data
        plot_data["Temperature (F)"].append(temperature_fahrenheit)
        plot_data["Humidity (%)"].append(humidity)
        plot_data["Condensate Production (gallons/hour)"].append(condensate_production)

    # Plotting and saving to disk
    plt.figure(figsize=(10, 6))
    for key, value in plot_data.items():
        plt.plot([date.date() for date, _, _ in historical_data], value, label=key)
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("Value")
    plt.title("Historical Weather Data")
    plt.legend()
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig("historical_weather_plot.png")
    plt.show()

if __name__ == "__main__":
    main()
