import serial
import time

data = b'275\n'
ser = serial.Serial("/dev/ttyUSB0", 9600, timeout = 1)

while True:
    try:
    #    if ser.in_waiting > 0:
    #        line = ser.readline().decode('utf-8')
    #        print("received :", line)
        ser.write(data)
        ser.flushInput()
        time.sleep(0.5)
    except KeyboardInterrupt:
        ser.close()
