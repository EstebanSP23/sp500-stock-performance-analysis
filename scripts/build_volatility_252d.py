import pandas as pd
import numpy as np

# ---------- CONFIG ----------
INPUT_FILE = "SnP_Fact_StockPrices_transformed.csv"
OUTPUT_FILE = "SnP_Fact_StockPrices_with_Vol252.csv"

WINDOW = 252
MIN_PERIODS = 30
# ----------------------------

print("Loading CSV...")
df = pd.read_csv(INPUT_FILE)

# Ensure correct dtypes
print("Parsing dates and sorting...")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

df = df.sort_values(["Ticker", "Trading Day Index"])

# Make sure Daily Return % is numeric
df["Daily Return %"] = pd.to_numeric(df["Daily Return %"], errors="coerce")

print("Computing rolling 252-day volatility...")

df["Volatility Last 252d"] = (
    df
    .groupby("Ticker")["Daily Return %"]
    .rolling(window=WINDOW, min_periods=MIN_PERIODS)
    .std(ddof=0)              # population std (matches STDEVX.P)
    .reset_index(level=0, drop=True)
    * np.sqrt(252)
)

print("Saving output CSV...")
df.to_csv(OUTPUT_FILE, index=False)

print("Done.")
print(f"Output saved as: {OUTPUT_FILE}")
