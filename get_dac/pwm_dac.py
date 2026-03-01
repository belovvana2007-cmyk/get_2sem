import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

gpio_bits = [16,20,21,25,26,17,27,22]

num = 0
dynamic_range = 3.131

GPIO.setup(gpio_bits, GPIO.OUT)
GPIO.output(gpio_bits, 0)

class PWM_DAC:
    def __init__(self, gpio_bits, pwm_frequency, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.pwm_frequency = pwm_frequency
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)
        self.pwm = GPIO.PWM(self.gpio_bits, self.pwm_frequency)
        self.pwm.start(0.0)

    def deinit(self):
        self.pwm.stop()
        GPIO.cleanup()

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
            print("Устанавлниваем 0.0 В")
            return 0
        num = int(voltage / self.dynamic_range * 100)
        self.pwm.stop()
        self.pwm.start(num)

if __name__ == "__main__":
    try:
        dac= PWM_DAC(12, 500, 3.290, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
        
    finally:
        dac.deinit()

