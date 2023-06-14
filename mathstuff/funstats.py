from scipy import stats
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1)
n = stats.norm

y = []
xs=[]
for x in range(100):
    xs.append(x/10)
    y.append( 1 - (n.cdf(x/10) - n.cdf(-x/10) ))

ax.plot(xs,y)
ax.set_yscale('log')
plt.show()
    
