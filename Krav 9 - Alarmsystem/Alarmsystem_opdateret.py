from machine import Pin, PWM, I2C
from time import sleep
from uthingsboard.client import TBDeviceMqttClient
import secrets
from mpu6050 import MPU6050  


BUZZER_PIN = 14
buzzer_pin = Pin(BUZZER_PIN, Pin.OUT)
buzzer_pwm = PWM(buzzer_pin, freq=2000, duty=0)

RED_PIN = 26
led1 = Pin(RED_PIN, Pin.OUT)


i2c = I2C(0)  
imu = MPU6050(i2c)

MOVEMENT_THRESHOLD = 30000  


alarm_activated = False


def LED(led, times, delay):
    for _ in range(times):
        led.on()
        sleep(delay)
        led.off()
        sleep(delay)


"""def buzzer_alarm(pwm_object, frequency, tone_duration, silence_duration):
    pwm_object.duty(512)
    pwm_object.freq(frequency)
    sleep(tone_duration)
    pwm_object.duty(0)
    sleep(silence_duration)
"""
# Alarmfunktion
def Alarm():
    print("Alarm")
    LED(led1, 5, 0.5)  
    #buzzer_alarm(buzzer_pwm, 3000, 1, 0.2)  


client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token=secrets.ACCESS_TOKEN)
client.connect()
print("Connected to ThingsBoard, starting to send and receive data")

def handler(req_id, method, params):
    global alarm_activated
    print(f'Response {req_id}: {method}, params {params}')
    try:
        if method == "toggle_alarm":
            if params:  
                alarm_activated = True
                print("Alarmsystem aktiveret")
            else:  
                alarm_activated = False
                print("Alarmsystem deaktiveret")
                led1.off()
                buzzer_pwm.duty(0)
    except Exception as e:
        print(f"Error: {e}")

client.set_server_side_rpc_request_handler(handler)


previous_values = imu.get_values()  

while True:
    client.check_msg()  
    
    if alarm_activated:  
        current_values = imu.get_values()
        delta_x = abs(current_values["acceleration x"] - previous_values["acceleration x"])
        delta_y = abs(current_values["acceleration y"] - previous_values["acceleration y"])
        delta_z = abs(current_values["acceleration z"] - previous_values["acceleration z"])
        
        
        if delta_x > MOVEMENT_THRESHOLD or delta_y > MOVEMENT_THRESHOLD or delta_z > MOVEMENT_THRESHOLD:
            Alarm()  
        previous_values = current_values  

    sleep(0.5)  
