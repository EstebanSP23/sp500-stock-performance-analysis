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
  Daily Open, High, Close, Low, Volume data for ~500 stocks, 2010-01-04 to 2026-01-05 (wide format).

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
- Validation → Manually checked group sizes (503 rows per metric) and specific ticker/date combinations (e.g., AAPL on 19/01/2010, AMZN on 14/01/2010, ABT on 22/01/2010) — each returned exactly one row with all five metrics (Open, High, Low, Close, Volume) after final pivot.

**Final Fact Table (Fact_StockPrices)**
- Grain: One row per Date + Ticker
- Columns: Date, Ticker, Open, High, Low, Close, Volume
- Row count: 1,903,495 (after pivot; ~6% missing rows due to delistings/gaps — normal for historical data)
- Transformation performed entirely in Power Query (ETL layer) before loading to the model.

This process mirrors real-world ETL for financial datasets — handling messy exports, verifying integrity, and documenting decisions.

**Major Power Query Steps (Chronological)**
1. Imported raw CSV without promoting headers  
2. Transposed table to make metric groups vertical  
3. Promoted dates as column headers  
4. Filled down PriceType and Ticker labels  
5. Removed junk rows/columns (e.g., empty "Date" column)  
6. Unpivoted date columns to long format for verification  
7. Pivoted PriceType back to wide format (Open, High, Low, Close, Volume)  
8. Verified grain with spot-checks on specific tickers/dates

Current state: Fact table loaded in wide format (1.9M rows), ready for star schema and DAX measures.

## Methodology & Tools
- **ETL & Cleaning:** Power Query (unpivot wide → long format, date handling)
- **Data Modeling:** Star schema in Power BI
- **Calculations:** Reusable DAX measures (e.g., daily/total returns, annualized volatility, Sharpe ratio)
- **Visualization:** Interactive dashboard for exploration and simple portfolio simulation

## Data Model & Relationships (Current State)
- Fact table: Fact_StockPrices (wide format, 1,903,495 rows)
  - Grain: One row per trading date + ticker
  - Columns: Date, Ticker, Open, High, Low, Close, Volume
- Next: Create Date dimension table, relate Stock dimension from sector enrichment, and establish star schema relationships.
- Goal: Enable time-intelligence functions (e.g., year-over-year returns) and sector-based slicing.

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
