# S&P 500 Stock Performance Analysis (2010–2026)

**Interactive Power BI Dashboard for Retail Investor Insights**

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

## Business Context
Retail investors often struggle with overwhelming market data when building portfolios. This project analyzes historical S&P 500 stock performance to provide actionable insights on returns, risk, and diversification.

**Business Problem:** How can we help everyday investors identify strong-performing stocks and sectors while managing risk using historical data?

**Key Questions Answered:**
- Which stocks/sectors delivered the highest risk-adjusted returns?
- How did performance vary during major events (e.g., 2020 COVID crash, 2022 inflation, recent 2025-2026 rallies)?
- What correlations exist to support better diversification?
- Metrics like Sharpe ratio >1.5 for recommendations.

## Data Sources & Limitations
- **Primary Source:** [Kaggle - S&P 500 Daily Update Dataset](https://www.kaggle.com/datasets/yash16jr/s-and-p500-daily-update-dataset)  
  Daily OHLCV data for ~500 stocks, 2010-01-04 to 2026-01-05 (wide format).
- **Enrichment:** Sector mapping from [Wikipedia List of S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) (GICS classifications, current as of Jan 6, 2026). Local copy: [sp500_sectors.csv](data/raw/sp500_sectors.csv).
- **Limitations:** 
  - No Adjusted Close (returns exclude dividends/splits—common approximation for price-based analysis).
  - Static sector assignments (no point-in-time changes for historical additions/removals)
  - Static snapshot (as of download date).
  
(See `/docs/` for data dictionary and full assumptions.)

## Data Preparation & ETL Process

The raw dataset was a wide-format CSV (~150 MB) with ~2516 columns containing daily OHLCV data for ~503 S&P 500 stocks from 2010-01-04 to 2026-01-05. The data was grouped by metric (all Closes together, then all Highs, etc.) with multi-row headers, requiring significant transformation.

**Key Challenges & Solutions**
- Multi-row headers & grouped columns → Used transpose to flip the structure, making metric groups vertical and easier to handle.
- Missing or inconsistent metadata → Filled down PriceType ("Close", "High", "Low", "Open", "Volume") and Ticker labels using Power Query Fill Down.
- Performance & crashes with large wide data → Avoided manual column selection; used transpose + targeted filtering and verification steps.
- Validation → Manually checked group sizes (503 rows per metric) and specific ticker/date combinations (e.g., AAPL on 19/01/2010, AMZN on 14/01/2010, ABT on 22/01/2010) — each returned exactly 5 metrics in one row after pivot.

**Final Fact Table (Fact_StockPrices)**
- Grain: One row per Date + Ticker
- Columns: Date, Ticker, Open, High, Low, Close, Volume
- Row count: 1,903,495
- Transformation steps performed in Power Query (ETL layer) before loading to the model.

This process mirrors real-world ETL for financial datasets — handling messy exports, verifying integrity, and documenting decisions.

Major Power Query Steps:
- Imported raw CSV without promoting headers
- Transposed table to make metric groups vertical
- Promoted dates as column headers
- Filled down PriceType and Ticker labels
- Removed junk rows/columns
- Unpivoted date columns to long format
- Pivoted PriceType back to wide format (Open, High, Low, Close, Volume)

## Methodology & Tools
- **ETL & Cleaning:** Power Query (unpivot wide → long format, date handling)
- **Data Modeling:** Star schema in Power BI
- **Calculations:** Reusable DAX measures (e.g., daily/total returns, annualized volatility, Sharpe ratio)
- **Visualization:** Interactive dashboard for exploration and simple portfolio simulation

## Key Insights & Recommendations
*(To be updated post-analysis – e.g., "Technology sector led with XX% cumulative returns since 2010, driven by... Recommend overweight for growth-oriented investors.")*

## Dashboard Overview
*(Screenshots and .pbix coming soon – interactive views for stock/sector comparison, time-period slicing, and risk metrics)*

![Dashboard Preview](powerbi/screenshots/overview.png) <!-- Replace with actual once uploaded -->

[Download Power BI File](powerbi/SP500_Dashboard.pbix) <!-- Add once .pbix committed -->

## Next Steps & Potential Enhancements
- Enrich with sector/industry metadata for segmented analysis
- Production idea: Integrate live API (e.g., Yahoo Finance) for real-time updates
- Risks: Market data volatility; past performance ≠ future results (note for ethical recommendations)

---
*Project by [EstebanSP23](https://github.com/EstebanSP23) – Building a job-ready data analytics portfolio*
