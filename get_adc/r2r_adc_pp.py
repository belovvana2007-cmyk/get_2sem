import RPi.GPIO as GPIO
import time


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def __del__(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        bits = [int(x) for x in bin(number)[2:].zfill(len(self.bits_gpio))]
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_adc(self):
        max_value = 2 ** len(self.bits_gpio) - 1
        for value in range(0, max_value + 1):
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            comp_state = GPIO.input(self.comp_gpio)
            if comp_state == 1:
                return value
        return max_value

    def successive_approximation_adc(self):
        n_bits = len(self.bits_gpio)
        min_val = 0
        max_val = 2 ** n_bits - 1
        
        for bit_pos in range(n_bits - 1, -1, -1):  
            test_value = min_val + (1 << bit_pos)
            
            self.number_to_dac(test_value)
            time.sleep(self.compare_time)
            comp_state = GPIO.input(self.comp_gpio)
            
            if comp_state == 1:  
                max_val = test_value - 1
            else:  
                min_val = test_value
        
        return min_val

    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        max_code = 2 ** len(self.bits_gpio) - 1
        return self.dynamic_range * code / max_code

    def get_sar_voltage(self):
        code = self.successive_approximation_adc()
        max_code = 2 ** len(self.bits_gpio) - 1
        return self.dynamic_range * code / max_code


if __name__ == "__main__":
    try:
        adc = R2R_ADC(dynamic_range=3.3, compare_time=0.001, verbose=False)
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(0.1)
            
    finally:
        del adc
