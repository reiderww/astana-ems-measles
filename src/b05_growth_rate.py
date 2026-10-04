import os
import numpy as np
import pandas as pd

os.makedirs("results/tables", exist_ok=True)

# Загрузка данных заболеваемости
df_inc = pd.read_csv("data/processed/incidence.csv")
df_nat = df_inc.groupby(["year", "month"])["total_corrected"].sum().reset_index()

# Интервал генерации кори: 14 дней ~ 14 / 30.4375 месяца
T_gen_months = 14.0 / 30.4375  # ~0.45995 месяца (0.46)

# Окна для оценки скорости роста (Таблица 17 протокола)
windows = [
    ("март-июнь 2023 (основное)", 2023, [3, 4, 5, 6]),
    ("март-май 2023", 2023, [3, 4, 5]),
    ("апрель-июль 2023", 2023, [4, 5, 6, 7]),
    ("август-ноябрь 2023", 2023, [8, 9, 10, 11]),
    ("август-декабрь 2023", 2023, [8, 9, 10, 11, 12])
]

records = []
for label, year, months in windows:
    sub = df_nat[(df_nat["year"] == year) & (df_nat["month"].isin(months))].sort_values("month")
    cases = sub["total_corrected"].values
    t = np.arange(len(cases))
    log_cases = np.log(cases)
    
    # Регрессия: slope r
    slope, intercept = np.polyfit(t, log_cases, 1)
    r = slope
    rT = r * T_gen_months
    
    R_a1 = 1.0 + rT
    R_inf = np.exp(rT)
    
    records.append({
        "Окно": label,
        "Число случаев": "; ".join(map(str, cases.astype(int))),
        "r, 1/месяц": round(r, 4),
        "R (a=1)": round(R_a1, 2),
        "R (большое a)": round(R_inf, 2)
    })

df_growth = pd.DataFrame(records)
df_growth.to_csv("results/tables/growth_rate_table.csv", index=False)
print("Saved results/tables/growth_rate_table.csv\n")

print("--- Таблица 17 протокола. Скорость роста и R по окнам ---")
print(df_growth.to_string(index=False))

# Сопоставление с шагом 4 при R0=12
r_main = records[0]["r, 1/месяц"]
R_main_a1 = records[0]["R (a=1)"]
R_main_inf = records[0]["R (большое a)"]
print(f"\nСопоставление: при R0=12 доля восприимчивых s = R/R0 составляет:")
print(f"s (a=1) = {R_main_a1 / 12 * 100:.1f}%, s (inf) = {R_main_inf / 12 * 100:.1f}%")