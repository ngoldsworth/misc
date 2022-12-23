import numpy as np
import matplotlib.pyplot as plt

def f(u):
    return np.exp(u)

u = 50*np.random.uniform(low=0, high=1, size=10**7)
# u = np.random.normal(0, 1, (5,10000))
plt.hist(np.log(f(u)), bins=1000)

plt.show()