import requests
import csv
from datetime import datetime
import os

LATITUDE = 13.0356
LONGITUDE = 80.1582
filename = "porur_cloud_weather_log.csv"

url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current=temperature_2m,direct_radiation,diffuse_radiation"

try:
    response = requests.get(url, timeout=10)
    print(f"API Response Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        current = data.get("current", {})
        
        temp_c = current.get("temperature_2m", 0)
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
        print(f"API Error: {response.text}")
        exit(1)
except Exception as e:
    print(f"Exception occurred: {e}")
    exit(1)
