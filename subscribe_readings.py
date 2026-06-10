import json
import paho.mqtt.client as mqtt

# ---------- CONFIG ----------
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "yourname/sensor/weight"  # must match publisher

# ---------- CALLBACKS ----------
def on_connect(client, userdata, flags, rc):
    print("Connected with result code:", rc)
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)

        print("------ NEW MESSAGE ------")
        print("Topic:", msg.topic)
        print("Value:", data.get("value"), data.get("unit"))
        print("Timestamp:", data.get("timestamp"))
        print("------------------------\n")

    except Exception as e:
        print("Error parsing message:", e)
        print("Raw:", msg.payload)

# ---------- SETUP CLIENT ----------
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

# ---------- LOOP ----------
client.loop_forever()