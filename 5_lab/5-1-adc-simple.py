import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17
maxVolt = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = 0)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def adc():
    for value in range(256):
        signal = decimal2binary(value)
        GPIO.output(dac, signal)
        time.sleep(0.002)
        CompValue = GPIO.input(comp)
        if CompValue == 0:
            break
    return value

try:
    while True:
        value = adc()
        Volt = value/(2**len(dac)) * maxVolt
        print ("ADC value = {:^3}, input voltage = {:.2f}".format(value, Volt))   
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()