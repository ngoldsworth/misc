import numpy as np
import matplotlib.pyplot as plt

L = 10**4

y = []
for k in range(100):
    H = 10*k
    x = np.random.uniform(0,1,L*H)
    x.resize((L,H))
    y.append(np.std(x.sum(-1)))

plt.plot(y)
# plt.hist(x.sum(-1), bins=100)
plt.show()