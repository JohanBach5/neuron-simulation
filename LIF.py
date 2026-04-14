from Neuron import Neuron


class LIF(Neuron):
    def __init__(self, resting=-70.0, threshold=-55.0, leak=0.05, peak=40.0, refractory_overshoot=-80.0):
        super().__init__(resting, threshold)
        self.Vm = resting
        self.leak = leak
        self.peak = peak
        self.refractory_overshoot = refractory_overshoot

    def step(self, input_current, t, dt=1.0):
        self.times.append(t)
        self.voltages.append(self.Vm)
        self.Vm = self.Vm + dt * (input_current - self.leak * (self.Vm - self.resting))

        if self.Vm >= self.threshold:
            self.voltages[-1] = self.peak
            self.Vm = self.refractory_overshoot
            self.spike_times.append(t)
