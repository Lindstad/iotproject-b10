try:
     import ujson as json
except:
    import json
import requests
from machine import Pin

class GroenOpladning:
    def __init__(self, pin1,pin2):
        self.pin_Green = Pin(pin1,Pin.OUT)
        self.pin_Red = Pin(pin2,Pin.OUT)
        self.pin_Green.off()
        self.pin_Red.off()
        
    def getEmissions(self):
        response = requests.get(
            url = "https://api.energidataservice.dk/dataset/CO2Emis?limit=5")

        responsedata = response.json()

        # En tommelfingerregel siger, at når der udledes under 50 gram CO2 pr. kwh strøm, er strømmen grøn.”
        # 'records' for listen, [1] for DK2, 'CO2Emission' for værdien.
        return responsedata['records'][1]['CO2Emission']
    
    # Denne funktion bruger vi til at styre om en pin skal tændes eller slukkes,
    # altså til at styre ladekræsen
    def calc(self):
        if self.getEmissions() < 50:
            self.pin_Green.on()
            self.pin_Red.off()
        else:
            self.pin_Green.off()
            self.pin_Red.on()