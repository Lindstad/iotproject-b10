from gpio_lcd import GpioLcd
from machine import I2C
import time
import OwnGPS
import gc
import secrets
from haversine import haversine

gps = OwnGPS.OwnGPS(2)
distance = 0
while True:
    if gps.isValid():
        lat1 = gps.getData()['latitude']
        lon1 = gps.getData()['longitude']
        lat2 = gps.getData()['latitude']
        lon2 = gps.getData()['longitude']
        #distance += haversine(lat1,lon1,lat2,lon2)
        print(type(lat1),type(lon1),lat1,lon1)
        time.sleep(1)
