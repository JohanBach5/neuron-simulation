from Neuron import Neuron
from math import exp


class HH(Neuron):
    def __init__(self, resting=-70.0, threshold=-55.0, m=0.05, h=0.6, n=0.32, g_na=120.0, g_k=36.0, g_leak=0.3,
                 E_na=50.0, E_k=-77.0, E_leak=-54.4, C=1.0, synaptic_input=0.0):
        super().__init__(resting, threshold)
        self.Vm = resting
        self.m = m
        self.h = h
        self.n = n
        self.g_na = g_na
        self.g_k = g_k
        self.g_leak = g_leak
        self.E_na = E_na
        self.E_k = E_k
        self.E_leak = E_leak
        self.C = C
        self.synaptic_input = synaptic_input

    def step(self, t, dt=0.01, excitatory=0.0, inhibitory=0.0, **kwargs):
        self.times.append(t)
        self.voltages.append(self.Vm)

        input_current = excitatory - inhibitory + self.synaptic_input
        self.synaptic_input = 0.0

        # Alpha and beta rate functions
        if abs(self.Vm + 40) < 1e-7:
            alpha_m = 1.0
        else:
            alpha_m = 0.1 * (self.Vm + 40) / (1 - exp(-0.1 * (self.Vm + 40)))
        beta_m = 4.0 * exp(-0.0556 * (self.Vm + 65))

        alpha_h = 0.07 * exp(-0.05 * (self.Vm + 65))
        beta_h = 1 / (1 + exp(-0.1 * (self.Vm + 35)))

        if abs(self.Vm + 55) < 1e-7:
            alpha_n = 0.1
        else:
            alpha_n = 0.01 * (self.Vm + 55) / (1 - exp(-0.1 * (self.Vm + 55)))
        beta_n = 0.125 * exp(-0.0125 * (self.Vm + 65))

        # Update gating variables
        dm = alpha_m * (1 - self.m) - beta_m * self.m
        dh = alpha_h * (1 - self.h) - beta_h * self.h
        dn = alpha_n * (1 - self.n) - beta_n * self.n

        self.m += dt * dm
        self.h += dt * dh
        self.n += dt * dn

        # Clamp gating variables between 0 and 1
        self.m = max(0.0, min(1.0, self.m))
        self.h = max(0.0, min(1.0, self.h))
        self.n = max(0.0, min(1.0, self.n))

        # Compute currents
        I_na = self.g_na * self.m ** 3 * self.h * (self.Vm - self.E_na)
        I_k = self.g_k * self.n ** 4 * (self.Vm - self.E_k)
        I_leak = self.g_leak * (self.Vm - self.E_leak)

        # Update Vm
        dVm = (input_current - I_na - I_k - I_leak) / self.C
        self.Vm += dt * dVm

        # Spike detection
        if self.Vm >= self.threshold and (not self.spike_times or t - self.spike_times[-1] > 2):
            self.spike_times.append(t)
