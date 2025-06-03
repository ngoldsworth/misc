import numpy as np
import scipy.fft
import matplotlib.pyplot as plt


def digitsum(n):
    return sum([int(c) for c in list(str(n))])


N = 300
arr = np.zeros((N, N))

for j in range(N):
    print(j)
    for i in range(N):
        arr[i, j] = digitsum(i * j)

plt.imshow(arr)

plt.show()
