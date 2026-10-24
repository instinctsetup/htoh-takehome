# Draft: report.pdf source (Task 1 + Task 2) - for review, not submission

This is a draft the candidate can edit and export as the <=3-page report.pdf. It is AI-assisted (see README Provenance) - rewrite it in your own words and make sure you can defend every line live before using it.

## Task 1 - NIFTY futures intraday strategy

**Hypothesis.** On trend days, the opening range (first 90 minutes) often breaks in the direction of the larger daily trend; trading only with a slow trend filter and exiting by close avoids overnight gap risk and carry cost.

**Signal (3 params).** Opening-range breakout over the first 6 15-min bars; long only if the 60-trading-day close-to-close return is positive, short only if negative; no entries after 13:45; flat by the 15:15 bar. One position at a time, intraday only.

**Results (pack harness, 2017-04 to 2022-01).** CAGR 20.27%, max DD -7.52%, Sharpe 1.55, 370 trades, 61.4% win rate, 17.2% time in market. Year-wise: 2017 +8.9%, 2018 +8.2%, 2019 +24.5%, 2020 +34.8%, 2021 +23.1%, Jan-22 +0.2%.

**Robustness.** 2-bar fill delay: Sharpe 1.74 (delay helps - post-breakout reversal; not execution-fragile). 2x costs: Sharpe 1.07 - this is the weak point, driven by ~77 round trips/yr; documented openly. Delay + 2x costs: 1.31. Sensitivity over orb_bars {4,6,8} x trend_lookback {40,60,90}: Sharpe 1.27-1.72, a plateau, not a spike.

**Limitations.** Performance depends on the cost assumption; a mean-reversion intraday regime hurts breakouts (2017 was the softest full year). No claim about the hidden Feb-2022-Oct-2026 holdout.

## Task 2 - NSE stock portfolio

**Hypothesis.** Cross-sectional momentum in Indian equities, risk-adjusted and liquidity-filtered, harvested monthly with low turnover.

**Signal (5 params).** Every 30 days: score = 126-day return / 63-day volatility; hold the top 15 names with 60-day median traded value >= Rs 10 cr and positive score, equal weights; exit names that fall out. Max 15 names / 15% each respected; no adds to open positions; market orders only.

**Results (pack harness, 2022-03-02 to 2024-06-28).** CAGR 60.91%, max DD -21.69%, Sharpe 2.065, 200 trades, 52.5% win rate, avg hold 40 days, turnover 10.8x/yr. Year-wise: 2022 +17.5%, 2023 +74.6%, 2024 +47.3%.

**Robustness.** Lookback {90,126,189} x n {10,12,15}: Sharpe 1.69-2.19, plateau. Excluding 2023 entirely, remaining days still compound +73.1%. Top-10 trades = 41.8% of gross gains - no single-name luck. SPLPETRO (-49% on 2022-06-07): never held; filters exclude it, and even if held, 1/15 weight caps the damage (~-3.3% portfolio hit).

**Limitations.** Sensitive to the arbitrary monthly anchor (Sharpe ~1.7-2.1 across anchors; reported value uses the natural anchor, not the max). 2023's momentum regime drives a large share of returns; a momentum crash (sharp reversal) is the main tail risk, partially mitigated by the volatility divisor. No claim about the hidden Jul-2024-Oct-2026 holdout.

## Survivorship / data notes
The stock panel contains the symbols the organisers shipped; symbols that cease trading simply stop producing data and are never re-selected (positions in them can only be exited if a last price exists - the pack handles SPLPETRO-class events by data absence). No stock-level survivorship correction was applied beyond the liquidity and data-availability filters; this is a factual limitation of the provided panel.
