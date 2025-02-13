import math
repeats_count = 0

map_num_to_char = {x: str(x) for x in range(10)}
for k_ord in range(ord("a"), ord("z") + 1):
    map_num_to_char[k_ord - 96] = chr(k_ord)

map_char_to_num = {v: k for k, v in map_num_to_char.items()}


def num_to_arb_base(num, base):
    if num == 0:
        return [0]

    n = num
    x = []
    while n:
        n, r = divmod(n, base)
        x.append(r)
    return x


def base_b_counter(base, stop, start=0, step=1):
    # only supports up to base 36 right now
    x = start  # keep integer copy of original number for increment
    x_lst = num_to_arb_base(x, base)
    while x < stop:
        x += 1
        x_lst[0] += step
        x_lst = check_list_counter(base, x_lst)
        yield x_lst

def check_list_counter(base, x_lst):
    if any(di >= base for di in x_lst):
    
        for d in range(len(x_lst)):
            if x_lst[d] >= base:
                q, r = divmod(x_lst[d], base)
                if (d+1) >= len(x_lst):
                    x_lst.append(0)
                x_lst[d] = r
                x_lst[d+1] += q

    return x_lst


def list_to_string_repr(base, x):
    # only supports up to base 36 right now
    if any(xi >= base for xi in x):
        raise ValueError(
            f"input list represenation of number contains entry larger than base b={base}"
        )

    s = ""
    for k in range(len(x)):
        s += map_num_to_char[x[~k]]
    return s

def distinct_list(x:list):
    return len(x) == len(set(x))


for x in range(10**5, 10**6):

    # break number into seperate digits
    digits_list = [int(j) for j in list(str(x))]
    num_digits = len(digits_list)
    num_unique_digits = len(set(digits_list))

    if num_unique_digits < num_digits:
        repeats_count += 1


if __name__ == "__main__":
    base = 16
    digi_ct = 5
    lo = base**(digi_ct-1)
    hi = base**digi_ct

    uniq = 0
    # for x in base_b_counter(base, start=lo, stop=hi):
    #     if distinct_list(x):
    #         uniq += 1

    # print(digi_ct, uniq)

    for j in range(1,17):
        k = (base-1)*math.factorial(base-1) // math.factorial(base - j)
        print(k)