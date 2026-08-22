import json
import os
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "myhome/sensor/data"
CLIENT_ID = "data-collector-004"
DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

def on_connect(client, userdata, flags, rc,properties):
    if rc == 0:
        print(" 数据采集器已连接 ")
        client.subscribe(TOPIC)
    else:
        print(f"连接失败: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"收到:{data}")
        filename = os.path.join(DATA_DIR, f"{datetime.now():%Y-%m-%d}.jsonl")
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(data,ensure_ascii=False) + "\n")
        print(f" 已保存到{filename}")
    except Exception as e:
        print(f"处理消息出错：{e}")

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=CLIENT_ID,
)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
