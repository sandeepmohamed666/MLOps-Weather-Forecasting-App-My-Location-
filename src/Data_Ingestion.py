# #==================================================
# # From Chatgpt
# #==================================================
# import openmeteo_requests

# import pandas as pd
# import requests_cache
# from retry_requests import retry

# # Setup the Open-Meteo API client with cache and retry on error
# cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
# retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
# openmeteo = openmeteo_requests.Client(session = retry_session)

# # Make sure all required weather variables are listed here
# # The order of variables in hourly or daily is important to assign them correctly below
# url = "https://api.open-meteo.com/v1/forecast"
# params = {
# 	"latitude": 8.5241,
# 	"longitude": 76.9366,
# 	"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "wind_speed_10m", "wind_direction_10m"],
# }
# responses = openmeteo.weather_api(url, params = params)

# # Process first location. Add a for-loop for multiple locations or weather models
# response = responses[0]
# print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
# print(f"Elevation: {response.Elevation()} m asl")
# print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# # Process hourly data. The order of variables needs to be the same as requested.
# hourly = response.Hourly()
# hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
# hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
# hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
# hourly_rain = hourly.Variables(3).ValuesAsNumpy()
# hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
# hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()

# hourly_data = {
# 	"date": pd.date_range(
# 		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
# 		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
# 		freq = pd.Timedelta(seconds = hourly.Interval()),
# 		inclusive = "left"
# 	)
# }

# hourly_data["temperature_2m"] = hourly_temperature_2m
# hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
# hourly_data["dew_point_2m"] = hourly_dew_point_2m
# hourly_data["rain"] = hourly_rain
# hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
# hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

# hourly_dataframe = pd.DataFrame(data = hourly_data)
# print("\nHourly data\n", hourly_dataframe)
# import os

# # Create data folder if it doesn't exist
# os.makedirs("data", exist_ok=True)

# # Save DataFrame to CSV
# csv_path = os.path.join("data", "weather_data.csv")
# hourly_dataframe.to_csv(csv_path, index=False)

# print(f"\nCSV file saved successfully: {csv_path}")


## ==================================================
## From Gemini
## ==================================================
# import os  # Imported to handle folder creation
# import openmeteo_requests
# import pandas as pd
# import requests_cache
# from retry_requests import retry

# # Setup the Open-Meteo API client with cache and retry on error
# cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
# retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
# openmeteo = openmeteo_requests.Client(session = retry_session)

# # Make sure all required weather variables are listed here
# url = "https://api.open-meteo.com/v1/forecast"
# params = {
# 	"latitude": 8.5241,
# 	"longitude": 76.9366,
# 	"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "wind_speed_10m", "wind_direction_10m"],
# }
# responses = openmeteo.weather_api(url, params = params)

# # Process first location.
# response = responses[0]
# print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
# print(f"Elevation: {response.Elevation()} m asl")
# print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# # Process hourly data.
# hourly = response.Hourly()
# hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
# hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
# hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
# hourly_rain = hourly.Variables(3).ValuesAsNumpy()
# hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
# hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()

# hourly_data = {
# 	"date": pd.date_range(
# 		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
# 		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
# 		freq = pd.Timedelta(seconds = hourly.Interval()),
# 		inclusive = "left"
# 	)
# }

# hourly_data["temperature_2m"] = hourly_temperature_2m
# hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
# hourly_data["dew_point_2m"] = hourly_dew_point_2m
# hourly_data["rain"] = hourly_rain
# hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
# hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

# hourly_dataframe = pd.DataFrame(data = hourly_data)
# print("\nHourly data\n", hourly_dataframe)

# # ==========================================
# # NEW CODE: Save to CSV inside 'data' folder  
# # ==========================================

# # 1. Define the folder and file name
# folder_name = "data"
# file_name = "weather_forecast.csv"
# file_path = os.path.join(folder_name, file_name)

# # 2. Create the 'data' folder if it doesn't already exist
# os.makedirs(folder_name, exist_ok=True)

# # 3. Save the DataFrame to the CSV file (index=False prevents writing row numbers)
# hourly_dataframe.to_csv(file_path, index=False)

# print(f"\nSuccessfully saved data to: {file_path}")

#==================================================
# From grok
#==================================================
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import os
from datetime import datetime

# ====================== CREATE DATA FOLDER ======================
# Create 'data' folder if it doesn't exist
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

# ====================== SETUP OPEN-METEO CLIENT ======================
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# ====================== API REQUEST ======================
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 8.5241,
    "longitude": 76.9366,
    "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", 
               "rain", "wind_speed_10m", "wind_direction_10m"],
}

responses = openmeteo.weather_api(url, params=params)
response = responses[0]

print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")

# ====================== PROCESS HOURLY DATA ======================
hourly = response.Hourly()

hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
hourly_rain = hourly.Variables(3).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()

hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["dew_point_2m"] = hourly_dew_point_2m
hourly_data["rain"] = hourly_rain
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

hourly_dataframe = pd.DataFrame(data=hourly_data)

# ====================== SAVE TO CSV ======================
# Create filename with current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"weather_thiruvananthapuram_{timestamp}.csv"
csv_path = os.path.join(data_folder, csv_filename)

hourly_dataframe.to_csv(csv_path, index=False)

print(f"\n✅ Data successfully saved to: {csv_path}")
print(f"Total records: {len(hourly_dataframe)}")

# Optional: Display first few rows
print("\nPreview of data:")
print(hourly_dataframe.head())

