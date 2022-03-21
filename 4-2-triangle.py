import RPi.GPIO as GPIO
import time

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def notdigit(str):
    if str.isdigit():
        return 0
    else:
        try:
            float (str)
            return 0
        except:
            return 1


dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = 1)

try:
    while True:
        i = input()
        if i == 'q':
            exit()
        elif notdigit(i):
            print("Value should be int or float")
        elif float(i) < 0:
            print("Value should be > 0")
        else:
            T = float (i)
            T = T/256/2

            for x in range (0, 256):
                volt = 3.3*x/256
                bits = decimal2binary(x)
                GPIO.output(dac, bits)
                time.sleep(T)
            for x in range (254, -1, -1):
                volt = 3.3*x/256
                bits = decimal2binary(x)
                GPIO.output(dac, bits)
                time.sleep(T)


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()