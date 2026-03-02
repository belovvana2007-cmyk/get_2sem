import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):

    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage, 'b-', linewidth=2)
    
    plt.title('График зависимости напряжения на входе АЦП от времени')
    plt.xlabel('Время, с')
    plt.ylabel('Напряжение, В')
    
    plt.xlim(0, max(time))
    plt.ylim(0, max_voltage)
    
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_sampling_period_hist(time):

    sampling_periods = []
    for i in range(1, len(time)):
        period = time[i] - time[i-1]
        sampling_periods.append(period)
    
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins=30, edgecolor='black', alpha=0.7)
    plt.title('Распределение периодов дискретизации')
    plt.xlabel('Период измерения, с')
    plt.ylabel('Количество измерений')
    plt.xlim(0, 0.06)
    plt.grid(True, alpha=0.3)
    
    plt.show()
