import math


class Synapse:
    def __init__(self, source, target, weight=3.0, delay=1, tau=20.0, a_plus=0.01, a_minus=0.01, max_weight=10.0,
                 min_weight=0.0):
        self.source = source
        self.target = target
        self.weight = weight
        self.delay = delay
        self.tau = tau
        self.a_plus = a_plus
        self.a_minus = a_minus
        self.max_weight = max_weight
        self.min_weight = min_weight

    def step(self, t):
        past_t = t - self.delay
        if past_t in self.source.spike_times:
            self.target.synaptic_input += self.weight

        if self.source.spike_times and self.target.spike_times:
            t_source = self.source.spike_times[-1]
            t_target = self.target.spike_times[-1]
            dt = t_source - t_target
            if dt < 0:
                self.weight += self.a_plus * math.exp(-abs(dt) / self.tau)
            elif dt > 0:
                self.weight -= self.a_minus * math.exp(-abs(dt) / self.tau)

            self.weight = max(self.min_weight, min(self.max_weight, self.weight))
            