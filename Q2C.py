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
    stimA = nengo.Node(lambda x: x)
    stimB = nengo.Node(lambda y: y)

    ensA = nengo.Ensemble(2000, dimensions=2)
    ensB = nengo.Ensemble(1000, dimensions=1)
    nengo.Connection(stimA, ensA[0])
    nengo.Connection(stimB, ensA[1])

    nengo.Connection(ensA, ensB, function=lambda x: np.sin(x[0] * x[1]))

    stimA_p = nengo.Probe(stimA)
    stimB_p = nengo.Probe(stimB)
    ensA_p = nengo.Probe(ensA, synapse=.01)
    ensB_p = nengo.Probe(ensB, synapse=.01)

sim = nengo.Simulator(model)
sim.run(T)

t = sim.trange()
plt.figure()
plt.plot(t, sim.data[ensA_p][:, 0], 'black', label="$\hat{x}[0]$")
plt.plot(t, sim.data[ensA_p][:, 1], 'green', label="$\hat{x}[1]$")
plt.plot(t, sim.data[ensB_p], 'r', label="$sin(\hat{x[0]}\cdot\hat{x[1]})$")
plt.legend(loc='best')
plt.ylabel("Output")
plt.xlabel("Time")
plt.show()
