from function.weather_service import WeatherService

API_KEY = "fe2b7efd97721ecf933cebff6eaa15e7"
LOG_FILE_PATH = "log/data_weather.json"

def getIntervalInput():
    while True:
        interval_input = input("Masukkan interval dalam detik (>0): ")

        if not interval_input.isdigit():
            print("Input tidak valid (Masukkan angka di atas 0)")
            continue

        interval = int(interval_input)

        if interval <= 0:
            print("Input tidak valid (Masukkan angka di atas 0)")
            continue

        return interval


def getCityInput():
    city = input("Masukkan nama kota : ")
    return city


if __name__ == "__main__":
    city = getCityInput()
    interval = getIntervalInput()

    weather_service = WeatherService(API_KEY, LOG_FILE_PATH, interval, city, False)
    weather_service.start()
