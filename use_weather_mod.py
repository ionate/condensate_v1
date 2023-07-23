# other_script.py

from weather_mod import WeatherDataModule

api_key = "fe8956fc897e35b70b64ca71de302451"
location = "Austin, TX"
start_date = "2023-07-01"
end_date = "2023-0721"
# location = "Los Angeles, CA"
# start_date = "2023-01-01"
# end_date = "2023-01-31"

weather_module = WeatherDataModule(api_key)
weather_data = weather_module.get_weather_data(location, start_date, end_date)

print("Historical Weather Data:")
print(weather_data)

# Save the report to a CSV file
weather_module.save_report(weather_data, "los_angeles_weather.csv")
