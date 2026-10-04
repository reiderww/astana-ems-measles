import os
import pandas as pd
import numpy as np

os.makedirs("results/tables", exist_ok=True)

df_status = pd.read_csv("data/processed/case_status.csv")

# Агрегация по республике для 2025 и 2026 (январь-июль)
df_rk = df_status.groupby("period").sum(numeric_only=True).reset_index()

categories = [
    ("Привиты однократно", "vaccinated_1_dose", "Третье объяснение (эффективность вакцины, холодовая цепь)"),
    ("Привиты двукратно", "vaccinated_2_doses", "Третье объяснение (эффективность вакцины, холодовая цепь)"),
    ("Не привиты, отказ", "unvaccinated_refusal", "Первое объяснение (неоднородность): группа непривитых"),
    ("Не привиты, медицинский отвод", "unvaccinated_medical_exemption", "Первое объяснение (неоднородность): группа непривитых"),
    ("Не привиты, иные причины (упущенные)", "unvaccinated_other", "Первое объяснение (неоднородность): группа непривитых"),
    ("Не привиты, недостижение возраста", "unvaccinated_too_young", "Четвёртое объяснение (возрастная структура)"),
    ("Неизвестный статус", "status_unknown", "Пятое объяснение (качество регистрации)")
]

records_t20 = []
for label, col, expl in categories:
    val_2025 = df_rk[df_rk["period"] == "2025"][col].values[0]
    val_2026 = df_rk[df_rk["period"] == "2026_jan_jul"][col].values[0]
    tot_2025 = df_rk[df_rk["period"] == "2025"]["confirmed"].values[0]
    tot_2026 = df_rk[df_rk["period"] == "2026_jan_jul"]["confirmed"].values[0]
    
    records_t20.append({
        "Категория": label,
        "2025_случаев": val_2025,
        "2025_%": round(val_2025 / tot_2025 * 100.0, 1),
        "2026_случаев": val_2026,
        "2026_%": round(val_2026 / tot_2026 * 100.0, 1),
        "Связь с пунктом B.5 протокола": expl
    })

df_t20 = pd.DataFrame(records_t20)
df_t20.to_csv("results/tables/vaccination_status_table20.csv", index=False)
print("Saved results/tables/vaccination_status_table20.csv\n")

print("--- Таблица 20 протокола. Прививочный статус подтвержденных случаев по стране ---")
print(df_t20[["Категория", "2025_случаев", "2025_%", "2026_случаев", "2026_%"]].to_string(index=False))