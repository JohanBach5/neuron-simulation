import matplotlib
import matplotlib.pyplot as plt
import LIF
import Synapse

matplotlib.use('TkAgg')

neuron1 = LIF.LIF()
neuron2 = LIF.LIF()
synapse = Synapse.Synapse(neuron1, neuron2, weight=20)
excitatory = 3.0
inhibitory = 1.0

print(synapse.source is neuron1)

for t in range(100):
    neuron1.step(t, excitatory=excitatory, inhibitory=inhibitory)
    neuron2.step(t)
    synapse.step(t)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

ax1.plot(neuron1.times, neuron1.voltages)
ax1.axhline(y=neuron1.threshold, color='orange', linestyle='--', label='threshold')
ax1.set_ylabel('Vm (mV)')
ax1.set_title('Neuron A')
ax1.legend()

ax2.plot(neuron2.times, neuron2.voltages)
ax2.axhline(y=neuron2.threshold, color='orange', linestyle='--', label='threshold')
ax2.set_ylabel('Vm (mV)')
ax2.set_xlabel('Time (ms)')
ax2.set_title('Neuron B')
ax2.legend()

plt.tight_layout()
plt.xlim(0, 100)
plt.savefig('LIF.png')
