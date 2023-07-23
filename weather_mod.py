import requests
import pandas as pd

apikey = "fe8956fc897e35b70b64ca71de302451"
urlstr = f"https://api.openweathermap.org/data/2.5/weather?q=Austin&mode=xml&appid={apikey}"
print(urlstr)

class WeatherDataModule:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather_data(self, location, start_date, end_date):
        weather_api_url = f"https://api.weather.com/v3/wx/historical/daily"
        payload = {
            "apiKey": self.api_key,
            "location": location,
            "startDate": start_date,
            "endDate": end_date,
            "units": "m",
        }
        response = requests.get(weather_api_url, params=payload)

        if response.status_code != 200:
            print(response)
            raise Exception(f"Failed to fetch weather data. Status code: {response.status_code}. Response: {response.text}")

        data = response.json()["historicalObservations"]
        df = pd.DataFrame(data)
        df = df[["valid_date", "max_temp", "min_temp", "precip_total"]]
        df["valid_date"] = pd.to_datetime(df["valid_date"])
        df.set_index("valid_date", inplace=True)

        return df

    def get_climate_data(self, location):
        climate_api_url = f"https://api.weather.com/v3/wx/climate/daily"
        payload = {
            "apiKey": self.api_key,
            "location": location,
            "units": "m",
        }
        response = requests.get(climate_api_url, params=payload)

        if response.status_code != 200:
            raise Exception("Failed to fetch climate data")

        data = response.json()["climateNorms"][0]
        df = pd.DataFrame(data)
        df = df[["date", "maxTempAvg", "minTempAvg", "precipAvg"]]
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        return df

    def save_report(self, df, filename):
        df.to_csv(filename)


# Example usage:
if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual API key from weather.com
    api_key = "fe8956fc897e35b70b64ca71de302451"
    location = "Austin, TX"
    start_date = "2023-07-01"
    end_date = "2023-0721"

    # location = "New York, NY"
    # start_date = "2023-01-01"
    # end_date = "2023-01-31"

    weather_module = WeatherDataModule(api_key)

    weather_data = weather_module.get_weather_data(location, start_date, end_date)
    climate_data = weather_module.get_climate_data(location)

    print("Historical Weather Data:")
    print(weather_data)

    print("\nClimate Data:")
    print(climate_data)

    # Save the reports to CSV files
    weather_module.save_report(weather_data, "weather_report.csv")
    weather_module.save_report(climate_data, "climate_report.csv")
