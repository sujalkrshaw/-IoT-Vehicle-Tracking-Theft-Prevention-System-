import paho.mqtt.client as mqtt
import json

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "iot/vehicle/tracking"

client = mqtt.Client()

client.connect(BROKER, PORT, 60)

def publish_location(data):

    payload = json.dumps(data)

    client.publish(
        TOPIC,
        payload
    )