import requests
import csv
from datetime import datetime
import os

# Porur, Chennai Coordinates
LATITUDE = 13.0356
LONGITUDE = 80.1582
filename = "porur_cloud_weather_log.csv"

# Fetch live weather data from Open-Meteo API
url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,direct_radiation,diffuse_radiation"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    current = data.get("current", {})
    
    temp_c = current.get("temperature_2m", "N/A")
    direct = current.get("direct_radiation", 0)
    diffuse = current.get("diffuse_radiation", 0)
    irradiance = (direct or 0) + (diffuse or 0)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Ambient_Temp_C", "Solar_Irradiance_W_m2"])
        writer.writerow([timestamp, temp_c, irradiance])
        
    print(f"Successfully logged at {timestamp}: Temp={temp_c}°C, Irradiance={irradiance}W/m²")
else:
    print("Failed to fetch weather data from API.")