# #==================================================
# # From deepseek - xlsx file (impossible format)
# #==================================================
# import openmeteo_requests
# import pandas as pd
# import requests_cache
# from retry_requests import retry
# import os  # Added for directory and file operations

# # Create 'data' folder if it doesn't exist
# data_folder = "data"
# if not os.path.exists(data_folder):
#     os.makedirs(data_folder)
#     print(f"Created folder: '{data_folder}'")
# else:
#     print(f"Folder '{data_folder}' already exists")

# # Setup the Open-Meteo API client with cache and retry on error
# cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
# retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
# openmeteo = openmeteo_requests.Client(session=retry_session)

# # Make sure all required weather variables are listed here
# # The order of variables in hourly or daily is important to assign them correctly below
# url = "https://api.open-meteo.com/v1/forecast"  # Fixed URL - removed my-server.tld
# params = {
#     "latitude": 8.5241,
#     "longitude": 76.9366,
#     "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "wind_speed_10m", "wind_direction_10m"],
# }
# responses = openmeteo.weather_api(url, params=params)

# # Process first location. Add a for-loop for multiple locations or weather models
# response = responses[0]
# print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
# print(f"Elevation: {response.Elevation()} m asl")
# print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# # Process hourly data. The order of variables needs to be the same as requested.
# hourly = response.Hourly()
# hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
# hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
# hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
# hourly_rain = hourly.Variables(3).ValuesAsNumpy()
# hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
# hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()

# hourly_data = {
#     "date": pd.date_range(
#         start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#         end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#         freq=pd.Timedelta(seconds=hourly.Interval()),
#         inclusive="left"
#     )
# }

# hourly_data["temperature_2m"] = hourly_temperature_2m
# hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
# hourly_data["dew_point_2m"] = hourly_dew_point_2m
# hourly_data["rain"] = hourly_rain
# hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
# hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

# hourly_dataframe = pd.DataFrame(data=hourly_data)
# print("\nHourly data preview (first 10 rows):\n", hourly_dataframe.head(10))
# print(f"\nTotal rows: {len(hourly_dataframe)}")

# # Create CSV file inside the 'data' folder
# csv_filename = os.path.join(data_folder, "weather_data.csv")
# hourly_dataframe.to_csv(csv_filename, index=False)
# print(f"\n✓ CSV file successfully created: '{csv_filename}'")

# # Optional: Create a timestamped CSV file to avoid overwriting
# from datetime import datetime
# timestamped_filename = os.path.join(data_folder, f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
# hourly_dataframe.to_csv(timestamped_filename, index=False)
# print(f"✓ Timestamped CSV file created: '{timestamped_filename}'")

# # Optional: Save as different formats
# # Save as Excel file
# excel_filename = os.path.join(data_folder, "weather_data.xlsx")
# hourly_dataframe.to_excel(excel_filename, index=False)
# print(f"✓ Excel file created: '{excel_filename}'")

# # Save as JSON
# json_filename = os.path.join(data_folder, "weather_data.json")
# hourly_dataframe.to_json(json_filename, orient="records", date_format="iso")
# print(f"✓ JSON file created: '{json_filename}'")

# # Display file information
# print(f"\n--- File Summary ---")
# print(f"All files saved in: '{os.path.abspath(data_folder)}'")
# print(f"CSV file size: {os.path.getsize(csv_filename)} bytes")

# #==================================================
# # From copilot - subfolder
# #==================================================
# import os
# import pandas as pd
# import requests_cache
# from retry_requests import retry
# import openmeteo_requests

# # Setup the Open-Meteo API client with cache and retry on error
# cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
# retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
# openmeteo = openmeteo_requests.Client(session=retry_session)

# # Make sure all required weather variables are listed here
# url = "https://api.open-meteo.com/v1/forecast"
# params = {
#     "latitude": 8.5241,
#     "longitude": 76.9366,
#     "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "wind_speed_10m", "wind_direction_10m"],
# }
# responses = openmeteo.weather_api(url, params=params)

# # Process first location
# response = responses[0]
# print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
# print(f"Elevation: {response.Elevation()} m asl")
# print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# # Process hourly data
# hourly = response.Hourly()
# hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
# hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
# hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
# hourly_rain = hourly.Variables(3).ValuesAsNumpy()
# hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
# hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()

# hourly_data = {
#     "date": pd.date_range(
#         start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#         end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#         freq=pd.Timedelta(seconds=hourly.Interval()),
#         inclusive="left"
#     ),
#     "temperature_2m": hourly_temperature_2m,
#     "relative_humidity_2m": hourly_relative_humidity_2m,
#     "dew_point_2m": hourly_dew_point_2m,
#     "rain": hourly_rain,
#     "wind_speed_10m": hourly_wind_speed_10m,
#     "wind_direction_10m": hourly_wind_direction_10m
# }

# hourly_dataframe = pd.DataFrame(data=hourly_data)
# print("\nHourly data\n", hourly_dataframe)

# # --- NEW CODE TO SAVE AS CSV ---
# # Ensure folder exists
# output_folder = os.path.join("data", "import", "openmeteo_requests")
# os.makedirs(output_folder, exist_ok=True)

# # Save DataFrame to CSV
# csv_path = os.path.join(output_folder, "hourly_weather.csv")
# hourly_dataframe.to_csv(csv_path, index=False)

# print(f"\nCSV file saved at: {csv_path}")
