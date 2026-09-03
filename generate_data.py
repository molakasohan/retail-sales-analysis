"""
generate_data.py
-----------------
Generates a synthetic retail sales dataset and saves it to data/sales_data.csv.

This simulates one year of daily transactions across multiple product
categories, regions, and sales channels — similar in shape to real-world
retail data a data analyst might be handed.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

# ---- Configuration ----
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"
PRODUCTS = {
    "Electronics": (150, 900),
    "Home & Kitchen": (20, 250),
    "Clothing": (10, 120),
    "Sports": (15, 200),
    "Books": (5, 40),
}
REGIONS = ["North", "South", "East", "West"]
CHANNELS = ["Online", "In-Store"]

def generate_sales_data(n_rows: int = 5000) -> pd.DataFrame:
    dates = pd.date_range(START_DATE, END_DATE, freq="D")

    rows = []
    for i in range(n_rows):
        date = np.random.choice(dates)
        category = np.random.choice(list(PRODUCTS.keys()), p=[0.25, 0.2, 0.25, 0.15, 0.15])
        low, high = PRODUCTS[category]
        unit_price = round(np.random.uniform(low, high), 2)
        quantity = np.random.randint(1, 6)

        # Add a mild seasonal boost in Nov/Dec (holiday shopping)
        month = pd.Timestamp(date).month
        if month in (11, 12):
            quantity += np.random.randint(0, 3)

        region = np.random.choice(REGIONS)
        channel = np.random.choice(CHANNELS, p=[0.65, 0.35])
        discount_pct = np.random.choice([0, 0, 0, 5, 10, 15, 20], p=[0.4, 0.15, 0.1, 0.15, 0.1, 0.05, 0.05])

        revenue = round(unit_price * quantity * (1 - discount_pct / 100), 2)

        rows.append({
            "order_id": 1000 + i,
            "date": pd.Timestamp(date).strftime("%Y-%m-%d"),
            "category": category,
            "unit_price": unit_price,
            "quantity": quantity,
            "discount_pct": discount_pct,
            "revenue": revenue,
            "region": region,
            "channel": channel,
        })

    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = generate_sales_data()
    df.to_csv("data/sales_data.csv", index=False)
    print(f"Generated {len(df)} rows -> data/sales_data.csv")
