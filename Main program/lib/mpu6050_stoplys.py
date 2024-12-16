from machine import Pin, I2C
from time import sleep, ticks_ms
from mpu6050 import MPU6050
import sys
from neo_ring import selfneopixel

class mpu:
    def __init__ (self, accel_y, antal_ticks, ring):
        self.start_ticks1 = antal_ticks
        self.acceleration_y_værdi = accel_y
        
        self.start = ticks_ms()
        self.start2 = ticks_ms()
        self.brake = False
        
        i2c = I2C(0)
        self.imu = MPU6050(i2c)
        self.ring = ring        
        
    def instance(self):
        try:
            if ticks_ms() - self.start > 200:
                print(self.imu.get_values()['acceleration y'])
                
                if ticks_ms() - self.start > self.start_ticks1:
                    if self.imu.get_values()['acceleration y'] > self.acceleration_y_værdi:
                        self.ring.set_color(100, 0, 0) 
                        self.start2 = ticks_ms()
                        self.brake = True
                    self.start = ticks_ms()
                    
                if self.brake: 
                    if ticks_ms() - self.start2 > 2000:
                        self.ring.set_color(0, 0, 0) 
                        self.brake = False
                    
        except KeyboardInterrupt:
            print("Ctrl+C pressed - exiting program.")
            sys.exit()







