from time import sleep
from machine import Pin

class MockGroenOpladning:
    def __init__(self, pin1, pin2):
        self.pin_Green = Pin(pin1, Pin.OUT)
        self.pin_Red = Pin(pin2, Pin.OUT)
        self.pin_Green.off()
        self.pin_Red.off()
        self.emission_toggle = True  # Bruges til at skifte værdi

    def getEmissions(self):
        # Skifter mellem grøn og ikke-grøn energi
        self.emission_toggle = not self.emission_toggle
        return 40 if self.emission_toggle else 60

    def calc(self):
        if self.getEmissions() < 50:
            self.pin_Green.on()
            self.pin_Red.off()
        else:
            self.pin_Green.off()
            self.pin_Red.on()

# Initialiser mock-klassen
opladning = MockGroenOpladning(13, 26)

# Accepttesten: Kør 10 iterationer med skiftende energi
for i in range(10):
    opladning.calc()
    sleep(2)  # Vent 2 sekund mellem hver iteration