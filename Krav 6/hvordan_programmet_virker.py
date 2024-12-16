from neo_ring import selfneopixel
from time import sleep
from mpu6050_stoplys import mpu

# Definere værdierne fra neoring
ring = selfneopixel(12,26)
run = mpu(1500,200,ring)
while True:
    run.instance()