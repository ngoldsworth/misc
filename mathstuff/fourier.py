import matplotlib.pyplot as plt
import numpy as np
import scipy.fft

import itertools

T = 10**4

x = np.arange(T)
w = 2*np.pi/T * x

y1 = np.sin(w *1)
y2 = np.sin(w * 2)
y3 = np.sin(3 * w)
y5 = np.sin(5 * w)
y6 = np.sin(6 * w)
y10 = np.sin(10 * w)
y15 = np.sin(15 * w)
y30 = np.sin(30 * w)

yT = y2 * y3 * y5 * y30

# fft_kT = abs(scipy.fft.fft(yT))
# kT = scipy.fft.fftfreq(yT.size, 1/T)

# plt.plot(kT, fft_kT)
# plt.plot(yT)

fpos = [2, 3, 5, 30]
f2 = [1, 6, 10, 15]

fs = ([x, -x] for x in fpos)
fs2 = ([x, -x] for x in f2)

num = []
for k in itertools.product(*fs):
    num.append(abs(sum(k)))

den = []
for k in itertools.product(*fs2):
    den.append(abs(sum(k)))

num = set(num)
den = set(den)
print(num)
print(den)
