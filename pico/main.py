"""File to run on Pico-bot startup.

This file will run upon powering the Pico-bot on, so the Flask server on the Raspberry Pi should already be up and running. 
Using a connected servo and distance sensor, the code performs a servo sweep and creates a list of data. That data will
then be sent to the Raspberry Pi over the Flask server.

Attributes:
    SSID (str): The SSID of the network the Raspberry Pi is connected to.
    PASSWORD (str): The password of the network the Raspberry Pi is connected to.
    RPI_SERVER_IP (str): The IP address of the Raspberry Pi.
    RPI_PORT (int): The Flask port to connect to the Raspberry Pi.
    SERVO_PIN (int): The GPIO pin on the Pico board to which the servo's signal wire should be connected.
    PWM_FREQ (int): Frequency for the servo.
    TRIG_PIN (int): The GPIO pin on the Pico board to which the distance sensor's trigger should be connected.
    ECHO_PIN (int): The GPIO pin on the Pico board to which the distance sensor's echo should be connected.
    SOUND_SPEED_CM_PER_US (int): The speed of sound in centimeters per microsecond.
    MAX_DISTANCE_CM (int): The maximum distance for the distance sensor.
    sensor_data (list of list of int): Set of data points to send to Raspberry Pi.
"""
import network
import time
import urequests as requests
import json
import machine, utime
from machine import Pin
import adjustment

# CONSTANTS
SSID = 'SU-ECE-LAB'
PASSWORD = 'FaraDay8086!'
RPI_SERVER_IP = '10.133.0.147' 
RPI_PORT = 5000
PICO_DATA_URL = f"http://{RPI_SERVER_IP}:{RPI_PORT}/pico_data"
RPI_DATA_URL = f"http://{RPI_SERVER_IP}:{RPI_PORT}/get_rpi_data"

SERVO_PIN = 6
PWM_FREQ = 50

TRIG_PIN = 28
ECHO_PIN = 27

SOUND_SPEED_CM_PER_US = 0.0343 
MAX_DISTANCE_CM = 500

# Servo Setup
# Create a PWM object on the specified pin, set frequency
pwm = machine.PWM(machine.Pin(SERVO_PIN))
pwm.freq(PWM_FREQ)

# Convert angle (0-180) to nanosecond pulse width (approx 0.5ms to 2.5ms)
# For 50Hz (20ms period): ~1ms = 5%, ~2ms = 10% duty cycle range
def set_angle(angle):
    """Set angle of servo.

    Converts angle in degrees into a pulse width, then sets a duty cycle for the servo.
    
    Args:
        angle (int): The angle in degrees to turn the servo to.
    """
    # duty_ns expects microseconds (µs) for 50Hz
    # 500µs for 0 deg, 2500µs for 180 deg (adjust if needed)
    pulse_width_us = 500 + (angle / 180.0) * 2000 # 500µs to 2500µs
    pwm.duty_ns(int(pulse_width_us * 1000)) # Convert µs to ns
    
# USR Setup
# Initialize the trigger pin as an output
trigger = Pin(TRIG_PIN, Pin.OUT)
trigger.value(0) # Ensure trigger is low initially

# Initialize the echo pin as an input
echo = Pin(ECHO_PIN, Pin.IN)

# Variables for frequency calculation
MEASUREMENTS_TO_AVERAGE = 50 
read_count = 0
start_time = utime.ticks_ms() # Use millisecond ticks for frequency tracking

