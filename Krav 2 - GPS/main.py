from gpio_lcd import GpioLcd
import time
import OwnGPS
from dht import DHT11
from machine import Pin


lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)

dht11 = DHT11(Pin(34,Pin.IN))

gps = OwnGPS.OwnGPS(2)
while True:
    lcd.clear()
    lat = 'lat '+str(gps.getData()['latitude'])[:4]
    lon = 'lon '+str(gps.getData()['longitude'])[:4]
    lcd.move_to(0,0)
    lcd.putstr('spd '+str(gps.getData()['speed'])[:3])
    lcd.move_to(0,1)
    lcd.putstr(lat)
    lcd.move_to(len(lat)+1,1)
    lcd.putstr(lon)
    dht11.measure()
    print(dht11.temperature())
    time.sleep(1)
    
    
    
    
    