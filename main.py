import matplotlib
import matplotlib.pyplot as plt
import LIF

matplotlib.use('TkAgg')


neuron = LIF.LIF()
input_current = 2.0

for t in range(500):
    neuron.step(input_current, t)

plt.plot(neuron.times, neuron.voltages)
plt.axhline(y=neuron.threshold, color='orange', linestyle='--', label='threshold')
plt.xlabel('Time (ms)')
plt.ylabel('Vm (mV)')
plt.legend()
plt.savefig('LIF.png')

print(neuron.spike_times)
