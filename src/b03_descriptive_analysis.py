import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("results/figures", exist_ok=True)
os.makedirs("results/tables", exist_ok=True)

# Загрузка подготовленных данных
df_inc = pd.read_csv("data/processed/incidence.csv")
df_reg = pd.read_csv("data/processed/region_map.csv")

# 1. ТАБЛИЦА: cases_by_region_year.csv
df_reg_year = df_inc[df_inc["year"] >= 2023].groupby(["region", "year"])["total_corrected"].sum().reset_index()
df_pivot = df_reg_year.pivot(index="region", columns="year", values="total_corrected").reset_index()
df_pivot = df_pivot.merge(df_reg[["region_id", "name_sheet_3"]], left_on="region", right_on="region_id")
df_pivot.rename(columns={"name_sheet_3": "region_name"}, inplace=True)
df_pivot = df_pivot[["region_id", "region_name", 2023, 2024, 2025, 2026]]
df_pivot.to_csv("results/tables/cases_by_region_year.csv", index=False)
print("Saved results/tables/cases_by_region_year.csv")

# 2. РИСУНОК 1: Национальный помесячный ряд
df_nat = df_inc.groupby(["year", "month"])["total_corrected"].sum().reset_index()
df_nat["date"] = pd.to_datetime(df_nat["year"].astype(str) + "-" + df_nat["month"].astype(str) + "-01")
df_nat = df_nat.sort_values("date").reset_index(drop=True)

plt.figure(figsize=(12, 5))
plt.plot(df_nat["date"], df_nat["total_corrected"], marker="o", markersize=4, color="#1f77b4", linewidth=1.8, label="Всего случаев (total_corrected)")

# Выделение границ волн
plt.axvspan(pd.Timestamp("2023-02-01"), pd.Timestamp("2024-08-01"), color="orange", alpha=0.2, label="Волна 1 (фев 2023 - авг 2024)")
plt.axvspan(pd.Timestamp("2025-10-01"), pd.Timestamp("2026-07-01"), color="red", alpha=0.2, label="Волна 2 (окт 2025 - июль 2026)")

# Пики
plt.annotate("Пик: 10 016\n(дек 2023)", xy=(pd.Timestamp("2023-12-01"), 10016), xytext=(pd.Timestamp("2023-04-01"), 9000),
             arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=9)
plt.annotate("Пик: 2 048\n(янв 2026)", xy=(pd.Timestamp("2026-01-01"), 2048), xytext=(pd.Timestamp("2025-03-01"), 3500),
             arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=9)

plt.title("Рисунок 1. Помесячная динамика заболеваемости корью в Республике Казахстан (2019-2026 гг.)\n(значение января 2024 г. пересчитано по методике п. 4.2 протокола)", fontsize=11, pad=10)
plt.xlabel("Дата", fontsize=10)
plt.ylabel("Число зарегистрированных случаев", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(loc="upper right")
plt.tight_layout()
plt.savefig("results/figures/figure_1_national_incidence.png", dpi=300)
plt.close()
print("Saved results/figures/figure_1_national_incidence.png")

# 3. РИСУНОК 3: Возрастная структура по годам
df_age = df_inc.groupby("year")[["cases_0_14", "cases_15_17", "cases_18_plus", "total_corrected"]].sum().reset_index()
df_age["pct_0_14"] = df_age["cases_0_14"] / df_age["total_corrected"] * 100
df_age["pct_15_17"] = df_age["cases_15_17"] / df_age["total_corrected"] * 100
df_age["pct_18_plus"] = df_age["cases_18_plus"] / df_age["total_corrected"] * 100

years = df_age["year"].values
p1 = df_age["pct_0_14"].values
p2 = df_age["pct_15_17"].values
p3 = df_age["pct_18_plus"].values

plt.figure(figsize=(10, 6))
bar_width = 0.6
plt.bar(years, p1, width=bar_width, label="0-14 лет", color="#2ca02c")
plt.bar(years, p2, width=bar_width, bottom=p1, label="15-17 лет", color="#ff7f0e")
plt.bar(years, p3, width=bar_width, bottom=p1+p2, label="18 лет и старше", color="#1f77b4")

plt.title("Рисунок 3. Возрастная структура зарегистрированных случаев кори по годам (%)", fontsize=12, pad=15)
plt.xlabel("Год", fontsize=10)
plt.ylabel("Доля случаев (%)", fontsize=10)
plt.ylim(0, 100)
plt.xticks(years, [str(y) if y != 2026 else "2026*" for y in years])
plt.legend(loc="lower right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("results/figures/figure_3_age_structure.png", dpi=300)
plt.close()
print("Saved results/figures/figure_3_age_structure.png")
print("Анализ и визуализация успешно завершены!")