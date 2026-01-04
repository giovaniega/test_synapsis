import json
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt


class MqttService:


    def __init__(self, broker, port, candidate_name, scheduler):
        self.broker = broker
        self.port = port
        self.candidate_name = candidate_name
        self.publish_topic = f"mqtt/{candidate_name}/data"
        self.subscribe_topic = f"mqtt/{candidate_name}/command"

        self.scheduler = scheduler

        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage


    def connect(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()


    def onConnect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code", rc)
        client.subscribe(self.subscribe_topic)


    def onMessage(self, client, userdata, msg):
        timestamp = self.getTimestamp()
        payload = msg.payload.decode()

        print("-" * 50)
        print("Timestamp :", timestamp)
        print("Action    : Subscribe")
        print("Topic     :", msg.topic)
        print("Data      :", payload)
        print("-" * 50)

        self.handleCommand(payload)


    def publish(self, data):
        payload = json.dumps(data, indent=4)
        result = self.client.publish(self.publish_topic, payload)

        timestamp = self.getTimestamp()
        status = "Success" if result.rc == 0 else "Failed"

        print("-" * 50)
        print("Timestamp :", timestamp)
        print("Action    : Publish")
        print("Topic     :", self.publish_topic)
        print("Data      :")
        print(payload)
        print("State     :", status)
        print("-" * 50)

        return status

    def getTimestamp(self):
        gmt7 = datetime.utcnow() + timedelta(hours=7)
        return gmt7.strftime("%Y-%m-%d %H:%M:%S")

    
    def handleCommand(self, payload):
        payload = payload.strip().lower()

        if payload == "pause":
            self.scheduler.pause()

        elif payload == "resume":
            self.scheduler.resume()

        elif payload.startswith("set_interval:"):
            interval = int(payload.split(":")[1])
            self.scheduler.setInterval(interval)
