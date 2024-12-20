from gpio_lcd import GpioLcd
from machine import I2C, Pin
import random
import time
import OwnGPS
import gc
import secrets
from haversine import haversine


lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)
gps = OwnGPS.OwnGPS(2)
distance = 0
while True:
    pos1 = False
    pos2 = False
    if gps.isValid():
        lat1 = gps.getData()['latitude']
        lon1 = gps.getData()['longitude']
        pos1 = True
    else:
        pos1 = False
    time.sleep(3)
    if gps.isValid():
        lat2 = gps.getData()['latitude']
        lon2 = gps.getData()['longitude']
        pos2 = True
    else:
        pos2 = False
    if pos1 and pos2:
        new_distance = haversine(lat1,lon1,lat2,lon2) 
        distance += new_distance
        if new_distance < 5:
            lcd.clear()
            calc = 0.1082*distance
            lcd.move_to(0,0)
            lcd.putstr('Du har sparet')
            lcd.move_to(0,1)
            displaystr = str(calc)+" g CO2"
            lcd.putstr(displaystr)
            stat = random.randint(0,2)
            if stat == 0:
                bottlewatercalc = calc/250
                lcd.move_to(0,2)
                lcd.putstr("Det er "+str(bottlewatercalc)[:3]+" flasker")
            elif stat == 1:
                if distance == 0:
                    ecocalc = 0
                else:
                    ecocalc = 0.00371/distance   
                lcd.move_to(0,2)
                lcd.putstr("Det er "+str(ecocalc)[:3]+" kr")
            elif stat == 2:
                if distance == 0:
                    kcalcalc = 0
                else:
                    kcalcalc = 0.0231/distance
                lcd.move_to(0,2)
                lcd.putstr("Det er "+str(kcalcalc)[:3]+" kcal")
        else:
            lcd.clear()
            