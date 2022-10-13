import numpy as np
import matplotlib.pyplot as plt
from numpy.core.numeric import ones_like
from numpy.lib.arraysetops import isin


def generate_fibonacci(n):
    lst = [0, 1]
    while len(lst) < n:
        lst.append(lst[-1] + lst[-2])

    return np.asarray(lst)


def g(x: int, y: int, fibo: np.ndarray, n: int = -1):
    return x * fibo[n - 1] + y * fibo[n]


def g_sequence(x, y, fibo):
    return x * fibo[:-1] + y * fibo[1:]


def consecutive_ratio(q, fibo):
    if not isinstance(q, np.ndarray):
        q = np.asarray([q])

    lower = fibo[:-2]
    mid = fibo[1:-1]
    upper = fibo[2:]

    num = np.outer(mid, q) + np.outer(upper, np.ones_like(q))
    denom = np.outer(lower, q) + np.outer(mid, np.ones_like(q))

    return num / denom


if __name__ == "__main__":
    phi = (1 / 2) * (1 + np.sqrt(5))
    fibo = generate_fibonacci(1000)
    q = np.linspace(
        0,
        25,
        300,
    )
    arr = consecutive_ratio(q, fibo)
    print(arr.shape)

    idx = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for j in idx:
        plt.plot(q, arr[j], label="$n={}$".format(j))

    plt.legend()
    plt.vlines([phi, phi - 1], np.amin(arr), np.amax(arr))
    plt.xlabel("$Q$")

    plt.show()
