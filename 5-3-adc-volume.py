import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [24, 25, 8, 7, 12, 16, 20, 21]
comp = 4
troyka = 17
maxVolt = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = 0)
GPIO.setup(leds, GPIO.OUT, initial = 0)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def adc():
    signal = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        signal[i] = 1
        GPIO.output(dac, signal)
        time.sleep(0.01)
        CompValue = GPIO.input(comp)
        if CompValue == 0:
            signal[i] = 0

    value = 0
    for i in range(8):
        if signal[i] == 1:
            value = value + 2**(7-i)
    return value

def sig(value):
    if value == 0:
        GPIO.output(leds, 0)
    else:
        s = [0, 0, 0, 0, 0, 0, 0, 0]
        i = value // 32
        if i == 0:
            s[0] = 1
        else: 
            for j in range(i):
                s[j] = 1
        GPIO.output(leds, s)

try:
    while True:
        value = adc ()
        sig(value)
        voltage = value/(2**len(dac)) * maxVolt
        print ("input voltage = {:.2f}".format(voltage))
        time.sleep(1)
finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()