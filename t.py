#!/usr/bin/env python3

import sys
import yfinance as yf
from argparse import ArgumentParser
from pathlib import PosixPath

from utils import HERE, SQLite, today, prev_weekday


TODAY = today()
PREV_WEEKDAY_1 = prev_weekday(TODAY)
PREV_WEEKDAY_2 = prev_weekday(PREV_WEEKDAY_1)

DB_PATH = str(HERE / 'scavg.db')
SYMBOLS = ['AAPL']
MODEL_KEYS = ['symbol', 'previousClose']


def create_tables(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id         INTEGER PRIMARY KEY,
            symbol     TEXT,
            buy_date   TEXT,
            buy_price  REAL,
            volume     INTEGER
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS monitor (
            id         INTEGER PRIMARY KEY,
            date       TEXT,
            symbol     TEXT,
            close      REAL,
            change     REAL
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS todo (
            id         INTEGER PRIMARY KEY,
            action     TEXT,
            symbol     TEXT,
            volume     INTEGER
        )''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id         INTEGER PRIMARY KEY,
            action     TEXT,
            date       TEXT,
            symbol     TEXT,
            price      REAL,
            volume     INTEGER
        )''')


def get_data(symbols):
    symbols = [s.upper() for s in symbols]
    return {sym: yf.Ticker(sym).info for sym in symbols}


def scrape():
    with SQLite(DB_PATH) as cur:
        for sym, data in get_data(SYMBOLS).items():
            prev_close = data['previousClose']

            cur.execute(
                '''SELECT * FROM monitor
                   WHERE date=? AND symbol=?''',
                (YESTERDAY, sym))
            if cur.fetchall():
                cur.execute(
                    '''UPDATE monitor
                       SET close=?
                       WHERE date=? AND symbol=?''',
                    (YESTERDAY, prev_close, sym))
            else:
                change = prev_close - prev_prev_close
                cur.executemany(
                    '''INSERT INTO TABLE
                       monitor (date, symbol, close, change)
                       VALUES (?, ?, ?, ?)''',
                    (YESTERDAY, sym, prev_close, change))


def trade():
    pass


def log():
    import json
    print(json.dumps(get_data(SYMBOLS)))


def main():
    parser = ArgumentParser()
    parser.add_argument('command', choices=('scrape', 'trade', 'log'))
    ns = parser.parse_args()

    with SQLite(DB_PATH) as cur:
        create_tables(cur)

    if ns.command == 'scrape':
        scrape()
    elif ns.command == 'trade':
        trade()
    elif ns.command == 'log':
        log()
    else:
        print('Not possible', file=sys.stderr)


if __name__ == '__main__':
    main()
