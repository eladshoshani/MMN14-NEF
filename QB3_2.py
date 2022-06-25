import nengo
import numpy as np
import matplotlib.pyplot as plt

# Point attractor
model = nengo.Network('Attractor - Q3B')
with model:
    stim = nengo.Node(lambda t: 0.5 if t < .01 else 0)
    attractor = nengo.Ensemble(2000, dimensions=1)


    def feedback(x):
        # Determining the point:
        p = 0.1
        return x - (x - p)

    nengo.Connection(attractor, attractor, function=feedback, synapse=.01)
    nengo.Connection(stim, attractor)

    stim_p = nengo.Probe(stim)
    osc_p = nengo.Probe(attractor, synapse=.01)

sim = nengo.Simulator(model)
sim.run(.5)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(sim.trange(), sim.data[osc_p]);
plt.plot(sim.trange(), sim.data[stim_p], 'r', label="stim", linewidth=4)
plt.xlabel('Time (s)')
plt.ylabel('State value')
plt.subplot(1, 2, 2)
plt.plot(sim.data[osc_p], sim.data[osc_p])
plt.xlabel('$x_0$')
plt.ylabel('$x_1$');
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()
