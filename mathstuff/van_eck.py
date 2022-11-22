"""
I was watching a Numberphile video with Matt Parker, he was talking about the Van Eck sequence.
"""

import matplotlib.pyplot as plt
import numpy as np


def next_van_eck(seq: list) -> int:
    j = 0
    current_number = seq[~j]
    lenseq = len(seq)
    j += 1

    while seq[~j] != current_number:
        j += 1
        if j >= lenseq:
            return 0

    return j


def next_stern_row(line):
    new_row = []

    for j in range(len(line) - 1):
        new_row.append(line[j])
        new_row.append(line[j] + line[j + 1])

    new_row.append(line[-1])  # emit last line, get fractions enumeration
    return new_row


if __name__ == "__main__":
    s = [1, 2, 1]
    for z in range(3):
        s = next_stern_row(s)
        print(s)
