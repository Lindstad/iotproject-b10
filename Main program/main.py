import OwnGPS
from machine import ADC, Pin
from gpio_lcd import GpioLcd
from uthingsboard.client import TBDeviceMqttClient
from gps_klasse import client_program, gps_program
from machine import UART
from gps_simple import GPS_SIMPLE
import gc
from time import ticks_diff
import secrets
from neo_ring import selfneopixel
from mpu6050 import MPU6050
from machine import I2C
from ina219_lib import INA219
from dht import DHT11
from lmt87 import LMT87

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)

potmeter_adc = ADC(Pin(36))
potmeter_adc.atten(ADC.ATTN_11DB)

adc1 = 2591
U1 = 6.0
adc2 = 3629
U2 = 8.4

a = (U1-U2)/(adc1-adc2)
b = U2 - a*adc2

def batt_voltage(adc_v):
    u_batt = a*adc_v+b
    return u_batt

def batt_percentage(u_batt):
    without_offset = (u_batt-6)
    normalized = without_offset / (8.4-6.0)
    percent = normalized * 100
    return percent

start_1 = ticks_ms()
interval_1 = 1000

gps = OwnGPS.OwnGPS(2)
symbol_grader = bytearray([0b00111,
              0b00101,
              0b00111,
              0b00000,
              0b00000,
              0b00000,
              0b00000,
              0b00000])
lcd.custom_char(0,symbol_grader)

start_2 = ticks_ms()
interval_2 = 3000


client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
client.connect()
print("connected to thingsboard, starting to send and receive data")

program_4 = gps_program(UART, GPS_SIMPLE)

start_4 = ticks_ms()
interval_4 = 1000

STILLNESS_TIME = 3 * 60 * 1000  
MOVEMENT_THRESHOLD = 0.0002
last_position = None
last_movement_time = ticks_ms()
stillness_flag = False

ring = selfneopixel(12,26)
ring.set_color(0,0,0)

start_6 = ticks_ms()
interval_6 = 200
brake = False
brake_start = ticks_ms()
i2c = I2C(0)
imu = MPU6050(i2c)
test = 0

i2c_port = 0
ina219_i2c_addr = 0x40

i2c = I2C(i2c_port)
ina219 = INA219(i2c, ina219_i2c_addr)
print("\nINA219 Current Measurement Program\n")

ina219.set_calibration_16V_400mA()
start_7 = ticks_ms()
interval_7 = 1000

def handler(req_id, method, params):
    print(f'Response {req_id}: {method}, params {params}')
    print(params, "params type:", type(params))
    try:
        if method == "toggle_alarm":
            if params == True:
                print("Alarm on")
                ring.set_color(10,0,0)
            else:
                print("Alarm off")
                ring.set_color(0,0,0)

    except TypeError as e:
        print(e)
start_9 = ticks_ms()
interval_9 = 1000

dht11 = DHT11(Pin(2))
lmt87 = LMT87(35)
mosfet_pin = Pin(4, Pin.OUT)

lmt87_threshold = 30
dht11_threshold = 30

# last_dht11_time = 0    SLET evt da vi ikke bruger den
start_10 = ticks_ms()
interval_10 = 5000

start_11 = ticks_ms
interval_11 = 5000
moving_11 = True
distance = 0

while True:
    try:
        if ticks_ms() - start_1 > interval_1:
            val = potmeter_adc.read()
            battery_percent = batt_voltage(val)/8.4*100
            print(f'\nKrav 1: U percentage {round(battery_percent)}%')
            telemetry_1 = {'batteri': battery_percent}
            client.send_telemetry(telemetry_1)
            start_1 = ticks_ms()

        if ticks_ms() - start_4 > interval_4:
            current_time = ticks_ms()
            current_position = program_4.get_lat_lon()
            if gc.mem_free() < 2000:          
                gc.collect()
                print("Trash collected")
            print(f"Krav 4: Current position: {current_position}")
            if last_position:
                lat_diff = abs(current_position[0] - last_position[0])
                lon_diff = abs(current_position[1] - last_position[1])
                moving = lat_diff > MOVEMENT_THRESHOLD or lon_diff > MOVEMENT_THRESHOLD
            else:
                moving = True
            if moving:
                last_movement_time = current_time
                if stillness_flag:
                    telemetry_4 = {'latitude4': current_position[0], 'longitude4': current_position[1]}
                    client.send_telemetry(telemetry)
                    print("Movement detected, telemetry sent:", telemetry)
                    stillness_flag = False 
            else:
                if ticks_diff(current_time, last_movement_time) > STILLNESS_TIME:
                    stillness_flag = True
                    print("Cyklen har stået stille i mere end 3 minutter.")
            last_position = current_position
            start_4 = ticks_ms()
            
        if ticks_ms() - start_2 > interval_2 and moving_11:
            if gps.isValid():
                lcd.clear()
                lat = 'lat:'+str(current_position[0])[:5]          
                lon = 'lon:'+str(current_position[1])[:5]          
                temp = str(imu.get_values()['temperature celsius'])[:5] 
                spd = 'spd:  '+str(gps.getData()['speed'])[:3]            
                course = 'NESW:'+str(gps.getData()['course'])
                lcd.move_to(0,0)
                lcd.putstr(spd)
                lcd.move_to(len(spd)+2,0)
                lcd.putstr(course)
                lcd.move_to(0,1)
                lcd.putstr(lat)
                lcd.move_to(len(lat)+1,1)
                lcd.putstr(lon)
                lcd.move_to(0,2)
                lcd.putstr(f"bat: {str(int(battery_percent))}%")
                lcd.move_to(0,3)
                lcd.putstr("Tem: "+temp)
                lcd.move_to(len("Tem"+temp)+1,3)
                lcd.putchar(chr(0))
                telemetry_3 = {'latitude': gps.getData()['latitude'],
                             'longitude': gps.getData()['longitude'],
                             'temperature':temp,
                             'batteryLevel':battery_percent,
                             'course':gps.getData()['course']}
                client.send_telemetry(telemetry_3)
            start_2 = ticks_ms()
            
        if ticks_ms() - start_6 > interval_6:
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

        if ticks_ms() - start_7 > interval_7:
            current = ina219.get_current()
            remaning_current_time = ((battery_percent * 1800) / current) / 60
            
            print("Krav 7:", str(current) + " mA")
            print("Krav 7:", str(remaning_current_time) + " Timer tilbage")
            telemetry_7 = {'stromforbrug': current,
                           "restlevetid": remaning_current_time}
            client.send_telemetry(telemetry_7)
            start_7 = ticks_ms()

        if ticks_ms() - start_9 > interval_9:
            client.set_server_side_rpc_request_handler(handler) 
            client.check_msg()
            start_9 = ticks_ms()
            
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
            
    except Exception as e:
        print(e)
