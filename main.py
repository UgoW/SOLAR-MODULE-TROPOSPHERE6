import time
from grovepi import *
import json
import paho.mqtt.client as mqtt
from grove_rgb_lcd import *

servomotor0_pin = 3     #Port D5 for servomotor0
servomotor1_pin = 5
potentiometer = 2       #Port A2 for potentiometer
light_sensor1 = 0
light_sensor2 = 1
light_sensor3 = 2

pinMode(light_sensor1, "INPUT")
pinMode(light_sensor2, "INPUT")

# --- Configuration ---
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "junia/solar/data"
CLIENT_ID = "Receiver"
servoAttach(servomotor0_pin)
servoAttach(servomotor1_pin)


# Configuration pour les capteurs
somme_l1 = 0
somme_l2 = 0
somme_l3 = 0
nb_mesures = 0

debut = time.time()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to {BROKER}")
        client.subscribe(TOPIC, qos=1)
        print(f"Subscribed to {TOPIC}")
    else:
        print(f"Connection failed, code: {rc}")


def on_message(client, userdata, msg):
    global somme_l1, somme_l2, somme_l3, nb_mesures
    try:
        payload_text = msg.payload.decode("utf-8")
        payload_json = json.loads(payload_text)
        servoWrite(servomotor0_pin, payload_json.get('azimuth'))
        servoWrite(servomotor1_pin, payload_json.get('elevation'))

        # Light sensor
        l1 = analogRead(light_sensor1)
        l2 = analogRead(light_sensor2)
        l3 = analogRead(light_sensor3)
        somme_l1 += l1
        somme_l2 += l2
        somme_l3 += l3
        nb_mesures += 1
        moyenne_l1 = somme_l1 / nb_mesures
        moyenne_l2 = somme_l2 / nb_mesures
        moyenne_l3 = somme_l3 / nb_mesures

        # LCD
        setRGB(0,255,0)
        setText_norefresh("A0: " + str(moyenne_l1) + "; A1: " + str(moyenne_l2) + "; A2: " + str(moyenne_l3))

        print(f"Received JSON on {msg.topic}: {payload_json}")
        print(f"Azimuth: {payload_json.get('azimuth')}, Elevation: {payload_json.get('elevation')}")
    except json.JSONDecodeError:
        print(f"Received non-JSON payload on {msg.topic}: {msg.payload!r}")


client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, keepalive=60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Stopping...")
    servoDetach(servomotor0_pin)
finally:
    client.disconnect()