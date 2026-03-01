import r2r_dac as r2r
import signal_generator as sg
import time

t = 0
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000
dynamic_range = 3.183

try:
    dac= r2r.R2R_DAC([16,20,21,25,26,17,27,22], dynamic_range, True)
    
    while True:
        a = sg.get_sin_wave_amplitude(signal_frequency, t)
        voltage = a * amplitude
        dac.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
        t = t + 1.0 / sampling_frequency       

finally:
    dac.deinit()
