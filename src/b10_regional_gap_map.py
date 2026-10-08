import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("results/figures", exist_ok=True)

# 1. Загрузка таблицы разрыва
df_gap = pd.read_csv("results/tables/gap_by_region.csv")

# 2. Сортировка регионов по медианному разрыву
df_sorted = df_gap.sort_values(by="gap_median_pp", ascending=True)

# 3. Визуализация регионального распределения медианного разрыва
fig, ax = plt.subplots(figsize=(10, 8))
y_pos = np.arange(len(df_sorted))

colors = ["#d73027" if g >= 2.0 else "#4575b4" for g in df_sorted["gap_median_pp"]]

bars = ax.barh(y_pos, df_sorted["gap_median_pp"], color=colors, alpha=0.85, edgecolor="black", linewidth=0.8)

# Порог гипотезы H1 (2 п.п.)
ax.axvline(2.0, color="darkred", linestyle="--", linewidth=1.5, label="Порог гипотезы H1 (+2 п.п.)")
ax.axvline(0.0, color="gray", linestyle="-", linewidth=0.8)

ax.set_yticks(y_pos)
ax.set_yticklabels(df_sorted["region"], fontsize=9)
ax.set_xlabel("Медианный разрыв охвата (процентные пункты, gap_median_pp)", fontsize=10)
ax.set_title("Рисунок 4. Медианный разрыв между восстановленной восприимчивостью\nи заявленным охватом по регионам Казахстана (gap_r)", fontsize=12, pad=15)
ax.grid(axis="x", linestyle="--", alpha=0.6)
ax.legend(loc="lower right")

# Добавление подписей значений
for bar in bars:
    width = bar.get_width()
    offset = 0.2 if width >= 0 else -0.8
    ax.text(width + offset, bar.get_y() + bar.get_height()/2, f"{width:.1f}", 
            va="center", ha="left" if width >= 0 else "right", fontsize=8)

plt.tight_layout()
plt.savefig("results/figures/figure_4_regional_gap_distribution.png", dpi=300)
plt.close()
print("Saved results/figures/figure_4_regional_gap_distribution.png")