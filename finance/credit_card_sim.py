
balance = 7200
apr = 27.99

per_period_rate = apr /(100*12)

# monthly_pay = balance * (per_period_rate) + 0.5
monthly_pay = 400

if __name__ == '__main__':

    initial_balance = balance
    total_interest_paid = 0
    month = 1
    while balance > 0:
        interest = per_period_rate * balance

        if interest > monthly_pay:
            raise ValueError(f"Monthly interest (${interest:.2f}) is greater than payment ({monthly_pay:>.2f}) and card will never be paid off, monthly payment must be greater than {interest:.2f}")
    
        to_balance = monthly_pay - interest
        total_interest_paid += interest
        balance -= to_balance
        if balance <= 0:
            balance = 0

        s = f'Month {month:>3} | I={interest:>8.2f} | P={to_balance:>8.2f} | B={balance:>8.2f} | TI={total_interest_paid:>8.2f} |'
        month += 1
        print(s)

    print(f'Total interest is {total_interest_paid/initial_balance:>.3f}x original balance')
