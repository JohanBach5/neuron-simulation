class Synapse:
    def __init__(self, source, target, weight=3.0, delay=1):
        self.source = source
        self.target = target
        self.weight = weight
        self.delay = delay

    def step(self, t):
        past_t = t - self.delay
        if past_t in self.source.spike_times:
            self.target.synaptic_input += self.weight
