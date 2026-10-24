"""
Task 2: long-only NSE stock portfolio on daily bars.

REFERENCE IMPLEMENTATION - AI-assisted, for private review and learning. See README "Provenance".
Not represented as the candidate's own unaided work; the assignment requires "the signal logic must be
your own code" and includes a live walkthrough.

Idea (risk-adjusted momentum, monthly):
  - Every `rebalance_days` days, rank liquid stocks by 6-month total return divided by recent
    volatility (`vol_lookback`-day std of daily returns) - risk-adjusted momentum.
  - Hold the top `n_stocks` names in equal weights, exit names that fall out of the list.
  - Liquidity filter: 60-day median traded value >= `min_turnover` (Rs 10 crore), same as the pack template.

Why it should work economically: cross-sectional momentum is a persistent anomaly in Indian equities
(fund flows chase recent winners); dividing by volatility avoids loading up on the wildest names, which
is where momentum crashes start; a monthly cadence keeps turnover and cost drag low.

Robustness notes:
  - Stocks with incomplete history (listed < lookback days) are simply not ranked.
  - One-day crashes like SPLPETRO (2022-06-07, -49%) hurt the held position but cannot break the
    portfolio: max 1/15 weight per name and no leverage. No special-casing is applied.
  - No look-ahead: only hist data up to and including `date` is used; orders execute next day.
"""
import numpy as np
import pandas as pd

PARAMS = {
    'lookback': 126,          # momentum lookback in trading days (~6 months)
    'n_stocks': 15,           # portfolio size (max allowed)
    'vol_lookback': 63,       # days for the volatility estimate (~3 months)
    'rebalance_days': 30,     # calendar days between rebalances
    'min_turnover': 1e8,      # 60-day median traded value floor, Rs
}


def orders(date, hist, portfolio, params, state):
    c = hist['close']
    if len(c) < 2:
        return []
    last_reb = state.get('last_reb')
    if last_reb is not None and (c.index[-1] - last_reb).days < params['rebalance_days']:
        return []
    state['last_reb'] = c.index[-1]

    lb = int(params['lookback'])
    tail = c.iloc[-(lb + 30):]
    if len(tail) <= lb:
        return []  # not enough history yet (start of the evaluation window)
    turnover = (tail * hist['volume'].iloc[-len(tail):]).rolling(60, min_periods=40).median().iloc[-1]
    ret = tail.iloc[-1] / tail.iloc[-1 - lb] - 1
    vol = tail.pct_change(fill_method=None).iloc[-int(params['vol_lookback']):].std()
    score = ret / vol.replace(0, np.nan)
    ok = score[(turnover >= params['min_turnover']) & score.notna() & (score > 0)]
    top = list(ok.sort_values(ascending=False).index[:int(params['n_stocks'])])

    out = [{'symbol': s, 'side': 'sell', 'type': 'market'} for s in portfolio['positions'] if s not in top]
    w = 1.0 / int(params['n_stocks'])
    out += [{'symbol': s, 'side': 'buy', 'type': 'market', 'weight': w}
            for s in top if s not in portfolio['positions']]
    return out
