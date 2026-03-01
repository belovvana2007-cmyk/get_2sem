import mcp4725_driver as mc
import signal_generator as sg
import time

t = 0
amplitude = 3.2
signal_frequency = 10
sampling_frequency = 100


try:
    mcp=mc.MCP4725(5, True)

    while True:
        a = sg.get_sin_wave_amplitude(signal_frequency, t)
        voltage = a * amplitude
        mcp.set_voltage(voltage)
        sg.wait_for_sampling_period(sampling_frequency)
        t = t + 1.0 / sampling_frequency 
finally:
    mcp.deinit()