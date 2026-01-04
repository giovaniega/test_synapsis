import time
import threading
from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime, timedelta
from function.scheduler_service import SchedulerBase

HOST = "localhost"
PORT = 5020

class ModbusMasterService:

    def __init__(self):
        self.client = ModbusTcpClient(HOST, port=PORT)
        self.status_toggle = 0

    def timestamp_gmt7(self):
        return (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")

    def read_data(self):
        rr = self.client.read_holding_registers(0, 3, unit=1)

        temp = rr.registers[0] / 100
        hum  = rr.registers[1] / 100
        stat = rr.registers[2]

        print(f"({self.timestamp_gmt7()}) | Suhu: {temp:.2f}°C | Hum: {hum:.2f}% | Status: {stat}")

    def write_status(self):
        self.status_toggle = 1 if self.status_toggle == 0 else 0
        self.client.write_register(2, self.status_toggle)
        print(f"[MASTER] Write Status -> {self.status_toggle}")

    def start(self):
        self.client.connect()

        scheduler_read = SchedulerBase(5, False)
        scheduler_write = SchedulerBase(30, False)

        scheduler_read.executeTask = self.read_data
        scheduler_write.executeTask = self.write_status

        threading.Thread(target=scheduler_read.start, daemon=True).start()
        threading.Thread(target=scheduler_write.start, daemon=True).start()


        while True:
            time.sleep(1)


if __name__ == "__main__":

    master = ModbusMasterService()
    master.start()
