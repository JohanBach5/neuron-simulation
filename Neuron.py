from abc import ABC, abstractmethod


class Neuron(ABC):
    def __init__(self, resting=-70.0, threshold=-55.0):
        self.resting = resting
        self.threshold = threshold
        self.times = []
        self.voltages = []
        self.spike_times = []

    @abstractmethod
    def step(self, t, dt=1.0, **kwargs):
        pass
