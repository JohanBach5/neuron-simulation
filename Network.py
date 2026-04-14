import random

from Synapse import Synapse


class Network:
    def __init__(self, sources, targets, p=0.3, weight=1.0):
        self.sources = sources
        self.targets = targets
        self.p = p
        self.synapses = []
        self.weight = weight

    def connect(self):
        for src in self.sources:
            for trg in self.targets:
                if random.random() < self.p:
                    self.synapses.append(Synapse(src, trg, self.weight))

    def step(self, t):
        for src in self.sources:
            src.step(t)
        for trg in self.targets:
            trg.step(t)
        for snp in self.synapses:
            snp.step(t)
