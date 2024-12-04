try:
     import ujson as json
except:
    import json
import requests

response = requests.get(
    url = "https://api.energidataservice.dk/dataset/CO2Emis?limit=5")

responsedata = response.json()


# En tommelfingerregel siger, at når der udledes under 50 gram CO2 pr. kwh strøm, er strømmen grøn.”
# 'records' for listen, [1] for DK2, 'CO2Emission' for værdien.
print(responsedata['records'][1]['CO2Emission'])