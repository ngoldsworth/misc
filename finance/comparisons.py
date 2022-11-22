import numpy as np


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
