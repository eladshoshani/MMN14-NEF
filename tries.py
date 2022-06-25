import numpy as np
import nengo
import matplotlib.pyplot as plt
from nengo.utils.matplotlib import rasterplot
from nengo.dists import Uniform
from nengo.dists import Choice
from nengo.utils.ensemble import tuning_curves
from nengo.processes import Piecewise

model = nengo.Network()
with model:
    a = nengo.Ensemble(n_neurons=1,
                       dimensions=1)


    def stim_func(t):
        return np.sin(10 * t)

    stim = nengo.Node(stim_func)

    nengo.Connection(stim, a)
