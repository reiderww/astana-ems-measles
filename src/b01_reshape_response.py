import os
import pandas as pd
import numpy as np

# Создаем папку data/processed, если её нет
os.makedirs("data/processed", exist_ok=True)

excel_path = "data/raw/Приложение_2.xlsx"

# 1. Формирование region_map.csv
region_mapping_data = [
    (1, "АБАЙ", "Абайская"),
    (2, "АКМОЛИНСКАЯ", "Акмолинская"),
    (3, "АКТЮБИНСКАЯ", "Актюбинская"),
    (4, "АЛМАТИНСКАЯ", "Алматинская"),
    (5, "АТЫРАУСКАЯ", "Атырауская"),
    (6, "ВОСТОЧНО-КАЗАХСТАНСКАЯ", "ВКО"),
    (7, "ЖАМБЫЛСКАЯ", "Жамбылская"),
    (8, "ЖЕТІСУ", "Жетысуская"),
    (9, "ЗАПАДНО-КАЗАХСТАНСКАЯ", "ЗКО"),
    (10, "КАРАГАНДИНСКАЯ", "Карагандинская"),
    (11, "КОСТАНАЙСКАЯ", "Костанайская"),
    (12, "КЫЗЫЛОРДИНСКАЯ", "Кызылординская"),
    (13, "МАНГИСТАУСКАЯ", "Мангистауская"),
    (14, "ПАВЛОДАРСКАЯ", "Павлодарская"),
    (15, "СЕВЕРО-КАЗАХСТАНСКАЯ", "СКО"),
    (16, "ТУРКЕСТАНСКАЯ", "Туркестанская"),
    (17, "ҰЛЫТАУ", "Улытауская"),
    (18, "г.АЛМАТЫ", "г. Алматы"),
    (19, "г.АСТАНА", "г. Астана"),
    (20, "г.ШЫМКЕНТ", "г.Шымкент")
]
df_region_map = pd.DataFrame(region_mapping_data, columns=["region_id", "name_sheets_1_2", "name_sheet_3"])
df_region_map.to_csv("data/processed/region_map.csv", index=False)
print("Saved data/processed/region_map.csv")

# 2. Обработка листа 'попривит.' -> case_status.csv
df_raw_status = pd.read_excel(excel_path, sheet_name="попривит.", header=None)
records_status = []

name3_to_id = dict(zip(df_region_map["name_sheet_3"], df_region_map["region_id"]))

for row_idx in range(5, 25): # строки 6-25 в Excel
    raw_name = str(df_raw_status.iloc[row_idx, 0]).strip()
    reg_id = name3_to_id.get(raw_name)
    if not reg_id:
        continue
    
    # 2025 год: столбцы B-I (1-8)
    records_status.append({
        "region": reg_id,
        "period": "2025",
        "confirmed": df_raw_status.iloc[row_idx, 1],
        "vaccinated_1_dose": df_raw_status.iloc[row_idx, 2],
        "vaccinated_2_doses": df_raw_status.iloc[row_idx, 3],
        "unvaccinated_refusal": df_raw_status.iloc[row_idx, 4],
        "unvaccinated_medical_exemption": df_raw_status.iloc[row_idx, 5],
        "unvaccinated_other": df_raw_status.iloc[row_idx, 6],
        "unvaccinated_too_young": df_raw_status.iloc[row_idx, 7],
        "status_unknown": df_raw_status.iloc[row_idx, 8]
    })
    
    # 2026_jan_jul: столбцы J-Q (9-16)
    records_status.append({
        "region": reg_id,
        "period": "2026_jan_jul",
        "confirmed": df_raw_status.iloc[row_idx, 9],
        "vaccinated_1_dose": df_raw_status.iloc[row_idx, 10],
        "vaccinated_2_doses": df_raw_status.iloc[row_idx, 11],
        "unvaccinated_refusal": df_raw_status.iloc[row_idx, 12],
        "unvaccinated_medical_exemption": df_raw_status.iloc[row_idx, 13],
        "unvaccinated_other": df_raw_status.iloc[row_idx, 14],
        "unvaccinated_too_young": df_raw_status.iloc[row_idx, 15],
        "status_unknown": df_raw_status.iloc[row_idx, 16]
    })

df_case_status = pd.DataFrame(records_status)
df_case_status.to_csv("data/processed/case_status.csv", index=False)
print("Saved data/processed/case_status.csv")

# 3. Обработка листа 'Охват' -> coverage.csv
df_cov_raw = pd.read_excel(excel_path, sheet_name="Охват", header=None)
records_cov = []

