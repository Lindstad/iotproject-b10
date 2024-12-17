from uthingsboard.client import TBDeviceMqttClient
from machine import reset, UART
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
    def __init__(self, UART, GPS_SIMPLE):                
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
    

                                            


        