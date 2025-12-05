from multiprocessing import Process
from gpiozero import DistanceSensor
from time import sleep, time
import os

def spin_servo():
    import servo_spin
    
#p = Process(target=spin_servo)
#p.start()

sensor = DistanceSensor(echo=24, trigger=23)
print('Sensor initialized with echo pin:', sensor.echo, 'and trigger pin:', sensor.trigger)

radar_points = []

try:
    start_time = time()
    while True:
        elapsed_time = round((time() - start_time)%0.5,5)
        angle = elapsed_time*180/0.5
        distance = sensor.distance * 100
        radar_points.append([angle, distance])
        sleep(0.02)
finally:
    sensor.close()
    print(radar_points)
    if p:
        p.kill()
        p.terminate()
        p.join()
        p.close()
