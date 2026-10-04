import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("results/figures", exist_ok=True)
os.makedirs("results/tables", exist_ok=True)

# 1. Загрузка данных заболеваемости
df_table = pd.read_csv("results/tables/cases_by_region_year.csv")

# Население регионов (на 1 января 2023 г., БНС АСПиР РК)
pop_dict = {
    1: 610_200,   # Абайская
    2: 788_000,   # Акмолинская
    3: 928_000,   # Актюбинская
    4: 1_500_000, # Алматинская
    5: 695_000,   # Атырауская
    6: 730_000,   # ВКО
    7: 1_215_000, # Жамбылская
    8: 698_000,   # Жетысуская
    9: 689_000,   # ЗКО
    10: 1_135_000,# Карагандинская
    11: 832_000,  # Костанайская
    12: 833_000,  # Кызылординская
    13: 766_000,  # Мангистауская
    14: 755_000,  # Павлодарская
    15: 534_000,  # СКО
    16: 2_118_000,# Туркестанская
    17: 221_000,  # Улытауская
    18: 2_162_000,# г. Алматы
    19: 1_354_000,# г. Астана
    20: 1_212_000 # г. Шымкент
}

df_table["population"] = df_table["region_id"].map(pop_dict)

# Расчет показателей на 100 000 населения
for y in ["2023", "2024", "2025", "2026"]:
    df_table[f"rate_{y}"] = (df_table[y] / df_table["population"]) * 100_000

df_table.to_csv("results/tables/incidence_per_100k_by_region.csv", index=False)
print("Saved results/tables/incidence_per_100k_by_region.csv")

# 2. Построение Рисунка 2: Заболеваемость на 100 000 населения в 2023 и 2024 гг. (основные годы волны 1)
df_sorted = df_table.sort_values(by="rate_2023", ascending=True)

fig, ax = plt.subplots(figsize=(10, 8))
y_pos = np.arange(len(df_sorted))
bar_height = 0.38

rects1 = ax.barh(y_pos + bar_height/2, df_sorted["rate_2023"], bar_height, label="2023 г.", color="#1f77b4")
rects2 = ax.barh(y_pos - bar_height/2, df_sorted["rate_2024"], bar_height, label="2024 г.", color="#ff7f0e")

ax.set_yticks(y_pos)
ax.set_yticklabels(df_sorted["region_name"], fontsize=9)
ax.set_xlabel("Число зарегистрированных случаев на 100 000 населения", fontsize=10)
ax.set_title("Рисунок 2. Региональная заболеваемость корью на 100 000 населения (2023-2024 гг.)", fontsize=12, pad=12)
ax.grid(axis="x", linestyle="--", alpha=0.6)
ax.legend(loc="lower right")

plt.tight_layout()
plt.savefig("results/figures/figure_2_regional_incidence.png", dpi=300)
plt.close()
print("Saved results/figures/figure_2_regional_incidence.png")