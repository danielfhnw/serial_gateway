from dataclasses import fields

import serial
import re
import json
import time
from datetime import datetime
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

# ---------- SERIAL ----------
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# ---------- MQTT ----------
load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

client = mqtt.Client()

if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()


def extract_value(line):
    match = re.search(r"(-?\d+\.\d+)", line)
    return float(match.group(1)) if match else None

while True:
    line = ser.readline().decode(errors="ignore").strip()

    if not line:
        continue

    fields = [f.strip() for f in line.split(",")]

    if fields is None or len(fields) < 6:
        continue

    payload = {
        "status": fields[1],
        "weight": float(fields[2]),
        "tare_weight": float(fields[3]),
        "unit": fields[5],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    topic = MQTT_TOPIC

    client.publish(topic, json.dumps(payload))

    print("Published:", payload)

    time.sleep(0.05)