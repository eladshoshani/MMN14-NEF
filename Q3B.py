
import nengo
import numpy as np
import matplotlib.pyplot as plt

# Point attractor
model = nengo.Network('Attractor - Q3B')
with model:
    stim = nengo.Node(lambda t: [.5 ,.5] if t < .01 else [0, 0])
    attractor = nengo.Ensemble(2000, dimensions=2)

    def feedback(x):
        # Determining the point:
        p1 = 0.6
        p2 = 0.2
        return x[0] - (x[0] - p1), x[1] - (x[1] - p2)


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
plt.plot(sim.data[osc_p][:, 0], sim.data[osc_p][:, 1])
plt.xlabel('$x_0$')
plt.ylabel('$x_1$');
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()