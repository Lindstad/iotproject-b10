from machine import Pin
from time import sleep, time, localtime
import dht

# Pins
dht11 = dht.DHT11(Pin(2))
MOSFET_PIN = Pin(4, Pin.OUT)

# Temperaturgrænser
TEMP_THRESHOLD_ON = 5.0
TEMP_THRESHOLD_OFF = 35.0  # Lavere for test

HEATING_ON = False
last_dht11_time = 0
dht11_temp = 0.0

# Log funktion
def log_temperature(temp_lmt87, temp_dht11):
    t = localtime()
    print(f"[{t[3]:02}:{t[4]:02}:{t[5]:02}] LMT87: {temp_lmt87:.2f} °C | DHT11: {temp_dht11:.2f} °C")

# Styr varme
def control_heating(temp_lmt87, temp_dht11):
    global HEATING_ON
    log_temperature(temp_lmt87, temp_dht11)

    if not HEATING_ON and temp_lmt87 < TEMP_THRESHOLD_ON:
        print(f"[INFO] Varmen TÆNDES (LMT87 = {temp_lmt87:.2f} °C).")
        MOSFET_PIN.on()
        HEATING_ON = True
    elif HEATING_ON and temp_dht11 > TEMP_THRESHOLD_OFF:
        print(f"[INFO] Varmen SLUKKES (DHT11 = {temp_dht11:.2f} °C).")
        MOSFET_PIN.off()
        HEATING_ON = False
    else:
        print(f"[INFO] Ingen ændring - HEATING_ON = {HEATING_ON}")

# Startværdi for LMT87
lmt87_temp = 3.0
print(f"\n[INFO] Startværdi for LMT87 er sat til {lmt87_temp:.2f} °C.\n")

# Hovedprogram
while True:
    try:
        if time() - last_dht11_time > 2:
            dht11.measure()
            dht11_temp = dht11.temperature()
            last_dht11_time = time()
        control_heating(lmt87_temp, dht11_temp)
        sleep(5)  # Giv tid til opvarmning
    except Exception as e:
        print(f"[FEJL] {e}")
        sleep(2)
