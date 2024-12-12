try:
    import ujson as json
except:
    import json
import requests
import GroenOpladning
from time import sleep

# Initialize GroenOpladning with the specified pins
opladning = GroenOpladning.GroenOpladning(13, 26)

while True:
    print(opladning.getEmissions())
    opladning.calc()
    sleep(300)

# Remember: The ESP32 must be connected to the internet to fetch data from the API.
