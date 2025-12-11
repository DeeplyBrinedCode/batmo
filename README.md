# batmo
**Main repository for ECEGR 2000 final project**

![IMG_1524](https://github.com/user-attachments/assets/b44fb513-f408-4014-be90-3ee305e28877)

**Plan:**
Make an remote controlled car that can detect obstacles

**Setup:**

**Pico-Pico Connections:**

Both Picos should be placed side by side, with VSYS and GND connected

Any GPIO pin connected or file uploaded can be done to either Pico

**Pico-Servo Connections:**

Servo GND (brown wire) to Pico GND

Servo Vcc (red wire) to Pico 3v3 or Pico 5v if available

S1 (orange wire) to Pico GPIO6

S2 unconnected

<img width="581" height="269" alt="image" src="https://github.com/user-attachments/assets/e910def1-6b8f-4961-bba8-65e68d6512c7" />

**Pico-Reciever Connections:**

Reciever GND to Pico GND

Reciever Vcc to Pico 3V *Eliminates need for voltage divider, but decreases range and accuracy

Reciever Echo to Pico GPIO27

Reciever Trig to Pico GPIO28

**Hardware Connections:**

Pico-bot has a battery connected to it, just ensure the battery is plugged in

Second Pico can be taped to Pico-bot with electrical tape

Ultrasonic Reciever can be taped with electrical tape to Servo chassis

Servo base can be taped with electrical tape to Pico-bot

**Code Installation:**

Replace SSID, PASSWORD, and RPI_SERVER_IP in pico/main.py with the relevant strings for your device

Install files in /pico directory to Pico controller using the USB connector and an interpreter

Install files in /rpi directory to Raspberry Pi with git
