#!/usr/bin/env python3

import sys
import yfinance as yf
from pathlib import PosixPath


HERE = PosixPath(__file__).resolve().parent
SYMBOLS = ['AAPL']
MODEL_KEYS = ['ask', 'dayHigh', 'dayLow']


def get_data(symbols):
    data = {}
    for sym in symbols:
        sym = sym.upper()
        data[sym] = {}
        info = yf.Ticker(sym).info
        for k in MODEL_KEYS:
            data[sym][k] = info[k]
    return data


def main(argv):
    data = get_data(SYMBOLS)


if __name__ == '__main__':
    main(sys.argv)
