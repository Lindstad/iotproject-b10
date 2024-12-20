# Krav 7 - Beregning af resterende batterilevetid
from ina219_lib import INA219

i2c_port = 0
ina219_i2c_addr = 0x40

i2c = I2C(i2c_port)
ina219 = INA219(i2c, ina219_i2c_addr)

# INA219 initialisering
ina219.set_calibration_16V_400mA()

BATTERY_CAPACITY = 1800  # Batteriets kapacitet i mAh

# Beregning af resterende batterilevetid
current = ina219.get_current()  # Strømforbrug i mA
if current > 0:
    remaining_battery_time = (battery_percentage * BATTERY_CAPACITY) / current  # Formlen
else:
    remaining_battery_time = float('inf')  # Uendelig tid, hvis ingen strømforbrug

# Udskriv resterende levetid
print(f"Krav 7: Resterende batterilevetid: {remaining_battery_time:.2f} timer")
