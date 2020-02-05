import sqlite3
from datetime import datetime, timedelta
from pathlib import PosixPath


HERE = PosixPath(__file__).resolve().parent


class SQLite:

    def __init__(self, file='sqlite.db'):
        self.conn = None
        self.file = file

    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


def today():
    return datetime.today().date().isoformat()


def prev_weekday(d):
    if isinstance(d, str):
        d = datetime.strptime(d, '%Y-%m-%d').date()
    while True:
        # Subtract 1 day
        d = d - timedelta(days=1)
        # Return prev if it's not a Saturday or Sunday
        if d.weekday() < 5:
            return d
