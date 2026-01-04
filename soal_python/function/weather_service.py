import time
import json
import requests
import os
from datetime import datetime, timedelta
from function.scheduler_service import SchedulerBase

class WeatherService(SchedulerBase):

    WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key, log_file_path, interval, city, debug=False):
        super().__init__(interval, debug)

        self.api_key = api_key
        self.log_file_path = log_file_path
        self.city = city

        log_dir = os.path.dirname(self.log_file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)


    def executeTask(self):
        if(self.debug):
            print()
            print("=====================================================")
            print("[DEBUG] interval : ", self.interval)
            print("[DEBUG] city     : ", self.city)
        
        self.samplingWeather(self.city)


    def samplingWeather(self, city):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }

        response = requests.get(self.WEATHER_API_URL, params=params)

        if response.status_code != 200:
            result = response.json()
            message = result.get("message", "Unknown Error")
            self.printFailed(response.status_code, message)
            return

        result = response.json()

        temperature = result["main"]["temp"]
        humidity = result["main"]["humidity"]

        data = {
            "timestamp": self.getTimestamp(),
            "city": city,
            "temperature": temperature,
            "temperature_unit": "C",
            "humidity": humidity,
            "humidity_unit": "%"
        }

        if(self.debug):
            print()
            print("[DEBUG] data raw : \n",result)
            print()
            print("[DEBUG] output data : \n", data)

        self.saveToJson(data)
        self.printSuccess(temperature, "C", humidity, "%")


    def saveToJson(self, data):
        try:
            with open(self.log_file_path, "r") as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []
        except json.JSONDecodeError:
            existing_data = []

        existing_data.append(data)

        with open(self.log_file_path, "w") as file:
            json.dump(existing_data, file, indent=4)


    def getTimestamp(self):
        gmt7_time = datetime.utcnow() + timedelta(hours=7)
        return gmt7_time.strftime("%Y-%m-%d %H:%M:%S")


    def printSuccess(self, temperature, temp_unit, humidity, humidity_unit):
        timestamp = self.getTimestamp()
        print(
            "({}) - Success Running Sampling Data Weather with Result Temperature {} {} & Humidity {} {}".format(
                timestamp,
                temperature,
                temp_unit,
                humidity,
                humidity_unit
            )
        )


    def printFailed(self, status_code, message):
        timestamp = self.getTimestamp()
        print(
            "({}) - Failed Running Sampling Data Weather with Status Code {} - {}".format(
                timestamp,
                status_code,
                message
            )
        )


if __name__ == "__main__":

    API_KEY = "fe2b7efd97721ecf933cebff6eaa15e7"
    LOG_FILE_PATH = "log/data_weather.json"
    CITY = "yogyakarta"
    INTERVAL = 10

    my_wheater = WeatherService(API_KEY, LOG_FILE_PATH, INTERVAL, CITY, False)
    my_wheater.start()