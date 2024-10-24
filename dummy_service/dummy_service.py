import paho.mqtt.client as mqtt
import random
import time

def publish_sensor_data():
    client = mqtt.Client()
    client.connect("mqtt", 1883, 60)
    while True:
        sensor_value = random.uniform(20.0, 30.0)
        client.publish("sensor/data", sensor_value)
        time.sleep(5)

if __name__ == "__main__":
    publish_sensor_data()
