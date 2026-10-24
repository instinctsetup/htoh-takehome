# H TO H harness, explained

Plain-English mechanics of `harness_public.py` and the two task interfaces, from reading the pack.
Nothing here is strategy logic; it is how the scoring works so you can build against it correctly.

## Layout and how to run

- The harness loads data from a `data/` folder **next to itself** (`pack/data/`), so keep the pack's structure intact.
- Run it exactly like this from the pack folder (or use `scripts/run.py` from the repo root):

```
python harness_public.py task1 task1.py
python harness_public.py task2 task2.py
```

- It needs only numpy + pandas (Python 3.9+). It prints CAGR, total return, max drawdown, Sharpe, Calmar,
  trades, win rate, average trade, turnover, time in market, and a year-wise return table.
- Sharpe is annualised with sqrt(252) from **daily** returns, in excess of what idle cash earns
  (6%/yr for Task 1, 0% for Task 2). In Task 1 the cash credit is added daily, so Sharpe there is
  roughly "how much better than the liquid fund, per unit of volatility".

## Task 1: Nifty futures on 15-min bars

Interface:

```python
PARAMS = {...}                                  # max 6 entries
def positions(bars: pd.DataFrame, params: dict) -> pd.Series:
    ...                                         # one value per bar, exactly -1, 0 or +1, no NaN
```

- `bars` has a DatetimeIndex (bar **start**, IST) and columns open/high/low/close. 25 bars per normal day;
  short sessions exist (e.g. 3 bars on 2021-11-04), so never assume 25.
- The value at bar i is what you want, decided at the **close of bar i**; the harness holds it from the
  **open of bar i+1**. First 200 bars are forced flat (your warm-up).
- The look-ahead check re-runs your `positions()` on truncated data at 4 random cut points and requires the
  last value to match the full-data run. Anything that uses the whole series at once (global mean/std,
  z-score over all data, `.shift(-k)`, centered windows) fails. Use rolling/expanding calculations only.
- Daily accounting, all as fractions of capital:
  - overnight gap: previous position x (today's open / yesterday's close - 1)
  - in-bar move: today's position x (close / open - 1)
  - cost: 0.025% per side on every position **change**; a +1 to -1 flip costs 2 sides
  - carry: a position held overnight pays pos x (6% - 1.3%) / 252 (longs pay, shorts receive)
  - roll: if the previous day was a monthly expiry, a carried position pays 2 sides (0.05%)
  - cash: +6%/252 every trading day whether invested or not
  - returns are summed within a day, compounded daily
- Positions are 1x capital only (-1/0/+1); there is no sizing to tune.

## Task 2: long-only NSE stock portfolio on daily bars

Interface:

```python
PARAMS = {...}                                  # max 6 entries
def orders(date, hist, portfolio, params, state) -> list:
    ...                                         # list of order dicts, valid next day only
```

- Called once per trading day **after the close**. `hist` never contains anything after `date`:
  wide DataFrames open/high/low/close/volume (index date, columns symbol, NaN before listing) plus
  `hist['nifty']`. `state` is your persistent dict between calls.
- The first call happens on the close of 2022-03-01 so the first fills land on 2022-03-02 (window start).
  Data starts 2021-04-26, so about 10 months of warm-up; a 252-day lookback is not fully available at the
  window start - handle short history.
- Order types:
  - buy market: fills at next open
  - buy stop with trigger x: fills only if next high > x, at max(open, x)
  - sell market: whole position at next open
  - sell stop with trigger x: fills only if next low < x, at min(open, x)
- Next-day execution order: market sells at the open, then buys **in the order you listed them**, then
  stop sells. A stop sell cannot trigger on a position bought that same day.
- Buy size = min(weight, 15%) x portfolio value at the decision close, capped by available cash. Max 15
  open positions, no leverage, no shorting, **no adding to an open position** (a buy for a held symbol is
  skipped). `'max_positions': k` on a buy makes it fill only while fewer than k positions are open.
- Orders on a symbol with no price that day lapse; anything unfilled is cancelled (orders never carry over).
- Cost 0.2% per side, both ways. Idle cash earns **nothing**. Positions are valued at the latest close
  (forward-filled through missing days).
- Sharpe uses rf = 0. `time_in_market` reported is average gross exposure.
- Speed: `hist` grows daily; slice the tail (`hist['close'].iloc[-300:]`) for rolling indicators.

## Rules that the harness enforces or that they check manually

- `PARAMS` must exist and have at most 6 entries (harness raises otherwise).
- Task 1 positions must be exactly -1/0/+1 with no NaN (harness raises otherwise).
- Deterministic output; if you use randomness, fix the seed.
- No hard-coded dates or ranges; no external data; no reading data files from inside your functions.
- Do not modify `harness_public.py` - they score with an identical copy on hidden data (Task 1 hidden:
  Feb 2022 - Oct 2026; Task 2 hidden: Jul 2024 - Oct 2026, judged on risk-adjusted terms).
- Your file must run through the harness on a laptop in under ~10 minutes.

## Known data quirks (from the pack README)

- Task 2 universe is stocks liquid **in October 2026** - survivorship bias flatters long-only results;
  the report must discuss it. A per-day liquidity filter is still a good idea.
- Five stocks in their full dataset have >45% one-day drops that look like unadjusted corporate actions;
  only **SPLPETRO (2022-06-07)** is inside the training file. Code should not blow up on such jumps.
- Task 1: a few bars have fewer than 15 one-minute candles; Muhurat short sessions exist.
- Task 2 prices are adjusted for splits/bonuses but **not** for dividends.

## Submission checklist (one zip, `<your_name>.zip`)

- `task1.py`, `task2.py` (from the templates), `report.pdf` (max 3 pages), `failed_ideas.md` (3+ failed
  ideas with real numbers), survivorship-bias note, plus any helper .py files you import.
- Do **not** include the data folder or the harness in the zip.
- Deadline: 5 days from the assignment email (received 24 Oct 2026, 02:37 IST).
