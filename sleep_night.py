import numpy as np

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SleepNights:
    def __init__(self):
        self._date = None
        self._try_to_sleep = None
        self._final_wake = None
        self._get_up = None
        self._time_to_sleep = None
        self._wakes_count = None
        self._wakes_duration = None

    def get_data(spreadsheet_id, range_name, creds):
        """Use Sheets API to get desired data. Load said data into this data structure"""
        try:
            service = build("sheets", "v4", credentials=creds)

            result = (
                service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    majorDimansion="COLUMNS"
                    # TODO: dateTimeRenderOption
                )
                .execute()
            )

            cols = result.get("values", [])

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
