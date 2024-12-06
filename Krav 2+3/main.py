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


#initialisering af I2C objektet
i2c = I2C(0)
#initialisering af MPU6050 objektet
imu = MPU6050(i2c)
#LCD display definition
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)


#Opretter et OwnGPS objekt, som vi selv har lavet
gps = OwnGPS.OwnGPS(2)
#Opretter et batteri objekt, som vi selv har lavet
batteri = batteri.Batteri()
#Opretter forbindelse til ThingsBoard
client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)
client.connect()

#Grader karakter
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
    lat = 'lat:'+str(gps.getData()['latitude'])[:5]         #Træk latitude fra vores eget gps objekt og skærer nogle decimaler fra  
    lon = 'lon:'+str(gps.getData()['longitude'])[:5]        #Træk longitude fra vores eget gps objekt og skærer nogle decimaler fra  
    temp = str(imu.get_values()['temperature celsius'])[:4] #Mål temperatur og skærer nogle decimaler fra
    spd = 'spd:'+str(gps.getData()['speed'])[:3]            #Træk retning fra gpsobjektet. 
    #Printer alt data på lcd-displayet 
    lcd.move_to(0,0)
    lcd.putstr(spd)
    lcd.move_to(len(spd)+2,0)
    lcd.putstr('NESW:'+str(gps.getData()['course']))
    lcd.move_to(0,1)
    lcd.putstr(lat)
    lcd.move_to(len(lat)+1,1)
    lcd.putstr(lon)
    lcd.move_to(0,2)
    lcd.putstr('bat:'+str(batteri.Battery_procent())[:5]+"%")
    lcd.move_to(0,3)
    lcd.putstr("Temp:"+temp)
    lcd.move_to(len("Temp"+temp)+1,3)
    lcd.putchar(chr(0))
    #Sender data til ThingsBoard
    telemetry = {'latitude': gps.getData()['latitude'], 'longitude': gps.getData()['longitude'],'temperature':temp,'batteryLevel':batteri.Battery_procent(),'course':gps.getData()['course']}
    client.send_telemetry(telemetry)
    #Printer i konsollen 
    print("lat: "+str(gps.getData()['latitude']),"lon: "+str(gps.getData()['longitude']))
    print("Speed: "+str(gps.getData()['speed'])[:3])
    print('temperature: '+temp)
    print('Retning: '+str(gps.getData()['course']))
    print("batteriprocent: "+str(batteri.Battery_procent()))
    print()
    #Sleep timer - burde erstattes af en ticks funktion. Så den ikke blokerer. 
    time.sleep(3)
    