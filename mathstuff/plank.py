import matplotlib.pyplot as plt
import numpy as np

import astropy.units as u
import astropy.constants as c

# h = 6.626e-34
# c = 3.0e8
# k = 1.38e-23
print(c.k_B)


def planck(wav, T, norm=True):
    a = 2.0 * c.h * c.c**2
    b = c.h * c.c / (wav * c.k_B * T)
    print(b)
    intensity = a / ((wav**5) * (np.exp(b) - 1.0))
    if norm:
        intensity /= intensity.sum()
    return intensity


# generate x-axis in increments from 1nm to 3 micrometer in 1 nm increments
# starting at 1 nm to avoid wav = 0, which would result in division by zero.
wavelengths = np.arange(1e-9, 3e-6, 1e-9)

# intensity at 4000K, 5000K, 6000K, 7000K
intensity1800 = planck(wavelengths, 4000.0*u.K)
intensity2100 = planck(wavelengths, 2100.0*u.K)
intensity2400 = planck(wavelengths, 2400.0*u.K)
intensity2700 = planck(wavelengths, 2700.0*u.K)
intensity3000 = planck(wavelengths, 3000.0*u.K)


# plt.plot(wavelengths*1e9, intensity1800, 'r-')
# plot intensity4000 versus wavelength in nm as a red line
# plt.plot(wavelengths*1e9, intensity2100, 'g-') # 5000K green line
# plt.plot(wavelengths*1e9, intensity2400, 'b-') # 6000K blue line
# plt.plot(wavelengths*1e9, intensity2700, 'c-') # 7000K black line
# plt.plot(wavelengths*1e9, intensity3000, 'm-') # 7000K black line


plt.plot(wavelengths * 1e9, intensity2100, "g-")  # 5000K green line
plt.plot(
    wavelengths * 1e9, (intensity1800 + intensity2400) / 2, "b-"
)  # 6000K blue line

plt.show()
