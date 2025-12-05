from gpiozero import AngularServo
from time import sleep
import os

if __name__ == '__main__':
    print('Process running with pid:', os.getpid())

    servo = AngularServo(14, min_angle=0, max_angle=180, \
                         min_pulse_width=0.0005, max_pulse_width=0.0025, \
                         frame_width=0.02)

    try:
        while True:
            servo.min()
            sleep(0.50)
            servo.max()
            sleep(0.50)
    finally:
        servo.close()
