import smbus
import time

class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)  
        self.dynamic_range = dynamic_range
        self.address = 0x4D  
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):

        data = self.bus.read_word_data(self.address, 0x00)
        lower_data_byte = data >> 8   
        upper_data_byte = data & 0xFF
        number = ((upper_data_byte & 0xFF) << 2) | (lower_data_byte >> 6)
        
        if self.verbose:
            print(f"Данные: {data:04x}, upper: {upper_data_byte:02x}, lower: {lower_data_byte:02x}, число: {number}")
        
        return number

    def get_voltage(self):
        code = self.get_number()
        max_code = 2**10 - 1 
        voltage = self.dynamic_range * code / max_code
        return voltage


if __name__ == "__main__":
    try:
        adc = MCP3021(dynamic_range=3.183, verbose=True)        
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(1.0)
            
    finally:
        adc.deinit()
