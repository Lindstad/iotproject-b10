# -*- coding: utf-8 -*-

from uthingsboard.client import TBDeviceMqttClient
from time import sleep, ticks_ms, ticks_diff
from machine import reset, UART
import gc
import secrets
from gps_simple import GPS_SIMPLE

# GPS-konfiguration
gps_port = 2
gps_speed = 9600
uart = UART(gps_port, gps_speed)
gps = GPS_SIMPLE(uart)

# ThingsBoard-konfiguration
client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token=secrets.ACCESS_TOKEN)
client.connect()
print("Connected to ThingsBoard")

# Konfigurationsparametre
STILLNESS_TIME = 3 * 60 * 1000  # 3 minutter i millisekunder
MOVEMENT_THRESHOLD = 0.0002    # Minimum ændring i latitude/longitude for at betragte bevægelse

# Variabler til tilstandsstyring
last_position = None
last_movement_time = ticks_ms()
stillness_flag = False

def get_lat_lon():
    """Hent latitude og longitude fra GPS-modulet."""
    if gps.receive_nmea_data():
        if gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0 and gps.get_validity() == "A":
            return gps.get_latitude(), gps.get_longitude()
    return None

while True:
    try:
        print(f"Free memory: {gc.mem_free()}")
        if gc.mem_free() < 2000:
            print("Garbage collected!")
            gc.collect()

        current_time = ticks_ms()
        current_position = get_lat_lon()

        if current_position:
            print(f"Current position: {current_position}")

            # Hvis vi har en tidligere position, sammenlign med den aktuelle
            if last_position:
                lat_diff = abs(current_position[0] - last_position[0])
                lon_diff = abs(current_position[1] - last_position[1])
                moving = lat_diff > MOVEMENT_THRESHOLD or lon_diff > MOVEMENT_THRESHOLD
            else:
                moving = True  # Første gang antager vi, at cyklen er i bevægelse

            if moving:
                last_movement_time = current_time
                if stillness_flag:
                    # Send besked om bevægelse
                    telemetry = {'latitude': current_position[0], 'longitude': current_position[1]}
                    client.send_telemetry(telemetry)
                    print("Movement detected, telemetry sent:", telemetry)
                    stillness_flag = False
            else:
                if ticks_diff(current_time, last_movement_time) > STILLNESS_TIME:
                    stillness_flag = True
                    print("Cyklen har stået stille i mere end 3 minutter.")

            # Opdater den seneste position
            last_position = current_position

        sleep(10)  # Reducer hyppigheden af GPS-opdateringer

    except KeyboardInterrupt:
        print("Disconnected!")
        client.disconnect()
        reset()