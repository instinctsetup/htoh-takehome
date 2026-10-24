#!/usr/bin/env python3
"""Run the H TO H public harness against a strategy file. Cross-platform.

Usage (from the repo root):
    python scripts/run.py task1 strategies/task1.py
    python scripts/run.py task2 strategies/task2.py

Expects the candidate pack unzipped at pack/ so that pack/harness_public.py
and pack/data/ exist. The pack is gitignored; do not commit it.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HARNESS = os.path.join(ROOT, 'pack', 'harness_public.py')


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('task1', 'task2'):
        sys.exit(__doc__)
    if not os.path.exists(HARNESS):
        sys.exit('pack/harness_public.py not found - unzip candidate_pack.zip into pack/ first')
    strategy = sys.argv[2]
    if not os.path.exists(strategy):
        sys.exit('strategy file not found: %s' % strategy)
    subprocess.check_call([sys.executable, HARNESS, sys.argv[1], os.path.abspath(strategy)])


if __name__ == '__main__':
    main()
