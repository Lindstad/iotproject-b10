try:
    import ujson as json
except:
    import json
import requests
import GroenOpladning
from time import sleep

# Initialize GroenOpladning with the specified pins
opladning = GroenOpladning.GroenOpladning(13, 26)

print(opladning.getEmissions())
opladning.calc()

# Remember: The ESP32 must be connected to the internet to fetch data from the API.
