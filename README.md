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
- **Limitations:** 
  - No Adjusted Close (returns exclude dividends/splits—common approximation for price-based analysis).
  - Static snapshot (as of download date).
  
(See `/docs/` for data dictionary and full assumptions.)

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
