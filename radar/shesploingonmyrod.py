from multiprocessing import Process
from gpiozero import DistanceSensor
from time import sleep
import os

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np
import time

# ------------------------------------------------------------
# MEASURE DISTANCE
# ------------------------------------------------------------
def measure_distance():
    pass

# ------------------------------------------------------------
# POLAR RADAR PLOT SETUP
# ------------------------------------------------------------
plt.ion()
fig = plt.figure(figsize=(7, 7))
ax = plt.subplot(111, projection='polar')

ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_ylim(0, 300)
ax.grid(True)

# Dot for object detection
echo_dot = ax.scatter([], [], color="white", s=30)

plt.show(block=False)
plt.pause(0.1)

print("Servo-driven radar sweep activated...")

def spin_servo():
    import servo_spin
    
p = Process(target=spin_servo)
p.start()

sensor = DistanceSensor(echo=24, trigger=23)
print('Sensor initialized with echo pin:', sensor.echo, 'and trigger pin:', sensor.trigger)

try:
    increasing = True
    angle = 0
    current_time = time.time()
    while True:
        elapsed_time = round((current_time-time.time())%0.5,3)
        print(elapsed_time)
        # Convert to radians for polar chart
        theta = np.deg2rad(angle)

        # Measure distance
        distance = round(sensor.distance, 2) * 100

        if distance is None:
            echo_dot.set_offsets(np.empty((0, 2)))    # hide dot
        else:
            print(f"Angle: {angle}°, Distance: {distance} cm")

            # Color logic
            if distance < 100:
                color = "red"
            elif distance < 200:
                color = "yellow"
            else:
                color = "green"

            echo_dot.set_offsets([[theta, distance]])
            echo_dot.set_color(color)

        # Update plot
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Sweep logic: 0 → 180 → 0 → repeat
        if increasing:
            angle += 2
            if angle >= 180:
                increasing = False
        else:
            angle -= 2
            if angle <= 0:
                increasing = True

        time.sleep(0.02)
finally:
    sensor.close()
    p.kill()
    p.terminate()
    p.join()
    p.close()