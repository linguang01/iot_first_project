import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json

# ===== 配置区 =====
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "myhome/test"        # 换成你的专属前缀，比如 iot/你的名字/test
CLIENT_ID = "python-pub-003" # 每个人的 ID 要唯一
device_id = "sensor-003"

# 连接成功的一个回调函数
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ 连接 Broker 成功")
    else:
        print(f"❌ 连接失败，错误码: {reason_code}")

# 创建客户端（注意：paho-mqtt 2.x 必须加第一个参数）
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=CLIENT_ID
)
client.on_connect = on_connect

# 连接并启动网络循环
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

# 持续发布消息
try:
    while True:
        msg = json.dumps({
            "device_id": device_id,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": "温度25°C"
        })
        client.publish(TOPIC, msg,qos=1,retain=True)
        print(f"已发送: {msg}")
        time.sleep(6)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("已断开连接")
