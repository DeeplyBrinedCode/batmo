from gpiozero import AngularServo
from time import sleep
import os

servo = AngularServo(14, min_angle=0, max_angle=180, \
                     min_pulse_width=0.0005, max_pulse_width=0.0025, \
                     frame_width=0.02)

servo.min()
sleep(0.6)
servo.close()