"""
data_pipeline.py — pandas workflow with auto-tables
needs: pip install pandas python_vibe
"""

import python_vibe
python_vibe.set_theme("masala")  # masala mode for data work obv
python_vibe.enable()

import time

try:
    import pandas as pd
    import numpy as np
except ImportError:
    python_vibe.error("need pandas + numpy: pip install pandas numpy")
    raise SystemExit(1)


python_vibe.log("loading dataset...")
time.sleep(0.3)  # fake io

# generate fake sales data
rng = np.random.default_rng(42)
cities = ["bhopal", "indore", "pune", "mumbai", "delhi", "bangalore"]
n = 120

raw_df = pd.DataFrame({
    "city": rng.choice(cities, n),
    "revenue": rng.integers(5000, 80000, n),
    "units": rng.integers(10, 500, n),
    "margin": rng.uniform(0.05, 0.45, n).round(3),
    "returned": rng.choice([True, False], n, p=[0.1, 0.9]),
})

print("raw data (first 10 rows):")
print(raw_df.head(10))

# --- pipeline steps
print("\nrunning pipeline...")


@python_vibe.vibe
def clean_data(df):
    time.sleep(0.2)
    df = df[~df["returned"]].copy()
    df["revenue_per_unit"] = (df["revenue"] / df["units"]).round(2)
    return df


@python_vibe.vibe
def aggregate(df):
    time.sleep(0.15)
    return df.groupby("city").agg(
        total_revenue=("revenue", "sum"),
        avg_margin=("margin", "mean"),
        total_units=("units", "sum"),
        orders=("revenue", "count"),
    ).reset_index().sort_values("total_revenue", ascending=False)


@python_vibe.vibe
def flag_top(df):
    time.sleep(0.1)
    median_rev = df["total_revenue"].median()
    df["is_top"] = df["total_revenue"] > median_rev
    return df


cleaned = clean_data(raw_df)
agg = aggregate(cleaned)
final = flag_top(agg)

print("\ncity-wise sales summary:")
print(final)

python_vibe.log(f"processed {len(raw_df)} rows → {len(cleaned)} after cleaning")
python_vibe.success(f"pipeline done! top city: {final.iloc[0]['city']} ☕")

