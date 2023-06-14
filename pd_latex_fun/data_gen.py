import numpy as np
import pathlib as pl
import matplotlib.pyplot as plt

sz = 10000
x = np.arange(sz)
signal = np.sin(8*np.pi*x/sz)*np.cos(12*np.pi*x/sz)

noise = np.random.normal(loc=0,scale=.1,size=x.size)

y = signal + noise

plt.plot(x, y)
plt.show()