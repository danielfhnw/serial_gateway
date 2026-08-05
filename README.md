# Code zum Raspi 4 der die Waage über RS232 d ausliest

.env File mit folgendem Inhalt
```
SERIAL_PORT=/dev/ttyUSB0 
BAUD_RATE=9600
MQTT_BROKER=1.2.3.4
MQTT_PORT=1234
MQTT_USER=user
MQTT_PASSWORD=pass
MQTT_TOPIC=topic
```


## Boot-Service

```
[Unit]
Description=Start the serial gateway
After=network-online.target systemd-udev-settle.service
Wants=network-online.target systemd-udev-settle.service

[Service]
Type=simple
User=admin
WorkingDirectory=/home/admin/serial_gateway
ExecStartPre=/bin/bash -c 'until [ -e /dev/ttyUSB0 ]; do sleep 1; done'
ExecStartPre=/bin/bash -c 'until ping -c1 SERVER_IP >/dev/null 2>&1; do sle>
ExecStart=/home/admin/vigor_handbox/.venv/bin/python /home/admin/serial_gateway>
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target


```
