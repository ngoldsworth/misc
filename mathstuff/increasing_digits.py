from math import comb
import matplotlib.pyplot as plt


def increasing_digits_count(num_digits):
    return sum(comb(num_digits + k - 1, k) for k in range(10))


def count_bouncy(n):
    return 10 ** (n + 1) - 2 * increasing_digits_count(n)


print(2 * increasing_digits_count(6))
