from grovepi import *

class SolarTracker:
    def __init__(self, azimuth_pin, elevation_pin, light_pin):
        self.azimuth_pin = azimuth_pin
        self.elevation_pin = elevation_pin
        self.light_pin = light_pin
        
        pinMode(self.light_pin, "INPUT")
        servoAttach(self.azimuth_pin)
        servoAttach(self.elevation_pin)
        
        self.somme_l1 = 0
        self.nb_mesures = 0

    def update_servos(self, azimuth, elevation):
        safe_azimuth = max(0, min(180, int(azimuth)))
        safe_elevation = max(0, min(110, int(elevation)))
        
        servoWrite(self.azimuth_pin, safe_azimuth)
        servoWrite(self.elevation_pin, safe_elevation)

    def read_average_light(self):
        val = analogRead(self.light_pin)
        self.somme_l1 += val
        self.nb_mesures += 1
        return self.somme_l1 / self.nb_mesures

    def cleanup(self):
        servoDetach(self.azimuth_pin)
        servoDetach(self.elevation_pin)