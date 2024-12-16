try:
     import ujson as json
except:
    import json
import requests
import GroenOpladning
from time import sleep

opladning = GroenOpladning.GroenOpladning(13,26)

while True:
    opladning.calc()
    print(opladning.getEmissions())
    sleep(5 * 60)