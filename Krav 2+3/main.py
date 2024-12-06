from gpio_lcd import GpioLcd
from machine import I2C
import time
import OwnGPS
import gc
import secrets
import batteri
import sys
from uthingsboard.client import TBDeviceMqttClient
from mpu6050 import MPU6050



i2c = I2C(0)
imu = MPU6050(i2c)
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)



gps = OwnGPS.OwnGPS(2)
batteri = batteri.Batteri()
client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
client.connect()


custom_chr = bytearray([0b00111,
              0b00101,
              0b00111,
              0b00000,
              0b00000,
              0b00000,
              0b00000,
              0b00000])
lcd.custom_char(0,custom_chr)


while True:
    lcd.clear()
    lat = 'lat:'+str(gps.getData()['latitude'])[:5]
    lon = 'lon:'+str(gps.getData()['longitude'])[:5]
    temp = str(imu.get_values()['temperature celsius'])[:4]
    lcd.move_to(0,0)
    spd = 'spd:'+str(gps.getData()['speed'])[:3]
    lcd.putstr(spd)
    lcd.move_to(len(spd)+2,0)
    lcd.putstr('NESW:'+str(gps.getData()['course']))
    lcd.move_to(0,1)
    lcd.putstr(lat)
    lcd.move_to(len(lat)+1,1)
    lcd.putstr(lon)
    lcd.move_to(0,2)
    lcd.putstr(str(batteri.Battery_procent())[:5]+"%")
    lcd.move_to(0,3)
    lcd.putstr("Temp:"+temp)
    lcd.move_to(len("Temp"+temp)+1,3)
    lcd.putchar(chr(0))
    telemetry = {'latitude': gps.getData()['latitude'], 'longitude': gps.getData()['longitude'],'temperature':temp,'batteryLevel':batteri.Battery_procent(),'course':gps.getData()['course']}
    client.send_telemetry(telemetry)
    print("lat: "+str(gps.getData()['latitude']),"lon: "+str(gps.getData()['longitude']))
    print("Speed: "+str(gps.getData()['speed']))
    print('temperature: '+temp)
    print('Retning: '+str(gps.getData()['course']))
    print("batteriprocent: "+str(batteri.Battery_procent()))
    print()
    time.sleep(3)
    