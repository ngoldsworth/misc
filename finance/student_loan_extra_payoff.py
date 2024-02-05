import numpy as np


class Loan:
    def __init__(self, principle:float, per_period_interest:float, periods:int, name:str=None):
        self._principle = principle
        self._remaining = principle
        self._rate = per_period_interest
        self._total_periods = periods
        self._periods_complete = 0
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def minimum_payment(self):
        P = self._remaining
        r = self._rate
        n = self.periods_remaining

        c = r * P
        c /= 1 - (1 + r) ** -n
        # round up to nearest cent
        rounded = (100 * c) + 1
        rounded  = (rounded//1) / 100
        return rounded

    @property
    def remaining_balance(self):
        return self._remaining

    @remaining_balance.setter
    def remaining_balance(self, val):
        self._remaining = val

    @property
    def interest_rate(self):
        return self._rate

    @property
    def periods_remaining(self):
        return self._total_periods - self._periods_complete

    @property
    def periods_complete(self):
        return self._periods_complete

    @periods_complete.setter
    def periods_complete(self, val):
        self._periods_complete = val

    def make_monthly_payment(self, payment_amount):
        m = self.minimum_payment
        if payment_amount < m:
            raise ValueError(
                f"payment of {payment_amount} is too low, must be at least the minimum payment of {m}"
            )
        interest = self.interest_rate * self.remaining_balance
        to_principle = payment_amount - interest

        self.periods_complete += 1

        if self.remaining_balance < to_principle:
            # loan is paid off!
            to_principle -= self.remaining_balance
            self.remaining_balance = 0
            return to_principle, interest

        self.remaining_balance -= to_principle
        return 0, interest

def run_simulation(loan_list: list, desired_mohtly):
    # sort by interest rate, pay down highest interest rate loans first
    student_loans = sorted(loan_list, key=lambda x: x.interest_rate, reverse=True)

    minimum_monthly = sum(loan.minimum_payment for loan in student_loans)
    actual_monthly = max(minimum_monthly, desired_mohtly)

    out_str = f'min monthly payment is {minimum_monthly:>.2f}, actual monthly is {actual_monthly:>.2f}\n'

    total_remaining_balance = sum([ln.remaining_balance for ln in student_loans])
    total_initial_balance = total_remaining_balance
    total_interest_paid = 0

    while total_remaining_balance > 0:
        payment = actual_monthly

        complete = {loan.name: loan.remaining_balance == 0 for loan in student_loans}
        per_loan_payments = {loan.name: loan.minimum_payment for loan in student_loans} 

        total_mininum_payment = sum(loan.minimum_payment for loan in student_loans)
        extra = payment - total_mininum_payment

        # extra goes to still-existing loan with highest interest rate
        highest_interest = ''
        max_interest = 0
        for loan in student_loans:
            if not complete[loan.name] and loan.interest_rate > max_interest:
                highest_interest = loan.name
                max_interest = loan.interest_rate
        
        per_loan_payments[highest_interest] += extra

        remainder = 0 
        s = f'Month {student_loans[0].periods_complete+1:>3} | '
        for loan in student_loans:
            m = per_loan_payments[loan.name] + remainder
            remainder, interest = loan.make_monthly_payment(m) # remainder is amount leftover if pay-off whole loan
            total_interest_paid += interest
            s += f'{loan.name} '
            s += f'({m-remainder:>7.2f}) '
            s += f'{loan.remaining_balance:>9.2f}  | '

        out_str += s + '\n'

        total_remaining_balance = sum(loan.remaining_balance for loan in student_loans)
    
    final = f'Total interest paid: ${total_interest_paid:>.2f}, which is {total_interest_paid/total_initial_balance:.2%} the initial balance\n'
    out_str += final
    total_periods = loan_list[0].periods_complete

    return total_interest_paid, total_periods, out_str




if __name__ == "__main__":

    import matplotlib.pyplot as  plt
    import numpy as np

    # monthly_amounts = [350 + (12.5*x) for x in range(100)]
    monthly_amounts = 350 * np.logspace(0, 1, base=10, num=100)
    print(monthly_amounts)

    periods_to_complete = []
    interest_paid = []

    for pay in monthly_amounts:
        periods = 117  # number of payments left as of 2024-jan-02
        # loan info as of 2024-Jan-02
        student_loans = [
            Loan(principle=5631.61, per_period_interest=4.04 / (100 * 12), periods=periods, name="Fed 1-01"),
            Loan(principle=8286.29, per_period_interest=3.51 / (100 * 12), periods=periods, name="Fed 1-02"),
            Loan(principle=8134.01, per_period_interest=4.20 / (100 * 12), periods=periods, name="Fed 1-03" ),
            Loan(principle=7763.68, per_period_interest=4.80 / (100 * 12), periods=periods, name="Fed 1-04" ),
            Loan(principle=3001.33, per_period_interest=4.28 / (100 * 12), periods=periods, name="Fed 1-05" ),
            # Loan(principle=10000.00, per_period_interest=24.99 / (100 * 12), periods=periods, name="CC" ),
        ]
        total_principle = sum([ln.remaining_balance for ln in student_loans])

        i, n, s = run_simulation(student_loans, pay)
        interest_paid.append(100*i/total_principle)
        periods_to_complete.append(n)
        print(s)


    pay_ratio = [p/341.57 for p in monthly_amounts]
    plt.plot(pay_ratio, interest_paid)
    plt.xlabel('Monthly Payment / min starting payment')
    # plt.xscale('log')
    plt.ylabel('Percentage of original balance paid as interest')

    plt.figure()
    # plt.xscale('log')
    plt.xlabel('Monthly Payment / min starting payment')
    plt.ylabel('Months to pay off loans')
    plt.plot(pay_ratio, periods_to_complete)
    plt.show()
    