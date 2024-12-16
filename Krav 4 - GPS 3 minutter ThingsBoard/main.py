# Krav 4
from uthingsboard.client import TBDeviceMqttClient
from gps_klasse import client_program, gps_program
from machine import UART
from gps_simple import GPS_SIMPLE
import gc
from time import ticks_diff


program_4_1 = client_program(TBDeviceMqttClient, secrets)
program_4_1.client_run()
program_4 = gps_program(UART, GPS_SIMPLE)
start = ticks_ms()
delay = 3000

STILLNESS_TIME = 3 * 1 * 1000  # 3 minutter i millisekunder
MOVEMENT_THRESHOLD = 0.0002
last_position = None
last_movement_time = ticks_ms()
stillness_flag = False

ring.set_color(0,0,0)
while True:
    # Krav 4
    try:
        
        if ticks_ms() - start > 1000:
            current_time = ticks_ms()
            current_position = program_4.get_lat_lon()
            print(f"free memory: {gc.mem_free()}") 
            if gc.mem_free() < 2000:          
                print("Garbage collected!")
                gc.collect()                           
            print(f"Current position: {current_position}")
            if last_position:
                lat_diff = abs(current_position[0] - last_position[0])
                lon_diff = abs(current_position[1] - last_position[1])
                moving = lat_diff > MOVEMENT_THRESHOLD or lon_diff > MOVEMENT_THRESHOLD
            else:
                moving = True
                
            if moving:
                last_movement_time = current_time
                if stillness_flag:
                    # Send besked om bevægelse
                    telemetry = {'latitude': current_position[0], 'longitude': current_position[1]}
                    client.send_telemetry(telemetry)
                    print("Movement detected, telemetry sent:", telemetry)
                    stillness_flag = False
                    ring.set_color(0,0,0)
                    
            else:
                if ticks_diff(current_time, last_movement_time) > STILLNESS_TIME:
                    stillness_flag = True
                    print("Cyklen har stået stille i mere end 3 minutter.")
                    ring.set_color(0,0,100)
                    
            last_position = current_position
#              if lat_lon:   
#                  telemetry = {'latitude': lat_lon[0], 'longitude': lat_lon[1]}
#                  client.send_telemetry(telemetry) 
            start = ticks_ms()
            
    except Exception as e:
        print(e)

