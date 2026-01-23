# Assumptions & Limitations

- Returns are calculated using **Close prices only**.  
  Dividends and stock splits are not included (no Adjusted Close).  
  This is a common approximation for price-based analysis; production implementations would use adjusted prices.

- **Rolling metrics (Volatility and Max Drawdown)** are precomputed in Python and imported as static columns.  
  Values remain fixed between refreshes and do not dynamically recompute for arbitrary rolling windows.

- **Risk-free rate is fixed at 2% annually**, approximating long-term 10Y Treasury averages over the analysis period.  
  The rate is documented and intentionally static; a dynamic rate could be added in production.

- Drawdowns are calculated using **closing prices**, not intraday lows.  
  This reflects end-of-day portfolio valuation and avoids overstating risk due to intraday volatility.  
  Intraday drawdowns are more relevant for execution and stop-loss analysis and are intentionally excluded.

- Sector classifications are **static**, based on January 2026 GICS mappings.  
  Historical sector reclassifications and index additions/removals are not reflected.

- Data cutoff: **2026-01-05**, based on the dataset download date.  
  The model does not auto-update without re-running preprocessing scripts and refreshing the Power BI dataset.

These assumptions were chosen to balance analytical correctness, performance, and interpretability, and are explicitly documented to avoid misleading conclusions.
