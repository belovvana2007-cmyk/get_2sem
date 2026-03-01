import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

gpio_bits = [16,20,21,25,26,17,27,22]

num = 0
dynamic_range = 3.131

GPIO.setup(gpio_bits, GPIO.OUT)
GPIO.output(gpio_bits, 0)

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, num):
        binary = [int(bit) for bit in bin(num)[2:].zfill(8)]
        GPIO.output(self.gpio_bits, binary)

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
            print("Устанавлниваем 0.0 В")
            return 0
        num = int(voltage / self.dynamic_range * 255)
        self.set_number(num)

if __name__ == "__main__":
    try:
        dac= R2R_DAC([16,20,21,25,26,17,27,22], 3.183, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
        
    finally:
        dac.deinit()

