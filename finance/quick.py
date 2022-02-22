from loans import annuity
import matplotlib.pyplot as plt

if __name__ == "__main__":
    loan = 10**6
    factor = 4.0
    initial = loan
    term = 120
    apr = 4/100
    j = 0

    payments = []
    payments_perc = []
    owed = []
    owed_perc = []

    total = 0

    while loan > 0:
        loan += (loan * (apr/12))

        p = factor * annuity(loan, apr, term)
        payments.append(p)
        payments_perc.append(p/initial)

        loan -= p
        owed.append(loan)
        owed_perc.append(loan / initial)

        term += -1
        j += 1

        total += p

        print("{:>3} Paid: {:>8.2f} | Owed: {:>8.2f}".format(j, p, loan))
    
    print(total/initial)

    fig, ax = plt.subplots(1, 1)
    ax.plot(payments)
    ax.plot(owed)
    fig.suptitle("Abs")

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(payments_perc)
    fig2.suptitle("Paymnt perc")

    fig3, ax3 = plt.subplots(1, 1)
    ax3.plot(owed_perc)
    fig3.suptitle("Owed perc")

    plt.show()