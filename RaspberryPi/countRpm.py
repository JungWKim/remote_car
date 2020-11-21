import RPi.GPIO as GPIO
import time

prev_time = 0.0
encoderL = 10
pulseCountL = 0
ENA = 2
IN1 = 3
IN2 = 4
ppr = 235

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

pwmL = GPIO.PWM(ENA, 50)
pwmL.start(50)
GPIO.output(IN1, True)
GPIO.output(IN2, False)

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
