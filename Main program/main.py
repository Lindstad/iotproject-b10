# Krav 4
from uthingsboard.client import TBDeviceMqttClient
from gps_klasse import client_program, gps_program
from machine import UART
from gps_simple import GPS_SIMPLE
import gc
from time import ticks_diff
import secrets

client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
client.connect()

program_4 = gps_program(UART, GPS_SIMPLE)

start_4 = ticks_ms()
interval_4 = 1000

STILLNESS_TIME = 3 * 1 * 1000  
MOVEMENT_THRESHOLD = 0.0002
last_position = None
last_movement_time = ticks_ms()
stillness_flag = False

#krav 6
from neo_ring import selfneopixel
from time import sleep
from mpu6050 import MPU6050
from machine import I2C
ring = selfneopixel(12,26)
ring.set_color(0,0,0)

start_6 = ticks_ms()
interval_6 = 200
brake = False
brake_start = ticks_ms()
i2c = I2C(0)
imu = MPU6050(i2c)
test = 0 
while True:
    
    try:
    # Krav 4
        if ticks_ms() - start_4 > interval_4:
            current_time = ticks_ms()
            current_position = program_4.get_lat_lon()
            print(f"free memory: {gc.mem_free()}") 
            if gc.mem_free() < 2000:          
                print("Garbage collected!")
                gc.collect()                           
            print(f"Current position: {current_position}")
            if current_position: 
                telemetry_4 = {'latitude': current_position[0], 'longitude': current_position[1]}
                client.send_telemetry(telemetry_4)
            if last_position:
                lat_diff = abs(current_position[0] - last_position[0])
                lon_diff = abs(current_position[1] - last_position[1])
                moving = lat_diff > MOVEMENT_THRESHOLD or lon_diff > MOVEMENT_THRESHOLD
            else:
                moving = True
                
            if moving:
                last_movement_time = current_time
                if stillness_flag:
                    telemetry = {'latitude': current_position[0], 'longitude': current_position[1]}
                    client.send_telemetry(telemetry)
                    print("Movement detected, telemetry sent:", telemetry)
                    stillness_flag = False

                    
            else:
                if ticks_diff(current_time, last_movement_time) > STILLNESS_TIME:
                    stillness_flag = True
                    print("Cyklen har stået stille i mere end 3 minutter.")

                    
            last_position = current_position
            start_4 = ticks_ms()
            
    # Krav 6    
        if ticks_ms() - start_6 > interval_6:
            print(imu.get_values()['acceleration y'])
            
         
            if imu.get_values()['acceleration y'] > 1500:
                ring.set_color(100, 0, 0) 
                brake_start = ticks_ms()
                brake = True
                test += 1
                telemetry_6 = {'Stoplys': test}
                client.send_telemetry(telemetry_6)
            start_6 = ticks_ms()
                
            if brake: 
                if ticks_ms() - brake_start > 2000:
                    ring.set_color(0, 0, 0) 
                    brake = False
            
    # Krav 
    except Exception as e:
        print(e)


