import time
from datetime import datetime, timedelta


class SchedulerBase:

    def __init__(self, interval, debug=False):
        self.interval = interval
        self.debug = debug
        self.is_active = True


    def start(self):
        if self.debug:
            print("[DEBUG] Scheduler mulai..")

        while True:
            time.sleep(self.interval)
            if self.is_active:
                self.executeTask()
            else:
                self.printInactive()



    def executeTask(self):
        raise NotImplementedError("executeTask error/kosong")


    def pause(self):
        self.is_active = False


    def resume(self):
        self.is_active = True


    def setInterval(self, interval):
        if interval > 0:
            self.interval = interval


    def printInactive(self):
        print(
            "({}) - Scheduler Inactive".format(self.getGmt7Timestamp())
        )


    def getGmt7Timestamp(self):
        gmt7 = datetime.utcnow() + timedelta(hours=7)
        return gmt7.strftime("%Y-%m-%d %H:%M:%S")
