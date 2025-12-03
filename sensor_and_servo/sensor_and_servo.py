from multiprocessing import Process
from gpiozero import DistanceSensor
from time import sleep
import os

def spin_servo():
    import servo_spin
    
p = Process(target=spin_servo)
p.start()

sensor = DistanceSensor(echo=24, trigger=23)
print('Sensor initialized with echo pin:', sensor.echo, 'and trigger pin:', sensor.trigger)

try:
    while True:
        print('Distance: ', sensor.distance * 100)
        sleep(1)
finally:
    sensor.close()
    p.kill()
    p.terminate()
    p.join()
    p.close()