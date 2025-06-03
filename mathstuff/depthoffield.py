import astropy.units as u

import numpy as np
import matplotlib.pyplot as plt

def dof(u, f, N, c):
    return 2 * (u/f)**2 * N * c

if __name__ == '__main__':
    mm = u.meter / 1000
    # u = 3.5 * u.meter
    x = np.linspace(0,25,100) * u.meter
    f = 85 * mm
    N = 1.4
    c = .019 * mm

    d = dof(x, f, N ,c)
    plt.plot(x, d)
    plt.show()