from finance.comparisons import annuity
from os import remove
from prettytable import PrettyTable
import locale
import numpy as np
import prettytable
from prettytable.prettytable import PLAIN_COLUMNS


class Loan():
    def __init__(
        self,
        principle: float,
        period_rate: float,
        periods: int,
    ):
        self._original_principle = principle
        self._rate = period_rate
        self._term = periods
    
    def annuity(
        self, 
        principle=None,
        rate=None,
        term=None
        ):
        """Calculates per-period payment for a given loan. Unless otherwise
        specified, uses the values used in construction of the object"""

        if principle is None:
            principle = self._original_principle
        if rate is None:
            rate = self._rate
        if term is None:
            term = self._term

        a = principle * rate * (1+rate)**term
        a /= (1 * rate)**term -1
        return a

    def amoritization(self)->np.ndarray:
        amor_tab = np.empty((term, 3), dtype=float)
        monthly_payment = self.annuity()

        remaining_principle = self._original_principle

        for j in range(self._term):
            interest_payment = remaining_principle * self._rate
            principle_payment = monthly_payment - interest_payment
            remaining_principle -= monthly_payment
            amor_tab[j] = np.asarray([interest_payment, principle_payment, remaining_principle])

        return amor_tab

def amoritization_table(
    amount:float,
    apr:float,
    term:int,
)->np.ndarray:
    """
    @param amount: loan amount
    @param apr: Annual Percentage Rate expressed as fraction
    @param term: number of months in the loan
    """
    amor_tab = np.empty((term, 3), dtype=float)
    monthly_payment = annuity(amount, apr, term)
    effective_interest_rate = apr/12
    remaining=amount

    for j in range(term):
        interest = remaining * effective_interest_rate
        principle_payment = monthly_payment - interest
        remaining -= monthly_payment
        amor_tab[j] = np.asarray([float(interest), float(principle_payment), float(remaining)], dtype=float)

    return amor_tab

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    starting_savings = 7000
    monthly_rates = np.asarray([500, 600, 700, 750, 800, 1000])
    save_time = 1 # months after Feb 1, 2022
    cost = 28000 # brand new Tacoma cost 2021


    saved = starting_savings + (save_time * monthly_rates)
    loans = cost - saved

    # interest
    i = np.linspace(start=2.49, stop=5, num=20)/100
    n = np.asarray([12,18,24,30,36,42,48,54,60,66,72])

    base = 10000

    a = np.zeros((i.size, n.size))

    for ij, rate in enumerate(i):
        for nj, term in enumerate(n):
            a[ij, nj] = annuity(base, rate, term)
        print(rate, [locale.currency(m) for m in a[ij]])
    
    print(amoritization_table(10000, 4.15/100, 120))

