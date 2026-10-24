# htoh-takehome

Private workspace for the H TO H PARTNERS LLP Quant Research Intern take-home.

## Structure

- `strategies/` - strategy code (Task 1 and Task 2, built from the provided templates)
- `notebooks/` - exploration and analysis notebooks
- `data/` - assessment data, local only (gitignored, do not commit the candidate pack)
- `requirements.txt` - Python dependencies

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Unzip `candidate_pack.zip` into `data/` and read its README first.

## Notes

- Deadline: 5 days from receipt of the assignment email (received 24 Oct 2026, 02:37 IST).
- Per the assignment, the signal logic must be your own code: max 6 tunable parameters per strategy, no look-ahead, no hard-coded dates.
- Submission is one zip: the two strategy files, report.pdf (max 3 pages), failed_ideas.md, and the survivorship-bias note.
