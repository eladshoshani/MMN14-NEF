
import nengo
import numpy as np
import matplotlib.pyplot as plt

model = nengo.Network('Q4')
theta = [np.pi / 6, np.pi / 4, np.pi / 3]
with model:
    N = 100
    stim1 = nengo.Node(theta[0])
    stim2 = nengo.Node(theta[1])
    stim3 = nengo.Node(theta[2])

    ensA1 = nengo.Ensemble(N, dimensions=1)
    ensA2 = nengo.Ensemble(N, dimensions=1)
    ensA3 = nengo.Ensemble(N, dimensions=1)

    nengo.Connection(stim1, ensA1)
    nengo.Connection(stim2, ensA2)
    nengo.Connection(stim3, ensA3)

    # ensSum2 = theta1 + theta2
    ensSum2 = nengo.Ensemble(N, dimensions=1)
    nengo.Connection(ensA1, ensSum2)
    nengo.Connection(ensA2, ensSum2)

    # ensSum3 = theta1 + theta2 + theta3 = ensSum2 + theta3
    ensSum3 = nengo.Ensemble(N, dimensions=1)
    nengo.Connection(ensSum2, ensSum3)
    nengo.Connection(ensA3, ensSum3)

    # ensB1 = np.cos(theta1)
    ensB1 = nengo.Ensemble(N, dimensions=1)
    nengo.Connection(ensA1, ensB1, function=lambda x: np.cos(x))
    # ensB2 = np.cos(theta1 + theta2)
    ensB2 = nengo.Ensemble(N, dimensions=1)
    nengo.Connection(ensSum2, ensB2, function=lambda x: np.cos(x))
    # ensB3 = np.cos(theta1 + theta2 + theta3)
    ensB3 = nengo.Ensemble(N, dimensions=1)
    nengo.Connection(ensSum3, ensB3, function=lambda x: np.cos(x))

    # do the same for sin instead of cos:
    ensC1 = nengo.Ensemble(N, dimensions=1)
    nengo.Connection(ensA1, ensC1, function=lambda x: np.sin(x))

    ensC2 = nengo.Ensemble(N, dimensions=1)
    nengo.Connection(ensSum2, ensC2, function=lambda x: np.sin(x))

    ensC3 = nengo.Ensemble(N, dimensions=1)
    nengo.Connection(ensSum3, ensC3, function=lambda x: np.sin(x))

    # final Ensemble for the robot:
    robot = nengo.Ensemble(N, dimensions=2)
    # x_cord = ensB1 + ensB2 + ensB3:
    nengo.Connection(ensB1, robot[0])
    nengo.Connection(ensB2, robot[0])
    nengo.Connection(ensB3, robot[0])
    # y_cord = ensC1 + ensC2 + ensC3:
    nengo.Connection(ensC1, robot[1])
    nengo.Connection(ensC2, robot[1])
    nengo.Connection(ensC3, robot[1])


    # def feedback(x):
    #     p1 = np.cos(theta[0]) + np.cos(theta[0] + theta[1]) + np.cos(theta[0] + theta[1] + theta[0] + theta[2])
    #     p2 = np.sin(theta[0]) + np.sin(theta[0] + theta[1]) + np.sin(theta[0] + theta[1] + theta[0] + theta[2])
    #     return x[0] - (x[0] - p1), x[1] - (x[1] - p2)


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