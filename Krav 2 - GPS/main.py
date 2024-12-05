from machine import UART
from gps_simple import GPS_SIMPLE

import _thread
import time
import OwnGPS

gps = OwnGPS.OwnGPS(2)
while True:
    print(gps.getData())
    gps.drawOnLCD()
    time.sleep(1)