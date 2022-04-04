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

def adc():
    signal = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        signal[i] = 1
        GPIO.output(dac, signal)
        time.sleep(0.01)
        CompValue = GPIO.input(comp)
        if CompValue == 0:
            signal[i] = 0

    print ("signal = {}".format(signal))

    value = 0
    for i in range(8):
        if signal[i] == 1:
            value = value + 2**(7-i)
    return value

try:
    while True:
        value = adc ()
        voltage = value/(2**len(dac)) * maxVolt
        print ("ADC value = {}, input voltage = {:.2f}".format(value, voltage))
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()