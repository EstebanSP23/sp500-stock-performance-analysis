# Interview Preparation — S&P 500 Risk & Return Analytics Project

## How to Introduce the Project (30–60 seconds)

I built an end-to-end Power BI analytics project analyzing S&P 500 stock performance from 2010 to 2026.  
The project focuses on returns, volatility, drawdowns, and risk-adjusted performance.

I used a hybrid architecture where heavy rolling statistics were precomputed in Python, while Power BI handled the semantic layer, DAX measures, and interactive reporting.

The dashboard is structured into three analytical layers:
- Performance overview
- Risk stress via drawdowns
- Sector-level allocation insights

This mirrors how real investment decisions are typically made.

---

## Why did you use Python instead of DAX for volatility and drawdowns?

Rolling window calculations over ~1.9M rows are computationally expensive in DAX and significantly slow down refreshes and visuals.

Python with pandas allows vectorized rolling operations that are much faster and more reliable. By precomputing volatility and drawdowns upstream, Power BI remains focused on aggregation, interactivity, and semantic modeling.

This separation aligns with production analytics best practices.

---

## Why did you separate KPI measures from Series measures?

Although the mathematical formulas are the same, the business questions are different.

- **KPI measures** answer: *“What is the value as of now?”*  
  They are evaluated once per entity and are fast and stable.
- **Series measures** answer: *“How did this evolve over time?”*  
  They must be recomputed per axis date.

Separating them:
- Prevents accidental misuse
- Improves performance predictability
- Makes analytical intent explicit

---

## How do you ensure financial correctness in your metrics?

Several guardrails were implemented:

- Enforced trading-day logic using a **Trading Day Index** instead of calendar days
- Required a full **252-trading-day window** before computing metrics
- Excluded near-zero volatility values to avoid ratio blow-ups
- Documented all assumptions, including a static **2% risk-free rate**

These safeguards prevent misleading early-period or edge-case results.

---

## Why is the drawdown page unfiltered by default?

The drawdown page is intentionally designed as a **stress-testing view**.

Leaving it unfiltered exposes tail risk across the full universe, including extreme losses that volatility and Sharpe ratios can hide.

Users can apply filters if desired, but the default view highlights worst-case behavior to promote risk awareness.

---

## Why did you publish this project to Power BI Service?

Publishing to Power BI Service completes the full analytics lifecycle.

It demonstrates:
- Deployment beyond local analysis
- Validation in a shared environment
- Understanding of how dashboards are actually consumed in organizations

This step shows production readiness, not just analysis skills.

---

## How would this scale in a real production environment?

The architecture already follows scalable patterns:
- Heavy computations upstream
- Clean semantic model
- Scenario-specific measures
- Clear page intent

In production, the local CSV could be replaced with a database or dataflow, and scheduled refreshes added without changing the report logic.

---

## What would you improve or extend next?

Potential extensions include:
- Portfolio-level analysis (correlations, diversification benefits)
- Macro or regime overlays to analyze sensitivity across market conditions

These would add depth without overloading the current dashboard.

---

## Key Strengths to Emphasize

- End-to-end ownership (ETL → modeling → deployment)
- Performance-aware design decisions
- Financial reasoning, not just visualization
- Clear separation between computation and semantics
- Executive-friendly storytelling with analytical depth
