from grove_rgb_lcd import *

class LcdDisplay:
    def __init__(self, r=0, g=255, b=0):
        setRGB(r, g, b)

    def show_stats(self, value):
        setText_norefresh(f"Lumière: {value:.2f}")