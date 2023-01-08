import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def dice_hist(num_dice, die_size, verbose=False, stats=False):
    x = np.ones(die_size)
    p = np.ones(die_size)
    for j in range(num_dice-1):
        p = np.convolve(p, x, mode='full')
        if verbose:
            bins = np.arange(p.size) + num_dice
            u = np.dot(bins,p)/np.sum(p)
            deviations = np.dot(p, np.square(bins - u))
            s2 = deviations / p.sum()   
            std = np.sqrt(s2)
            print('{:>3}: std:{:>8.4}'.format(j, std/u))
    bins = np.arange(p.size) + num_dice
    if stats:
        u = np.dot(bins,p)/np.sum(p)
        s2 = np.dot(p, np.square(bins - u)) / p.sum()
        std = np.sqrt(s2)
        return p, bins, u, std
    else:
        return p, bins

def dice_mult_hist(num_dice, die_size):
    z = np.arange(die_size)+1
    x = np.arange(die_size)+1
    for j in range(num_dice):
        z = np.outer(z,x)
    z = z.flatten()
    plt.hist(z)
    plt.show()

def dice_hist_generator(max_num_dice:int, die_size:int, stats=True):
    x = np.ones(die_size)
    p = np.ones(die_size)
    dice_count = 1

    for j in range(max_num_dice-1):
        p = np.convolve(p, x, mode='full')
        dice_count += 1
        b = np.arange(p.size) + dice_count
        if stats:
            u = np.dot(b, p) / np.sum(p)
            s = np.sqrt( np.dot(p, np.square(b - u)) / p.sum())
            yield dice_count, p, b, u, s
        else:
            yield dice_count, p, b


def dice_hist_optimized(num_dice, die_size, stats=False):
    p = np.ones(die_size)

    b = np.flip(np.asarray([bool(int(k)) for k in format(num_dice, 'b')]))
    digits = len(b)
    p_units = [None] * digits
    p_units[0] = p
    for j in range(1, digits):
        p_units[j] = np.convolve(p_units[j-1], p_units[j-1], mode = 'full')

    agg = []
    for pi, bi in zip(p_units, b):
        if bi:
            agg.append(pi)
    
    p_out = aggregate_convolutions(agg)
    bins = np.arange(p_out.size) + num_dice
    if stats:
        N = p_out.sum()
        u = np.dot(bins, p_out) / np.sum(N)
        s = np.sqrt( np.dot(p_out, np.square(bins - u)) / N)
        return p_out, bins, u, s
    else:
        return p_out, bins

def dice_hist_sequence(seq, stats=False):
    """ Given a sequence of dice sizes, find the PDF of sums
    """
    min_roll_possible = len(seq) # assumes lowest number on each die is a 1
    agg = []
    while len(seq) >= 2:
        a = np.ones(seq.pop())
        b = np.ones(seq.pop())
        agg.append(np.convolve(a, b))
    
    if len(seq) > 0:
        for l in seq:
            agg.append(np.ones(l))
    
    p_out =  aggregate_convolutions(agg)

    bins = np.arange(p_out.size) + min_roll_possible
    if stats:
        N = p_out.sum()
        u = np.dot(bins, p_out) / np.sum(N)
        s = np.sqrt( np.dot(p_out, np.square(bins - u)) / N)
        return p_out, bins, u, s
    else:
        return p_out, bins

def aggregate_convolutions(agg:list):

    while len(agg) > 1:
        agglen = len(agg)
        new_agg = []
        if agglen % 2 == 0:
            ct = agglen / 2
        else:
            new_agg.append(agg[-1])
            ct = (agglen-1)/2
        for j in range(int(ct)):
            new_agg.append(np.convolve(agg[2*j], agg[2*j +1]))
        
        agg = new_agg
    
    return agg[0]
    



def monoExp(x, m, t, b):
    return m * np.exp(-t * x) + b

if __name__ == '__main__':
    rolls = 128
    # die_sizes = [4, 6, 10,20]
    die_sizes = np.arange(6,100)
    fig, ax = plt.subplots(1,1)

    lo = []
    hi = []
    mid = []
    for n in die_sizes:
        p, b, u, s = dice_hist_optimized(rolls, n, stats=True)
        # p, b, u, s = dice_hist(rolls, n, stats=True)
        p /= p.sum()
        xlo = int(np.floor(u-s))
        lo.append((xlo, p[xlo]))

        xu = u
        mid.append((xu, max(p)))

        xhi = int(np.floor(u+s))
        hi.append((xhi, p[xhi]))

        # if not (n % 7):
            # ax.bar(b, p, width=1, label='{}: u={:>5.4}, s={:>5.4}'.format(n, u, s), alpha=0.7)
        # ax.plot(b, p/p.sum(), '-o', label='{}: u={:>5.4}, s={:>5.4}'.format(n, u, s))
    lo = np.asarray(lo).T
    hi = np.asarray(hi).T
    mid = np.asarray(mid).T

    x_exp = mid[0]
    y_exp = mid[1]
    # ax.plot(lo[0], lo[1], '-o', label='u-s')
    # ax.plot(hi[0], hi[1], '-o', label='u+s')
    ax.plot(x_exp, y_exp, '-o', label='u')
    ax.legend()
    ax.set_title('{} rolls'.format(rolls))

    popt, pcov = curve_fit(monoExp,  x_exp, y_exp)
    print(popt)

    plt.show()
