import numpy as np

import loans

student_loans = [
    (8363, .0376),
    (5672, .0429), # 4.29% is .0429
    (8196, .0445),
    (3020, .0453),
    (7920, .0505),
]

saved = 22167
term = 120
monthly_payment = 1500

sl = np.asarray(student_loans)
# sort by interest rate
sl = sl[sl[:,1].argsort()]


if __name__ == '__main__':
    sl = np.asarray(student_loans)
    # sort by interest rate
    sl = sl[sl[:,1].argsort()]

    j = sl.shape[0] - 1
    while saved > 0:
        highest_interest_loan_amt = sl[j,0]
        if highest_interest_loan_amt < saved:
            saved = saved - highest_interest_loan_amt
            sl[j, 0] = 0
            j -= 1
        else:
            sl[j, 0] = sl[j,0] - saved
            saved = 0


    sl = sl[:j+1,:] # don't need paid off loans listed

    # start month counter
    m = 0

    while sl[:,0].sum() > 0:
        payment = monthly_payment
        # for each remainig loan, calculate the interest and pay the minimum payment
        for k in range(sl.shape[0]):
            min_pay = loans.annuity(sl[k,0], sl[k,1], term - m)
            interest_charged = (sl[k,1] / 12) * sl[k,0]
            sl[k,0] += interest_charged - min_pay

            payment -= min_pay #made the payment, those dollars come out of total

        print(payment, j)
        while payment > 0 and j >= 0:
            #j is still indx for highest interest loan
            if(sl[j,0] >= payment):
                sl[j,0] -= payment
                print(sl[j,0])
                payment = 0
            else:
                payment -= sl[j,0]
                sl[j,0] = 0
                j =- 1

        print(m, sl[:,0].sum())
        m += 1