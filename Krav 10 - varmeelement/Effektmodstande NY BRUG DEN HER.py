from machine import Pin
from time import sleep
from lmt87 import LMT87
import dht  # Importér DHT-biblioteket

# Initialisering af LMT87-sensoren
lmt87 = LMT87(35)  # Pin 35 til LMT87

# Initialisering af DHT11-sensoren
dht11 = dht.DHT11(Pin(2))  # Data-pin på GPIO 15

# MOSFET-pins
MOSFET_PIN_1 = Pin(4, Pin.OUT)   # Effektmodstand 1
MOSFET_PIN_2 = Pin(0, Pin.OUT)   # Effektmodstand 2

# Temperaturgrænser
TEMP_THRESHOLD_ON = 5.0    # LMT87 - Tænd varme under 5°C
TEMP_THRESHOLD_OFF = 40.0  # DHT11 - Sluk varme over 40°C
HEATING_ON = False

# Funktion til at styre varmen
def control_heating(temp_ambient, temp_modstand):
    global HEATING_ON

    if not HEATING_ON and temp_ambient < TEMP_THRESHOLD_ON:
        print(f"Udendørs temperatur: {temp_ambient:.2f} °C - Varmen TÆNDES.")
        MOSFET_PIN_1.on()
        MOSFET_PIN_2.on()
        HEATING_ON = True

    elif HEATING_ON and temp_modstand > TEMP_THRESHOLD_OFF:
        print(f"Modstandstemperatur: {temp_modstand:.2f} °C - Varmen SLUKKES.")
        MOSFET_PIN_1.off()
        MOSFET_PIN_2.off()
        HEATING_ON = False
    else:
        print(f"Udendørs: {temp_ambient:.2f} °C, Modstand: {temp_modstand:.2f} °C - Ingen ændring.")

# Hovedloop
while True:
    try:
        # Læs temperatur fra LMT87
        temp_ambient = lmt87.get_temperature(avg_exp=6)

        # Læs temperatur fra DHT11
        dht11.measure()
        temp_modstand = dht11.temperature()  # Temperatur i °C fra DHT11

        # Print temperaturerne
        print(f"\nUdendørs temperatur: {temp_ambient:.2f} °C")
        print(f"Modstandstemperatur: {temp_modstand:.2f} °C")

        # Kontrol af varme
        control_heating(temp_ambient, temp_modstand)

    except Exception as e:
        print(f"Fejl: {e}")

    sleep(2)  # Vent 2 sekunder før næste måling
