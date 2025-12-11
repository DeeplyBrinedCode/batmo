import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np
import time

# Polar radar plot setup
plt.ion()
fig = plt.figure(figsize=(7, 7))
ax = plt.subplot(111, projection='polar')

ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_ylim(0, 300)
ax.grid(True)

plt.show(block=False)
plt.pause(0.1)

fig.canvas.draw()
fig.canvas.flush_events()
