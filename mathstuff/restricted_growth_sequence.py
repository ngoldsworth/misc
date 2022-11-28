def __valid_rgs(a: list, unique_ct: int):
    """
    For what makes a valid 'Restricted Growth String':
    https://mathworld.wolfram.com/RestrictedGrowthString.html
    """
    if len(set(a)) > unique_ct:
        return False

    for j in range(0, len(a) - 1):
        if not (a[j + 1] <= 1 + max(a[: (j + 1)])):
            return False

    return True


def __increment_rgs(a: list, unique_ct: int):
    """Helper function to increment a valid rgs

    Assumes input `a` is valid rgs, i.e. __valid_rgs(a) returns true.
    """
    a[-1] += 1
    if __valid_rgs(a, unique_ct):
        return a

    else:
        return __increment_rgs(a[:-1], unique_ct) + [0]


def restricted_growth_string_generator(seqlen: int, unique_ct=None):

    if unique_ct is None:
        unique_ct = seqlen

    seq = [0] * seqlen
    maxseq = list(range(unique_ct))

    while len(maxseq) < seqlen:
        maxseq.append(maxseq[~0])

    while seq < maxseq:
        yield seq

        seq = __increment_rgs(seq, unique_ct)

    yield maxseq


if __name__ == "__main__":

    j = 0
    for s in restricted_growth_string_generator(5, 2):
        # print(''.join([chr(j+65) for j in s]), len(set(s)))
        print("".join([chr(j + 65) for j in s]))

        j += 1

    print(j)
