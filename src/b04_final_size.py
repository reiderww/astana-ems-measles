import os
import numpy as np
import pandas as pd
from scipy.optimize import brentq

os.makedirs("results/tables", exist_ok=True)

# 1. Загрузка данных по первой волне (2023-02 по 2024-08)
df_inc = pd.read_csv("data/processed/incidence.csv")
mask_w1 = ((df_inc["year"] == 2023) & (df_inc["month"] >= 2)) | ((df_inc["year"] == 2024) & (df_inc["month"] <= 8))
df_w1 = df_inc[mask_w1]

C_nat = df_w1["total_corrected"].sum()  # 57 587
N_nat = 20_000_000                     # Базовый национальный ориентир

r0_grid = [8, 10, 12, 14, 16, 18, 20]
rho_grid = [0.3, 0.5, 0.7, 1.0]

def solve_s0(r0, A):
    # Уравнение: f(s0) = ln(s0 / (s0 - A)) - R0 * A = 0
    # Область поиска: s0 > A. Нижняя граница A + 1e-12, верхняя 1.0
    f = lambda s0: np.log(s0 / (s0 - A)) - r0 * A
    low = A * (1.0 + 1e-8)
    high = 1.0
    try:
        return brentq(f, low, high)
    except:
        return np.nan

# Национальный расчет
records_nat = []
for r0 in r0_grid:
    for rho in rho_grid:
        A = C_nat / (rho * N_nat)
        s0 = solve_s0(r0, A)
        x = A / s0  # Доля заразившихся среди восприимчивых
        records_nat.append({
            "R0": r0,
            "rho": rho,
            "A": A,
            "s0": s0,
            "s0_pct": s0 * 100.0,
            "one_over_R0": 1.0 / r0,
            "x": x
        })

df_final_size_nat = pd.DataFrame(records_nat)
df_final_size_nat.to_csv("results/tables/final_size_national.csv", index=False)
print("Saved results/tables/final_size_national.csv")

# Печать контрольной сводки по Таблице 15 протокола
pivot_table_15 = df_final_size_nat.pivot(index="R0", columns="rho", values="s0_pct")
print("\n--- Таблица 15 протокола. Восстановленная доля s0 (%) по стране ---")
print(pivot_table_15.round(2))

# Анализ чувствительности: исходное некорректированное значение января 2024 г. (п. 8.6 протокола)
C_nat_raw = df_w1["total_as_received"].sum() # 76 224
A_sens = C_nat_raw / (0.3 * N_nat)
s0_sens = solve_s0(12, A_sens)
print(f"\nАнализ чувствительности (R0=12, rho=0.3):")
print(f"По total_corrected (C={int(C_nat)}): s0 = {solve_s0(12, C_nat/(0.3*N_nat))*100:.2f}%")
print(f"По total_as_received (C={int(C_nat_raw)}): s0 = {s0_sens*100:.2f}%\n")