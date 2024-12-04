try:
     import ujson as json
except:
    import json
import requests
import GroenOpladning

opladning = GroenOpladning.GroenOpladning(26)

print(opladning.getEmissions())
opladning.calc()