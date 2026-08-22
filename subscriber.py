import paho.mqtt.client as mqtt
import json

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "myhome/test"
CLIENT_ID = "python-sub-002"

def on_connect(client, userdata, flags, reason_code,properties):
    if reason_code == 0:
        print("订阅者已连接")
        client.subscribe(TOPIC)
    else:
        print("连接失败：{reason_code}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    try:
        data = json.loads(payload)  # 将JSON字符串转换为字典
        device_id = data.get("device_id")  # 提取device_id
        timestamp = data.get("timestamp")
        sensor_data = data.get("data")
        print(f"收到消息: 设备ID={device_id} | 时间={timestamp} | 数据={sensor_data}")
    except json.JSONDecodeError:
        print(f"消息格式错误: {payload}")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=CLIENT_ID
)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
