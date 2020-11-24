import RPi.GPIO as GPIO
import time

ENA = 2
IN1 = 3
IN2 = 4


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.output(IN1, True)
GPIO.output(IN2, False)
pwm = GPIO.PWM(ENA, 50)
pwm.start(10)

while True:
    pass
