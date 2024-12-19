from machine import Pin
from time import sleep, time
from lmt87 import LMT87
import dht

dht11 = dht.DHT11(Pin(2))
lmt87 = LMT87(35)
mosfet_pin = Pin(4, Pin.OUT)


lmt87_threshold = 30
dht11_threshold = 25

last_dht11_time = 0
start_10 = ticks_ms()
interval_10 = 5000
while True:
    if ticks_ms() - start_10 > interval_10:
        dht11.measure()
        dht11_temp = dht11.temperature()
        lmt87.get_temperature()
        lmt87_temp = int(lmt87.get_temperature())
        if lmt87_temp < lmt87_threshold and dht11_temp < dht11_threshold:
            mosfet_pin.on()
            print(f"varmer on DHT11: {dht11_temp} LMT87: {lmt87_temp}")
        else:
            mosfet_pin.off()
            print(f"varmer off DHT11: {dht11_temp} LMT87: {lmt87_temp}")
        start_10 = ticks_ms()
        
    
    