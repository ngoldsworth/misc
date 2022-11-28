import matplotlib.pyplot as plt
import numpy as np
import scipy.fft

n = 10**4
x = np.linspace(0, 1000, n)
k = 10

idx = np.arange(x.size)
signal = idx
signal[idx % 2 == 0] = 0

fourier = scipy.fft.fft(signal)

freq = np.fft.fftfreq(n, d=(1 / 1000))

plt.plot(x, signal)

plt.figure()
plt.plot(freq[1:], np.real(fourier[1:]))

plt.show()
