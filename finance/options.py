import datetime as dt

exercise_price = 1.80

vest_start_date = dt.date(2023, 6, 1)
vest_finish_date = dt.date(2026, 6, 1)
months = 36

share_ct_init = 1250
share_ct_final = 5000

monthly_vest_ct = (share_ct_final - share_ct_init )/months


def determine_vested_shares(
        date:dt.date,
        initial_shares=1250,
        final_shares=5000,
        start_date=vest_start_date,
        stop_date=vest_finish_date,
        months=36
):
    if date < start_date:
        return 0
    elif date >= stop_date:
        return final_shares
    else:
        total_dur = stop_date - start_date
        portion =  36 * (date - start_date)/total_dur
        portion = portion // 1
        shares = 1250 + portion*(monthly_vest_ct//1)

        return shares

if __name__ == '__main__':
    d = dt.date(2028, 1,1)
    s = determine_vested_shares(d)

    assumed_sale_price = 10000
    profit = (assumed_sale_price - exercise_price)*s
    print(f"Profit: {profit:,} on {s:,} shares")

    years = 30
    leave_it_alone = profit * (1.065 ** years)//1
    print(f"Let it sit for {years}yrs: {leave_it_alone:,}")