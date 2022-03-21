import RPi.GPIO as GPIO

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def notdigit(str):
    if str.isdigit():
        return 0
    else:
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
            print("Value should be int")
        elif int(i) < 0:
            print("Value should be > 0")
        elif int(i) > 255:
            print("Value should be < 255")
        else:
            bits = decimal2binary(int(i))

            ratio = 0.5
            voltageout = 0
            for x in bits:
                voltageout = voltageout + 3.3 * x * ratio
                ratio = ratio/2
            print (voltageout)

            GPIO.output(dac, bits)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
