from collections.abc import Sequence
import datetime
import os.path

import numpy as np

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import matplotlib.pyplot as plt

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def _get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


class SingleSleepNight:
    def __init__(
        self,
        date,
        time_into_bed,
        time_try_to_sleep,
        time_final_awakening,
        time_out_of_bed,
        time_to_fall_asleep,
        wake_up_count,
        wake_ups_duration,
        time_smartwatch_fell_asleep,
        time_smartwatch_wakeup,
        smartwatch_wake_ups_duration,
        sleep_quality,
    ):
        self._date = date
        self._time_into_bed = time_into_bed
        self._time_try_to_sleep = time_try_to_sleep
        self._time_final_awakening = time_final_awakening
        self._time_out_of_bed = time_out_of_bed
        self._time_to_fall_asleep = time_to_fall_asleep
        self._wake_up_count = wake_up_count
        self._wake_ups_duration = wake_ups_duration
        self._time_smartwatch_fell_asleep = time_smartwatch_fell_asleep
        self._time_smartwatch_wakeup = time_smartwatch_wakeup
        self._smartwatch_wake_ups_duration = smartwatch_wake_ups_duration
        self._sleep_quality = sleep_quality

    def __repr__(self):
        s = f'SingleSleepNight(date={self._date}, '
        s+=f'time_into_bed={self._time_into_bed}, '
        s+=f'time_try_to_sleep={self._time_try_to_sleep}, '
        s+=f'time_final_awakening={self._time_final_awakening}, '
        s+=f'time_out_of_bed={self._time_out_of_bed}, '
        s+=f'time_to_fall_asleep={self._time_to_fall_asleep}, '
        s+=f'wake_up_count={self._wake_up_count}, '
        s+=f'wake_ups_duration={self._wake_ups_duration}, '
        s+=f'time_smartwatch_fell_asleep={self._time_smartwatch_fell_asleep}, '
        s+=f'time_smartwatch_wakeup={self._time_smartwatch_wakeup}, '
        s+=f'smartwatch_wake_ups_duration={self._smartwatch_wake_ups_duration}, '
        s+=f'sleep_quality={self._sleep_quality})'
        return s

    @property
    def date(self):
        return self._date

    @property
    def time_into_bed(self):
        return self._time_into_bed

    @property
    def time_try_to_sleep(self):
        return self._time_try_to_sleep

    @property
    def time_final_awakening(self):
        return self._time_final_awakening

    @property
    def time_out_of_bed(self):
        return self._time_out_of_bed

    @property
    def time_to_fall_asleep(self):
        return self._time_to_fall_asleep

    @property
    def wake_up_count(self):
        return self._wake_up_count

    @property
    def wake_ups_duration(self):
        return self._wake_ups_duration

    @property
    def time_smartwatch_fell_asleep(self):
        return self._time_smartwatch_fell_asleep

    @property
    def time_smartwatch_wakeup(self):
        return self._time_smartwatch_wakeup

    @property
    def wake_ups_duration(self):
        return self._wake_ups_duration

    @property
    def sleep_quality(self):
        return self._sleep_quality


