import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

m = 5
b = 7

rows = 10
ct = 10**5

# x0 = np.random.uniform(-100, 100, ct)
x0 = np.linspace(-100, 100, ct)
y0 = m*x0 + b

sigma  = np.square(np.sin(np.pi*np.arange(ct)/ct))

y = np.zeros((rows, ct))
x = np.zeros((rows, ct))
for k in range(rows):
    x[k] = x0
    y[k] = y0 + np.random.normal(0, sigma, ct)
    plt.plot(x0, y[k], ',')

r = linregress(x.flatten(), y.flatten())
plt.title(f'$y={r.slope:.2f}x + {r.intercept:.2f}, (1-r^2) = {1-r.rvalue**2:.4e}$')

plt.show()