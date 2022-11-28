repeats_count = 0

for x in range(10**5, 10**6):

    # break number into seperate digits
    digits_list = [int(j) for j in list(str(x))]
    num_digits = len(digits_list)
    num_unique_digits = len(set(digits_list))

    if num_unique_digits < num_digits:
        repeats_count += 1


print(repeats_count)
