def kaprekar_iteration(n):
    if not (1000 <= n) and not (n <= 9998):
        return 0
    elif n < 1000:
        asstr = str(n)
        while len(asstr) < 4:
            asstr += '0'

    if(len(set(asstr))==1):
        return 0
    lower = "".join(sorted(asstr))

    upper = int(lower[::-1])
    return upper - int(lower)
    

if __name__ == '__main__':
    for k in range(1,100):
        print(kaprekar_iteration(k))



