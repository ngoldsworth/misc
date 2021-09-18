from os import remove
from prettytable import PrettyTable
import locale
import numpy as np
import prettytable
from prettytable.prettytable import PLAIN_COLUMNS


def annuity(
    amount: float,
    apr: float,
    months: int,
):
    i = apr / 12
    a = amount * i * (1 + i) ** months
    a /= (1 + i) ** months - 1
    return a


def annuity_table(
    amount: np.ndarray or list,
    apr: np.ndarray or list,
    months: np.ndarray or list,
):
    av, iv, mv = np.meshgrid(amount, apr / 12, months)
    a = av * iv * (1 + iv) ** mv
    a /= (1 + iv) ** mv - 1
    return a


def amoritization_table(
    amount: float,
    apr: float,
    term: int,
) -> np.ndarray:
    """
    @param amount: loan amount
    @param apr: Annual Percentage Rate expressed as fraction
    @param term: number of months in the loan
    """
    amor_tab = np.empty((term, 3), dtype=float)
    monthly_payment = annuity(amount, apr, term)
    effective_interest_rate = apr / 12
    remaining = amount

    for j in range(term):
        interest = remaining * effective_interest_rate
        principle_payment = monthly_payment - interest
        remaining -= monthly_payment
        amor_tab[j] = np.asarray(
            [float(interest), float(principle_payment), float(remaining)], dtype=float
        )

    return amor_tab


def pretty_annuity_table(
    amount: np.ndarray,
    apr: np.ndarray,
    months: int,
) -> PrettyTable:

    x = PrettyTable()
    x.set_style(PLAIN_COLUMNS)

    x.field_names = ["APR"] + [locale.currency(j) for j in amount]
    A = annuity_table(amount, apr, months)
    for rate, bills in zip(apr, A):
        tablerow = ["{:.2%}".format(rate)]
        for m in bills:
            tablerow.append(locale.currency(m))
        x.add_row(tablerow)
    return x


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "")
    starting_savings = 7000
    monthly_rates = np.asarray([500, 600, 700, 750, 800, 1000])
    save_time = 1  # months after Feb 1, 2022
    cost = 28000  # brand new Tacoma cost 2021

    saved = starting_savings + (save_time * monthly_rates)
    loans = cost - saved

    # interest
    i = np.linspace(start=2.49, stop=5, num=20) / 100
    n = np.asarray([12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72])

    base = 10000

    a = np.zeros((i.size, n.size))

    for ij, rate in enumerate(i):
        for nj, term in enumerate(n):
            a[ij, nj] = annuity(base, rate, term)
        print(rate, [locale.currency(m) for m in a[ij]])

    print(amoritization_table(10000, 4.15 / 100, 120))
