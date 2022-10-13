import matplotlib.pyplot as plt
from os import remove
from prettytable import PrettyTable
import locale
import numpy as np
import prettytable
from prettytable.prettytable import PLAIN_COLUMNS


class Payment:
    """
    Helper class
    GLorified struct with some helpful methods
    :param pay_principle: amount of money spent directly on the principle
    :param pay_interest: amount of money spent on interest
    """

    def __init__(self, pay_principle: float, pay_interest: float):
        self._pay_principle = pay_principle
        self._pay_interest = pay_interest


class Loan:
    """
    :param principle: initial principle on the loan
    :param period_rate: interest rate, amount charged per period
    :
    """

    def __init__(
        self,
        principle: float,
        period_rate: float,
        periods: int,
    ):
        self._original_principle = principle
        self._rate = period_rate
        self._term = periods

        self._current_balance = self._original_principle
        self._period_idx = 0

        self._payments = []
        self._interest = []

    @property
    def remaining_periods(self):
        return self._term - self._period_idx

    @property
    def rate(self):
        return self._rate

    def annuity(self, principle=None, rate=None, term=None):
        """Calculates per-period payment for a given loan. Unless otherwise
        specified, uses the values used in construction of the object"""

        if principle is None:
            principle = self._original_principle
        if rate is None:
            rate = self._rate
        if term is None:
            term = self._term

        # a = principle * rate * (1+rate)**term
        # a /= (1 * rate)**term -1

        a = rate * principle
        d = 1 - (1 + rate) ** (-term)
        return a / d

    @property
    def original_principle(self):
        return self._original_principle

    @property
    def original_minimum_payment(self):
        return self.payment(self._original_principle, self._rate, self._term)

    def reset(self):
        """
        Returns the loan to payment 0.
        """
        self._current_balance = self._original_principle
        self._period_idx = 0

        self._payments = []
        self._interest = []

    def minimum_payment(self):
        return self.annuity(self._current_balance, self._rate, self.remaining_periods)

    def make_payment(self, amount=None):
        """
        Progress the loan forward in its life one period. Raises value error if
        `amount` is smaller than the minimum on the remaining life of the loan.
        Defaults to minimum payment.
        """
        if amount is None:
            amount = self.minimum_payment()
        if amount < self.minimum_payment():
            raise ValueError("Too small a payment")

        interest = self._rate * self._current_balance
        self._current_balance += interest - amount

        self._interest.append(interest)
        self._payments.append(amount)
        self._period_idx += 1

    def amortization_schedule(self) -> np.ndarray:
        """
        Simulate the entire life of the loan.
        """
        amor_tab = np.empty((self._term, 3), dtype=float)
        monthly_payment = self.annuity()
        print(monthly_payment)

        remaining_principle = self._original_principle

        for j in range(self._term):
            interest_payment = remaining_principle * self._rate
            principle_payment = monthly_payment - interest_payment
            remaining_principle -= principle_payment
            amor_tab[j] = np.asarray(
                [interest_payment, principle_payment, remaining_principle]
            )

            print(interest_payment, principle_payment, remaining_principle)

        return amor_tab

    def amortization_bar_plot(self):
        fig, ax = plt.subplots()

        amor_tab = self.amortization_schedule()
        period = np.arange(self._term)
        ax.bar(period, amor_tab[:, 1], label="Principle")
        ax.bar(period, amor_tab[:, 0], label="Interest")

        ax.set_ylabel("Dollars")
        ax.set_xlabel("Period")
        ax.legend()

        return fig, ax


if __name__ == "__main__":
    """
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

    """
    my_loan = Loan(10 ** 6, 0.003, 360)
    fig, ax = my_loan.amortization_bar_plot()
    plt.show()
