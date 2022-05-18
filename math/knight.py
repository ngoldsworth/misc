import numpy as np
import scipy.special
from numpy.core.fromnumeric import size

def knight_move(i, j):
    return [(x,y) for (x,y) in [(i+2, j-1), (i+2, j+1), (i-2, j-1), (i-2, j+1), (i+1, j+2), (i+1, j-2), (i-1, j+2), (i-1, j-2)] if (x >=0 and y>=0)]

def find_next_spot(
    visited:list,
    location:tuple,
    traversing_array:np.ndarray,
):
    best = None
    new_location = (0, 0)

    for x, y in knight_move(location[0], location[1]):
        best = traversing_array.size+1
        if traversing_array[x, y] < best and (x, y) not in visited:
            new_location = x, y
        
    visited.append(new_location)
    return visited, new_location

def triangular(n:int or np.ndarray):
    """nth triangular number is defined as (n+1 choose 2)"""
    return array_combination(n+1, 2)

def __exact_fact(n):
    return scipy.special.factorial(n, exact=True)

def array_combination(n, k):
    """over arrays, do n choose k"""

    return (__exact_fact(n) / (__exact_fact(n-k) * __exact_fact(k)))

class TriangleBoard():
    """On a triangular board, returns coords of kth digit

    Triangle is structured:

      1   3  6 10 15 21 28 36 ...
      2   5  9 14 20 27 35 ...
      4   8 13 19 26 34 ...
      7  12 18 25 33 ...
      11 17 24 32 ...
      16 23 31 ...
      22 30 ...
      29 ...

      1st diagonal { 1 } has 1 entry and ends with 1st Triangular number T_1
      2nd diagonal { 2, 3 } has 2 entries and ends with 2nd Triangular number T_2
      nth diagonal has 'n' entries and ends with the nth triangular number
    """

    def __init__(self):
        return

    def get_coordinate(k):
        # given integer k, it lies on diagon n iff T_(n-1) < k <= T_n
        # solve for n in k = T_n, take ceiling of result
        n_diag = np.ceil(0.5 * (np.sqrt(8*k+1) - 1))
        Tn = triangular(n_diag)

        d = Tn - k # distance from k to Tn, which is located at (y=0, x=n-1)
        x = n_diag - 1 - d
        y = d
        return x, y
    
    def value_at(x, y):
        Tn = triangular(x + y + 1) # on nth diagonal, n = x + y + 1
        return(Tn - y)

class RectangularSpiralBoard():
    def __init__(self):
        return

    def diag_ur(self, n):
        return 4*(n**2) - 2*n + 1

    def diag_ul(self, n):
        return (2*n)**2 + 1

    def diag_dl(self, n):
        return 4*(n**2) + (2*n) + 1

    def diag_dr(self, n):
        return (2*n + 1)**2
    
    def diag_val(self, x, y):
        if x >= 0: 
            if y >= 0:
                return self.diag_ur(x)
            else:
                return self.diag_dr(x)
        else:
            if y>= 0:
                return self.diag_ul(x)
            else:
                return self.diag_dl(x)

    def value_at(self, x, y):
        y_abs = np.abs(y)
        x_abs = np.abs(x)

        if x_abs == y_abs:
            # x,y is a point along a diagonal
            return self.diag_val(x, y)

        elif x > y_abs:
            # x > 0, and -x < y < x
            # "right" quadrant
            # upper bound is y=x,
            # return value on y=x diagnal for this x, then subtract off y
            return self.diag_ur(x_abs) - (x - y)

        elif y > x_abs:
            # y > 0 and y > x and y > -x
            # upper quadrant
            # upper bound is y = -x
            return self.diag_ul(y_abs) - (y - x)

        elif x < -y_abs:
            # x < 0 and -x < y < x
            # left quad
            # "upper" bound (in ccw dir) is y = x
            return self.diag_dl(x_abs) - (y - x)

        elif y < x_abs:
            # bottom quad
            # in ccw direction, upper bounf is y = -x
            return self.diag_dr(y_abs) - (y - x)

        else:
            return None

    def get_coords(self, k: int):
        if k <= 0:
            raise ValueError("must be a positive integer")
        if k == 1:
            return (0, 0)

        n = np.ceil(0.5 * (np.sqrt(k) - 1))

        dr = self.diag_dr(n)
        dl = self.diag_dl(n)
        ul = self.diag_ul(n)
        ur = self.diag_ur(n)

        if dr == k:
            x =  n
            y = -n

        elif dl < k and k < dr:
            y = -n
            x = n - (dr - k)

        elif dl == k:
            x, y = ( -n, -n)

        elif ul < k and k < dl:
            x = -n
            y = -n + (dl - k)

        elif ul == k:
            x, y = (-n, n)

        elif ur < k and k < ul:
            y = n
            x = -n + (ul - k)

        elif ur == k:
            x, y = (n, n)

        elif k < ur:
            x = n
            y = n - (ur - k)

        return (x, y)

if __name__ == '__main__':
    rsb = RectangularSpiralBoard()
    t = rsb.value_at(3, -3)
    print(t)


