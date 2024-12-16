from neo_ring import selfneopixel
from time import sleep
from mpu6050_stoplys import mpu

ring = selfneopixel(12,26)
run = mpu(1500,ring,10)
while True:
    run.instance()