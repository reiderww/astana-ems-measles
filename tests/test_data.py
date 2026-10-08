import os
import pandas as pd
import numpy as np

def test_incidence_structure_and_sums():
    df = pd.read_csv("data/processed/incidence.csv")
    # 1. 1 820 строк, 144 без значений (новые области 2019-2022)
    assert len(df) == 1820, f"Expected 1820 rows, got {len(df)}"
    assert df["total_as_received"].isna().sum() == 144, "Expected 144 missing values for total_as_received"
    
    # 2. Контрольные суммы по стране
    assert int(round(df["total_as_received"].sum())) == 103266, "total_as_received sum mismatch"
    assert int(round(df["cases_0_14"].sum())) == 63848, "cases_0_14 sum mismatch"
    assert int(round(df["cases_15_17"].sum())) == 2504, "cases_15_17 sum mismatch"
    assert int(round(df["total_corrected"].sum())) == 84629, "total_corrected sum mismatch"

def test_incidence_spot_checks():
    df = pd.read_csv("data/processed/incidence.csv")
    
    # г. Астана (region_id 19)
    # Январь 2019: 946, 670, 14
    ast_2019 = df[(df["region"] == 19) & (df["year"] == 2019) & (df["month"] == 1)].iloc[0]
    assert ast_2019["total_as_received"] == 946
    assert ast_2019["cases_0_14"] == 670
    assert ast_2019["cases_15_17"] == 14
    
    # Январь 2024: 1605, 307, 19, после поправки 431
    ast_2024 = df[(df["region"] == 19) & (df["year"] == 2024) & (df["month"] == 1)].iloc[0]
    assert ast_2024["total_as_received"] == 1605
    assert ast_2024["cases_0_14"] == 307
    assert ast_2024["cases_15_17"] == 19
    assert ast_2024["total_corrected"] == 431
    
    # Акмолинская область (region_id 2), февраль 2019: 71, 39, 1
    akm_2019 = df[(df["region"] == 2) & (df["year"] == 2019) & (df["month"] == 2)].iloc[0]
    assert akm_2019["total_as_received"] == 71
    assert akm_2019["cases_0_14"] == 39
    assert akm_2019["cases_15_17"] == 1

def test_coverage_spot_checks():
    df = pd.read_csv("data/processed/coverage.csv")
    assert len(df) == 1820
    assert df["dose1_pct_of_annual_plan"].isna().sum() == 144
    
    # Акмолинская область (region_id 2), февраль 2019: 9.6 и 9.8
    akm_feb = df[(df["region"] == 2) & (df["year"] == 2019) & (df["month"] == 2)].iloc[0]
    assert np.isclose(akm_feb["dose1_pct_of_annual_plan"], 9.6)
    assert np.isclose(akm_feb["dose2_pct_of_annual_plan"], 9.8)
    
    # Годовые суммы за 2019 для Акмолинской: 105.4 и 95.3
    akm_2019_sum = df[(df["region"] == 2) & (df["year"] == 2019)]
    assert np.isclose(akm_2019_sum["dose1_pct_of_annual_plan"].sum(), 105.4)
    assert np.isclose(akm_2019_sum["dose2_pct_of_annual_plan"].sum(), 95.3)

def test_case_status_totals():
    df = pd.read_csv("data/processed/case_status.csv")
    assert len(df) == 40  # 20 регионов * 2 периода
    
    # Суммы по 20 регионам: 4 240 за 2025 и 7 127 за 2026_jan_jul
    sum_2025 = df[df["period"] == "2025"]["confirmed"].sum()
    sum_2026 = df[df["period"] == "2026_jan_jul"]["confirmed"].sum()
    assert sum_2025 == 4240
    assert sum_2026 == 7127

def test_region_map():
    df = pd.read_csv("data/processed/region_map.csv")
    assert len(df) == 20
    assert len(df["region_id"].unique()) == 20