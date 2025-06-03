import pathlib as pl

import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

fp = pl.Path(r'W:\NELSON\Desktop\west_yellowstone\sample-1.jpg')
im = Image.open(fp)
as_hsv = im.convert('HSV')
hsv_arr = np.asarray(as_hsv)

hue = hsv_arr[:,:,0] * np.pi / 180

N = 60
bottom = 1

image_arr = np.asarray(im)
print(image_arr.shape)

theta = np.linspace(0.0, 2 * np.pi, N, endpoint=True) # bins
heights, edges = np.histogram(hue, bins=N)

print(theta.shape)
print(edges.shape)
print(heights.shape)

heights = 10* np.asarray(heights, dtype=np.float64) / float(sum(heights)) 
width = (2*np.pi) / N

ax = plt.subplot(111, polar=True)
bars = ax.bar(theta, heights, width=width, bottom=bottom)

# Use custom colors and opacity
for r, bar in zip(theta, bars):
    bar.set_facecolor(plt.cm.hsv(bar.get_x()/(2*np.pi)))
    bar.set_alpha(1.0)

plt.show()