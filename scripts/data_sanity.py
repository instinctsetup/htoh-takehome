#!/usr/bin/env python3
"""Read-only sanity checks on the H TO H data pack: shapes, ranges, gaps and anomalies.

Usage (from the repo root):
    python scripts/data_sanity.py

Expects the pack unzipped at pack/. Prints a report; writes nothing.
"""
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pack', 'data')


def check_task1():
    path = os.path.join(DATA, 'nifty50_15min_train_2017-04-03_2022-01-31.csv')
    df = pd.read_csv(path, parse_dates=['datetime'])
    print('Task 1 15-min bars: %d rows, %s to %s'
          % (len(df), df['datetime'].min(), df['datetime'].max()))
    print('  missing values: %d' % df.isna().sum().sum())
    per_day = df.groupby(df['datetime'].dt.date).size()
    print('  bars per day: median %d, min %d, max %d'
          % (per_day.median(), per_day.min(), per_day.max()))
    print('  days with fewer than 25 bars: %d' % (per_day < 25).sum())
    print('  bars with n_1min < 15: %d' % (df['n_1min'] < 15).sum())


def check_task2():
    path = os.path.join(DATA, 'stocks_daily_train_2021-04-26_2024-06-30.csv')
    df = pd.read_csv(path, parse_dates=['date']).sort_values(['symbol', 'date'])
    print('Task 2 stocks daily: %d rows, %d symbols, %s to %s'
          % (len(df), df['symbol'].nunique(), df['date'].min().date(), df['date'].max().date()))
    print('  missing values: %d' % df.isna().sum().sum())
    ret = df.groupby('symbol')['close'].pct_change()
    big = df[ret < -0.45].assign(ret=ret[ret < -0.45])
    print('  one-day close drops beyond 45% (possible unadjusted corporate actions):')
    for _, row in big.iterrows():
        print('    %s  %-12s %+.1f%%' % (row['date'].date(), row['symbol'], 100 * row['ret']))
    symbols = open(os.path.join(DATA, 'symbols.txt')).read().split()
    print('  symbols.txt: %d names; all present in data: %s'
          % (len(symbols), set(symbols) <= set(df['symbol'].unique())))
    listed = df.groupby('symbol')['date'].min()
    print('  symbols listing after data start: %d' % (listed > df['date'].min()).sum())


if __name__ == '__main__':
    if not os.path.isdir(DATA):
        raise SystemExit('pack/data not found - unzip candidate_pack.zip into pack/ first')
    check_task1()
    print()
    check_task2()
