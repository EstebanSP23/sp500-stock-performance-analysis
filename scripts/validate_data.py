"""
validate_data.py

PASS/FAIL data-integrity suite for the enriched S&P 500 fact table.

Inputs (expected in the same directory you run the script from):
    SnP_Fact_StockPrices_with_Drawdown252.csv  (output of build_drawdown_252d.py)
    data/raw/sp500_sectors.csv                  (sector enrichment table)

What it checks:
    1. Composite primary key (Date, Ticker) is unique.
    2. No NULLs in critical columns (Date, Ticker, Close).
    3. OHLC sanity: Low <= min(Open, Close) and High >= max(Open, Close).
    4. No negative prices or volumes.
    5. Sector mapping coverage: every Ticker in the fact has a sector row.
    6. Volatility sanity: Volatility Last 252d >= 0 where populated.
    7. Drawdown sanity: Drawdown in [-1, 0]; Max Drawdown Last 252d <= 0.

Every check prints a PASS / FAIL line with the failing row count.
Run from the repo root:
    python scripts/validate_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np

# ---------- CONFIG ----------
FACT_FILE = "SnP_Fact_StockPrices_with_Drawdown252.csv"
SECTOR_FILE = Path("data/raw/sp500_sectors.csv")
# ----------------------------


def _print_check(name: str, bad_rows: int) -> bool:
    status = "PASS" if bad_rows == 0 else "FAIL"
    print(f"  [{status}] {name:<55} bad_rows={bad_rows}")
    return bad_rows == 0


def main() -> int:
    print(f"Loading fact: {FACT_FILE}")
    if not Path(FACT_FILE).exists():
        print(f"  ERROR: {FACT_FILE} not found in {Path.cwd()}")
        print("  Run build_volatility_252d.py and build_drawdown_252d.py first.")
        return 2

    fact = pd.read_csv(FACT_FILE)
    fact["Date"] = pd.to_datetime(fact["Date"], errors="coerce")

    print(f"Loading sectors: {SECTOR_FILE}")
    if not SECTOR_FILE.exists():
        print(f"  ERROR: {SECTOR_FILE} not found.")
        return 2

    sectors = pd.read_csv(SECTOR_FILE)
    print(f"Fact rows: {len(fact):,}   Tickers: {fact['Ticker'].nunique():,}")
    print(f"Sectors rows: {len(sectors):,}")
    print()

    all_pass = True

    # ---------- (1) Composite primary key uniqueness ----------
    dup_count = int(fact.duplicated(subset=["Date", "Ticker"]).sum())
    all_pass &= _print_check("PK (Date, Ticker) unique", dup_count)

    # ---------- (2) NULLs in critical columns ----------
    null_date = int(fact["Date"].isna().sum())
    null_ticker = int(fact["Ticker"].isna().sum())
    null_close = int(fact["Close"].isna().sum())
    all_pass &= _print_check("No NULL Date", null_date)
    all_pass &= _print_check("No NULL Ticker", null_ticker)
    all_pass &= _print_check("No NULL Close", null_close)

    # ---------- (3) OHLC sanity ----------
    # Low must be <= min(Open, Close); High must be >= max(Open, Close).
    ohlc_low_bad = int(
        ((fact["Low"] > fact[["Open", "Close"]].min(axis=1)) & fact["Low"].notna()).sum()
    )
    ohlc_high_bad = int(
        ((fact["High"] < fact[["Open", "Close"]].max(axis=1)) & fact["High"].notna()).sum()
    )
    all_pass &= _print_check("Low <= min(Open, Close)", ohlc_low_bad)
    all_pass &= _print_check("High >= max(Open, Close)", ohlc_high_bad)

    # ---------- (4) No negative prices / volume ----------
    neg_price = int(((fact[["Open", "High", "Low", "Close"]] < 0).any(axis=1)).sum())
    neg_volume = int(((fact["Volume"] < 0) & fact["Volume"].notna()).sum())
    all_pass &= _print_check("No negative OHLC prices", neg_price)
    all_pass &= _print_check("No negative Volume", neg_volume)

    # ---------- (5) Sector mapping coverage ----------
    fact_tickers = set(fact["Ticker"].dropna().unique())
    sector_tickers = set(sectors["Ticker"].dropna().unique())
    orphan_tickers = fact_tickers - sector_tickers
    all_pass &= _print_check(
        "Every fact Ticker has a sector mapping", len(orphan_tickers)
    )
    if orphan_tickers:
        sample = sorted(orphan_tickers)[:10]
        print(f"      sample orphans: {sample}")

    # ---------- (6) Volatility sanity ----------
    if "Volatility Last 252d" in fact.columns:
        neg_vol = int(
            (
                (fact["Volatility Last 252d"] < 0)
                & fact["Volatility Last 252d"].notna()
            ).sum()
        )
        all_pass &= _print_check("Volatility Last 252d >= 0", neg_vol)
    else:
        print("  [SKIP] Volatility Last 252d column not found")

    # ---------- (7) Drawdown sanity ----------
    if "Drawdown" in fact.columns:
        dd_out_of_range = int(
            (
                ((fact["Drawdown"] > 1e-9) | (fact["Drawdown"] < -1 - 1e-9))
                & fact["Drawdown"].notna()
            ).sum()
        )
        all_pass &= _print_check("Drawdown in [-1, 0]", dd_out_of_range)
    else:
        print("  [SKIP] Drawdown column not found")

    if "Max Drawdown Last 252d" in fact.columns:
        maxdd_positive = int(
            (
                (fact["Max Drawdown Last 252d"] > 1e-9)
                & fact["Max Drawdown Last 252d"].notna()
            ).sum()
        )
        all_pass &= _print_check("Max Drawdown Last 252d <= 0", maxdd_positive)
    else:
        print("  [SKIP] Max Drawdown Last 252d column not found")

    # ---------- Summary ----------
    print()
    if all_pass:
        print("All checks PASS.")
        return 0
    else:
        print("One or more checks FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
