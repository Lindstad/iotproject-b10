from machine import UART
from gps_simple import GPS_SIMPLE
from machine import Pin
import _thread
import time


class OwnGPS:
    def __init__(self,gpsPort):
        self.gpsPort = gpsPort                                 # ESP32 UART port, Educaboard ESP32 default UART port
        self.gpsSpeed = 9600                             # UART speed, defauls u-blox speed
        self.gpsEcho = False                              # Echo NMEA frames: True or False
        self.gpsAllNMEA = False                          # Enable all NMEA frames: True or False
        self.uart = UART(self.gpsPort, self.gpsSpeed)    # UART object creation
        self.gps = GPS_SIMPLE(self.uart, self.gpsAllNMEA)     # GPS object creation
        self.output = {'utc_year':'',
                       'utc_minutes':'',
                       'latitude':-999.0,
                       'longitude':-999.0,
                       'altitude':'',
                       'fix_quality':'',
                       'satellites':'',
                       'hdop':'',
                       'validity':'',
                       'speed':'',
                       'course':'',
                       'frames_received':''
                       }

        
    def getData(self):
        return self.output
        
    def isValid(self):
        if (self.gps.receive_nmea_data(self.gpsEcho)):
            self.output['utc_year'] = self.gps.get_utc_year()
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
            return True
        else:
            return False
