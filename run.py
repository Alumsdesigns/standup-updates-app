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
