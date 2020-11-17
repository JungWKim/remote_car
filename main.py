import RPi.GPIO as GPIO

def settings():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(2, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)

    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

def main():
    try:
        settings()
        pwmL = GPIO.PWM(2, 50)#frequency
        pwmR = GPIO.PWM(22, 50)
        pwmL.start(10)#duty cycle
        pwmR.start(10)#frequency and duty cycle are different!!!
        GPIO.output(3, True)
        GPIO.output(4, False)
        GPIO.output(17, True)
        GPIO.output(27, False)

        while True:
            pass

    except KeyboardInterrupt:
        #이렇게 하지 않으면 종료후에 왼쪽 바퀴가 저절로 돌게 됨
        pwmL.ChangeFrequency(0)
        pwmR.ChangeFrequency(0)
        pwmL.stop()
        pwmR.stop()
        GPIO.cleanup()

if __name__=="__main__":
    main()
