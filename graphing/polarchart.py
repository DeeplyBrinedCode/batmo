import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np
import time

# ------------------------------------------------------------
# GPIO SETUP
# ------------------------------------------------------------
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
SERVO_PIN = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Servo PWM at 50 Hz
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

# ------------------------------------------------------------
# SERVO CONTROL (angle 0–180)
# ------------------------------------------------------------
def set_angle(angle):
    duty = 2 + (angle / 18)   # map angle → duty cycle
    servo.ChangeDutyCycle(duty)
    time.sleep(0.02)

# ------------------------------------------------------------
# MEASURE DISTANCE
# ------------------------------------------------------------
def measure_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.03)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = time.time() + 0.04

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    distance = (pulse_end - pulse_start) * 17150
    return round(distance, 2)

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

# ------------------------------------------------------------
# MAIN SWEEP LOOP
# ------------------------------------------------------------
try:
    increasing = True
    angle = 0

    while True:

        # Move servo
        set_angle(angle)

        # Convert to radians for polar chart
        theta = np.deg2rad(angle)

        # Measure distance
        distance = measure_distance()

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

except KeyboardInterrupt:
    print("\nStopping radar.")

finally:
    servo.stop()
    GPIO.cleanup()