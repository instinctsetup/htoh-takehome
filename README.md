# htoh-takehome

Private workspace for the H TO H PARTNERS LLP Quant Research Intern take-home (assignment email
received 24 Oct 2026, 02:37 IST; deadline 5 days from receipt).

## Provenance

This project is **AI-assisted**: strategy code, experiments and docs in this repo were produced by an AI
assistant for private review and learning, and are **not** represented as the candidate's own unaided work.
The assignment's terms say "the signal logic must be your own code" and include a live walkthrough where the
candidate changes their own code on the spot. Nothing here has been submitted. Reviewing or understanding
this material does not by itself satisfy that authorship requirement; any eventual submission is the
candidate's own decision and responsibility.

## Structure

- `docs/harness-explained.md` - how the scoring harness and both task interfaces work, in plain English
- `strategies/` - reference strategy implementations (AI-assisted, see Provenance)
- `experiments/` - measured experiment results (parameter sensitivity, robustness runs)
- `scripts/` - `run.py` (run the harness on a strategy file), `data_sanity.py` (read-only data QA)
- `notebooks/` - exploration space
- `pack/` - the candidate pack unzipped (harness + proprietary data), local only, gitignored
- `requirements.txt` - Python dependencies

## Setup

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Unzip `candidate_pack.zip` into `pack/` (keeping its structure: `pack/harness_public.py`, `pack/data/`, ...).
Read `pack/README.md` first, then `docs/harness-explained.md`.

```bash
python scripts/run.py task1 strategies/task1.py
python scripts/run.py task2 strategies/task2.py
python scripts/data_sanity.py
```

## Assignment terms that govern any submission

- "Any library is fine, but the signal logic must be your own code."
- Max 6 tunable parameters per strategy; no look-ahead; no hard-coded dates; deterministic; runs in <10 min.
- Hidden-data holdout counts most (Task 1: Feb 2022 - Oct 2026; Task 2: Jul 2024 - Oct 2026).
- Submission zip: `task1.py`, `task2.py`, `report.pdf` (max 3 pages), `failed_ideas.md`, survivorship-bias note.
- Shortlisted candidates do a 45-minute live walkthrough, changing their own code on the spot.
