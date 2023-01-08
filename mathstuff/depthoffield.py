import astropy.units as u

def dof(u, f, N, c):
    return 2 * (u/f)**2 * N * c

if __name__ == '__main__':
    mm = u.meter / 1000
    u = 3.5 * u.meter
    f = 85 * mm
    N = 2.8
    c = .019 * mm

    print(dof(u, f, N ,c))