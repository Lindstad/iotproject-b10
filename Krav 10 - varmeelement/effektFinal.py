from machine import Pin
from time import sleep, time, localtime
import dht

# --- Pins ---
# DHT11 på GPIO2
dht11 = dht.DHT11(Pin(2))

# MOSFET styring for begge effektmodstande
MOSFET_PIN_1 = Pin(4, Pin.OUT)  # Effektmodstand 1
MOSFET_PIN_2 = Pin(0, Pin.OUT)  # Effektmodstand 2

# Temperaturgrænser
TEMP_THRESHOLD_ON = 5.0   # LMT87: Tærskel for at tænde varme
TEMP_THRESHOLD_OFF = 40.0 # DHT11: Tærskel for at slukke varme

# Variabler
HEATING_ON = False
last_dht11_time = 0
dht11_temp = 0.0

# --- Log Temperatur ---
def log_temperature(temp_lmt87, temp_dht11):
    t = localtime()
    print(f"[{t[3]:02}:{t[4]:02}:{t[5]:02}] LMT87: {temp_lmt87:.2f} °C | DHT11: {temp_dht11:.2f} °C")

# --- Styr Varme ---
def control_heating(temp_lmt87, temp_dht11):
    global HEATING_ON
    log_temperature(temp_lmt87, temp_dht11)

    # Tænd varme, hvis LMT87-temp er under tærsklen
    if not HEATING_ON and temp_lmt87 < TEMP_THRESHOLD_ON:
        print(f"[INFO] Varmen TÆNDES (LMT87 = {temp_lmt87:.2f} °C).")
        MOSFET_PIN_1.on()
        MOSFET_PIN_2.on()
        HEATING_ON = True

    # Sluk varme, hvis DHT11-temp overstiger tærsklen
    elif HEATING_ON and temp_dht11 > TEMP_THRESHOLD_OFF:
        print(f"[INFO] Varmen SLUKKES (DHT11 = {temp_dht11:.2f} °C).")
        MOSFET_PIN_1.off()
        MOSFET_PIN_2.off()
        HEATING_ON = False

    else:
        print(f"[INFO] Ingen ændring - HEATING_ON = {HEATING_ON}")

# --- Startværdi for LMT87 ---
lmt87_temp = 3.0  # Dummy LMT87 startværdi
print(f"\n[INFO] Startværdi for LMT87 er sat til {lmt87_temp:.2f} °C.\n")

# --- Hovedprogram ---
while True:
    try:
        # 1. Læs DHT11 temperatur hvert 2. sekund
        if time() - last_dht11_time > 2:
            dht11.measure()
            dht11_temp = dht11.temperature()
            last_dht11_time = time()

        # 2. Kontroller varmesystemet med LMT87 og DHT11
        control_heating(lmt87_temp, dht11_temp)

        # 3. Vent før næste måling
        sleep(2)

    except Exception as e:
        print(f"[FEJL] {e}")
        sleep(2)
