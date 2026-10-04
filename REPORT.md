\# Mathematical Modeling of Measles Transmission and Vaccine Coverage Gap in Kazakhstan (2019–2026)



\## Executive Summary (Резюме на русском языке)

Настоящее исследование посвящено математической реконструкции эпидемической динамики кори в Республике Казахстан за период 2019–2026 гг. на основе официальных деперсонифицированных данных Комитета санитарно-эпидемиологического контроля МЗ РК. Несмотря на официально декларируемый охват плановой вакцинацией детей (95–98%), страна столкнулась с двумя масштабными эпидемическими волнами: первой (февраль 2023 – август 2024 г., 57 587 подтвержденных случаев) и второй (с октября 2025 г., более 8 691 случая). 



С использованием уравнения конечного размера эпидемии (final size equation) и полулогарифмической оценки экспоненциальной скорости роста ($r = 0.815$ мес⁻¹) восстановлена эффективная доля восприимчивого населения перед первой волной: $s\_0 \\approx 8.5\\% - 8.8\\%$ (при базовом репродуктивном числе $R\_0 = 12$ и полноте учета $\\rho \\in \[0.3; 1.0]$). Анализ регионального разрыва показал, что фактическая доля восприимчивых существенно превосходит ожидаемую из официальных отчетов об охвате (в среднем на 2–11 п.п.), что подтверждает статистическую гипотезу о пространственной неоднородности и недоучете когорт непривитых лиц. Сформирован датированный прогноз накопления критического пула восприимчивых: порог повторной крупной вспышки ($S\_{\\text{crit}} = N / R\_0$) будет достигнут в диапазоне между концом 2026 и концом 2029 гг.



\---



\## 1. Introduction \& Research Questions

Measles remains one of the most contagious human pathogens, requiring a high critical vaccination coverage threshold:

$$V^\* = \\frac{1 - 1/R\_0}{E}$$

For realistic measles parameters ($R\_0 \\in \[12, 18]$, vaccine efficacy $E \\in \[0.93, 0.97]$), herd immunity requires 94.5% to >100% effective newborn coverage. While official administrative records in Kazakhstan consistently reported annual MCV1/MCV2 coverage exceeding 95%, the country registered over 84,000 cases between 2019 and 2026.



This study addresses four core research questions:

\* \*\*RQ1:\*\* What is the critical vaccination threshold $V^\*$ across plausible $(R\_0, E)$ combinations?

\* \*\*RQ2:\*\* What was the actual susceptible proportion ($s\_0$) prior to the major 2023–2024 outbreak?

\* \*\*RQ3:\*\* Does a statistically meaningful gap exist between declared immunization rates and model-inferred susceptibility?

\* \*\*RQ4:\*\* When will susceptible replenishment trigger subsequent epidemic risks?



\---



\## 2. Data Sources \& Integrity

1\. \*\*Official Health Surveillance Data:\*\* Primary epidemiological and vaccination datasets were obtained from the Committee of Sanitary and Epidemiological Control of the Ministry of Health of the Republic of Kazakhstan (Applications 1 and 2, processed with SHA-256 integrity verification).

2\. \*\*Correction of January 2024 Anomaly:\*\* An artifact in the raw January 2024 national incidence (28,147 cases, exactly matching the cumulative annual total) was corrected via marginal difference against February–December records (yielding 9,510 cases; full sensitivity analysis preserved in `DECISIONS.md`).

3\. \*\*Demographic Foundations:\*\* Regional population denominators on January 1, 2023, reflect official publications of the Bureau of National Statistics (ASP\&R RK) across all 20 post-reform administrative territories.



\---



\## 3. Methods

\* \*\*Epidemic Wave Partitioning:\*\* Pre-specified threshold criteria defined Wave 1 (Feb 2023 – Aug 2024, cumulative 57,587 cases; peak in Dec 2023 with 10,016 cases) and Wave 2 (Oct 2025 – Jul 2026, cumulative 8,691 cases).

\* \*\*Final Size Equation Inversion:\*\* Pre-epidemic susceptibility $s\_0$ was numerically resolved via Brent's method:

&#x20; $$\\ln\\left(\\frac{s\_0}{s\_0 - A}\\right) = R\_0 \\cdot A, \\quad \\text{where } A = \\frac{C}{\\rho \\cdot N}$$

&#x20; evaluated across a full parameter grid ($R\_0 \\in \[8, 20]$, reporting completeness $\\rho \\in \[0.3, 1.0]$).

\* \*\*Initial Exponential Growth Rate:\*\* Evaluated via semi-log linear regression on early upward trajectory (March–June 2023) using generation interval $T \\approx 14$ days.

\* \*\*Susceptible Dynamics \& Recurrence Timing:\*\* Modeled through annual birth cohort replenishment $B \\cdot (1 - v \\cdot E)$ against critical depletion thresholds $S\_{\\text{crit}} = N / R\_0$.



\---



\## 4. Limitations

1\. \*\*Closed Population Assumption:\*\* The classic final size relation assumes negligible migration during outbreak peaks.

2\. \*\*Supplementary Immunization Activities (SIA):\*\* Mass catch-up campaigns initiated in late 2023 modified susceptible pools non-linearly.

3\. \*\*Ascertainment Heterogeneity:\*\* True reporting completeness $\\rho$ is unobserved directly, necessitating scenario-bounded sensitivity bounds.

4\. \*\*Monthly Temporal Aggregation:\*\* Coarser temporal granularity restricts daily serial interval estimation.



\---



\## 5. Results \& Hypothesis Testing

\* \*\*Hypothesis H1 (Coverage Gap $\\ge 2\\%$):\*\* Confirmed across 16 of 20 regions (e.g., Almaty, Astana, Shymkent, Turkistan), where inferred susceptibility exceeded declared non-vaccination fractions by 2.5 to 11.1 percentage points.

\* \*\*Hypothesis H2 (Spatial Heterogeneity):\*\* Strongly confirmed. Declared coverage shows negligible variation across regions ($CV = 0.027$), whereas model-derived susceptibility gap exhibits high variance ($CV = 0.842$).

\* \*\*Hypothesis H3 (Unachievable Elimination under Suboptimal Efficacy):\*\* Confirmed via heatmap analysis; for $R\_0 \\ge 16$ and $E \\le 0.93$, required coverage $V^\*$ mathematically exceeds 100%.



\---



\## 6. Vaccination Status Analysis (Table 20)

Analysis of confirmed case records for 2025–2026 demonstrates:

\* Unvaccinated individuals accounted for \*\*>75%\*\* of all cases (parental refusals: 39.8%, medical exemptions: 12.1%, below vaccination age: 21.3%).

\* Breakthrough infections among fully vaccinated (2 doses) accounted for only \*\*3.1% – 3.5%\*\*, verifying sustained clinical vaccine efficacy and underscoring refusal clusters as the primary transmission engine.

