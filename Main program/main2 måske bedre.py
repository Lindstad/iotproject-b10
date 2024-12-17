# Krav 4
from uthingsboard.client import TBDeviceMqttClient
from gps_klasse import client_program, gps_program
from machine import UART
from gps_simple import GPS_SIMPLE
import gc
from time import ticks_diff

from neo_ring import selfneopixel
from mpu6050 import MPU6050
from machine import I2C

def krav_4(program_4, client, start_4, gc, last_position, last_movement_time, stillness_flag, MOVEMENT_THRESHOLD, STILLNESS_TIME):
    
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
    return start_4, last_position, last_movement_time, stillness_flag

def krav_6(start_6, brake, brake_start, imu, ring):
    print(imu.get_values()['acceleration y'])
    
 
    if imu.get_values()['acceleration y'] > 1500:
        ring.set_color(100, 0, 0) 
        brake_start = ticks_ms()
        brake = True
    start_6 = ticks_ms()
        
    if brake: 
        if ticks_ms() - brake_start > 2000:
            ring.set_color(0, 0, 0) 
            brake = False
    return start_6, brake, brake_start

client = client_program(TBDeviceMqttClient, secrets)
client.client_run()

program_4 = gps_program(UART, GPS_SIMPLE)
ring = selfneopixel(12,26)
ring.set_color(0,0,0)
start_4 = ticks_ms()
interval_4 = 1000

last_position = None
last_movement_time = ticks_ms()
stillness_flag = False
MOVEMENT_THRESHOLD = 0.0002
STILLNESS_TIME = 3 * 1 * 1000  


start_6 = ticks_ms()
interval_6 = 200
brake = False
brake_start = ticks_ms()
i2c = I2C(0)
imu = MPU6050(i2c)


while True:
    #sende til thingsboard er ikke med i program
    try:
        if ticks_ms() - start_4 > interval_4:
            start_4, last_position, last_movement_time, stillness_flag = krav_4(program_4, client, start_4, gc, last_position, last_movement_time, stillness_flag, MOVEMENT_THRESHOLD, STILLNESS_TIME)
        
        if ticks_ms() - start_6 > interval_6:
            start_6, brake, brake_start = krav_6(start_6, brake, brake_start, imu, ring)
        
    except KeyboardInterrupt:
        print("aa")