def get_distance():
    """Gets distance from distance sensor.

    Returns:
        int: Distance in centimeters between sensor and object.

    Raises:
        TimeoutError: Exception raised if distance sensor does not respond quickly. Ususually means something isn't plugged in right.
    """
    # Send the 10us Trigger Pulse
    trigger.value(1)
    utime.sleep_us(10)
    trigger.value(0)

    # Wait for the Echo Pulse (Signal HIGH)
    pulse_start = 0
    pulse_end = 0

    # Wait for the pin to go HIGH (start of the echo pulse)
    timeout = utime.ticks_ms()
    while echo.value() == 0:
        pulse_start = utime.ticks_us()
        if utime.ticks_diff(utime.ticks_ms(), timeout) > 200: # Timeout after 200ms
            return -1 # Error/Timeout
    
    # Wait for the pin to go LOW (end of the echo pulse)
    timeout = utime.ticks_ms()
    while echo.value() == 1:
        pulse_end = utime.ticks_us()
        if utime.ticks_diff(utime.ticks_ms(), timeout) > 200: # Timeout after 200ms
            return -1 # Error/Timeout

    # Calculate Time and Distance
    pulse_duration_us = utime.ticks_diff(pulse_end, pulse_start)

    # Distance calculation: Distance = (Time * Speed of Sound) / 2
    # Division by 2 because the time is for the sound to travel there AND back.
    distance_cm = (pulse_duration_us * SOUND_SPEED_CM_PER_US) / 2
    
    # Clamp distance to the maximum range
    if distance_cm > MAX_DISTANCE_CM:
        return MAX_DISTANCE_CM
        
    return distance_cm

sensor_data = []

# Network Setup
def connect_to_wifi():
    """Connects the Pico W to the specified Wi-Fi network.

    Returns:
        network.WLAN: The wireless local area network that the Pico tries to connect to.

    Raises:
        RuntimeError: Raises if Pico fails to connect to Network. Ensure Flask server is running and credentials are correct.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('Network connection failed')
    else:
        print('Connected')
        status = wlan.ifconfig()
        print( 'IP Address:', status[0] )
        return wlan

# Communication Functions

def send_data_to_rpi(wlan, uptime):
    """Sends a POST request with Pico sensor data to the RPI server.

        Args:
            wlan (network.WLAN): The network that the Pico is connected to
            uptime (Any): Not sure.
    """
    global sensor_data
    # The data the Pico is sending back
    pico_payload = {
        "sensor data": sensor_data 
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(PICO_DATA_URL, headers=headers, data=json.dumps(pico_payload))
        response.close()
        print("Pico POST successful.")
    except Exception as e:
        print(f"Pico POST failed: {e}")

def get_data_from_rpi():
    """Fetches data from the RPI server via a GET request.

    This function is currently defunct, but could be used in future applications.

    Returns:
        list: some list of data
    """
    try:
        response = requests.get(RPI_DATA_URL)
        rpi_data = response.json()
        response.close()
        
        # Process the received list (e.g., control an LED, change behavior)
        received_list = rpi_data.get('rpi_data')
        print(f"Pico GET successful. Received list: {received_list}")
        
        # Example processing: check the first element of the list
        print(recieved_list)
        
        return received_list
        
    except Exception as e:
        print(f"Pico GET failed: {e}")
        return None

# Main Loop
def main():
    """Runs main loop.

    Connects to wifi, then begins operating servo and sensor and sending data to Raspberry Pi. Data is only collected on the sweep 
    from 0 to 180 degrees. The code can be modified to collect in both directions, but currently the single direction is used to 
    allow time for the data to be sent to the Raspberry Pi.
    """
    global sensor_data
    try:
        wlan = connect_to_wifi()
        start_time = time.time()
    except RuntimeError as e:
        print(f"Fatal error: {e}. Cannot proceed.")
        return

    # Communication Interval
    SEND_INTERVAL_SECONDS = 0.6
    last_send_time = time.time()

    # Set servo to angle 0
    set_angle(0)
    time.sleep(0.5) # Wait for servo to move
    
    while True:
        current_time = time.time()
        uptime = current_time - start_time
        
         # Sweep from 0 to 180 degrees in 5 degree increments
        for angle in range(0, 180, 5):
            set_angle(angle)
            utime.sleep_ms(20) # Wait for servo to move
            sensor_data.append([angle, get_distance()]) # add angle and distance data to sensor data list

        # Sweep back from 180 to 0 degrees in 5 degree increments
        for angle in range(180, 0, -5):
            set_angle(angle)
            utime.sleep_ms(20) # Wait for servo to move
            
        send_data_to_rpi(wlan, uptime)

        # Reset sensor data for next sweep
        sensor_data = []
        
        last_send_time = current_time
            
        # RPI Initiated Communication (RPI -> Pico), currently defunct
        # The Pico can check for new RPI data on every loop iteration, or less often.
        get_data_from_rpi() 

main()


