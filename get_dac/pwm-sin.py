import pwm_dac as pw
import signal_generator as sg
import time

t = 0
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 50

try:
    pwm = pw.PWM_DAC(12, 500, 3.28, True)

    while True:
        a = sg.get_sin_wave_amplitude(signal_frequency, t)
        voltage = a * amplitude
        pwm.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
        t = t + 1.0 / sampling_frequency 
finally:
    pwm.deinit()