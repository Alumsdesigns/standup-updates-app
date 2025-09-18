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

def format_pretty_date(date: datetime.date) -> str:
    """
    Format a date into a friendly string like 'Mon 15th Sept'.
    Always uses UTC time for consistency.
    """
    suffix = "th"
    if date.day in [1, 21, 31]:
        suffix = "st"
    elif date.day in [2, 22]:
        suffix = "nd"
    elif date.day in [3, 23]:
        suffix = "rd"

    month = date.strftime("%B")[:4]
    return date.strftime(f"%a {date.day}{suffix} ") + month

def display_section(section_name: str, entries: list):
    """
    Show a neatly formatted table with a bold title, and
    each entry is listed as a numbered row. Uses Rich for styling.
    """
    table = Table(
        title=f"[bold bright_yellow]{section_name}[/bold bright_yellow]",
        show_lines=True,
        expand=False, padding=(0, 1)
    )
    table.add_column(
        "Line",
        style="bright_cyan",
        justify="center",
        width=4
    )
    table.add_column(
        "Text",
        style="white",
        justify="left",
        no_wrap=False,
        width=50
    )
    for i, line in enumerate(entries, 1):
        table.add_row(str(i), line)
    console.print(table)

def validate_line(
        line: str,
        max_words=MAX_WORDS_PER_LINE,
        max_length=MAX_INPUT_LENGTH):
    """
    Check a line to make sure it’s not too long 
    or too wordy to fit in gcells and its safe.
    """
    words = line.split()
    if len(words) > max_words:
        return False, f"Too many words: {len(words)} (max {max_words})"
    if len(line) > max_length:
        return False, f"Too many characters: {len(line)} (max {max_length})"
    sanitized = line.replace("\n", " ").replace(";", "")
    return True, sanitized


class DailyLog:
    """
    Keep track of daily updates in a simple
    log and provide helpers for saving/formatting.
    """

    def __init__(self, name: str, date: datetime.date = None):
        self.name = name.strip().title()
        self.today = (date or datetime.datetime.now(timezone.utc).date())
        self.yesterday = get_previous_working_day(self.today)
        self.sections = {
            "Yesterday": [],
            "Today": [],
            "Blockers": [],
            "FYI": []}

    def enter_sections(self):
        for key in self.sections:
            print(f"Section: {key}")
            while True:
                line = questionary.text(f"Add one line for {key}:").ask()
                valid, msg = validate_line(line)
                if valid:
                    self.sections[key].append(msg)
                    break
                else:
                    print(msg)

    def edit_line(self, section_name: str):
        entries = self.sections[section_name]
        if not entries:
            console.print("[bright_red]No lines to edit[/bright_red]")
            return
        idx = questionary.select(
            f"{section_name} - Select a line to edit:",
            choices=[f"{i + 1}: {line}" for i, line in enumerate(entries)] + ["Cancel edit"]
        ).ask()
        if idx == "Cancel edit":
            return
        idx = int(idx.split(":")[0]) - 1
        new_text = questionary.text(f"Replace line {idx + 1}:").ask()
        valid, msg = validate_line(new_text)
        if valid:
            entries[idx] = msg
            self.sections[section_name] = entries

# test edit section by running the app
if __name__ == "__main__":
    log = DailyLog("Alice")
    print(log.name)      
    log.enter_sections()
    log.enter_sections()         
    log.edit_line("Today")
