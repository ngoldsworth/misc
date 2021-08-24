import loans

if __name__ == '__main__':
    initial_amount = 80464
    term = 360
    apr = 7.125/100

    monthly_due = loans.annuity(initial_amount, apr=apr, months=term)

    remaining = initial_amount
    original_total = monthly_due * term

    monthly_actual = 1125

    m = 0

    payment = max(monthly_actual, monthly_due)
    total_paid = 0
    total_interest = 0
    
    while remaining > 0:
        interest = (apr/12) * remaining

        if payment > monthly_due:
            extra_paid = payment - loans.annuity(remaining, apr, (term - m + 1))
        else:
            extra_paid = 0

        remaining += interest - payment
        to_principle = payment - interest
        total_paid += payment
        total_interest += interest

        m += 1

        table_row  = 'Month: {:>3} | '.format(m)
        table_row += 'Interest: {:>7.2f} ({:>5.1%}) | '.format(interest, interest/payment)
        table_row += 'Principle: {:>8.2f} ({:>5.1%}) | '.format(to_principle, to_principle/payment)
        table_row += 'Extra: {:>8.2f} | '.format(extra_paid)
        table_row += 'Total Payment {:>8.2f} | '.format(payment)
        table_row += 'Remaining: {:>8.2f} | '.format(remaining)
        table_row += 'Cumulative Paid {:>10.2f} | '.format(total_paid)
        
        if remaining > 0:
            print(table_row)

    print('Total Interest: {:>10.2f} ({:>4.2%})'.format(total_interest, total_interest/total_paid))