# Draft: failed_ideas.md source - for review, not submission

AI-assisted draft (see README Provenance). Every number below was measured in the pack harness during development.

1. **Time-series momentum mapped daily -> intraday (Task 1).** Mapping yesterday's daily-close momentum signal onto today's intraday bars looked great until a within-day timing bug was found: a day's own close was being used on that same day's bars (look-ahead). Leaked Sharpe ~1.65-2.10; corrected with the timestamp rule (a day's close counts only at/after its 15:15 bar), the honest Sharpe collapsed to ~0.93. Lesson: never key daily signals by array position; key by timestamp.

2. **Pure opening-range breakout, no trend filter (Task 1).** Intraday-only ORB alone: Sharpe 0.64-0.75, and negative (-0.2) at 2x costs. Too many false breakouts in chop. The 60-day trend filter is what carries the strategy (1.55).

3. **ORB held overnight (Task 1).** An early version forgot end-of-day flattening and held breakouts overnight: Sharpe ~1.46 looked decent but violated the intended intraday-only design and exposed the book to gap risk and nightly carry. Fixed to flat-by-15:15.

4. **Naive absolute momentum without volatility adjustment (Task 2).** Ranking by raw 126-day return loads up on the most volatile names; drawdowns deepen and momentum crashes hit harder. Dividing by 63-day vol improved Sharpe and kept the wildest names out.

5. **Tranching / partial adds to reduce anchor sensitivity (Task 2).** Splitting the 30-day rebalance into weekly tranches would smooth the rebalance-anchor sensitivity, but the pack rule "no adding to an already-open position" blocks true tranching. Dropped; anchor sensitivity (Sharpe ~1.7-2.1) disclosed instead.

6. **Longer momentum lookbacks only (Task 2).** 189-day lookback alone is slower to drop broken trends; combined with n=15 it does score well (2.19) but we kept the middle-of-plateau 126-day config rather than the grid max.
