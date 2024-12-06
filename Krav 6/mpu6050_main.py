from machine import I2C
from machine import Pin
from time import sleep, ticks_ms
from mpu6050 import MPU6050
import sys
from neopixel import NeoPixel

#Initialisering af I2C objekt
i2c = I2C(0)


#Initialisering af Neopixel objekt
n = 12 #antallet af led
p = 26 #pin 26 er der hvor neopixels på educaboarded er. hvis pin sættes på med den virker de sammen. ellers kan 12,13,14 bruges
np = NeoPixel(Pin(p),n) #create NeoPixel instance

def set_color(r,g,b):
    for i in range(n):
        np[i] = (r,g,b)
    np.write()
    
set_color(100,100,0)
sleep(1)
set_color(0,0,0)
start = ticks_ms()
start2 = ticks_ms()
brake = False
#Initialisering af mpu6050 objekt
imu = MPU6050(i2c)
while True:
    try:
        print(imu.get_values()['acceleration y'])
        
        if ticks_ms() - start > 200:
            if imu.get_values()['acceleration y'] > 1500:
                set_color(100, 0, 0)  # Turn LED red
                start2 = ticks_ms()
                brake = True #Starter timer nede ved brake
            start = ticks_ms()
        
        if brake: #hvis break bliver true starter 
            if ticks_ms() - start2 > 2000:
                set_color(0, 0, 0) 
                brake = False
                
    except KeyboardInterrupt:
        print("Ctrl+C pressed - exiting program.")
        sys.exit()


