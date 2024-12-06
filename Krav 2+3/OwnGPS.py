from machine import UART
from gps_simple import GPS_SIMPLE
from machine import Pin
import _thread
import time


class OwnGPS:
    def __init__(self,gpsPort):
        self.gpsPort = gpsPort                                 # Hvilken port GPSen er koblet op på 
        self.gpsSpeed = 9600                                   # Baudrate på dataforbindelsen til GPSen
        self.gpsEcho = False                                   # Ikke sikker på hvad den gør, men den printer ikke data hvis den er False
        self.gpsAllNMEA = False                                # Ikke sikker på hvad den gør
        self.uart = UART(self.gpsPort, self.gpsSpeed)          # Laver et UART projekt
        self.gps = GPS_SIMPLE(self.uart, self.gpsAllNMEA)      # Laver et GPS objekt baseret på uart objektet og gpsAllNMEA variablen
        self.output = {'utc_year':'',                          # Laver en dict med alle de mulige outputs vi kan få fra gpsen
                       'utc_minutes':'',
                       'latitude':'',
                       'longitude':'',
                       'altitude':'',
                       'fix_quality':'',
                       'satellites':'',
                       'hdop':'',
                       'validity':'',
                       'speed':'',
                       'course':'',
                       'frames_received':''
                       }

        
    def getData(self):                                                         # Funktion til at trække data ud fra OwnGPS klassen
        if (self.gps.receive_nmea_data(self.gpsEcho)):                         # Ikke sikker på hvad den gør, men med gpsEcho sat til False printer den ikke 
            self.output['utc_year'] = self.gps.get_utc_year()                  # Alle efterfølgende linjer gemmer data i output dict
            self.output['utc_minutes'] = self.gps.get_utc_minutes()
            self.output['latitude'] = self.gps.get_latitude()
            self.output['longitude'] = self.gps.get_longitude()
            self.output['altitude'] = self.gps.get_altitude()
            self.output['fix_quality'] = self.gps.get_fix_quality()
            self.output['satellites'] = self.gps.get_satellites()
            self.output['hdop'] = self.gps.get_hdop()
            self.output['validity'] = self.gps.get_validity()
            self.output['speed'] = self.gps.get_speed()
            self.output['course'] = self.gps.get_course()
            self.output['frames_received'] = self.gps.get_frames_received()

            return self.output                                                #Returnere output dict med ny data
    