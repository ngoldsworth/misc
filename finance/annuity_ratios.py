import numpy as np

i = np.linspace(1.5, 10.0, 50, True) / (12*100)
n = np.asarray([48,60,72])

def rat(i, n):
    a = i * (1+i)**n
    a /= (1+i)**n - 1
    return a

iv, nv = np.meshgrid(i, n)

print(100*rat(iv, nv))
