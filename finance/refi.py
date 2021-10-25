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

saved = 16000

student_loans = [
    (5672, .0429),
    (8363, .0376),
    (8196-4060, .0445),
    (7920, .0505),
    (3020, .0453)
]

sl = np.asarray(student_loans)
sl = sl[sl[:,1].argsort()]
print(sl)

j = sl.shape[0] - 1
while saved > 0:
    highest_interest_loan_amt = sl[j,0]
    if highest_interest_loan_amt > saved:
        saved = saved - highest_interest_loan_amt
        sl[j, 0] = 0
    else:
        sl[j, 0] = sl[j,0] - saved
        saved = 0
    j -= 1


total_principle = sum(sl[:,0])
weight_factor = sum(sl[:,0] * sl[:,1])
new_rate = weight_factor/total_principle
print("New Rate: {:%}, Total Balance: {}".format(new_rate, total_principle))

months = 120
print("Monthly payment on {} month loan: {:.2f}".format(months, annuity(total_principle, new_rate, months)))