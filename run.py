#!/usr/bin/env python3
"""
Daily Log Terminal App with Google Sheets Integration
Author: Damaris Alum
Date: 14-09-2025
"""
import time
import datetime
from datetime import timezone
import os
import datetime
import gspread
import questionary
from rich.console import Console
from rich.table import Table
from gspread_formatting import (
    format_cell_range, CellFormat, Color, TextFormat, Borders, Border
)
from google.oauth2.service_account import Credentials
from google.auth.exceptions import GoogleAuthError

console = Console()

MAX_WORDS_PER_LINE = 25
MAX_INPUT_LENGTH = 200

IRISH_BANK_HOLIDAYS_2025 = [
    datetime.date(2025, 1, 1),
    datetime.date(2025, 3, 17),
    datetime.date(2025, 4, 21),
    datetime.date(2025, 5, 5),
    datetime.date(2025, 6, 2),
    datetime.date(2025, 8, 4),
    datetime.date(2025, 10, 27),
    datetime.date(2025, 12, 25),
    datetime.date(2025, 12, 26),
]

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('standup_updates_2025')

def get_previous_working_day(today: datetime.date) -> datetime.date:
    """
    Find the last working day before today ignoring
    weekends and 2025 Irish bank holidays.
    """
    day = today - datetime.timedelta(days=1)
    while day.weekday() >= 5 or day in IRISH_BANK_HOLIDAYS_2025:
        day -= datetime.timedelta(days=1)
    return day