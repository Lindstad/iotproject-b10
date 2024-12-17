from neopixel import NeoPixel
from machine import Pin

class selfneopixel:
    def __init__ (self,led,pin): 
        self.antal_led = led
        self.pin_nummer = Pin(pin,Pin.OUT)

self.np = NeoPixel(Pin(self.pin_nummer),self.antal_led)
                      
    def set_color(self,r,g,b):
        for i in range(self.antal_led):
            self.np[i] = (r,g,b)
        self.np.write()
    
