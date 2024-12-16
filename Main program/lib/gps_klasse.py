from uthingsboard.client import TBDeviceMqttClient
from time import sleep, ticks_ms
from machine import reset, UART
import gc
import secrets
from gps_simple import GPS_SIMPLE

class client_program:
    def __init__(self, TBDeviceMqttClient,secrets):
        self.secrets = secrets
        self.TBDeviceMqttClient = TBDeviceMqttClient
        self.client = self.TBDeviceMqttClient(self.secrets.SERVER_IP_ADDRESS, access_token = self.secrets.ACCESS_TOKEN)

    def client_run(self):
        self.client.connect()
        print("connected to thingsboard, starting to send and receive data")
        
class gps_program:
    def __init__(self, UART, GPS_SIMPLE, gc, secrets, client_program, ticks):
        self.delay = ticks
        self.start = ticks_ms()
        
        self.client = client_program
        self.gc = gc
        self.secrets = secrets
        
        self.gps_port = 2                               
        self.gps_speed = 9600                           
        self.uart = UART(self.gps_port, self.gps_speed)           
        self.gps = GPS_SIMPLE(self.uart)

    def get_lat_lon(self):
        self.lat = self.lon = None
        if self.gps.receive_nmea_data():            
                                               
            if self.gps.get_latitude() != -999.0 and self.gps.get_longitude() != -999.0 and self.gps.get_validity() == "A":
                return self.gps.get_latitude(), self.gps.get_longitude()
            else:                              
                return None
        else:
            return None
        
        
    def program (self):
        try:
            if ticks_ms() - self.start > self.delay:
                print(f"free memory: {self.gc.mem_free()}") 
                
                if self.gc.mem_free() < 2000:          
                    print("Garbage collected!")
                    self.gc.collect()                  
                
                self.lat_lon = self.get_lat_lon()           # multiple returns in tuple format
                print(self.lat_lon)
#                 if self.lat_lon:   
#                     self.telemetry = {'latitude': self.lat_lon[0], 'longitude': self.lat_lon[1]}
#                     self.client.send_telemetry(self.telemetry) #Sending telemetry
                self.start = ticks_ms()     
        except KeyboardInterrupt:
            print("Disconnected!")
            self.client.disconnect()               

program = client_program(TBDeviceMqttClient,secrets)
program.client_run()
program2 = gps_program(UART, GPS_SIMPLE, gc, secrets, client_program,1000)


while True:
    program2.program()
                                            


        