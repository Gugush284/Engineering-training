import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

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

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def main():
    global dac
    dac = [26, 19, 13, 6, 5, 11, 9, 10]
    global leds 
    leds = [24, 25, 8, 7, 12, 16, 20, 21]
    global comp
    comp = 4
    global troyka
    troyka = 17
    global maxVolt
    maxVolt = 3.3
    
    start_time = time.perf_counter()
    volt_start = 0
    volt_end = 0

    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dac, GPIO.OUT, initial = 0)
        GPIO.setup(leds, GPIO.OUT, initial = 0)
        GPIO.setup(troyka, GPIO.OUT, initial = 1)
        GPIO.setup(comp, GPIO.IN)

        volt_list = list()

        while True:
            value = adc()
            volt_start = value/(2**len(dac)) * maxVolt
            if (volt_start == 0):
                print(volt_start)
                volt_list.append(volt_start)
                break

        while True:
            value = adc()
            volt = value/(2**len(dac)) * maxVolt
            print(volt)
            volt_list.append(volt)
            if (volt >= maxVolt*0.97):
                print(volt_list)
                break

        GPIO.output(troyka, 0)
        while True:
            value = adc()
            volt = value/(2**len(dac)) * maxVolt
            print(volt)
            volt_list.append(volt)
            if (volt <= maxVolt*0.02):
                print(volt_list)
                volt_end = volt
                break
        
        end_time = time.perf_counter()

        del_t = end_time - start_time
        print(del_t)

        plt.plot(volt_list)
        plt.show()

    finally:
        GPIO.output(dac, 0)
        GPIO.output(leds, 0)
        GPIO.output(troyka, 0)
        GPIO.cleanup()
        exit()

main()
