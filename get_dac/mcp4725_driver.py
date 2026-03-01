import smbus
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

gpio_bits = [16,20,21,25,26,17,27,22]

num = 0
dynamic_range = 4.16

GPIO.setup(gpio_bits, GPIO.OUT)
GPIO.output(gpio_bits, 0)

class MCP4725:
    def __init__(self, dynamic_range, adress=0x61, verbose = True):
        self.bus = smbus.SMBus(1)

        self.adress = adress
        self.wm = 0x00
        self.pds = 0x00

        self.verbose = verbose
        self.dynamic_range = dynamic_range

    def deinit(self):
        self.bus.close()
    
    def self_number(self, number):
        if not isinstance(number, int):
            print('На вход ЦАП можно подавать только целые числа')

        if not (0<=number<=4095):
            print('Число выходит за разрядность MCP4752 (12 бит)')

        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(0x61, first_byte, second_byte)

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.adress << 1):02X}, 0x{first_byte: 02X}, 0x{second_byte: 02X}]\n")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
            print("Устанавлниваем 0.0 В")
            return 0

        number = int(voltage / self.dynamic_range * 4095)
        self.self_number(number)

if __name__ == "__main__":
    try:
        dac= MCP4725(4.16, True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")
        
    finally:
        dac.deinit()