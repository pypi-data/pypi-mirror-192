from fireTS.models import NARX
import numpy as np
from neupy import algorithms
from neupy.layers import *

x = np.array([[1, 2], [3, 4]])
y = np.array([[1], [0]])

#y = np.ravel(y) <-just to avoid a warning (the error is the same without comment)

network = Input(2) >> Sigmoid(3) >> Sigmoid(1)
optimizer = algorithms.LevenbergMarquardt(network)

mdl1 = NARX(
    optimizer,  #I change random forest for LevenbergMarquardt
    auto_order=2,
    exog_order=[2, 2],
    exog_delay=[1, 1])

mdl1.fit(x, y, batch_size=1)

ypred1 = mdl1.predict(x, y)
