import nengo
import numpy as np
import matplotlib.pyplot as plt

model = nengo.Network('Oscillator')

freq = -0.75

with model:
    stim = nengo.Node(lambda t: [.5, .5] if t < .02 else [0, 0])
    osc = nengo.Ensemble(200, dimensions=2)


    def feedback(x):
        return x[0] + freq * x[1], -freq * x[0] + x[1]

    nengo.Connection(osc, osc, function=feedback, synapse=.01)
    nengo.Connection(stim, osc)

    stim_p = nengo.Probe(stim)
    osc_p = nengo.Probe(osc, synapse=.01)

sim = nengo.Simulator(model)
sim.run(.5)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(sim.trange(), sim.data[osc_p])
plt.plot(sim.trange(), sim.data[stim_p], 'r', label="stim", linewidth=4)
plt.xlabel('Time (s)')
plt.ylabel('State value')
plt.subplot(1, 2, 2)
plt.plot(sim.data[osc_p][:, 0], sim.data[osc_p][:, 1])
plt.xlabel('$x_0$')
plt.ylabel('$x_1$')
plt.show()