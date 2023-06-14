import timeit
import numpy as np
from multiprocessing import Pool

def f(x):
    return x**x

if __name__ == '__main__':

    threads_ct = 3
    iterations = 100

    t = []

    for j in range(iterations):
        if not (j%10):
            print(j)
        start = timeit.default_timer()
        with Pool(threads_ct) as p:
            k = p.map(f, range(100))
        stop = timeit.default_timer()
        t.append(stop-start)

    t = np.asarray(t)
    print(t.mean(), t.std())
