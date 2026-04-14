class Synapse:
    def __init__(self, source, target, weight=2.0, delay=1):
        self.source = source
        self.target = target
        self.weight = weight
        self.delay = delay

    def step(self, t):
        past_t = t - self.delay
        print(
            f"t={t}, past_t={past_t}, spike_times={self.source.spike_times}, condition={past_t in self.source.spike_times}")
        if past_t in self.source.spike_times:
            self.target.synaptic_input += self.weight

        if t == 5:
            print(past_t)
            print(self.source.spike_times)