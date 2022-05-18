import numpy as np
from scipy.special import factorial

def stirlingapprox(n):
    return np.power(n, n) * np.exp(-n) * np.sqrt(n) * np.sqrt(2*np.pi)

if __name__ == "__main__":
    print(stirlingapprox(5))
    print(factorial(5, exact=True))