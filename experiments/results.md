# Experiment record - H TO H take-home reference implementation

All numbers below were measured with the pack's own `harness_public.py` (CLI: `python harness_public.py task1|task2 <file>`) on the pack's training data. Nothing here is estimated or assumed. Both final files print `look-ahead check: OK`.

Provenance: AI-assisted reference implementation (see README). These results describe this reference code only - they say nothing about performance on the hidden holdout sets (Task 1: Feb 2022 - Oct 2026; Task 2: Jul 2024 - Oct 2026).


## What these numbers are - and are not (read first)

- All results are IN-SAMPLE, measured on the pack's public training data, and the parameters were TUNED ON THAT SAME DATA. That is data snooping / selection bias by construction: I tried multiple signal families and parameter grids and kept what scored well. Out-of-sample performance will be worse; the honest expectation is degradation, not repetition.
- The pack's hidden holdouts (Task 1: Feb 2022 - Oct 2026; Task 2: Jul 2024 - Oct 2026) are the only independent test, and no claim is made or implied about them. Nothing here is a guarantee, projection, or promise of future returns.
- Sharpe figures are the harness's own: Task 1 annualizes 15-minute bar returns in excess of a 6% risk-free rate; Task 2 annualizes daily portfolio returns with rf = 0. CAGR/annualization assume the sample period's compounding continues, which it may not.
- The parameter sensitivity tables exist to show the chosen config is not a lone spike; they also reveal how much the score depends on arbitrary choices (e.g. the Task 2 rebalance anchor spread of roughly 1.70-2.09).

## Task 1 - NIFTY futures intraday (15-min, 2017-04-03 to 2022-01-31)

Chosen strategy: opening-range breakout (first 6 bars after 09:15), traded only in the direction of a 60-day close-to-close trend filter, entries cut off at 13:45, flat by 15:15, intraday only.

`PARAMS = {'orb_bars': 6, 'trend_lookback': 60, 'entry_cutoff': '13:45'}` - 3 tunable params (limit is 6).

Final file results (harness CLI):

| metric | value |
|---|---|
| CAGR | 20.27% |
| max drawdown | -7.52% |
| Sharpe (excess of 6%) | 1.55 |
| Calmar | 2.69 |
| trades | 370 (~77/yr) |
| win rate | 61.35% |
| time in market | 17.24% |

Year-wise: 2017 +8.85%, 2018 +8.18%, 2019 +24.52%, 2020 +34.82%, 2021 +23.13%, Jan-2022 +0.18%.

Their bar (Sharpe > 1.0 AND max DD better than -15%): PASS. Internal reference (CAGR 23.3% / DD -12.8% / Sharpe 1.22): beats Sharpe and DD, slightly lower CAGR.

Robustness (same file, harness variations):

| variation | CAGR | max DD | Sharpe |
|---|---|---|---|
| default | 20.27% | -7.52% | 1.55 |
| 2-bar fill delay | 24.24% | -7.74% | 1.74 |
| 2x costs (0.05%/side) | 15.52% | -7.94% | 1.07 |
| delay + 2x costs | 19.32% | -8.13% | 1.31 |

Notes: the 2-bar delay *improving* results is a real measured effect (short-term reversal right after a breakout) - the strategy is not fragile to execution delay. Doubled costs are the weak point: Sharpe drops to 1.07, barely above the bar. Cost drag is inherent to ~77 round trips/yr (2 sides x 2.5 bps each).

Parameter sensitivity (Sharpe, orb_bars x trend_lookback):

| orb_bars | lb=40 | lb=60 | lb=90 |
|---|---|---|---|
| 4 | 1.66 | 1.46 | 1.27 |
| 6 | 1.52 | **1.55** | 1.33 |
| 8 | 1.67 | 1.72 | 1.37 |

Broad plateau, no cliff around the chosen (6, 60). k=8/lb=60 scores 1.72; we keep 6 (middle of the tested range) rather than picking the grid maximum.

## Task 2 - NSE stock portfolio (daily, evaluation 2022-03-02 to 2024-06-28)

Chosen strategy: 30-calendar-day rebalance (checked on trading days, ~20-21 trading days apart, not month-aligned) into the top 15 liquid names by risk-adjusted momentum: 126-day total return / 63-day return volatility, equal weights, liquidity floor of Rs 10 crore 60-day median traded value, only positive-momentum names held.

`PARAMS = {'lookback': 126, 'n_stocks': 15, 'vol_lookback': 63, 'rebalance_days': 30, 'min_turnover': 1e8}` - 5 params.

Final file results (harness CLI):

| metric | value |
|---|---|
| CAGR | 60.91% |
| max drawdown | -21.69% |
| Sharpe (rf = 0) | 2.065 |
| Calmar | 2.81 |
| trades | 200 |
| win rate | 52.5% |
| avg hold | 40.4 days |
| turnover/yr | 10.8x |

Year-wise: 2022 +17.50% (from Mar), 2023 +74.56%, 2024 +47.31% (to Jun).

Their bar (Sharpe > 1.9 AND max DD better than -25%): PASS. Internal reference (CAGR 51.6% / Sharpe 1.93): beaten on both.

Report extras:
- Cost drag: turnover 10.8x/yr x 0.2%/side ~ 2.15%/yr.
- Best year removed: excluding all 2023 trading days, the remaining days still compound to +73.1% (330 trading days) - performance is not one year's fluke, though 2023 (small/mid-cap momentum rally) is clearly the strongest regime.
- Top-10 winning trades = 41.8% of gross winning return (200 trades) - profits are reasonably spread, not one lucky name.
- SPLPETRO (the -49% one-day crash on 2022-06-07): never traded by this strategy; liquidity + risk-adjusted filters keep such names out. No special-casing in code.

Parameter sensitivity (Sharpe, lookback x n_stocks):

| lookback | n=10 | n=12 | n=15 |
|---|---|---|---|
| 90 | 1.69 | 1.79 | 1.82 |
| 126 | 1.99 | 1.95 | **2.06** |
| 189 | 1.83 | 2.08 | 2.19 |

Honest caveat measured earlier: results move with the arbitrary rebalance anchor date (Sharpe range roughly 1.70-2.09 across month anchors). 2.065 is the natural anchor (rebalance on first available day then every 30 days), not the max of that spread. The rebalance anchor sensitivity is a real property of monthly momentum and is disclosed here rather than hidden.

## Runtime
Both backtests complete in seconds (Task 1 ~0.4s, Task 2 ~2s) - far under the 10-minute limit.
