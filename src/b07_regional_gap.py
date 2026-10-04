import os
import numpy as np
import pandas as pd
from scipy.optimize import brentq

os.makedirs("results/tables", exist_ok=True)

# 1. Загрузка данных
df_inc = pd.read_csv("data/processed/incidence.csv")
df_cov = pd.read_csv("data/processed/coverage.csv")
df_reg = pd.read_csv("data/processed/region_map.csv")

# Население регионов на начало 2023 года (ориентиры БНС АСПиР РК, сумма 19.8-20.0 млн)
# Пропорциональное распределение N_total = 20_000_000 по официальным долям
pop_distribution = {
    1: 610_200,   # Абай
    2: 788_000,   # Акмолинская
    3: 928_000,   # Актюбинская
    4: 1_500_000, # Алматинская
    5: 695_000,   # Атырауская
    6: 730_000,   # ВКО
    7: 1_215_000, # Жамбылская
    8: 698_000,   # Жетысу
    9: 689_000,   # ЗКО
    10: 1_135_000,# Карагандинская
    11: 832_000,  # Костанайская
    12: 833_000,  # Кызылординская
    13: 766_000,  # Мангистауская
    14: 755_000,  # Павлодарская
    15: 534_000,  # СКО
    16: 2_118_000,# Туркестанская
    17: 221_000,  # Улытау
    18: 2_162_000,# г. Алматы
    19: 1_354_000,# г. Астана
    20: 1_212_000 # г. Шымкент
}

# 2. Сумма случаев волны 1 по регионам (февраль 2023 - август 2024)
mask_w1 = ((df_inc["year"] == 2023) & (df_inc["month"] >= 2)) | ((df_inc["year"] == 2024) & (df_inc["month"] <= 8))
df_w1 = df_inc[mask_w1].groupby("region")["total_corrected"].sum().reset_index()
df_w1.rename(columns={"total_corrected": "C_w1"}, inplace=True)

# 3. Расчет заявленного охвата v_r (п. 11.1)
# Сумма за каждый год, cap на 100%
cov_annual = df_cov.groupby(["region", "year"])["dose1_pct_of_annual_plan"].sum().reset_index()
cov_annual["capped_dose1"] = cov_annual["dose1_pct_of_annual_plan"].apply(lambda x: min(x, 100.0) / 100.0)

v_declared = {}
for r_id in range(1, 21):
    sub = cov_annual[cov_annual["region"] == r_id]
    if r_id in [1, 8, 17]: # новые области
        val = sub[sub["year"] == 2023]["capped_dose1"].values[0]
    else:
        val = sub[sub["year"].isin([2019, 2020, 2021, 2022])]["capped_dose1"].mean()
    v_declared[r_id] = val

# Функция решения уравнения конечного размера
def solve_s0(r0, A):
    f = lambda s0: np.log(s0 / (s0 - A)) - r0 * A
    try:
        return brentq(f, A * (1.0 + 1e-8), 1.0)
    except:
        return np.nan

# 4. Расчет разрыва по сетке 28 сочетаний
r0_grid = [8, 10, 12, 14, 16, 18, 20]
rho_grid = [0.3, 0.5, 0.7, 1.0]

records_all = []
for r_id in range(1, 21):
    c_val = df_w1[df_w1["region"] == r_id]["C_w1"].values[0]
    n_val = pop_distribution[r_id]
    v_val = v_declared[r_id]
    
    gaps_reg = []
    for r0 in r0_grid:
        for rho in rho_grid:
            A = c_val / (rho * n_val)
            s0 = solve_s0(r0, A)
            gap = (s0 - (1.0 - v_val)) * 100.0  # в процентных пунктах
            gaps_reg.append(gap)
            records_all.append({
                "region": r_id, "R0": r0, "rho": rho,
                "s0": s0, "v": v_val, "gap_pp": gap
            })

df_all = pd.DataFrame(records_all)
df_all.to_csv("results/tables/final_size_regional.csv", index=False)
print("Saved results/tables/final_size_regional.csv")

# 5. Сводная таблица: gap_by_region.csv (Раздел 11.2)
summary_records = []
for r_id in range(1, 21):
    sub = df_all[df_all["region"] == r_id]
    v_val = v_declared[r_id]
    g_min = sub["gap_pp"].min()
    g_max = sub["gap_pp"].max()
    g_median = sub["gap_pp"].median()
    n_at_least_2 = (sub["gap_pp"] >= 2.0).sum()
    contains_zero = (g_min <= 0.0 <= g_max)
    
    r_name = df_reg[df_reg["region_id"] == r_id]["name_sheet_3"].values[0]
    
    summary_records.append({
        "region_id": r_id,
        "region": r_name,
        "declared_coverage_%": round(v_val * 100.0, 1),
        "gap_min_pp": round(g_min, 2),
        "gap_max_pp": round(g_max, 2),
        "gap_median_pp": round(g_median, 2),
        "n_comb_ge_2pp": n_at_least_2,
        "contains_zero": contains_zero
    })

df_summary = pd.DataFrame(summary_records)
df_summary.to_csv("results/tables/gap_by_region.csv", index=False)
print("Saved results/tables/gap_by_region.csv\n")

print("--- Сводка регионального разрыва (первые 5 регионов и города) ---")
print(df_summary[["region", "declared_coverage_%", "gap_min_pp", "gap_max_pp", "n_comb_ge_2pp"]].to_string(index=False))

# Проверка гипотезы H2 (коэффициент вариации)
cv_declared = df_summary["declared_coverage_%"].std() / df_summary["declared_coverage_%"].mean()
cv_gap = df_summary["gap_median_pp"].std() / abs(df_summary["gap_median_pp"].mean())
print(f"\nКоэффициент вариации: заявленный охват CV = {cv_declared:.3f}, разрыв CV = {cv_gap:.3f}")
if cv_gap > cv_declared:
    print("Гипотеза H2 подтверждается: вариация разрыва существенно выше вариации официального охвата.")