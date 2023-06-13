from collections.abc import Sequence
import datetime
import os.path
import pathlib as pl
import re
import typing

import numpy as np

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


## To get credentials: need to log into Google Cloud and find the OAuth 2.0 Client ID.
## Download the JSON.


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
        comment,
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
        self._comment = comment

    def __repr__(self):
        s = f"SingleSleepNight(date={self._date}, "
        s += f"time_into_bed={self._time_into_bed}, "
        s += f"time_try_to_sleep={self._time_try_to_sleep}, "
        s += f"time_final_awakening={self._time_final_awakening}, "
        s += f"time_out_of_bed={self._time_out_of_bed}, "
        s += f"time_to_fall_asleep={self._time_to_fall_asleep}, "
        s += f"wake_up_count={self._wake_up_count}, "
        s += f"wake_ups_duration={self._wake_ups_duration}, "
        s += f"time_smartwatch_fell_asleep={self._time_smartwatch_fell_asleep}, "
        s += f"time_smartwatch_wakeup={self._time_smartwatch_wakeup}, "
        s += f"smartwatch_wake_ups_duration={self._smartwatch_wake_ups_duration}, "
        s += f"sleep_quality={self._sleep_quality})"
        s += f"comment='{self._comment}')"
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
    def smartwatch_wake_ups_duration(self):
        return self._smartwatch_wake_ups_duration

    @property
    def sleep_quality(self):
        return self._sleep_quality

    @property
    def comment(self):
        return self._comment


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
        self._rested = None  # Column M
        self._comments = None  # Column N

    # this is a hack, because I want to pickle
    def from_single_sleep_night_sequence(self, seq: typing.Iterable[SingleSleepNight]):
        self._date = np.asarray([s.date for s in seq])
        self._sleep_quality = np.asarray([s.sleep_quality for s in seq])
        self._time_final_awakening = np.asarray([s.time_final_awakening for s in seq])
        self._time_into_bed = np.asarray([s.time_into_bed for s in seq])
        self._time_out_of_bed = np.asarray([s.time_out_of_bed for s in seq])
        self._time_smartwatch_fell_asleep = np.asarray(
            [s.time_smartwatch_fell_asleep for s in seq]
        )
        self._time_smartwatch_wakeup = np.asarray(
            [s.time_smartwatch_wakeup for s in seq]
        )
        self._minutes_to_fall_asleep = np.asarray([s.time_to_fall_asleep for s in seq])
        self._time_try_to_sleep = np.asarray([s.time_try_to_sleep for s in seq])
        self._wake_up_count = np.asarray([s.wake_up_count for s in seq])
        self._wake_ups_duration_minutes = np.asarray([s.wake_ups_duration for s in seq])
        self._smartwatch_wake_ups_duration_minutes = np.asarray(
            [s.smartwatch_wake_ups_duration for s in seq]
        )
        self._comments=[s.comment for s in seq]

    # this is a hack, because I want to pickle
    # def to_single_sleep_night_list(self):
    #     return [
    #         SingleSleepNight(
    #             date=s.date,
    #             sleep_quality=s.sleep_quality,
    #             time_final_awakening=s.time_final_awakening,
    #             time_into_bed=s.time_into_bed,
    #             time_out_of_bed=s.time_out_of_bed,
    #             time_smartwatch_fell_asleep=s.time_smartwatch_fell_asleep,
    #             time_smartwatch_wakeup=s.time_smartwatch_wakeup,
    #             time_to_fall_asleep=s.time_to_fall_asleep,
    #             time_try_to_sleep=s.time_try_to_sleep,
    #             wake_up_count=s.wake_up_count,
    #             wake_ups_duration=s.wake_ups_duration,
    #             smartwatch_wake_ups_duration=s.sma
    #         ) for s in self
    #     ]

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

    def _to_rel_mdate(self, d: str, t: str):
        """Helper function, converts HH:MM timestamp to relative to midnight.
        Assumes an HH>=12 is before mightnight (PM), and an HH<12 is after midnight (AM)
        """

        if t == "":
            return np.NaN

        d = mdates.num2date(d)

        m = re.search(r"(\d+):(\d+)", t)
        hour, minute = int(m[1]), int(m[2])
        ds = f"{d} {t}"
        midnight = mdates.datestr2num(f"{d} 00:00")
        if hour >= 12:
            mt = mdates.datestr2num(ds) - 1
        else:
            mt = mdates.datestr2num(ds)

        return mt - midnight

    def _to_mdate(self, d: str, t: str):
        return mdates.datestr2num(f"{d} {t}")

    @staticmethod
    def _mdate_to_hour_decimal(t):
        d = mdates.num2date(t)
        return d.hour + (d.minute / 60)

    def to_soca_format_csv(self, csvfile: pl.Path):
        headers = [
            "date",
            "day_of_week",
            "time into bed",
            "time tried to sleep",
            "final awakening",
            "got out of bed",
            "how long it took to fall asleep (minutes)" ,
            "how many times woke up",
            "duration of awakenings",
            "perceived quality of sleep (1 to 5)",
            "how rested feel throughout the day",
            "comments",
        ]

        weekday_map = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }

        with open(csvfile, "w") as fp:
            fp.write(",".join(headers) + "\n")

            for ssn in self:
                print(ssn)
                as_dt = mdates.num2date(ssn.date)

                s = f"{as_dt.year}-{as_dt.month}-{as_dt.day},"
                s += f"{weekday_map[as_dt.weekday()]},"

                s += f"{self._mdate_to_hour_decimal(ssn.time_into_bed):.2f},"
                s += f"{self._mdate_to_hour_decimal(ssn.time_try_to_sleep):.2f},"
                s += f"{self._mdate_to_hour_decimal(ssn.time_final_awakening):.2f},"
                s += f"{self._mdate_to_hour_decimal(ssn.time_out_of_bed):.2f},"
                s += f"{ssn.time_to_fall_asleep},"
                s += f"{ssn.wake_up_count},"
                s += f"{ssn.wake_ups_duration},"
                s += f"{ssn.sleep_quality},"
                s += f"{ssn.comment}\n"

                fp.write(s)

    def get_sheets_data(self, spreadsheet_id, range_name):
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
            data_cols = result.get("values", [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

        # in sheet, column A (idx 0) is date
        night = [mdates.datestr2num(n) for n in data_cols[0]]
        self._date = np.asarray(night)

        # in sheet, column B (idx 1) is "What time did you get into bed"
        self._time_into_bed = np.array(
            [self._to_rel_mdate(d, t) for d, t in zip(self.date, data_cols[1])]
        )

        # in sheet, column C (idx 2) is "What time did you try to get to sleep"
        self._time_try_to_sleep = np.array(
            [self._to_rel_mdate(d, t) for d, t in zip(self.date, data_cols[2])]
        )

        # in sheet, column D (idx 3) is "What time was your final awakening?"
        self._time_final_awakening = np.array(
            [self._to_rel_mdate(d, t) for d, t in zip(self.date, data_cols[3])],
        )

        # column E (idx 4)
        self._time_out_of_bed = np.array(
            [self._to_rel_mdate(d, t) for d, t in zip(self.date, data_cols[4])],
        )

        # column F (idx 5)
        self._minutes_to_fall_asleep = np.asarray(
            [self._val_convert(val) for val in data_cols[5]]
        )

        # column G (idx 6)
        self._wake_up_count = np.asarray(
            [self._val_convert(val) for val in data_cols[6]]
        )

        # column H (idx 7)
        self._wake_ups_duration_minutes = [
            self._val_convert(val) for val in data_cols[7]
        ]

        # column I (idx 8)
        self._time_smartwatch_fell_asleep = np.array(
            [self._to_rel_mdate(d, t) for d, t in zip(self.date, data_cols[8])]
        )

        # column J (idx 9)
        self._time_smartwatch_wakeup = np.array(
            [self._to_rel_mdate(d, t) for d, t in zip(self.date, data_cols[9])]
        )

        # column K (idx 10)
        self._smartwatch_wake_ups_duration_minutes = np.asarray(
            [self._val_convert(val) for val in data_cols[10]]
        )

        # column L (idx 11)
        self._sleep_quality = np.asarray(
            [self._val_convert(val) for val in data_cols[11]]
        )

        # column M (idx 12)
        self._rested = np.asarray([self._val_convert(val) for val in data_cols[12]])

        # column N (idx 13)
        self._comments = [c for c in data_cols[13]]

        # len of each array needs to be same
        len_self = self._date.size
        if len(self._comments) < len_self:
            pad_amount = len_self - len(self._comments)
            self._comments = np.pad(self._comments, (0, pad_amount), "constant")

        if len(self._minutes_to_fall_asleep) < len_self:
            pad_amount = len_self - len(self._minutes_to_fall_asleep)
            self._minutes_to_fall_asleep = np.pad(
                self._minutes_to_fall_asleep, (0, pad_amount), "constant"
            )

        if len(self._rested) < len_self:
            pad_amount = len_self - len(self._rested)
            self._rested = np.pad(self._rested, (0, pad_amount), "constant")

        if len(self._sleep_quality) < len_self:
            pad_amount = len_self - len(self._sleep_quality)
            self._sleep_quality = np.pad(
                self._sleep_quality, (0, pad_amount), "constant"
            )

        if len(self._smartwatch_wake_ups_duration_minutes) < len_self:
            pad_amount = len_self - len(self._smartwatch_wake_ups_duration_minutes)
            self._smartwatch_wake_ups_duration_minutes = np.pad(
                self._smartwatch_wake_ups_duration_minutes, (0, pad_amount), "constant"
            )

        if len(self._time_final_awakening) < len_self:
            pad_amount = len_self - len(self._time_final_awakening)
            self._time_final_awakening = np.pad(
                self._time_final_awakening, (0, pad_amount), "constant"
            )

        if len(self._time_into_bed) < len_self:
            pad_amount = len_self - len(self._time_into_bed)
            self._time_into_bed = np.pad(
                self._time_into_bed, (0, pad_amount), "constant"
            )

        if len(self._time_out_of_bed) < len_self:
            pad_amount = len_self - len(self._time_out_of_bed)
            self._time_out_of_bed = np.pad(
                self._time_out_of_bed, (0, pad_amount), "constant"
            )

        if len(self._time_smartwatch_fell_asleep) < len_self:
            pad_amount = len_self - len(self._time_smartwatch_fell_asleep)
            self._time_smartwatch_fell_asleep = np.pad(
                self._time_smartwatch_fell_asleep, (0, pad_amount), "constant"
            )

        if len(self._time_smartwatch_wakeup) < len_self:
            pad_amount = len_self - len(self._time_smartwatch_wakeup)
            self._time_smartwatch_wakeup = np.pad(
                self._time_smartwatch_wakeup, (0, pad_amount), "constant"
            )

        if len(self._time_try_to_sleep) < len_self:
            pad_amount = len_self - len(self._time_try_to_sleep)
            self._time_try_to_sleep = np.pad(
                self._time_try_to_sleep, (0, pad_amount), "constant"
            )

        if len(self._wake_up_count) < len_self:
            pad_amount = len_self - len(self._wake_up_count)
            self._wake_up_count = np.pad(
                self._wake_up_count, (0, pad_amount), "constant"
            )

        if len(self._wake_ups_duration_minutes) < len_self:
            pad_amount = len_self - len(self._wake_ups_duration_minutes)
            self._wake_ups_duration_minutes = np.pad(
                self._wake_ups_duration_minutes, (0, pad_amount), "constant"
            )

        # any TIMES in the spreadsheet, save them as a number relative to the beginning time of the date
        # ie, June 6 at 10pm will be saved as -2 hours, relative to midnight at the start of June 7

    def __len__(self):
        return self._date.size

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
            comment=self._comments[index]
        )

    def __iter__(self):
        for j in range(len(self)):
            yield self[j]

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

    def sleep_duration(self, unit="m"):
        # get_sheets_data2 returns all times in units of 1 day (in matplotlib.dates 1.0 = 1 day)
        match unit:
            case "m":
                multiplier = 24 * 60
            case "h":
                multiplier = 24
            case "s":
                multiplier = 24 * 60 * 60

        return (self.time_final_awakening - self.time_try_to_sleep) * multiplier

    def hist_sleep_qual(
        self,
    ):
        d = self.sleep_duration("h")
        fig, ax = plt.subplots(1)

        # num of unique values in sleep quality array
        u = np.unique(self.sleep_quality)
        colors = ["red", "orange", "yellow", "green", "blue"]

        e = np.histogram_bin_edges(d)
        e_centers = (e[:-1] + e[1:]) / 2
        top = None

        for i, ui in enumerate(u):
            subset = d[self.sleep_quality == ui]
            h, e = np.histogram(subset, bins=e)
            ax.bar(e_centers, h, bottom=top, label=str(ui), color=colors[i])
            if top is None:
                top = h
            else:
                top += h

        ax.legend()
        return fig, ax

    def plt_hist_duration(self):
        fig, ax = plt.subplots(1, 1)
        ax.hist(self.sleep_duration(unit="h"))

        ax.set_xlabel("Hours of sleep")
        ax.set_ylabel("Number of nights")
        ax.set_title("Histogram: Hours of sleep vs number of nights")

        return fig, ax

    def plt_nightly_duration(self):
        fig, ax = plt.subplots(1, 1)
        ax.plot(self.date, self.sleep_duration(unit="h"), "o")

        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())
        )

        ax.set_title("Sleep duration")
        ax.set_xlabel("Night")
        ax.set_ylabel("Hours slept")

        return fig, ax

    def plt_nightly_sleep_wake(self):
        x = self.date
        y0 = self.time_try_to_sleep
        y1 = self.time_final_awakening

        fig, ax = plt.subplots(1, 1)
        ax.vlines(x, y0, y1, "k")
        ax.plot(x, y0, "o", label="Fell asleep")
        ax.plot(x, y1, "o", label="Final wake")

        # date formating on axes ticks
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())
        )

        formatter = mdates.DateFormatter("%H:%M")
        ax.yaxis.set_major_locator(mdates.AutoDateLocator())
        ax.yaxis.set_major_formatter(formatter)
        ax.invert_yaxis()

        ax.set_xlabel("Night")
        ax.set_ylabel("Time of night")
        ax.set_title("Nightly sleep/wake times")
        ax.legend()

        return fig, ax

    def plt_nightly_multihist(
        self,
        time_try_to_sleep: bool = True,
        time_final_awakening: bool = True,
        time_into_bed: bool = True,
        time_out_of_bed: bool = True,
    ) -> typing.Tuple:
        fig, ax = plt.subplots(1, 1)

        x = self.date

        time_lst = []
        labels = []

        if time_into_bed:
            time_lst.append(self.time_into_bed)
            labels.append("Got into bed")

        if time_try_to_sleep:
            time_lst.append(self.time_try_to_sleep)
            labels.append("Tried to sleep")

        # if time_middle_sleep:
        #     m = (self.time_final_awakening + self.time_try_to_sleep)/2
        #     labels.append('middle of sleep')
        #     time_lst.append(m)

        if time_final_awakening:
            time_lst.append(self.time_final_awakening)
            labels.append("Final awakening")

        if time_out_of_bed:
            time_lst.append(self.time_out_of_bed)
            labels.append("Got out of bed")

        tmax = max(np.maximum.reduce(time_lst))
        tmin = min(np.minimum.reduce(time_lst))

        # want nearest 18min interval of the day, which is 1/80 a day
        round_to_nearest = 40

        hist_min = round(tmin * round_to_nearest - 1) / round_to_nearest
        hist_max = round(tmax * round_to_nearest + 1) / round_to_nearest

        t_bins = np.arange(
            hist_min,
            hist_max + (1 / round_to_nearest),
            step=1 / round_to_nearest,
        )
        for lab, t in zip(labels, time_lst):
            ax.hist(t, bins=t_bins, label=lab, alpha=0.5)

        ax.legend()

        formatter = mdates.DateFormatter("%H:%M")
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(formatter)

        return fig, ax

    def plt_nightly_times(
        self,
        time_try_to_sleep: bool = True,
        time_final_awakening: bool = True,
        time_into_bed: bool = True,
        time_out_of_bed: bool = True,
        time_middle_sleep: bool = True,
    ):
        x = self.date

        time_lst = []
        labels = []

        if time_into_bed:
            time_lst.append(self.time_into_bed)
            labels.append("Got into bed")

        if time_try_to_sleep:
            time_lst.append(self.time_try_to_sleep)
            labels.append("Tried to sleep")

        if time_middle_sleep:
            m = (self.time_final_awakening + self.time_try_to_sleep) / 2
            labels.append("middle of sleep")
            time_lst.append(m)

        if time_final_awakening:
            time_lst.append(self.time_final_awakening)
            labels.append("Final awakening")

        if time_out_of_bed:
            time_lst.append(self.time_out_of_bed)
            labels.append("Got out of bed")

        fig, ax = plt.subplots(1, 1)

        if len(time_lst) > 1:
            tmaxs = np.maximum.reduce(time_lst)
            tmins = np.minimum.reduce(time_lst)
            ax.vlines(x, tmins, tmaxs, "k")

        for lbl, times in zip(labels, time_lst):
            ax.plot(x, times, "o", label=lbl)

        # date formating on axes ticks
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(
            mdates.ConciseDateFormatter(ax.xaxis.get_major_locator())
        )

        formatter = mdates.DateFormatter("%H:%M")
        ax.yaxis.set_major_locator(mdates.AutoDateLocator())
        ax.yaxis.set_major_formatter(formatter)
        ax.invert_yaxis()

        ax.set_xlabel("Night")
        ax.set_ylabel("Time of night")
        ax.legend()

        return fig, ax

    def plt_prob_asleep(self, normalize=True):
        s = self.time_try_to_sleep
        w = self.time_final_awakening
        tmin = min(s.min(), w.min())
        tmax = max(s.max(), w.max())

        t = np.linspace(tmin, tmax, num=100)
        n = np.zeros(t.size)

        for si, wi in zip(s, w):
            n += np.logical_and(t > si, t < wi)

        if normalize:
            n /= s.size

        fig, ax = plt.subplots(1, 1)

        ax.plot(t, n)

        formatter = mdates.DateFormatter("%H:%M")
        ax.xaxis.set_major_locator(mdates.HourLocator())
        ax.xaxis.set_major_formatter(formatter)

        return fig, ax


