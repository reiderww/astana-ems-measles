import subprocess
import sys

scripts = [
    "src/b01_reshape_response.py",
    "src/b02_required_coverage_heatmap.py",
    "src/b03_descriptive_analysis.py",
    "src/b04_final_size.py",
    "src/b05_growth_rate.py",
    "src/b06_susceptible_accumulation.py",
    "src/b07_regional_gap.py",
    "src/b08_vaccination_status_analysis.py",
    "src/b09_figure2_regional_incidence.py",
    "src/b10_regional_gap_map.py"
]

print("=== ЗАПУСК ПОЛНОГО ВОСПРОИЗВОДИМОГО КОНВЕЙЕРА ===")
for script in scripts:
    print(f"\n[RUNNING] {script}...")
    res = subprocess.run([sys.executable, script])
    if res.returncode != 0:
        print(f"[ERROR] Ошибка при выполнении {script}!")
        sys.exit(res.returncode)

print("\n=== ЗАПУСК АВТОМАТИЧЕСКИХ ТЕСТОВ ===")
res_test = subprocess.run([sys.executable, "-m", "pytest", "tests/"])
if res_test.returncode != 0:
    print("[ERROR] Тесты завершились с ошибкой!")
    sys.exit(res_test.returncode)

print("\n=== КОНВЕЙЕР УСПЕШНО ВЫПОЛНЕН! ВСЕ РЕЗУЛЬТАТЫ ВОСПРОИЗВЕДЕНЫ ===")