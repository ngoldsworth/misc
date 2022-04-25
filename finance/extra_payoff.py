from loans import annuity
import numpy as np

import loans


def extra_payoff(
    original_principle: float,
    installment: float,
    term: int,
    apr: int,
):
    monthly_due = loans.annuity(original_principle, apr=apr, months=term)

    remaining = original_principle
    original_total = monthly_due * term

    monthly_actual = installment

    m = 1

    payment = max(monthly_actual, monthly_due)
    total_paid = 0
    total_interest = 0

    while remaining > 0:
        interest = (apr / 12) * remaining

        if payment > monthly_due:
            extra_paid = payment - loans.annuity(remaining, apr, (term - m + 1))
        else:
            extra_paid = 0

        if payment <= (interest + remaining):
            remaining += interest - payment
            total_paid += payment
            total_interest += interest

        else:
            payment = remaining + interest
            total_paid += payment
            total_interest += interest
            remaining = 0

        m += 1

    return m, original_total, total_paid, total_interest


def extra_payoff_table(term: int, apr: np.ndarray, extras_percent: np.ndarray):
    """
    @param term: number of installments in the loan
    @param apr: array of APR's
    @param extras_percent: extra as <1 percentage of payment.
    """
    original = 10 ** 6

    headers = "{:>8} |".format(" ")
    for rate in apr:
        headers += "{:>12.2%} |".format(rate)
    print(headers)

    for extra in extras_percent:
        row = "{:>8.1%} |".format(extra)

        for rate in apr:
            normal_amount = annuity(original, rate, term)
            installment_with_extra = normal_amount * (1 + extra)
            m, original_total, total_paid, total_interest = extra_payoff(
                original_principle=original,
                installment=installment_with_extra,
                apr=rate,
                term=term,
            )
            row += "{:>4}, {:>6.2%} |".format(m - 2, total_interest / total_paid)
        print(row)


if __name__ == "__main__":
    amount = 100000
    apr = np.asarray([2.5, 3.0, 3.5, 4.0, 4.5, 5.0 , 5.5, 6.17, 6.85, 11, 11.5, 12, 12.5]) / 100
    term = 30*12
    # extras = np.asarray([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]) / 100
    extras = np.linspace(0, 100, num=50, endpoint=True)/100
    extra_payoff_table(term, apr, extras)
