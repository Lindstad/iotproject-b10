# Krav 4
from uthingsboard.client import TBDeviceMqttClient
from gps_klasse import client_program, gps_program
from machine import UART
from gps_simple import GPS_SIMPLE
import gc

program_4_1 = client_program(TBDeviceMqttClient, secrets)
program_4_1.client_run()
program_4 = gps_program(UART, GPS_SIMPLE)
start = ticks_ms()
delay = 3000

# Krav 6
from neo_ring import selfneopixel
from mpu6050_stoplys import mpu

ring = selfneopixel(12,26)
program_6 = mpu(1500,ring,200)

while True:
    # Krav 4
    try:
        if ticks_ms() - start > 1000:
            print(f"free memory: {gc.mem_free()}") 
            if gc.mem_free() < 2000:          
                print("Garbage collected!")
                gc.collect()                  
            lat_lon = program_4.get_lat_lon()           
            print(lat_lon)
#              if lat_lon:   
#                  telemetry = {'latitude': lat_lon[0], 'longitude': lat_lon[1]}
#                  client.send_telemetry(telemetry) 
            start = ticks_ms()
            
    except Exception as e:
        print(e)