if __name__ == "__main__":
    import pickle
    import pathlib as pl

    pkl_file = pl.Path("./sleepnight.pickle")

    spreadsheet_id = "1eSSOl3b9VTu12zw1vkdYovycNnjxxDNYPZtdfSMUhlc"
    sheetrange = "!A3:N"

    sn = SleepNights()

    if not pkl_file.exists():
        print("downloading data")
        sn.get_sheets_data(spreadsheet_id, sheetrange)
        as_lst = []
        for j, ssn in enumerate(sn):
            print(j, ssn.date)
            as_lst.append(ssn)

        with open(pkl_file, "wb") as o:
            print("writing pickle")
            pickle.dump(as_lst, o)

    else:
        print("loading pickle")
        with open(pkl_file, "rb") as o:
            ssn_lst = pickle.load(o)
            sn = SleepNights()
            sn.from_single_sleep_night_sequence(ssn_lst)

    # fig,ax = sn.plt_nightly_times()
    # f2, a2 = sn.plt_hist_duration()
    # f3, a3 = sn.plt_nightly_multihist()
    # f4, a4 = sn.plt_nightly_duration()

    # mt = mdates.num2date(np.median(sn.time_final_awakening))
    # print(mt)

    # print(
    #     f"avg time to fall asleep {mdates.num2date(np.nanmedian(sn.time_try_to_sleep))}"
    # )

    # weeknights = mdates.num2date(sn.time_try_to_sleep)
    # arr = np.asarray([w.weekday() for w in weeknights])

    # weeknights = mdates.num2date(np.nanmedian((sn.time_try_to_sleep[arr])))
    # x = sn.time_to_fall_asleep
    # print(np.mean(x))
    # print(weeknights)

    sn.to_soca_format_csv(pl.Path('./out.csv'))


