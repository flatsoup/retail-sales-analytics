import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # -> /home/tjk/UpWork

DB = BASE_DIR / "database" / "quiz.db"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "defects_impact.png"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)
df = pd.read_sql("SELECT * FROM defects", conn)
conn.close()

df["DefectRate"] = df["Defects"] / df["Orders"]
df["ProfitMargin"] = df["Profit"] / df["Revenue"]

corr = df["DefectRate"].corr(df["ProfitMargin"])
print(f"Корреляция defect_rate <-> margin = {corr:.3f}")

m, b = np.polyfit(df["DefectRate"], df["ProfitMargin"], 1)
x_line = np.array([df["DefectRate"].min(), df["DefectRate"].max()])
y_line = m * x_line + b

plt.style.use("seaborn-v0_8-whitegrid")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

ax1.scatter(df["DefectRate"] * 100, df["ProfitMargin"] * 100,
            s=28, alpha=0.6, color="#C0392B", edgecolor="white", linewidth=0.4)
ax1.plot(x_line * 100, y_line * 100, color="#1F3864", linewidth=2.2,
         label=f"Trend (r = {corr:.2f})")
ax1.set_title("Impact of Defects on Profit Margin", fontweight="bold", fontsize=14)
ax1.set_xlabel("Defect Rate (%)")
ax1.set_ylabel("Profit Margin (%)")
ax1.legend(loc="upper right")
ax1.annotate("Higher defects → lower margin\n(near-perfect inverse relationship)",
             xy=(35, 40), fontsize=10, color="#555",
             bbox=dict(boxstyle="round,pad=0.4", fc="#FDF2E9", ec="#C0392B", alpha=0.9))

df_sorted = df.sort_values("Date")
ax2.plot(pd.to_datetime(df_sorted["Date"]), df_sorted["DefectRate"] * 100,
         color="#C0392B", linewidth=1.1, label="Defect Rate (%)")
ax2.plot(pd.to_datetime(df_sorted["Date"]), df_sorted["ProfitMargin"] * 100,
         color="#1F3864", linewidth=1.1, label="Profit Margin (%)")
ax2.set_title("Defect Rate vs Profit Margin Over 2023", fontweight="bold", fontsize=14)
ax2.set_xlabel("Date")
ax2.set_ylabel("Percent (%)")
ax2.legend(loc="center right")

plt.tight_layout()
plt.savefig(fname=OUTPUT_FILE, dpi=150, bbox_inches="tight")
print("Сохранено: defects_impact.png")
