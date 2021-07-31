def annuity(
    amount:float,
    apr:float,
    months:int,
):
    i = apr/12
    a = amount * i * (1 + i)**months
    a /= (1+i)**months -1
    return a

if __name__ == '__main__':
    cost = 100000
    i = 0.04
    n = 12 * 5

    A = annuity(cost, i, n)
    print(A)

    owed = cost

    k = 0
    while owed > 0 :
        k+= 1
        interest = owed * i/12
        owed += interest - A
        print('After month {: >2}, ${:>5,} left'.format(k, owed))
