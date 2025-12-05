from multiprocessing import Process, Queue
from gpiozero import DistanceSensor, AngularServo
from time import sleep, time
import servo_spin
import os
import graph

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
        i=0
        prev_dist = 0
        while True:
            elapsed_time = (time() - start_time)%1
            distance = round(sensor.distance * 100, 2)
            angle = round(elapsed_time/0.5*180,2)
            if angle <= 180:
                data_passed = False
                if distance == 100 or prev_dist != distance:
                    radar_data.append([angle, distance])
                    prev_dist = distance
            elif data_passed is False:
                i += 1
                print('send',i)
                graph.update_plot_from_list(radar_data)
                radar_data = []
                data_passed = True
            sleep(0.02)
    finally:
        sensor.close()
        p.kill()
        p.terminate()
        p.join()
        p.close()
        
radar()