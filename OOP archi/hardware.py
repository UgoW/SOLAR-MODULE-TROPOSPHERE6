from time import time

from grovepi import *

class SolarTracker:
    def __init__(self, azimuth_pin, elevation_pin, light_pin, initial_azimuth=90, initial_elevation=90):
        self.azimuth_pin = azimuth_pin
        self.elevation_pin = elevation_pin
        self.light_pin = light_pin
        self.initial_azimuth = initial_azimuth
        self.initial_elevation = initial_elevation

        pinMode(self.light_pin, "INPUT")
        servoAttach(self.azimuth_pin)
        servoAttach(self.elevation_pin)

        servoWrite(self.azimuth_pin, self.initial_azimuth)
        servoWrite(self.elevation_pin, self.initial_elevation)
        
        self.somme_l1 = 0
        self.nb_mesures = 0

    def update_servos(self, azimuth, elevation):
        safe_azimuth = max(0, min(180, int(azimuth)))
        safe_elevation = max(0, min(110, int(elevation)))
        
        while(self.initial_azimuth != safe_azimuth and self.initial_elevation != safe_elevation):
            step = 1 if self.initial_azimuth < safe_azimuth else -1
            self.initial_azimuth += step
            servoWrite(self.azimuth_pin, self.initial_azimuth)
            time.sleep(0.02)

        while(self.initial_elevation != safe_elevation):
            step = 1 if self.initial_elevation < safe_elevation else -1
            self.initial_elevation += step
            servoWrite(self.elevation_pin, self.initial_elevation)
            time.sleep(0.02)


    def read_average_light(self):
        val = analogRead(self.light_pin)
        self.somme_l1 += val
        self.nb_mesures += 1
        return self.somme_l1 / self.nb_mesures

    def cleanup(self):
        servoDetach(self.azimuth_pin)
        servoDetach(self.elevation_pin)