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

        return responsedata['records'][1]['CO2Emission']
    
    def calc(self):
        if self.getEmissions() < 50:
            self.pin_Green.on()
            self.pin_Red.off()
        else:
            self.pin_Green.off()
            self.pin_Red.on()