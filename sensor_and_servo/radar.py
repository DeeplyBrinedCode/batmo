from multiprocessing import Process, Queue
from gpiozero import DistanceSensor, AngularServo
from time import sleep, time
import servo_spin
import os

def spin():
    exec(open('servo_spin.py').read())

def radar():
    try:
        radar_data = []
        data_passed = False
        p = Process(target=spin)
        p.start()
        sensor = DistanceSensor(echo=24, trigger=23)
        print('Sensor initialized with echo pin:', \
            sensor.echo, 'and trigger pin:', sensor.trigger)
        start_time = time()
        while True:
            elapsed_time = (time() - start_time)%1
            distance = round(sensor.distance * 100, 2)
            angle = round(elapsed_time/0.5*180,2)
            if angle <= 180:
                data_passed = False
                radar_data.append([angle, distance])
            elif data_passed is False:
                print(radar_data)
                radar_data = []
                data_passed = True
            sleep(0.02)
    finally:
        p.kill()
        p.terminate()
        p.join()
        p.close()
        
radar()