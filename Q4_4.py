
import nengo
import numpy as np
import matplotlib.pyplot as plt

model = nengo.Network('Q4')
theta = [np.pi / 6, np.pi / 4, np.pi / 3]
with model:
    N = 1000
    p1 = np.cos(theta[0]) + np.cos(theta[0] + theta[1]) + np.cos(theta[0] + theta[1] + theta[0] + theta[2])
    p2 = np.sin(theta[0]) + np.sin(theta[0] + theta[1]) + np.sin(theta[0] + theta[1] + theta[0] + theta[2])

    stim1 = nengo.Node(p1)
    stim2 = nengo.Node(p2)

    # final Ensemble for the robot:
    robot = nengo.Ensemble(N, dimensions=2)
    nengo.Connection(stim1, robot[0])
    nengo.Connection(stim2, robot[1])

    output = nengo.Node(None, size_in=2)
    c = nengo.Connection(robot.neurons, output,
                         transform=np.zeros((2, N)),
                         learning_rule_type=nengo.PES(
                             learning_rate=0.0001))

    error = nengo.Node(None, size_in=1)
    nengo.Connection(output, error)
    nengo.Connection(stim1, error, transform=-1)
    nengo.Connection(error, c.learning_rule)




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