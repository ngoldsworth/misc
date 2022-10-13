import matplotlib.pyplot as plt
import numpy as np

digits = 6
sml = 10 ** (digits - 1)
lrg = (10 ** digits) - 1

counts = [0] * digits

print(sml, lrg + 1)

# for j in range(sml, lrg+1):
for j in range(lrg + 1):
    n = len(set(str(j).zfill(digits)))
    counts[n - 1] += 1
    if j % (10 ** (digits - 2)) == 0:
        print(j)


print(counts)
print(sum(counts))

x = np.arange(digits) + 1
c = np.asarray(counts) / sum(counts)

plt.bar(x, c)
plt.show()


# 10^9 result: [10, 22950, 2178000, 39160800, 210198240, 400075200, 279417600, 65318400, 3628800]
