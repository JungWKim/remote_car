import RPi.GPIO as GPIO
import time
import sys
import termios
import tty
import threading
import serial

ENA = 2
IN1 = 3
IN2 = 4
ENB = 22
IN3 = 17
IN4 = 27
encoderL = 10
speedL = 60
speedR = 60
Kp = 0.1
steering_signal = 0
target_rpm_gap = 67
actual_rpm_gap = ""

def speed_limit():
    global speedL, speedR
    if speedL > 100:
        speedL = 100
    if speedR > 100:
        speedR = 100
    if speedL < 10:
        speedL = 10
    if speedR < 10:
        speedR = 10


def changeSpeed(left = speedL, right = speedR):
    pwmL.ChangeDutyCycle(left)
    pwmR.ChangeDutyCycle(right)


def speed_calibration():
    global steering_signal, speedL, speedR, target_rpm_gap, actual_rpm_gap
    while True:
        try:
            actual_rpm_gap = ser.readline().decode('utf-8')
            actual_rpm_gap = actual_rpm_gap.rstrip('\n')
            actual_rpm_gap = actual_rpm_gap.rstrip('\r')
            actual_rpm_gap = int(float(actual_rpm_gap))
            if steering_signal is 1:
                error = actual_rpm_gap
                if error > 1:
                    Pcontrol = Kp * error
                    speedR += Pcontrol
                elif error < -1:
                    Pcontrol = abs(Kp * error)
                    speedL += Pcontrol
                speed_limit()
            elif steering_signal is 2:
                error = actual_rpm_gap - target_rpm_gap
                if error > 1:
                    Pcontrol = Kp * error
                    speedR -= Pcontrol
                elif error < -1:
                    Pcontrol = abs(Kp * error)
                    speedR += Pcontrol
                speed_limit()
            elif steering_signal is 3:
                error = actual_rpm_gap - target_rpm_gap
                if error > 1:
                    Pcontrol = Kp * error
                    speedL -= Pcontrol
                elif error < -1:
                    Pcontrol = abs(Kp * error)
                    speedL += Pcontrol
                speed_limit()
            elif steering_signal is 0:
                speedL = 0
                speedR = 0
            changeSpeed()
        except serial.SerialException as e:
            pass


def timer_thread():
    thread1 = threading.Thread(target = speed_calibration)
    thread1.daemon = True
    thread1.start()


def settings():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    #Left side
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(encoderL, GPIO.IN)

    #Right side
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)

    global pwmL, pwmR
    pwmL = GPIO.PWM(ENA, 50)#frequency
    pwmL.start(0)#duty cycle
    pwmR = GPIO.PWM(ENB, 50)
    pwmR.start(0)#frequency and duty cycle are different!!!

    global ser
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    timer_thread()


def show_usage():
    print("---------- How to Use -----------")
    print("")
    print("          Q  W  E ")
    print("                           U")
    print("          A  S  D  ")
    print("                           J")
    print("          Z  X  C ")
    print("")
    print("    W : forward")
    print("    A : left spinning")
    print("    D : right spinning")
    print("    X : backward")
    print("    Q : go left")
    print("    E : go right")
    print("    Z : go back left")
    print("    C : go back right")
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


def forward():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)


def backward():
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)


def main():
    global speedL, speedR, key, steering_signal, actual_rpm_gap

    show_usage()
    settings()

    try:
        while True:
            print("----------------------------------")
            key = getch()
            if key is 'w':
                forward()
                changeSpeed()
                steering_signal = 1
            elif key is 'x':
                backward()
                changeSpeed()
                steering_signal = 1
            elif key is 'a':
                GPIO.output(IN1, False)
                GPIO.output(IN2, True)
                GPIO.output(IN3, True)
                GPIO.output(IN4, False)
                changeSpeed()
                steering_signal = 1
            elif key is 'd':
                GPIO.output(IN1, True)
                GPIO.output(IN2, False)
                GPIO.output(IN3, False)
                GPIO.output(IN4, True)
                changeSpeed()
                steering_signal = 1
            elif key is 'q':
                forward()
                changeSpeed(20, 60)
                steering_signal = 2
            elif key is 'e':
                forward()
                changeSpeed(60, 20)
                steering_signal = 3
            elif key is 'z':
                backward()
                changeSpeed(20, 60)
                steering_signal = 2
            elif key is 'c':
                backward()
                changeSpeed(60, 20)
                steering_signal = 3
            elif key is 's':
                changeSpeed(0, 0)
                steering_signal = 0
            elif key is 'u':
                speedL += 10
                speedR += 10
                if speedL > 100:
                    speedL = 100
                if speedR > 100:
                    speedR = 100
                changeSpeed()
            elif key is 'j':
                speedL -= 10
                speedR -= 10
                if speedL < 10:
                    speedL = 10
                if speedR < 10:
                    speedR = 10
                changeSpeed()
            elif key is chr(27):
                #if I don't do this, even if the program stops, the left motor will keep moving
                pwmL.ChangeFrequency(0)
                pwmR.ChangeFrequency(0)
                pwmL.stop()
                pwmR.stop()
                GPIO.cleanup()
                break
            else:
                print("Inappropriate Key!!")
            print("[Pressed]", key)
            print("[rpm gap]", actual_rpm_gap)
            print("[Left speed]", speedL)
            print("[Right speed]", speedR)
            print("Press any keys......")
            print("")

    except KeyboardInterrupt:
        #if I don't do this, even if the program stops, the left motor will keep moving
        pwmL.ChangeFrequency(0)
        pwmR.ChangeFrequency(0)
        pwmL.stop()
        pwmR.stop()
        GPIO.cleanup()


if __name__=="__main__":
    main()