month_names = ["январь", "февраль", "март", "апрель", "май", "июнь",
               "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]

# Сбор колонок по месяцам
col_idx = 1
years_months = []
for y in range(2019, 2026):
    for m in range(1, 13):
        years_months.append((y, m, col_idx, col_idx + 1))
        col_idx += 2
# 2026 (7 месяцев)
for m in range(1, 8):
    years_months.append((2026, m, col_idx, col_idx + 1))
    col_idx += 2

name12_to_id = dict(zip(df_region_map["name_sheets_1_2"], df_region_map["region_id"]))

for row_idx in range(3, 23): # строки 4-23
    r_name = str(df_cov_raw.iloc[row_idx, 0]).strip()
    reg_id = name12_to_id.get(r_name)
    for (y, m, c1, c2) in years_months:
        v1 = df_cov_raw.iloc[row_idx, c1]
        v2 = df_cov_raw.iloc[row_idx, c2]
        records_cov.append({
            "region": reg_id,
            "year": y,
            "month": m,
            "dose1_pct_of_annual_plan": np.nan if pd.isna(v1) else float(v1),
            "dose2_pct_of_annual_plan": np.nan if pd.isna(v2) else float(v2)
        })

df_coverage = pd.DataFrame(records_cov)
df_coverage.to_csv("data/processed/coverage.csv", index=False)
print("Saved data/processed/coverage.csv")

# 4. Обработка листа 'заболев' -> incidence.csv
df_inc_raw = pd.read_excel(excel_path, sheet_name="заболев", header=None)

# Карта колонок листа "заболев":
# 2019-2025: 12 месяцев * 3 + 2 годовых итога = 38 колонок на год
# 2026: 7 месяцев * 3 = 21 колонка
inc_cols = []
c_ptr = 1
for y in range(2019, 2026):
    for m in range(1, 13):
        inc_cols.append((y, m, c_ptr, c_ptr + 1, c_ptr + 2))
        c_ptr += 3
    c_ptr += 2 # пропуск двух годовых итогов
for m in range(1, 8):
    inc_cols.append((2026, m, c_ptr, c_ptr + 1, c_ptr + 2))
    c_ptr += 3

records_inc = []
for row_idx in range(3, 23):
    r_name = str(df_inc_raw.iloc[row_idx, 0]).strip()
    reg_id = name12_to_id.get(r_name)
    
    for (y, m, c_tot, c_0_14, c_15_17) in inc_cols:
        v_tot = df_inc_raw.iloc[row_idx, c_tot]
        v_0_14 = df_inc_raw.iloc[row_idx, c_0_14]
        v_15_17 = df_inc_raw.iloc[row_idx, c_15_17]
        
        records_inc.append({
            "region": reg_id,
            "year": y,
            "month": m,
            "total_as_received": np.nan if pd.isna(v_tot) else float(v_tot),
            "cases_0_14": np.nan if pd.isna(v_0_14) else float(v_0_14),
            "cases_15_17": np.nan if pd.isna(v_15_17) else float(v_15_17)
        })

df_incidence = pd.DataFrame(records_inc)

# Расчет поправки января 2024 года (Раздел 4.2 протокола):
# total_corrected для января 2024 = ячейка января - сумма (февраль-декабрь 2024)
df_incidence["total_corrected"] = df_incidence["total_as_received"]

for reg_id in df_region_map["region_id"]:
    mask_2024_feb_dec = (df_incidence["region"] == reg_id) & (df_incidence["year"] == 2024) & (df_incidence["month"] >= 2)
    sum_feb_dec = df_incidence.loc[mask_2024_feb_dec, "total_as_received"].sum()
    
    mask_jan = (df_incidence["region"] == reg_id) & (df_incidence["year"] == 2024) & (df_incidence["month"] == 1)
    val_jan = df_incidence.loc[mask_jan, "total_as_received"].values[0]
    
    corrected_jan = val_jan - sum_feb_dec
    df_incidence.loc[mask_jan, "total_corrected"] = corrected_jan

df_incidence["cases_18_plus"] = df_incidence["total_corrected"] - df_incidence["cases_0_14"] - df_incidence["cases_15_17"]

df_incidence = df_incidence[["region", "year", "month", "total_as_received", "total_corrected", "cases_0_14", "cases_15_17", "cases_18_plus"]]
df_incidence.to_csv("data/processed/incidence.csv", index=False)
print("Saved data/processed/incidence.csv")
print("Обработка успешно завершена!")