# installing service on unix systems with systemd
sudo cp apez1_mqtt.service /etc/systemd/system/apez1_mqtt.service

sudo systemctl daemon-reload
sudo systemctl enable apez1_mqtt.service

sudo systemctl start apez1_mqtt.service