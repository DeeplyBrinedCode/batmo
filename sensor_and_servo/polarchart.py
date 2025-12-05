import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np
import time

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
except KeyboardInterrupt:
    print("\nStopping radar.")

finally:
    pass