################################################################
class SleepNights(Sequence):
    def __init__(self):
        self._spreadsheet_id = None
        self._creds = None

        self._date = None

        self._time_into_bed = None  # Column B
        self._time_try_to_sleep = None  # Column C
        self._time_final_awakening = None  # Column D
        self._time_out_of_bed = None  # Column E
        self._minutes_to_fall_asleep = None  # Column F

        self._wake_up_count = None  # Column G
        self._wake_ups_duration_minutes = None  # Column H

        self._time_smartwatch_fell_asleep = None  # Column I
        self._time_smartwatch_wakeup = None  # Column J
        self._smartwatch_wake_ups_duration_minutes = None  # Column K

        self._sleep_quality = None  # Column L
        self._rested = None #Column M
        self._comments = None # Column N

        self._length = 0

    def _val_convert(self, val: str):
        if val == "":
            return np.NaN
        else:
            return int(val)

    def _to_npdatetime(self, d, t: str):

        if t == "":
            return np.datetime64("NaT")

        """Helper funtion"""
        str_d = str(d)
        d = datetime.datetime.fromisoformat(str(d))

        # convert sheet's string for the hour:minute to a datetime.time
        t = datetime.time.fromisoformat(t)

        # is the time 'before midnight', i.e. is is for the evening before the day listed for indexing the row
        if datetime.time(hour=12) < t < datetime.time(hour=23, minute=59, second=59):
            d = d - datetime.timedelta(days=1)

        d = d + datetime.timedelta(hours=t.hour, minutes=t.minute)

        return np.datetime64(d.isoformat())

    # def _minutes_rel_midnight(t):
    #     pass

    def get_sheets_data(
        self,
        spreadsheet_id,
        range_name,
    ):
        creds = _get_creds()
        try:
            service = build("sheets", "v4", credentials=creds)

            result = (
                service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    majorDimension="COLUMNS",
                )
                .execute()
            )
            cols = result.get("values", [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

        # in sheet, column A (idx 0) is date
        self._date = np.array(cols[0], dtype="datetime64[D]")

        # set the length
        self._length = len(self._date)

        # in sheet, column B (idx 1) is "What time did you get into bed"
        self._time_into_bed = np.array(
            [self._to_npdatetime(d, t) for d, t in zip(self.date, cols[1])],
            dtype="datetime64",
        )

        # in sheet, column C (idx 2) is "What time did you try to get to sleep"
        self._time_try_to_sleep = np.array(
            [self._to_npdatetime(d, t) for d, t in zip(self.date, cols[2])],
            dtype="datetime64",
        )

        # in sheet, column D (idx 3) is "What time was your final awakening?"
        self._time_final_awakening = np.array(
            [self._to_npdatetime(d, t) for d, t in zip(self.date, cols[3])],
            dtype="datetime64",
        )

        # column E (idx 4)
        self._time_out_of_bed = np.array(
            [self._to_npdatetime(d, t) for d, t in zip(self.date, cols[4])],
            dtype="datetime64",
        )

        # column F (idx 5)
        self._minutes_to_fall_asleep = np.asarray(
            [self._val_convert(val) for val in cols[5]]
        )

        # column G (idx 6)
        self._wake_up_count = np.asarray([self._val_convert(val) for val in cols[6]])

        # column H (idx 7)
        self._wake_ups_duration_minutes = [self._val_convert(val) for val in cols[7]]

        # column I (idx 8)
        self._time_smartwatch_fell_asleep = np.array(
            [self._to_npdatetime(d, t) for d, t in zip(self.date, cols[8])],
            dtype="datetime64",
        )

        # column J (idx 9)
        self._time_smartwatch_wakeup = np.array(
            [self._to_npdatetime(d, t) for d, t in zip(self.date, cols[9])],
            dtype="datetime64",
        )

        # column K (idx 10)
        self._smartwatch_wake_ups_duration_minutes = np.asarray(
            [self._val_convert(val) for val in cols[10]]
        )

        # column L (idx 11)
        self._sleep_quality = np.asarray([self._val_convert(val) for val in cols[11]])

        # column M (idx 12)
        self._rested = np.asarray(self._val_convert(val) for val in cols[12])

        #column N (idx 13)
        self._comments = [c for c in cols[13]]

        return

    def __len__(self):
        return self._length

    def __getitem__(self, index):
        return SingleSleepNight(
            date=self._date[index],
            time_into_bed=self._time_into_bed[index],
            time_try_to_sleep=self._time_try_to_sleep[index],
            time_final_awakening=self._time_final_awakening[index],
            time_out_of_bed=self._time_out_of_bed[index],
            time_to_fall_asleep=self._minutes_to_fall_asleep[index],
            wake_up_count=self._wake_up_count[index],
            wake_ups_duration=self._wake_ups_duration_minutes[index],
            time_smartwatch_fell_asleep=self._time_smartwatch_fell_asleep[index],
            time_smartwatch_wakeup=self._time_smartwatch_wakeup[index],
            smartwatch_wake_ups_duration=self._smartwatch_wake_ups_duration_minutes[
                index
            ],
            sleep_quality=self._sleep_quality[index],
        )

    @property
    def date(self):
        return self._date

    @property
    def time_into_bed(self):
        return self._time_into_bed

    @property
    def time_try_to_sleep(self):
        return self._time_try_to_sleep

    @property
    def time_final_awakening(self):
        return self._time_final_awakening

    @property
    def time_out_of_bed(self):
        return self._time_out_of_bed

    @property
    def time_to_fall_asleep(self):
        return self._minutes_to_fall_asleep

    @property
    def wake_up_count(self):
        return self._wake_up_count

    @property
    def wake_ups_duration(self):
        return self._wake_ups_duration_minutes

    @property
    def time_smartwatch_fell_asleep(self):
        return self._time_smartwatch_fell_asleep

    @property
    def time_smartwatch_wakeup(self):
        return self._time_smartwatch_wakeup

    @property
    def wake_ups_duration(self):
        return self._wake_ups_duration_minutes

    @property
    def sleep_quality(self):
        return self._sleep_quality

    @property
    def rested(self):
        return self._rested

    @property
    def comments(self):
        return self._comments

    def sleep_duration(self, unit='m'):
        return (self.time_final_awakening - self.time_try_to_sleep) / np.timedelta64(1, unit)

if __name__ == "__main__":
    import pickle
    import pathlib as pl
    pkl_file = pl.Path('./sleepnight.pickle')

    spreadsheet_id = "1eSSOl3b9VTu12zw1vkdYovycNnjxxDNYPZtdfSMUhlc"
    sheetrange = "!A3:N"

    sn = SleepNights()

    if not pkl_file.exists():
        print('downloading data')
        sn.get_sheets_data(spreadsheet_id, sheetrange)
        print(sn)
        # o = open(pkl_file, 'wb')
        # print('writing pickle')
        # pickle.dump(sn, o)
    else:
        print('loading pickle')
        o = open(pkl_file, 'rb')
        sn = pickle.load(o)

    # plt.hist(sn.sleep_quality, bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
    # plt.show()
    d = sn.sleep_duration('h')
    # plt.plot(sn.sleep_quality, d, 'o')
    # plt.show()

    fig, ax = plt.subplots(1)

    # edges
    
    # num of unique values in sleep quality array
    u = np.unique(sn.sleep_quality)
    colors = ['red', 'orange', 'yellow', 'green', 'blue']

    e = np.histogram_bin_edges(d)
    top=None
    e_centers = (e[:-1] + e[1:])/2

    for i, ui in enumerate(u):
        subset = d[sn.sleep_quality==ui]
        h, e = np.histogram(subset, bins=e)
        ax.bar(e_centers, h, bottom=top, label=str(ui), color=colors[i])

        if top is None:
            top = h
        else:
            top += h

        print(top)
    
    ax.legend()
    plt.show()
    print(e_centers)