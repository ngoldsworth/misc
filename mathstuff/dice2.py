import numpy as np
import dice as dicelib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def possible_best_fit(x, k):
    return np.power((x*k), -0.5)

def hyper(x, b, c):
    return 12 - b/((x-c))

if __name__ == '__main__':

    # die_sizes = [4,6,8,12,20,100,] # platonic solids
    die_sizes = np.arange(2,200,2)
    rolls = 50

    fig, ax = plt.subplots(1,1)
    kfig, kax = plt.subplots(1,1)

    kx, ky = [], []
    for d in die_sizes:
        x = []
        y = []

        for r, p, b, u, s in dicelib.dice_hist_generator(rolls, d):
            x.append(r)
            span = b[-1] - b[0]
            y.append(s/span)
            # y.append(s/u)


        popt, pcov = curve_fit(possible_best_fit, x, y)
        k = popt[0]

        t = np.linspace(x[0], x[-1], rolls*4)
        yt = possible_best_fit(t, k)

        # ax.plot(x, y, 'o', label='{}-sided die'.format(d))
        # ax.plot(t, yt, '-', label='best fit for {}-sided die: k={}'.format(d, k))

        kx.append(d)
        ky.append(k)



    x = np.linspace(x[0],x[-1],500)
    # ax.plot(x, np.sqrt(1/(12*x)), label='$(12n)^{-1/2}$')

    popt2, pcov2 = curve_fit(hyper, kx, ky)
    print('b={}, c={}'.format(popt2[0], popt2[1]))
    kax.plot(kx, ky)
    kax.plot(kx, hyper(np.asarray(kx), popt2[0], popt2[1]))
    # kax.set_yscale('log')
    
    ax.set_xlabel('Rolls')
    # ax.set_ylabel('$\sigma / \mu$')
    ax.set_ylabel('$\sigma / \\rm{R}$')
    ax.legend()
    plt.show()
