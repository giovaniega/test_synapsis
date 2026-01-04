import time
from function.mqtt_service import MqttService
from function.log_service import LogService
from function.sensor_service import SensorService
from function.scheduler_service import SchedulerBase


if __name__ == "__main__":

    CANDIDATE_NAME = "giovani"
    INTERVAL = 5
    LOG_DIR = "log"
    SENSOR_FILE_PATH = "log/data_weather.json"
    
    BROKER = "test.mosquitto.org"
    PORT = 1883

    sensor_service = SensorService(CANDIDATE_NAME, SENSOR_FILE_PATH)
    log_service = LogService(LOG_DIR)
    scheduler = SchedulerBase(INTERVAL)
    mqtt_service = MqttService(BROKER, PORT, CANDIDATE_NAME, scheduler)
    
    mqtt_service.connect()

    def publishTask():
        sensor_data = sensor_service.generateSensorData()
        status = mqtt_service.publish(sensor_data)
        log_service.writeLog(sensor_data, status)

    time.sleep(2)
    scheduler.executeTask = publishTask
    scheduler.start()
