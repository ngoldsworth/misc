from itertools import permutations
from typing import Iterable

def cyclic_permutations(I:Iterable):
    i0 = I[0]
    for p in permutations(I[1:]):
        yield i0, *p

if __name__ == '__main__':
    st = "ABCDEF"
    z = sorted(a for a in cyclic_permutations(st))
    for zi in z:
        print(*zi)