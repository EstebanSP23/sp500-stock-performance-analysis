# Data Dictionary

This document describes the structure and meaning of the datasets used in the S&P 500 Risk & Return Analytics project, including raw inputs, transformed fact tables, and engineered analytical features.

---

## Raw Data (Wide Format – Source CSV)

Original dataset as downloaded from Kaggle.

- **Date**: Trading date
- **[Ticker]_Open**: Opening price for ticker
- **[Ticker]_High**: Daily high price
- **[Ticker]_Low**: Daily low price
- **[Ticker]_Close**: Closing price
- **[Ticker]_Volume**: Trading volume

**Notes:**
- Data is organized by metric groups (all closes, all highs, etc.)
- Multi-row headers required extensive transformation before analysis
- No adjusted close is provided (dividends and splits excluded)

---

## Dimension Table: Stocks & Sectors (`sp500_sectors.csv`)

Static enrichment table used for sector-based slicing and aggregation.

| Column        | Description              | Example                    |
|--------------|--------------------------|----------------------------|
| Ticker       | Stock symbol             | AAPL                       |
| Sector       | GICS Sector              | Information Technology     |
| Industry     | GICS Sub-Industry        | Technology Hardware        |
| Company Name | Full company name        | Apple Inc.                 |

**Notes:**
- Sector classifications are static (no historical reclassification)
- Used as a dimension table in the Power BI star schema

---

## Fact Table: `Fact_StockPrices` (Final Analytical Table)

Primary fact table used in the Power BI data model.

**Grain:**  
One row per **Trading Date + Ticker**

### Core Price & Volume Columns

| Column | Description |
|------|-------------|
| Date | Trading date |
| Ticker | Stock symbol |
| Open | Opening price |
| High | Daily high price |
| Low | Daily low price |
| Close | Closing price |
| Volume | Daily traded volume |

---

### Engineered Columns (Power BI – Calculated at Refresh)

These columns are computed once at model refresh to ensure performance and correct trading-day logic.

| Column | Description |
|------|-------------|
| Trading Day Index | Sequential index per ticker representing trading-day order (handles weekends, holidays, delistings) |
| Daily Return % | Close-to-close percentage return using the previous trading day |

---

### Precomputed Statistical Features (Python)

Computed outside Power BI using pandas/numpy for performance reasons and imported as static columns.

| Column | Description |
|------|-------------|
| Volatility 252d | Rolling 252-trading-day annualized standard deviation of daily returns |
| Drawdown | Percentage decline from most recent peak closing price |
| Max Drawdown Last 252d | Worst peak-to-trough loss over the trailing 252 trading days |

**Notes:**
- Rolling calculations use trading-day indexing (not calendar days)
- `min_periods = 30` guardrail applied for stability
- Population standard deviation (`ddof = 0`) used for financial consistency
- Closing prices used for drawdown calculations (NAV-style analysis)

---

## Measures (DAX – Semantic Layer)

Measures are not stored as columns and are evaluated dynamically based on filter context.

### Key Measures

| Measure | Description |
|-------|-------------|
| Cumulative Return (Selected Range) | Growth of $1 over the selected date range |
| Annualized Return (Trailing 252d) | Mean daily return × 252 |
| Sharpe Ratio (Trailing 252d) | Risk-adjusted return using 2% risk-free rate |
| Volatility (Trailing 252d) | Aggregated volatility measure |
| Max Drawdown (Trailing 252d) | As-of maximum capital loss |

**Design Note:**
- KPI measures and time-series measures are intentionally separated to reflect different analytical questions
- Measures rely on trading-day logic rather than calendar assumptions

---

## Assumptions & Constraints

- Risk-free rate fixed at **2% annually**
- No dividends or split adjustments
- Static sector classification
- Historical analysis only (no live refresh)

(See [Assumptions & Limitations](docs/assumptions_limitations.md) for full context.) 

