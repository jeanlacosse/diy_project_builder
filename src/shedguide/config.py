"""Project configuration. Skeleton values only; no secrets belong here."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
TABLES_DIR = DATA_DIR / "tables"
STUB_TABLE = TABLES_DIR / "stub_joists.csv"
STOCK_CSV = DATA_DIR / "stock.csv"
EVALS_DIR = ROOT / "evals"
CASES_DIR = EVALS_DIR / "cases"
RESULTS_DIR = EVALS_DIR / "results"
CANNED_CASES = CASES_DIR / "canned.jsonl"

MODEL_ID = "fake-model"
PROMPT_VERSION = "skeleton-0"

DISCLAIMER = (
    "Planning aid only. This is not an engineered design or a code-compliance check. "
    "Verify all sizes with the reference tables and your local building authority."
)
STUB_MARKER = "*** STUB DATA: fake values, not from any reference. Do not build from this. ***"
