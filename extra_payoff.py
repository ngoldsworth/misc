import loans


if __name__ == '__main__':
    amount = 80464
    apr = 6.5/100
    term = 360

    j = 1

    ir = (apr)/12

    # extra_principle_payment = 300
    monthly = 0

    while amount > 0:
        min_payment = loans.annuity(amount, apr, term)

        interest = amount * ir
        pricinple_payment = min_payment - interest

        total_payment = monthly
        extra_principle_payment = monthly - min_payment 

        amount += interest - total_payment
        # amount += interest - monthly

        string = 'Month: {:>3} | Interest: {:>8.2f} | Principle: {:>8.2f} | Extra: {:>8.2f} | Total Payment: {:>8.2f} | Remaining: {:>10.2f}'.format(
            j, interest, pricinple_payment, extra_principle_payment, total_payment, amount)
        print(string)

        j += 1
        term += -1
