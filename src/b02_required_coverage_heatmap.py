import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("results/figures", exist_ok=True)
os.makedirs("results/tables", exist_ok=True)

# Сетка параметров по разделу 6.4 протокола
r0_values = np.arange(8, 21, 1)          # R0 от 8 до 20 с шагом 1
eff_values = np.round(np.arange(0.90, 1.001, 0.01), 2)  # Эффективность E от 0.90 до 1.00

# Построение матрицы V*
v_star_matrix = np.zeros((len(r0_values), len(eff_values)))

for i, r0 in enumerate(r0_values):
    for j, e in enumerate(eff_values):
        v_star = (1.0 - 1.0 / r0) / e * 100.0
        v_star_matrix[i, j] = v_star

df_heatmap = pd.DataFrame(
    v_star_matrix,
    index=[f"R0 = {r}" for r in r0_values],
    columns=[f"{int(e*100)}%" for e in eff_values]
)

# Сохранение таблицы V* для отчета (проверочные точки R0=8..20 шаг 2, E=0.93 и E=0.97)
check_r0 = [8, 10, 12, 14, 16, 18, 20]
check_eff = [0.93, 0.97]
table_records = []
for r0 in check_r0:
    rec = {"R0": r0}
    for e in check_eff:
        rec[f"E_{int(e*100)}%"] = round((1.0 - 1.0 / r0) / e * 100.0, 1)
    table_records.append(rec)
pd.DataFrame(table_records).to_csv("results/tables/v_star_table.csv", index=False)
print("Saved results/tables/v_star_table.csv")

# Построение тепловой карты
plt.figure(figsize=(10, 8))
ax = sns.heatmap(
    df_heatmap,
    annot=True,
    fmt=".1f",
    cmap="YlOrRd",
    cbar_kws={'label': 'Требуемый охват V* (%)'}
)

plt.title("Требуемый охват вакцинацией новорожденных V* (%)", fontsize=14, pad=15)
plt.xlabel("Эффективность вакцины E", fontsize=12)
plt.ylabel("Базовое репродуктивное число R0", fontsize=12)

# Добавление изолинии заявленного охвата 96%
# Находим координаты изолинии контуром
X, Y = np.meshgrid(np.arange(len(eff_values)) + 0.5, np.arange(len(r0_values)) + 0.5)
CS = ax.contour(X, Y, v_star_matrix, levels=[96.0], colors='blue', linewidths=2.5, linestyles='--')
ax.clabel(CS, inline=True, fmt='V* = 96%%', fontsize=11)

plt.tight_layout()
plt.savefig("results/figures/figure_vstar_heatmap.png", dpi=300)
plt.close()
print("Saved results/figures/figure_vstar_heatmap.png")
print("Расчет требуемого охвата V* завершен!")