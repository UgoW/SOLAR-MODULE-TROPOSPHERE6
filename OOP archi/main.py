import time
from hardware import SolarTracker
from display import LcdDisplay
from network import SolarMqttClient

BROKER = "broker.hivemq.com"
TOPIC = "junia/solar/data"

def main():
    tracker = SolarTracker(azimuth_pin=5, elevation_pin=3, light_pin=0)
    display = LcdDisplay(0, 0, 189)
    mqtt_app = SolarMqttClient(BROKER, 1883, TOPIC, tracker, display)

    print("Démarrage du système...")
    mqtt_app.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt demandé...")
    finally:
        mqtt_app.stop()
        tracker.cleanup()
        print("Système arrêté proprement.")

if __name__ == "__main__":
    main()