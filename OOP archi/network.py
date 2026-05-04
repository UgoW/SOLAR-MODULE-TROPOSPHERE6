import json
import paho.mqtt.client as mqtt

class SolarMqttClient:
    def __init__(self, broker, port, topic, tracker, lcd):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.tracker = tracker
        self.lcd = lcd

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connecté au Broker MQTT")
            self.client.subscribe(self.topic, qos=1)
        else:
            print(f"Erreur de connexion : {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode("utf-8"))
            self.tracker.update_servos(data.get('solar_azimuth', 90), 
                                      data.get('solar_elevation', 90))
            
            moyenne = self.tracker.read_average_light()
            self.lcd.show_stats(moyenne)
        except Exception as e:
            print(f"Erreur message : {e}")

    def start(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()