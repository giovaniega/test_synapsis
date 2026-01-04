import csv
import os
from datetime import datetime, timedelta


class LogService:


    def __init__(self, log_dir):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)


    def writeLog(self, sensor_data, status):
        file_path = self.getLogFilePath()
        file_exists = os.path.isfile(file_path)

        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file, delimiter=";")

            if not file_exists:
                writer.writerow([
                    "timestamp",
                    "sensor1",
                    "sensor2",
                    "sensor3",
                    "sensor4",
                    "sensor5",
                    "status"
                ])

            writer.writerow([
                self.getGmt7Timestamp(),
                sensor_data["data"]["sensor1"],
                sensor_data["data"]["sensor2"],
                sensor_data["data"]["sensor3"],
                sensor_data["data"]["sensor4"],
                sensor_data["data"]["sensor5"],
                status
            ])


    def getLogFilePath(self):
        date_str = self.getGmt7Timestamp("%d%m%y")
        return f"{self.log_dir}/mqtt_log_{date_str}.csv"


    def getGmt7Timestamp(self, fmt="%Y-%m-%d %H:%M:%S"):
        gmt7 = datetime.utcnow() + timedelta(hours=7)
        return gmt7.strftime(fmt)


# TESTING
# if __name__ == "__main__":

#     dummy_data = {
#         "nama": "ega",
#         "data": {
#             "sensor1": 12,
#             "sensor2": 123.45,
#             "sensor3": True,
#             "sensor4": 12.34,
#             "sensor5": 12.3
#         }
#     }

#     log_service = LogService("log")
#     log_service.writeLog(dummy_data, "Success")

#     print("CSV log written")