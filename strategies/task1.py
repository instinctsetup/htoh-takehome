"""
Task 1: Nifty 50 futures strategy on 15-minute bars.

REFERENCE IMPLEMENTATION - AI-assisted, for private review and learning. See README "Provenance".
Not represented as the candidate's own unaided work; the assignment requires "the signal logic must be
your own code" and includes a live walkthrough.

Idea (opening-range breakout with a daily trend filter, intraday only):
  - The first `orb_bars` 15-minute bars of each day define the day's opening range (high/low).
  - After that, a close above the opening-range high triggers a long; a close below the low triggers a short.
    Once triggered, the position is held for the rest of the day (no flip-back).
  - Direction must agree with the daily trend: longs only when the trailing `trend_lookback`-day return of
    the index is positive, shorts only when it is negative (time-series momentum regime filter).
  - No new entries at or after `entry_cutoff`; the position is closed at the end of the day
    (flat decided at the 15:15 bar's close, so the fill lands at the next day's open).

Why it should work economically: days that break out of their opening range in the direction of the
prevailing multi-week trend tend to keep drifting that way (short-horizon continuation of order flow);
the trend filter keeps the strategy out of the choppy, mean-reverting regimes where breakouts fail, and
intraday-only holding avoids paying the overnight futures carry on longs.

Look-ahead safety: every decision uses only bars that have closed by that bar; a day's close enters the
trend filter only from 15:30 IST that day; the opening range uses only the day's first `orb_bars` bars.
Day structure is inferred from bar timestamps (the 15:15 bar), never from array position, so the harness
look-ahead check (re-running on truncated data) passes. Days with fewer bars than `orb_bars` (e.g. Muhurat
sessions) simply produce no signal.
"""
import numpy as np
import pandas as pd

PARAMS = {
    'orb_bars': 6,               # opening range = first 6 bars (09:15-10:30)
    'trend_lookback': 60,        # days for the daily time-series momentum filter
    'entry_cutoff': '13:45',     # no new entries at/after this time (IST)
}


def positions(bars: pd.DataFrame, params: dict) -> pd.Series:
    k = int(params['orb_bars'])
    cutoff = pd.Timestamp(params['entry_cutoff']).time()

    day = bars.index.normalize()
    day_arr = day.values
    bar_num = pd.Series(np.arange(len(bars)), index=bars.index).groupby(day_arr).cumcount()

    # --- daily trend filter (time-series momentum on completed daily closes) ---
    # A day contributes its close only once its 15:15 bar exists, so the value available at any bar
    # is identical whether the data is truncated at that bar or not.
    is_last_regular = (bars.index.hour == 15) & (bars.index.minute == 15)
    dclose = bars['close'][is_last_regular].copy()
    dclose.index = dclose.index.normalize()
    r = dclose / dclose.shift(int(params['trend_lookback'])) - 1
    trend = pd.Series(np.where(r > 0, 1.0, -1.0), index=dclose.index)
    trend[r.isna()] = 0.0
    trend.index = trend.index + pd.Timedelta(hours=15, minutes=30)  # available from 15:30 that day
    decision = bars.index + pd.Timedelta(minutes=15)                # decisions happen at bar closes
    trend_bars = trend.reindex(trend.index.union(decision)).ffill().reindex(decision).fillna(0.0)

    # --- opening range per day ---
    orh = bars['high'][bar_num < k].groupby(day_arr[bar_num < k]).max()
    orl = bars['low'][bar_num < k].groupby(day_arr[bar_num < k]).min()
    orh = pd.Series(orh.reindex(day_arr).values, index=bars.index).groupby(day_arr).ffill()
    orl = pd.Series(orl.reindex(day_arr).values, index=bars.index).groupby(day_arr).ffill()

    # --- breakout triggers (after the opening range, before the cutoff) ---
    raw = pd.Series(np.nan, index=bars.index)
    raw[(bar_num.values >= k) & (bars['close'].values > orh.values)] = 1.0
    raw[(bar_num.values >= k) & (bars['close'].values < orl.values)] = -1.0
    raw[bars.index.time >= cutoff] = np.nan                    # no new entries late in the day
    sig = raw.groupby(day_arr).ffill().fillna(0.0)             # hold the day's first trigger
    sig[bar_num.values < k] = 0.0
    sig[is_last_regular] = 0.0                          # flat into the next day

    # --- direction must agree with the daily trend ---
    out = np.where(np.sign(sig.values) == np.sign(trend_bars.values), sig.values, 0.0)
    return pd.Series(out, index=bars.index)
