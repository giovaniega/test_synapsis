from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from function.scheduler_service import SchedulerBase
from function.sensor_service import SensorService
import threading

HOST = "localhost"
PORT = 5020
NAME = "giovani"
FILE_PATH = "log/data_weather.json"
INTERVAL = 5

class ModbusSlaveService:

    def __init__(self):
        self.weather = SensorService(NAME, FILE_PATH)

        self.store = ModbusSlaveContext(
            hr=ModbusSequentialDataBlock(0, [0]*10)
        )

        self.context = ModbusServerContext(slaves=self.store, single=True)

    def update_weather(self):
        temp_hum = self.weather.getWeatherData()
        temp = temp_hum[0]
        hum  = temp_hum[1]

        self.store.setValues(3, 0, [int(temp*100)])
        self.store.setValues(3, 1, [int(hum*100)])

        print()
        print("=========================")
        print("temperature : ", temp)
        print("humidity    : ", hum)
        print("=========================")

    def monitor_status(self):
        status = self.store.getValues(3, 2, count=1)[0]
        print(f"[SLAVE] Device Status : {status}")

    def scheduler_loop(self):
        scheduler = SchedulerBase(INTERVAL, False)
        scheduler.executeTask = self.update_weather
        print("start scheduler...")
        scheduler.start()

    def start(self):
        threading.Thread(target=self.scheduler_loop, daemon=True).start()
        StartTcpServer(self.context, address=(HOST, PORT))


if __name__ == "__main__":
    server = ModbusSlaveService()
    server.start()