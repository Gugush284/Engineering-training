import RPi.GPIO as GPIO

i = 0
dac = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = 0)

try:
    p = GPIO.PWM (dac, 1000)
    while True:
        p.start(i)
        i = int(input())
        print (3.3 * i / 100)
        p.stop()

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()