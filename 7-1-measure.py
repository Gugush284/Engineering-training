import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import os

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
                volt_list.append(volt_start)
                break

        prev = volt_start
        prev_time = start_time
        steps_quant = list()
        time_list = list()

        while True:
            value = adc()
            volt = value/(2**len(dac)) * maxVolt
            volt_list.append(volt)

            current_time = time.perf_counter()
            time_list.append(current_time-prev_time)
            prev_time = current_time

            steps_quant.append(volt - prev)
            prev = volt

            if (volt >= maxVolt*0.95):
                break

        GPIO.output(troyka, 0)
        while True:
            value = adc()
            volt = value/(2**len(dac)) * maxVolt
            volt_list.append(volt)

            steps_quant.append(prev - volt)
            prev = volt

            current_time = time.perf_counter()
            time_list.append(current_time-prev_time)
            prev_time = current_time

            if (volt <= maxVolt*0.02):
                break
        
        end_time = time.perf_counter()

        del_t = end_time - start_time

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.txt')
        with open(path, "w") as output:
            for item in volt_list:
                data_str = str(item)
                data_str += "\n"
                output.write(data_str)

        sampling = len(volt_list)/del_t

        sum = 0
        for elem in steps_quant:
            sum += elem
        step_quant = sum / len(steps_quant)

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'settings.txt')
        with open(path, "w") as output_set:
            str1 = "Sampling: "
            str1 += str(sampling)
            str1 += "\n"
            output_set.write(str1)

            str2 = "Step of quantization: "
            str2 += str(step_quant)
            str2 += "\n"
            output_set.write(str2)

        time_sum = 0
        for time_item in time_list:
            time_sum += time_item
        measure_period = time_sum / len(time_list)

        print("Settings:")
        print("Time = {}".format(del_t))
        print("Measurement period = {}".format(measure_period))
        print("Sampling = {}".format(sampling))
        print("Step of quantization = {}".format(step_quant))
        print("Amount of points = {}".format(len(volt_list)))

        plt.plot(volt_list)
        plt.show()
    finally:
        GPIO.output(dac, 0)
        GPIO.output(leds, 0)
        GPIO.output(troyka, 0)
        GPIO.cleanup()
        exit()

main()
