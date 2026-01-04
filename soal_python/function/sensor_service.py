import json
import random
from datetime import datetime


class SensorService:


    def __init__(self, candidate_name, file_path):
        self.candidate_name = candidate_name
        self.file_path = file_path


    def generateSensorData(self):
        temp_hum = self.getWeatherData()
        temperature = temp_hum[0]
        humidity = temp_hum[1]

        data = {
            "nama": self.candidate_name,
            "data": {
                "sensor1": random.randint(0, 100),
                "sensor2": round(random.uniform(0, 1000), 2),
                "sensor3": random.choice([True, False]),
                "sensor4": float(temperature),
                "sensor5": float(humidity)
            },
            "timestamp": self.getUtcTimestamp()
        }

        return data


    def getWeatherData(self):
        try:
            with open(self.file_path, "r") as file:
                weather_data = json.load(file)

            last_data = weather_data[-1]
            temperature = float(last_data.get("temperature"))
            humidity = float(last_data.get("humidity"))

            return [temperature, humidity]

        except Exception:
            return [0.0, 0.0]


    def getUtcTimestamp(self):
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    sensor_service = SensorService("giovani")
    data = sensor_service.generateSensorData()
    print(data)