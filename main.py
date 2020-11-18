import RPi.GPIO as GPIO
import time
import sys
import termios
import tty

pulseCountL = 0
pulseCountR = 0
encoderL = 10
encoderR = 9
ENA = 2
IN1 = 3
IN2 = 4
ENB = 22
IN3 = 17
IN4 = 27

def pulseCounterL(channel):
    global pulseCountL
    pulseCountL += 1


def pulseCounterR(channel):
    global pulseCountR
    pulseCountR += 1


def settings():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    #Left side
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(encoderL, GPIO.IN)
    GPIO.add_event_detect(encoderL, GPIO.RISING, callback = pulseCounterL)

    #Right side
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    GPIO.setup(encoderR, GPIO.IN)
    GPIO.add_event_detect(encoderR, GPIO.RISING, callback = pulseCounterR)

    global pwmL, pwmR
    pwmL = GPIO.PWM(ENA, 50)#frequency
    pwmL.start(0)#duty cycle
    pwmR = GPIO.PWM(ENB, 50)
    pwmR.start(0)#frequency and duty cycle are different!!!


def show_usage():
    print("----------How to Use-----------")
    print("")
    print("             W    ")
    print("                           U")
    print("          A  S  D  ")
    print("                           J")
    print("             X    ")
    print("")
    print("    W : forward")
    print("    A : left spinning")
    print("    D : right spinning")
    print("    X : backward")
    print("")
    print("    W + A : go left")
    print("    W + D : go right")
    print("    X + A : go back left")
    print("    X + D : go back right")
    print("")
    print("    U : speed up")
    print("    J : speed down")
    print("")
    print("Press any keys......")


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def changeSpeed():
    pwmL.ChangeDutyCycle(speedL)
    pwmR.ChangeDutyCycle(speedR)


def main():
    settings()
    show_usage()
    global speedL, speedR
    speedL = 40
    speedR = 40
    try:
        while True:
            input = getch()
            print("Key : ", input)
            if input is 'w':
                GPIO.output(IN1, True)
                GPIO.output(IN2, False)
                GPIO.output(IN3, True)
                GPIO.output(IN4, False)
                changeSpeed()
            elif input is 'x':
                GPIO.output(IN1, False)
                GPIO.output(IN2, True)
                GPIO.output(IN3, False)
                GPIO.output(IN4, True)
                changeSpeed()
            elif input is 'a':
                GPIO.output(IN1, False)
                GPIO.output(IN2, True)
                GPIO.output(IN3, True)
                GPIO.output(IN4, False)
                changeSpeed()
            elif input is 'd':
                GPIO.output(IN1, True)
                GPIO.output(IN2, False)
                GPIO.output(IN3, False)
                GPIO.output(IN4, True)
                changeSpeed()
            elif input is 's':
                pwmL.ChangeDutyCycle(0)
                pwmR.ChangeDutyCycle(0)
            elif input is 'q':
                #if I don't do this, even if the program stops, the left motor will keep moving
                pwmL.ChangeFrequency(0)
                pwmR.ChangeFrequency(0)
                pwmL.stop()
                pwmR.stop()
                GPIO.cleanup()
                break
            elif input is 'u':
                speedL += 10
                speedR += 10
                if speedL > 100:
                    speedL = 100
                if speedR > 100:
                    speedR = 100
                changeSpeed()
            elif input is 'j':
                speedL -= 10
                speedR -= 10
                if speedL < 10:
                    speedL = 10
                if speedR < 10:
                    speedR = 10
                changeSpeed()
            else:
                pass
            print("Left speed : ", speedL)
            print("Right speed : ", speedR)
            print("Left pulse : ", pulseCountL)
            print("Right pulse : ", pulseCountR)
            time.sleep(1)

    except KeyboardInterrupt:
        #if I don't do this, even if the program stops, the left motor will keep moving
        pwmL.ChangeFrequency(0)
        pwmR.ChangeFrequency(0)
        pwmL.stop()
        pwmR.stop()
        GPIO.cleanup()


if __name__=="__main__":
    main()
