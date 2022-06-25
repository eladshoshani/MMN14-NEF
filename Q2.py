import nengo
import numpy as np
import matplotlib.pyplot as plt
from nengo.utils.matplotlib import rasterplot
from nengo.processes import WhiteNoise

# Transforming sin(x) to 2sin(x) by decoder scaling

T = 1.0
max_freq = 5

model = nengo.Network()

with model:
    N = 1000
    stim = nengo.Node(lambda t: t)
    ensA = nengo.Ensemble(N, dimensions=1)
    ensB = nengo.Ensemble(N, dimensions=1)

    nengo.Connection(stim, ensA)
    nengo.Connection(ensA, ensB, function=lambda x: np.cos(x))  # function=lambda x: 3*x

    stim_p = nengo.Probe(stim)
    ensA_p = nengo.Probe(ensA, synapse=.01)
    ensB_p = nengo.Probe(ensB, synapse=.01)
    # Probeable attributes: ('output', 'voltage', 'refractory_time', 'input')
    ensA_spikes_p = nengo.Probe(ensA.neurons, 'output')
    ensB_spikes_p = nengo.Probe(ensB.neurons, 'output')

sim = nengo.Simulator(model, seed=4)
sim.run(T)

t = sim.trange()
plt.figure(figsize=(6, 4))
plt.ax = plt.gca()
plt.plot(t, sim.data[stim_p], 'r', linewidth=4, label='x')
plt.plot(t, sim.data[ensA_p], 'g', label='$\hat{x}$')
plt.plot(t, sim.data[ensB_p], 'b', label='$f(\hat{x})=cos(\hat{x})$')  # name of the function
plt.legend()
plt.ylabel("Output")
plt.xlabel("Time")
plt.show()
