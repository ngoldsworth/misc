from calendar import month
import loans
from math import ceil
import numpy as np

from loan import Loan


def annuity(amount: float, apr: float, periods: int, periods_per_year: int = 12):
    i = apr / periods_per_year
    a = amount * i * (1 + i) ** periods
    a /= (1 + i) ** periods - 1
    return a


if __name__ == "__main__":

    forgiveness = 0
    months = 120
    monthly_payment = 10000

    student_loans = [
        (8363, 0.0376),
        (5672, 0.0429),  # 4.29% is .0429
        (8196, 0.0445),
        (3020, 0.0453),
        (7920, 0.0505),
    ]

    sl = np.asarray(student_loans)

    # sort by interest rate
    sl = sl[sl[:, 1].argsort()]
    sl = np.flip(sl, 0)

    # j = sl.shape[0] - 1
    j = 0
    while forgiveness > 0:
        highest_interest_loan_amt = sl[j, 0]
        if highest_interest_loan_amt < forgiveness:
            forgiveness = forgiveness - highest_interest_loan_amt
            sl[j, 0] = 0
        else:
            sl[j, 0] = sl[j, 0] - forgiveness
            forgiveness = 0
        j += 1

    loan_list = []
    for l in sl:
        if l[0] > 0:
            loan_list.append(
                Loan(principle=l[0], period_rate=l[1] / 12, periods=months)
            )

    total_remaining_principle = np.asarray(
        [loan.remaining_balance for loan in loan_list]
    )
    while np.sum(total_remaining_principle) > 0:
        print(total_remaining_principle)
        amounts_due = (
            np.around(np.asarray([loan.minimum_payment() for loan in loan_list]), 2)
            + 0.01
        )
        min_payment = amounts_due.sum()

        if min_payment < monthly_payment:
            extra = monthly_payment - amounts_due.sum()
            total_remaining_principle -= amounts_due

            k = 0
            while extra > 0:
                if extra > total_remaining_principle[k]:
                    extra -= total_remaining_principle[k]
                    amounts_due[k] += total_remaining_principle[k]
                    total_remaining_principle[k] = 0
                    k += 1
                else:
                    total_remaining_principle[k] -= extra
                    amounts_due[k] += extra
                    extra = 0

            for i in range(amounts_due.size):
                loan_list[i].make_payment(amounts_due[i])

        else:
            for loan in loan_list:
                loan.make_payment()

        total_remaining_principle = np.asarray(
            [loan.remaining_balance for loan in loan_list]
        )
