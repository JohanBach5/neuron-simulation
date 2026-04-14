from Neuron import Neuron


class LIF(Neuron):
    def __init__(self, resting=-70.0, threshold=-55.0, leak=0.05, peak=40.0, refractory_overshoot=-80.0,
                 refractory_duration=2.0, synaptic_input=0.0):
        super().__init__(resting, threshold)
        self.Vm = resting
        self.leak = leak
        self.peak = peak
        self.refractory_overshoot = refractory_overshoot
        self.is_refractory = False
        self.refractory_time = 0
        self.refractory_duration = refractory_duration
        self.synaptic_input = synaptic_input

    def step(self, t, dt=1.0, excitatory=0.0, inhibitory=0.0):
        self.times.append(t)
        self.voltages.append(self.Vm)

        if self.is_refractory and (self.refractory_time < self.refractory_duration):
            self.Vm = self.refractory_overshoot
            self.refractory_time += 1
        else:
            self.is_refractory = False
            self.refractory_time = 0
            self.Vm = self.Vm + dt * (
                        (excitatory + self.synaptic_input - inhibitory) - self.leak * (self.Vm - self.resting))
            self.synaptic_input = 0.0

        if self.Vm >= self.threshold:
            self.voltages[-1] = self.peak
            self.Vm = self.refractory_overshoot
            self.spike_times.append(t)
            self.is_refractory = True
