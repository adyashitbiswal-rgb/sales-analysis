"""Analyze a small sales dataset and save summary tables and charts."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(HERE / "sales.csv", parse_dates=["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

print("\nDataset preview:\n", df.head())
print("\nMissing values:\n", df.isna().sum())
print("\nRevenue by product:\n", df.groupby("product")["revenue"].sum().sort_values(ascending=False))
print("\nRevenue by region:\n", df.groupby("region")["revenue"].sum().sort_values(ascending=False))

monthly = df.groupby("month", as_index=False)["revenue"].sum()
monthly.to_csv(OUT / "monthly_revenue.csv", index=False)
product = df.groupby("product", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
product.to_csv(OUT / "product_revenue.csv", index=False)

monthly.plot(x="month", y="revenue", kind="line", marker="o", legend=False, title="Monthly Revenue")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUT / "monthly_revenue.png", dpi=150)
plt.close()

product.plot(x="product", y="revenue", kind="bar", legend=False, title="Revenue by Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUT / "product_revenue.png", dpi=150)
plt.close()

print(f"\nDone. Tables and charts saved to: {OUT}")
