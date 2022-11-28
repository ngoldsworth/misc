"""
You will have to change the names of the files inside the pl Path quotes.
You may also have to run `py -m pip install pandas` in Windows Power Shell
"""

import pandas as pds
import pathlib as pl

csv = pl.Path(r'.\dad\MSM - CRC HOLIDAY CARDS WAVE 1 - FULL LIST.CSV')
out_file = pl.Path(r'.\dad\output2.csv')
dist_file = pl.Path(r'.\dad\distances.csv')

number_sold_limits = {
    # dealer id: max number to mark as "in nearest"
    10690:750, 10728:750, 18176:750, 18192:750, 20467:750, 20491:1000,
    20813:750, 23606:789, 23795:750, 24519:750, 28144:750, 28517:750, 28566:750,
    29857:750, 32257:750, 32599:750, 32872:750, 32873:597, 33875:750, 34064:750,
    34848:750, 35930:750, 36343:750, 36570:750, 39887:300, 40776:750, 40777:750,
    41396:750, 42095:750, 42295:750, 45792:750, 45793:750, 45859:750, 46285:692,
    46854:750, 49203:750, 49226:750, 50046:750, 50675:750, 50792:750, 50793:750,
    50794:750, 50806:750, 50900:750, 51337:750, 51794:750, 58244:750, 65653:750,
    78295:750, 87997:750, 88182:750, 95242:192, 98150:750, 99999:1500,
    41607:750, 88125:750, 32598:750, 33803:750, 37028:750, 41671:750, 41956:750,
    43292:750, 43444:750, 48356:750, 48762:750, 58366:750
}

if __name__ == '__main__':

    # import the csv, ensure sorted
    df = pds.read_csv(csv)
    df = df.sort_values(by=['DEALERID', 'DISTANCE'])

    # add the 'ToSend' column
    df['InNearest'] = False

    # set up DEALER counter
    unique_ids = set(list(df['DEALERID']))
    dealer_counter = {did:0 for did in unique_ids}
    dealer_max_distance = {did:0 for did in unique_ids}

    # loop through rows
    for i, row in enumerate(df.iterrows()):
        # get dealer ID for this row, count it
        did = df.at[i, 'DEALERID']
        dealer_counter[did] += 1

        # check if should be included
        # if so, change 'in nearest' to true
        if dealer_counter[did] <= number_sold_limits[did]:
            df.at[i, 'InNearest'] = True
            dealer_max_distance[did] = max(dealer_max_distance[did], df.at[i, 'DISTANCE'])

    df.to_csv(out_file, index=False)

    maxdist = pds.DataFrame([(k,v) for (k,v) in dealer_max_distance.items()], columns=['Dealer ID', 'Max Distance'])    
    maxdist.to_csv(dist_file, index=False)

    

