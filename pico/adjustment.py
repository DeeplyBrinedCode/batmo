# main.py
import network
import socket
import time
from machine import Pin, PWM

# --- CONFIGURATION ---
AP_SSID = "PicoBot_Control"
AP_PASSWORD = "pico_robot_password"

# DRV8833 Pins
A_IN1_PIN = 0
A_IN2_PIN = 1
B_IN1_PIN = 2
B_IN2_PIN = 3

FREQUENCY = 1000
MAX_DUTY = 65025

# --- GLOBAL STATE ---
speed_percent = 0      # -100 to 100 (- reverse, + forward)
turn_bias_percent = 0  # -100 left, +100 right
is_running = False

# Pin Setup
motor_pins = {
    'R1': Pin(A_IN1_PIN, Pin.OUT),
    'R2': Pin(A_IN2_PIN, Pin.OUT),
    'L1': Pin(B_IN1_PIN, Pin.OUT),
    'L2': Pin(B_IN2_PIN, Pin.OUT)
}

pwm_R1 = PWM(motor_pins['R1'])
pwm_R2 = PWM(motor_pins['R2'])
pwm_L1 = PWM(motor_pins['L1'])
pwm_L2 = PWM(motor_pins['L2'])

for pwm_obj in [pwm_R1, pwm_R2, pwm_L1, pwm_L2]:
    pwm_obj.freq(FREQUENCY)

def connect_to_wifi():
    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    wlan.config(essid=AP_SSID, password=AP_PASSWORD)
    while not wlan.active():
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Access Point running at {ip}")
    return ip

def set_motor(pwm_fwd, pwm_rev, duty_percent):
    duty = int((abs(duty_percent)/100) * MAX_DUTY)
    if duty_percent >= 0:
        pwm_fwd.duty_u16(duty)
        pwm_rev.duty_u16(0)
    else:
        pwm_fwd.duty_u16(0)
        pwm_rev.duty_u16(duty)

def update_motors():
    global speed_percent, turn_bias_percent
    if not is_running or speed_percent == 0:
        for pwm_obj in [pwm_R1, pwm_R2, pwm_L1, pwm_L2]:
            pwm_obj.duty_u16(0)
        return

    # Tank motor calculation
    right_speed = speed_percent - turn_bias_percent
    left_speed = speed_percent + turn_bias_percent
    # Clamp -100 to 100
    right_speed = max(-100, min(100, right_speed))
    left_speed = max(-100, min(100, left_speed))

    set_motor(pwm_R1, pwm_R2, right_speed)
    set_motor(pwm_L1, pwm_L2, left_speed)

def process_joystick(x_percent, y_percent):
    """x_percent: -100 left, +100 right, y_percent: -100 reverse, +100 forward"""
    global speed_percent, turn_bias_percent, is_running
    speed_percent = y_percent
    turn_bias_percent = -x_percent  # invert X for intuitive turning
    is_running = speed_percent != 0
    update_motors()

# --- MAIN SERVER ---
try:
    ip = connect_to_wifi()
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print(f"Server running at http://{ip}")

    while True:
        conn, _ = s.accept()
        request = conn.recv(1024)
        try:
            path = request.decode('utf-8').split(' ')[1]
        except:
            path = "/"

        # Parse joystick command
        if path.startswith("/joystick"):
            try:
                # Example: /joystick?x=30&y=-50
                query = path.split("?")[1]
                params = dict(param.split("=") for param in query.split("&"))
                x = int(params.get("x", 0))
                y = int(params.get("y", 0))
                process_joystick(x, y)
                response = '{"status":"ok"}'
            except:
                response = '{"status":"error"}'
        else:
            # Serve simple HTML joystick page
            response = """<!DOCTYPE html>
<html>
<head>
<title>PicoBot Joystick</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
#joystick { width:200px;height:200px;background:#ccc;border-radius:50%;position:relative;margin:50px auto; }
#stick { width:60px;height:60px;background:#888;border-radius:50%;position:absolute;left:70px;top:70px;touch-action:none; }
button { width:100px;height:50px;margin:10px; font-size:18px; }
</style>
</head>
<body>
<div id="joystick"><div id="stick"></div></div>
<script>
let stick = document.getElementById('stick');
let joystick = document.getElementById('joystick');
let origin = {x:100,y:100};
let maxDistance = 100;
let x_percent=0, y_percent=0;

function sendData(x,y){
  fetch(`/joystick?x=${x}&y=${y}`).catch(console.log);
}

stick.addEventListener('pointerdown', function(e){
  stick.setPointerCapture(e.pointerId);
});
stick.addEventListener('pointermove', function(e){
  let rect = joystick.getBoundingClientRect();
  let x = e.clientX - rect.left;
  let y = e.clientY - rect.top;
  let dx = x - origin.x;
  let dy = origin.y - y; // invert Y
  let dist = Math.sqrt(dx*dx + dy*dy);
  if(dist>maxDistance){ dx*=maxDistance/dist; dy*=maxDistance/dist; }
  stick.style.left = (origin.x + dx -30)+'px';
  stick.style.top = (origin.y - dy -30)+'px';
  x_percent = Math.round(dx);
  y_percent = Math.round(dy);
  sendData(x_percent, y_percent);
});
stick.addEventListener('pointerup', function(e){
  stick.style.left = '70px';
  stick.style.top = '70px';
  sendData(0,0);
});
</script>
</body>
</html>"""
        # Send response
        conn.send('HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}'.format(len(response), response))
        conn.close()
except Exception as e:
    print("Error:", e)
    for pwm_obj in [pwm_R1, pwm_R2, pwm_L1, pwm_L2]:
        pwm_obj.duty_u16(0)
    time.sleep(1)
