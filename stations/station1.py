import json
import os
import random
import time

import paho.mqtt.client as mqtt


def get_config():
    """Get configuration from environment variables."""
    return {
        "station_id": os.getenv("STATION_ID", "WS-XX"),
        "interval": int(os.getenv("INTERVAL", "5")),
        "broker": "mosquitto",
        "port": 1883,
        "topic": "weather",
    }


def generate_temperature():
    """Generate temperature reading with 2% chance of error sentinel value."""
    if random.random() < 0.02:
        return -999
    return round(random.uniform(15, 30), 1)


def generate_humidity():
    """Generate humidity reading with 2% chance of out-of-range error values."""
    if random.random() < 0.02:
        return round(random.uniform(-100, 200), 1)
    return round(random.uniform(30, 60), 1)


def create_data_payload(station_id, temperature, humidity):
    """Create JSON payload for MQTT message."""
    return {
        "stationId": station_id,
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def main():
    """Main loop for weather station simulation."""
    config = get_config()
    station_id = config["station_id"]
    interval = config["interval"]
    broker = config["broker"]
    port = config["port"]
    topic = config["topic"]

    client = mqtt.Client()
    client.connect(broker, port, 60)

    while True:
        temperature = generate_temperature()
        humidity = generate_humidity()

        # Simulate random total failure (0.5% chance)
        if random.random() < 0.005:
            print("Simulierter Totalausfall")
            break

        data = create_data_payload(station_id, temperature, humidity)
        client.publish(topic, json.dumps(data))
        print(f"[{station_id}] Published: {data}")
        time.sleep(interval)


if __name__ == "__main__":
    main()
