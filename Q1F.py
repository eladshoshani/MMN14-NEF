import matplotlib.pyplot as plt
import numpy as np

import nengo
from nengo.utils.matplotlib import rasterplot

from nengo.dists import Uniform

model = nengo.Network(label="A Single Neuron")
with model:
    a = nengo.Ensemble(1,
                       dimensions=1,  # Represent a scalar
                       # Set intercept to 0.5
                       intercepts=Uniform(-0.5, -0.5),
                       # Set the maximum firing rate of the neuron to 100hz
                       max_rates=Uniform(100, 100),
                       # Set the neuron's firing rate to increase for positive input
                       encoders=[[1]], )


    # Create an input node generating a function wave
    def stim_func(t):
        return np.cos(8 * t)


    func = nengo.Node(stim_func)

    # Connect the input signal to the neuron
    nengo.Connection(func, a)

    # The original input
    func_probe = nengo.Probe(func)
    # The raw spikes from the neuron
    spikes = nengo.Probe(a.neurons)
    # Spikes filtered by a 10ms post-synaptic filter
    filtered = nengo.Probe(a, synapse=0.01)

    with nengo.Simulator(model) as sim:  # Create the simulator
        sim.run(1)  # Run it for 1 second
        # Plot the decoded output of the ensemble
        plt.figure()
        plt.plot(sim.trange(), sim.data[filtered])
        plt.plot(sim.trange(), sim.data[func_probe])
        plt.xlim(0, 1)

        # Plot the spiking output of the ensemble
        plt.figure(figsize=(10, 8))
        plt.subplot(221)
        rasterplot(sim.trange(), sim.data[spikes])
        plt.ylabel("Neuron")
        plt.xlim(0, 1)
