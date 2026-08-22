import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "myhome/sensor/data"
CLIENT_ID = "sensor-sim-003"

def on_connect(client, userdata, flags, reason_code,properties):
    print(f"传感器模拟器连接状态：{reason_code}")

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=CLIENT_ID,
)
client.on_connect = on_connect
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

try:
    while True:
        data = {
            "device_id": "sensor-001",
            "temperature": round(random.uniform(20, 30), 1),
            "humidity": round(random.uniform(40, 70), 1),
            "status": "online",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        client.publish(TOPIC, json.dumps(data))
        print(f" 发送: {data}")
        time.sleep(5)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()