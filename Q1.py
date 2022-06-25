import numpy as np
import nengo
from matplotlib import pyplot as plt
from nengo.utils.matplotlib import rasterplot
from nengo.dists import Uniform

# FOR Q1F
# model = nengo.Network()
# with model:
#     stim = nengo.Node([0])
#     a = nengo.Ensemble(n_neurons=50, dimensions=1)
#
#     def stim_func(x):
#         return np.sin(x) + x
#
#     nengo.Connection(stim, a)

def q1d():
    from nengo.utils.ensemble import tuning_curves
    model = nengo.Network(label='Neurons')
    N = 3
    with model:
        neurons = nengo.Ensemble(N, dimensions=1, radius=10)
        connection = nengo.Connection(neurons, neurons)  # This is just to generate the decoders

    sim = nengo.Simulator(model)

    d = sim.data[connection].weights.T
    x, A = tuning_curves(neurons, sim)
    xhat = np.dot(A, 1 * d)

    x = 1 * x
    plt.figure(figsize=(3, 4))
    plt.plot(x, A)
    plt.xlabel('x')
    plt.ylabel('firing rate (Hz)')

    plt.figure()
    plt.plot(x, x, linewidth=4, label='f(x)=x')
    plt.plot(x, xhat, 'r', linewidth=4, label='$\hat{x}$')
    plt.xlabel('$x$')
    plt.ylabel('$f(x)$')
    plt.legend()
    plt.show()

def q1h():
    from nengo.utils.ensemble import tuning_curves
    model = nengo.Network(label='Neurons')
    N = 100
    with model:
        neurons = nengo.Ensemble(N, dimensions=1)
        connection = nengo.Connection(neurons, neurons)  # This is just to generate the decoders

    sim = nengo.Simulator(model)

    d = sim.data[connection].weights.T
    x, A = tuning_curves(neurons, sim)
    xhat = np.dot(A, 1 * d)

    x = 1 * x
    plt.figure(figsize=(3, 4))
    plt.plot(x, A)
    plt.xlabel('x')
    plt.ylabel('firing rate (Hz)')

    plt.figure()
    plt.plot(x, x, linewidth=4, label='f(x)=x')
    plt.plot(x, xhat, 'r', linewidth=4, label='$\hat{x}$')
    plt.xlabel('$x$')
    plt.ylabel('$f(x)$')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    q1d()