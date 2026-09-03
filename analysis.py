"""
analysis.py
------------
Loads data/sales_data.csv and produces:
  - Key performance indicators (printed + saved to outputs/summary.txt)
  - Revenue trend over time (monthly)
  - Revenue by product category
  - Revenue by region and channel
  - Top 5 categories by average order value

Charts are saved as PNG files in outputs/.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

DATA_PATH = "data/sales_data.csv"
OUT_DIR = "outputs"


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    import os
    if not os.path.exists(path) and os.path.exists("sales_data.csv"):
        path = "sales_data.csv"
    df = pd.read_csv(path, parse_dates=["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    return {
        "total_revenue": round(df["revenue"].sum(), 2),
        "total_orders": df["order_id"].nunique(),
        "avg_order_value": round(df["revenue"].mean(), 2),
        "total_units_sold": int(df["quantity"].sum()),
        "top_category": df.groupby("category")["revenue"].sum().idxmax(),
        "top_region": df.groupby("region")["revenue"].sum().idxmax(),
        "online_share_pct": round(
            df.loc[df["channel"] == "Online", "revenue"].sum() / df["revenue"].sum() * 100, 1
        ),
    }


def plot_monthly_revenue(df: pd.DataFrame):
    monthly = df.groupby("month")["revenue"].sum().reset_index()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly, x="month", y="revenue", marker="o")
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Trend (2025)")
    plt.ylabel("Revenue ($)")
    plt.xlabel("Month")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/monthly_revenue_trend.png", dpi=150)
    plt.close()


def plot_revenue_by_category(df: pd.DataFrame):
    cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=cat_rev, x="revenue", y="category", hue="category", palette="viridis", legend=False)
    plt.title("Total Revenue by Category")
    plt.xlabel("Revenue ($)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/revenue_by_category.png", dpi=150)
    plt.close()


def plot_region_channel(df: pd.DataFrame):
    pivot = df.pivot_table(index="region", columns="channel", values="revenue", aggfunc="sum")
    pivot.plot(kind="bar", stacked=True, figsize=(8, 5), colormap="tab20")
    plt.title("Revenue by Region and Channel")
    plt.ylabel("Revenue ($)")
    plt.xlabel("Region")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/revenue_by_region_channel.png", dpi=150)
    plt.close()


def main():
    df = load_data()
    kpis = compute_kpis(df)

    print("=== Retail Sales Analysis Summary ===")
    for k, v in kpis.items():
        print(f"{k}: {v}")

    with open(f"{OUT_DIR}/summary.txt", "w") as f:
        f.write("Retail Sales Analysis Summary\n")
        f.write("=" * 32 + "\n")
        for k, v in kpis.items():
            f.write(f"{k}: {v}\n")

    plot_monthly_revenue(df)
    plot_revenue_by_category(df)
    plot_region_channel(df)

    print(f"\nCharts and summary saved to {OUT_DIR}/")


if __name__ == "__main__":
    main()
