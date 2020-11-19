import RPi.GPIO as GPIO
import time

encoderL = 10
pulseCountL = 0
ENA = 2
IN1 = 3
IN2 = 4

def pulseCounterL(channel):
    global pulseCountL
    pulseCountL += 1
    print("pulse count :", pulseCountL)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(encoderL, GPIO.IN)
GPIO.add_event_detect(encoderL, GPIO.RISING, callback = pulseCounterL)

while True:
    pass
