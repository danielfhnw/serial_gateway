import serial
import re
import json
import time
from datetime import datetime
import paho.mqtt.client as mqtt

# ---------- SERIAL ----------
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# ---------- PUBLIC MQTT BROKER ----------
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "dj1000/sensor/weight"  # IMPORTANT: make it unique

# ---------- SETUP ----------
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

def extract_value(line):
    match = re.search(r"(-?\d+\.\d+)", line)
    return float(match.group(1)) if match else None

while True:
    line = ser.readline().decode(errors="ignore").strip()

    if not line:
        continue

    value = extract_value(line)

    if value is None:
        continue

    payload = {
        "value": value,
        "unit": "g",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    topic = MQTT_TOPIC

    client.publish(topic, json.dumps(payload))

    print("Published:", payload)

    time.sleep(0.1)