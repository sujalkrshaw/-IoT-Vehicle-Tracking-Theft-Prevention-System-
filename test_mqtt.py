from mqtt.mqtt_client import publish_location

publish_location(
    {
        "latitude": 22.5726,
        "longitude": 88.3639,
        "status": "SAFE"
    }
)

print("MQTT Message Sent")