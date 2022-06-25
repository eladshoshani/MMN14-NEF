import numpy as np
import nengo
import matplotlib.pyplot as plt
from nengo.utils.matplotlib import rasterplot
from nengo.dists import Uniform
from nengo.dists import Choice
from nengo.utils.ensemble import tuning_curves
from nengo.processes import Piecewise

model = nengo.Network(label='Neurons')
with model:
    neurons = nengo.Ensemble(50, dimensions=1)
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
