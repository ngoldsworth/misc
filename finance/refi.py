import numpy as np
from math import ceil


def annuity(
    amount: float,
    apr: float,
    months: int,
):
    i = apr / 12
    a = amount * i * (1 + i) ** months
    a /= (1 + i) ** months - 1
    return a

student_loans = [
    (8363, 0.0376),
    (5672, 0.0429),  # 4.29% is .0429
    (8196, 0.0445),
    (3020, 0.0453),
    (7920, 0.0505),
]

saved = 7920


sl = np.asarray(student_loans)
# sort by interest rate
sl = sl[sl[:, 1].argsort()]

for row in sl:
    print(f'{row[0]:>10.2f} @ {row[1]:>.2%}')

print(f'{sl[:,0].sum():>10.2f}')

j = sl.shape[0] - 1
while saved > 0:
    highest_interest_loan_amt = sl[j, 0]
    if highest_interest_loan_amt < saved:
        saved = saved - highest_interest_loan_amt
        sl[j, 0] = 0
    else:
        sl[j, 0] = sl[j, 0] - saved
        saved = 0
    j -= 1


total_principle = sum(sl[:, 0])
weight_factor = sum(sl[:, 0] * sl[:, 1])
new_rate = weight_factor / total_principle
rounded_rate = ceil(new_rate * 800) / 800
discounted_rate = rounded_rate - (0.25 / 100)


print("{:%} is rounded up to nearest eighth at {:%}".format(new_rate, rounded_rate))
print("New Rate: {:%}, Total Balance: {}".format(rounded_rate, total_principle))
print("With a .25% interest deduction: {:%}".format(rounded_rate - 0.0025))

months = 120
print(
    "Monthly payment on {} month loan at {:%}: {:.2f}".format(
        months, discounted_rate, annuity(total_principle, discounted_rate, months)
    )
)
