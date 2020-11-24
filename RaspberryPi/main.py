import RPi.GPIO as GPIO
import time
import sys
import pdb
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
Kp = 0.7
speedL = 0
speedR = 0
target_rpm_gap = 67
actual_rpm_gap = ""
steering_signal = 0
ser = 0

def speed_limit():
    global speedL, speedR
    if speedL > 100:
        speedL = 100
    elif speedL < 10:
        speedL = 10
    if speedR > 100:
        speedR = 100
    elif speedR < 10:
        speedR = 10


def speed_calibration():
    global actual_rpm_gap, steering_signal, speedL, speedR, target_rpm_gap
    while True:
        try:
            actual_rpm_gap = ser.readline().decode('utf-8')
            actual_rpm_gap = actual_rpm_gap.rstrip('\r\n')
            actual_rpm_gap = int(float(actual_rpm_gap))
            if steering_signal is not 0:
                if steering_signal is 1:
                    error = actual_rpm_gap
                    if error > 1:
                        speedR += Kp * error
                    elif error < -1:
                        speedL += abs(Kp * error)
                elif steering_signal is 2:
                    error = actual_rpm_gap - target_rpm_gap
                    if error > 1:
                        speedR -= Kp * error
                    elif error < -1:
                        speedR += abs(Kp * error)
                elif steering_signal is 3:
                    error = actual_rpm_gap - target_rpm_gap
                    if error > 1:
                        speedL -= Kp * error
                    elif error < -1:
                        speedL += abs(Kp * error)
                speed_limit()
                pwmL.ChangeDutyCycle(speedL)
                pwmR.ChangeDutyCycle(speedR)
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
    global speedL, speedR, steering_signal
    prev_key = ''
    show_usage()
    settings()

    try:
        while True:
            print("----------------------------------")
            key = getch()
            if key is not prev_key:
                if key is 'w':
                    forward()
                    speedL = 60
                    speedR = 60
                    steering_signal = 1
                elif key is 'x':
                    backward()
                    speedL = 60
                    speedR = 60
                    steering_signal = 1
                elif key is 'a':
                    GPIO.output(IN1, False)
                    GPIO.output(IN2, True)
                    GPIO.output(IN3, True)
                    GPIO.output(IN4, False)
                    speedL = speedR = 60
                    steering_signal = 1
                elif key is 'd':
                    GPIO.output(IN1, True)
                    GPIO.output(IN2, False)
                    GPIO.output(IN3, False)
                    GPIO.output(IN4, True)
                    speedL = 60
                    speedR = 60
                    steering_signal = 1
                elif key is 'q':
                    forward()
                    speedL = 20
                    speedR = 60
                    steering_signal = 2
                elif key is 'e':
                    forward()
                    speedL = 60
                    speedR = 20
                    steering_signal = 3
                elif key is 'z':
                    backward()
                    speedL = 20
                    speedR = 60
                    steering_signal = 2
                elif key is 'c':
                    backward()
                    speedL = 60
                    speedR = 20
                    steering_signal = 3
                elif key is 's':
                    speedL = 0
                    speedR = 0
                    steering_signal = 0
                elif key is chr(27):
                    #if I don't do this, even if the program stops, the left motor will keep moving
                    pwmL.ChangeFrequency(0)
                    pwmR.ChangeFrequency(0)
                    pwmL.stop()
                    pwmR.stop()
                    GPIO.cleanup()
                    break
                else:
                    if key is 'u' or key is 'j':
                        pass
                    print("Inappropriate Key!!")
            if key is 'u':
                speedL += 10
                speedR += 10
                if speedL > 100:
                    speedL = 100
                if speedR > 100:
                    speedR = 100
            if key is 'j':
                speedL -= 10
                speedR -= 10
                if speedL < 10:
                    speedL = 10
                if speedR < 10:
                    speedR = 10
            pwmL.ChangeDutyCycle(speedL)
            pwmR.ChangeDutyCycle(speedR)
            prev_key = key
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
