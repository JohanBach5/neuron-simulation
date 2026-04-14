import matplotlib
import matplotlib.pyplot as plt
from LIF import LIF
from Network import Network

matplotlib.use('TkAgg')

sources = [LIF() for _ in range(5)]
targets = [LIF() for _ in range(5)]

network = Network(sources, targets, p=0.5)
network.connect()

excitatory = 3.0
inhibitory = 1.0

for t in range(100):
    for src in sources:
        src.step(t, excitatory=excitatory, inhibitory=inhibitory)
    for trg in targets:
        trg.step(t)
    for snp in network.synapses:
        snp.step(t)

fig, axes = plt.subplots(len(sources) + len(targets), 1, sharex=True, figsize=(12, 10))

for i, neuron in enumerate(sources):
    axes[i].plot(neuron.times, neuron.voltages)
    axes[i].axhline(y=neuron.threshold, color='orange', linestyle='--')
    axes[i].set_ylabel('Vm (mV)', fontsize=7)
    axes[i].set_title(f'Source {i+1}', fontsize=8)

for i, neuron in enumerate(targets):
    axes[len(sources) + i].plot(neuron.times, neuron.voltages)
    axes[len(sources) + i].axhline(y=neuron.threshold, color='orange', linestyle='--')
    axes[len(sources) + i].set_ylabel('Vm (mV)', fontsize=7)
    axes[len(sources) + i].set_title(f'Target {i+1}', fontsize=8)

plt.xlabel('Time (ms)')
plt.tight_layout()
plt.savefig('LIF.png')