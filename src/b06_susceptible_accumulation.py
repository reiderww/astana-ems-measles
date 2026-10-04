import os
import pandas as pd
import numpy as np

os.makedirs("results/tables", exist_ok=True)

# Параметры по разделу 10 протокола
B = 400_000          # рождаемость в год
v = 0.96             # охват
E = 0.97             # эффективность 2 доз
N = 20_000_000       # численность населения
R0 = 12
S_crit = N / R0      # 1 666 667

annual_replenishment = B * (1.0 - v * E)  # 27 520 чел./год

C1 = 57_587
C2 = 8_691

# s0 берем из таблицы final_size_national.csv для R0=12
df_fs = pd.read_csv("results/tables/final_size_national.csv")
df_fs_r12 = df_fs[df_fs["R0"] == R0].set_index("rho")

records_t19 = []
records_forecast = []

for rho in [0.3, 0.5, 0.7, 1.0]:
    s0 = df_fs_r12.loc[rho, "s0"]
    A1 = C1 / (rho * N)
    S_end1 = (s0 - A1) * N
    deficit = S_crit - S_end1
    T_recover = (C1 / rho) / annual_replenishment
    T_crit = deficit / annual_replenishment
    
    records_t19.append({
        "rho": rho,
        "s0_%": round(s0 * 100, 2),
        "Заразившихся (волна 1)": int(round(C1 / rho)),
        "S_end": int(round(S_end1)),
        "S_crit - S_end": int(round(deficit)),
        "T_вост, лет": round(T_recover, 1),
        "T_крит, лет": round(T_crit, 1)
    })
    
    # Расчет к волне 2 и прогноз (п. 10.3)
    S_start2 = S_end1 + annual_replenishment * (14.0 / 12.0)
    S_end2 = S_start2 - (C2 / rho)
    T2_years = (S_crit - S_end2) / annual_replenishment
    
    records_forecast.append({
        "rho": rho,
        "S_start2": int(round(S_start2)),
        "S_end2": int(round(S_end2)),
        "T2_years": round(T2_years, 2),
        "Критический_год": 2026.58 + T2_years
    })

df_t19 = pd.DataFrame(records_t19)
df_t19.to_csv("results/tables/susceptible_accumulation_table19.csv", index=False)
print("Saved results/tables/susceptible_accumulation_table19.csv\n")

print("--- Таблица 19 протокола. Накопление восприимчивых после волны 1 (R0=12) ---")
print(df_t19.to_string(index=False))

df_fc = pd.DataFrame(records_forecast)
df_fc.to_csv("results/tables/forecast_2027.csv", index=False)
print("\n--- Прогноз сроков достижения S_crit от июля 2026 года ---")
print(df_fc.to_string(index=False))