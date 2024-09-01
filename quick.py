import matplotlib.pyplot as plt
import numpy as np

x = np.logspace(5,6)
y = x * 1.1* 5.5/(12*100)
plt.plot(x,y)
plt.xscale('log')
plt.show()