import pandas as pd
import numpy as np

# ---------- CONFIG ----------
INPUT_FILE = "SnP_Fact_StockPrices_with_Vol252.csv"
OUTPUT_FILE = "SnP_Fact_StockPrices_with_Drawdown252.csv"

WINDOW = 252
# ----------------------------

print("Loading CSV...")
df = pd.read_csv(INPUT_FILE)

print("Parsing dates and sorting...")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.sort_values(["Ticker", "Trading Day Index"])

print("Computing running peak price...")
df["Running Peak Close"] = (
    df.groupby("Ticker")["Close"]
      .cummax()
)

print("Computing daily drawdown...")
df["Drawdown"] = (
    df["Close"] / df["Running Peak Close"] - 1
)

print("Computing rolling 252-day max drawdown...")
df["Max Drawdown Last 252d"] = (
    df.groupby("Ticker")["Drawdown"]
      .rolling(window=WINDOW, min_periods=30)
      .min()
      .reset_index(level=0, drop=True)
)

print("Saving output CSV...")
df.to_csv(OUTPUT_FILE, index=False)

print("Done.")
print(f"Output saved as: {OUTPUT_FILE}")
