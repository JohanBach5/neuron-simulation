from HH import HH
import matplotlib.pyplot as plt

neuron = HH()

for t in range(5000):
    neuron.step(t, excitatory=15.0)

plt.plot(neuron.times, neuron.voltages)
plt.axhline(y=-55, color='orange', linestyle='--', label='threshold')
plt.xlabel('Time (ms)')
plt.ylabel('Vm (mV)')
plt.savefig('HH.pdf')
