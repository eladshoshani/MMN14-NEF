
import nengo
import numpy as np
import matplotlib.pyplot as plt

model = nengo.Network('Q4')
theta = [np.pi / 6, np.pi / 4, np.pi / 3]
with model:
    stim = nengo.Node(lambda t: [.5 ,.5] if t < .01 else [0, 0])
    robot = nengo.Ensemble(2000, dimensions=2)

    def feedback(x):
        p1 = np.cos(theta[0]) + np.cos(theta[0] + theta[1]) + np.cos(theta[0] + theta[1] + theta[0] + theta[2])
        p2 = np.sin(theta[0]) + np.sin(theta[0] + theta[1]) + np.sin(theta[0] + theta[1] + theta[0] + theta[2])
        return x[0] - (x[0] - p1), x[1] - (x[1] - p2)


    nengo.Connection(robot, robot, function=feedback, synapse=.01)
    nengo.Connection(stim, robot)

    stim_p = nengo.Probe(stim)
    osc_p = nengo.Probe(robot, synapse=.01)

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