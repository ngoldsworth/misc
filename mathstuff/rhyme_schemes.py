import numpy as np
import matplotlib.pyplot as plt


def increasing_digits(num_digits: int, base: int = 10):
    arr = num_digits * [0]
    max_arr = num_digits * [base - 1]

    while arr <= max_arr:
        yield arr

        if arr == max_arr:
            break

        if arr[-1] == base - 1:
            j = 0
            while arr[~j] + 1 == base:
                j += 1
            dig = arr[~j] + 1
            for k in range(j + 1):
                arr[~k] = dig

        else:
            arr[-1] += 1


if __name__ == "__main__":
    base = 10

    up = 10
    lo = 2
    end_counts_arr = np.zeros((up - lo, base))
    for n in range(2, 10):
        j = 0

        end_counts = base * [0]
        # f = open('increasing_digits.txt', 'w')
        for k in increasing_digits(n, base):
            j += 1
            as_str = "".join((str(s) for s in k))
            # f.write(f"{as_str}\n")
            end_counts_arr[n, int(as_str) % base] += 1

        # f.close()
        # print('total under 10^{} is {}'.format(n, j))
        # x.append(n)
        # y.append(j/10**n)

        # print([(j,s) for j,s in enumerate(end_counts)])
        ln = ""
        for k in end_counts_arr[n]:
            ln += f"{int(k):>8}"
        print(ln)
    # plt.plot(x, y)
    # plt.show()
