from machine import ADC, Pin
from time import sleep

pin_potmeter = 34

class Batteri:
    def __init__(self):
        #config
        self.pin_potmeter = 34

        #object
        self.potmeter_adc = ADC(Pin(pin_potmeter))
        self.potmeter_adc.atten(ADC.ATTN_11DB)
        #adc værdier
        self.x1 = 2798 
        self.y1 = 8.4 
        self.x2 = 1999
        self.y2 = 6.0
        self.a = (self.y2-self.y1) /(self.x2-self.x1)
        self.b = self.y1-self.a*self.x1
    def getADCValue(self):
        
        return self.potmeter_adc.read()
    
    
    def Battery_voltage(self):
        return self.a*self.getADCValue()+self.b
    
    def Battery_procent(self):
        return min((self.Battery_voltage()-3)/1.2*100,100)    
 
    

    