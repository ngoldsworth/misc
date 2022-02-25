import typing as t
import math
from sympy import re

from sympy.utilities.iterables import partitions


def multinomial_coefficient(n: int, k: t.List[int]) -> int:
    num = math.factorial(n)

    # don't need to divide by 1
    for i in k:
        num /= i

    return num


def partitions_generator(n, k=None):
    """Generate all partitions of integer n (>= 0) using integers no
    greater than k (default, None, allows the partition to contain n).

    Each partition is represented as a multiset, i.e. a dictionary
    mapping an integer to the number of copies of that integer in
    the partition.  For example, the partitions of 4 are {4: 1},
    {3: 1, 1: 1}, {2: 2}, {2: 1, 1: 2}, and {1: 4} corresponding to
    [4], [1, 3], [2, 2], [1, 1, 2] and [1, 1, 1, 1], respectively.
    In general, sum(k * v for k, v in a_partition.iteritems()) == n, and
    len(a_partition) is never larger than about sqrt(2*n).

    Note that the _same_ dictionary object is returned each time.
    This is for speed:  generating each partition goes quickly,
    taking constant time independent of n. If you want to build a list
    of returned values then use .copy() to get copies of the returned
    values:

    >>> p_all = []
    >>> for p in partitions(6, 2):
    ...         p_all.append(p.copy())
    ...
    >>> print p_all
    [{2: 3}, {1: 2, 2: 2}, {1: 4, 2: 1}, {1: 6}]

    Reference
    ---------
    Modified from Tim Peter's posting to accomodate a k value:
    http://code.activestate.com/recipes/218332/
    """

    # shamlessly stolen from:
    # https://code.activestate.com/recipes/218332-generator-for-integer-partitions/

    if n < 0:
        raise ValueError("n must be >= 0")

    if n == 0:
        yield {}
        return

    if k is None or k > n:
        k = n

    q, r = divmod(n, k)
    ms = {k: q}
    keys = [k]
    if r:
        ms[r] = 1
        keys.append(r)
    yield ms

    while keys != [1]:
        # Reuse any 1's.
        if keys[-1] == 1:
            del keys[-1]
            reuse = ms.pop(1)
        else:
            reuse = 0

        # Let i be the smallest key larger than 1.  Reuse one
        # instance of i.
        i = keys[-1]
        newcount = ms[i] = ms[i] - 1
        reuse += i
        if newcount == 0:
            del keys[-1], ms[i]

        # Break the remainder into pieces of size i-1.
        i -= 1
        q, r = divmod(reuse, i)
        ms[i] = q
        keys.append(i)
        if r:
            ms[r] = 1
            keys.append(r)

        yield ms


def partition_to_list(partition:dict)->list:
    lst = []
    for k in partition:
        for j in range(partition[k]):
            lst.append(k)
    
    return lst

def partition_number_of_parts(partition:dict)->int:
    count = 0
    for k in partition:
        count += partition[k]
    
    return count

def repeat_count(partition:dict)->int:
    r = 1
    for k in partition:
        r *= math.factorial(partition[k]) 
    
    return r

def g(digit_count: int, base: int, partition: dict):

    # account for any digit that could fill a slot
    # if a number hs 3 unique digits "A", "B", and "C"
    # 10 ways to assign to A, leaving 9 ways to  assign to B, C has 8...

    # if "AABC", filling assigning digits is not dependent on number of digits, but number of unique digits
    unique_digits = partition_number_of_parts(partition)
    assign_digits = math.perm(base, unique_digits)

    # a four-digit number with three 2 unique digits can be written "ABAB", "AABB" "BABA" "BBAA"...
    # there are multiple qays to arrange repeated values
    arrangement_coeff = multinomial_coefficient(digit_count, partition_to_list(partition))

    # In a 6 digit number, the pattern "AAABBB" and "BBBAAA" describe the same set of numbers, divide by 2!
    # "AABBCC" and "BBAACC" and "CCBBAA"... describe te same set of numbers, divide by 6 = 3!
    # do this division since acounting for A={1..9}, B={1..9, != A} done in 
    repeat_divisor = repeat_count(partition)

    return assign_digits * arrangement_coeff / repeat_divisor
    # return arrangement_coeff * assign_digits





if __name__ == "__main__":
    base = 10  # try for hexadecimal later
    num_digits = 6  # total number of digits in the number
    num_unique = 3  # number of uniqe digits in the number


    """
    sympy.utilities.iterables.partitions produces dicts of the format
    {4: 1} as in "4 occurs in this partition once"
    {3: 2, 1: 1} as in "3 occurs as a part twice and 1 occurs once as a part"
    """

    g_tot = 0

    for j in partitions(num_digits, m=base):
        gi = g(num_digits, base, j)
        g_tot += gi
        print(gi, j)
        print(j, partition_number_of_parts(j))

    print("")
    print(g_tot)
    print(math.perm(base, num_digits))

    # c = 0
    # for j in range(0, 10000):
    #     if len(set(str(j).zfill(4))) == 2:
    #         print(j)
    #         c += 1
    # print(c)
        