import random
import matplotlib
import matplotlib.pyplot as plt
from LIF import LIF
from Network import Network

matplotlib.use('TkAgg')

sources = [LIF(vm_init=random.uniform(-70, -60),
               leak=random.uniform(0.04, 0.06),
               threshold=random.uniform(-57, -53)) for _ in range(5)]

targets = [LIF(vm_init=random.uniform(-70, -60),
               leak=random.uniform(0.04, 0.06),
               threshold=random.uniform(-57, -53)) for _ in range(5)]

network = Network(sources, targets, p=0.5, weight=10.0)
network.connect()

for t in range(200):
    for src in sources:
        excitatory = 3.0 + random.gauss(0, 0.5)
        inhibitory = 1.0 + random.gauss(0, 0.2)
        src.step(t, excitatory=excitatory, inhibitory=inhibitory)
    for trg in targets:
        trg.step(t)
    for snp in network.synapses:
        snp.step(t)

for i, snp in enumerate(network.synapses):
    print(f"Synapse {i} (S{sources.index(snp.source)+1} → T{targets.index(snp.target)+1}): weight = {snp.weight:.4f}")
for i, trg in enumerate(targets):
    print(f"Target {i+1} spikes: {len(trg.spike_times)}")

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
plt.savefig('LIF.pdf')
