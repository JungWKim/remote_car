import RPi.GPIO as GPIO
import time
import serial

ENA = 2
IN1 = 3
IN2 = 4
ENB = 22
IN3 = 17
IN4 = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

pwmL = GPIO.PWM(ENA, 50)
pwmL.start(60)
pwmR = GPIO.PWM(ENB, 50)
pwmR.start(80)
GPIO.output(IN1, True)
GPIO.output(IN2, False)
GPIO.output(IN3, True)
GPIO.output(IN4, False)


while True:
#    current_time = time.time()
#    time_gap = current_time - prev_time
#    if time_gap >= 0.500:
#        prev_time = current_time
#        rpmL = int((pulseCountL / ppr) * (60.0 / time_gap))
#        pulseCountL = 0
#        print("rpm :", rpmL)
    try:
        pass
    except KeyboardInterrupt:
        pwmL.ChangeDutyCycle(0)
        pwmL.stop()
        GPIO.cleanup()
