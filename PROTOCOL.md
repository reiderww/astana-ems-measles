# Research Protocol and Execution Plan

**Project:** Astana EMS coverage and Kazakhstan measles immunity gap
**Author:** Damir Butabaev
**Protocol version:** 1.0
**Date:** August 2026

## 0. Purpose of this document

A protocol is written before analysis begins. It fixes, in advance, the question being asked, the data that will answer it, the method that will be used, what counts as confirmation of a hypothesis, what counts as disconfirmation, and what happens if the planned data cannot be obtained. Once results exist, the question cannot be quietly adjusted to fit the answer. That is the line between a research project and a well produced presentation.

This document covers two linked studies:

- **Project A.** Optimal ambulance station placement in Astana, a covering location analysis under Kazakhstan's ten minute emergency response standard.
- **Project B.** Reported coverage versus implied susceptibility, reconstructing regional measles immunity gaps in Kazakhstan.

This file is committed to the repository first, before any code. The commit date and history stand as evidence that the plan was fixed in advance of the results.

The document has four parts. Part 1 sets out rules common to both projects. Part 2 is the protocol for Project A. Part 3 is the protocol for Project B. Part 4 is a short working schedule. The appendices cover repository structure and the literature list.

---

## Part 1. Rules common to both projects

### 1.1 Repository and proof of authorship

A public GitHub repository with commit history is dated evidence that the work was done by the named author, incrementally, over time.

- The repository is created before analysis starts. The first commit is this protocol.
- A commit is made at the end of every working session, even if the session produced nothing usable. Commit messages are written in English, in the imperative mood, and describe the change rather than the feeling: not "finally works" but "add MCLP formulation and 10 minute coverage constraint."
- `DECISIONS.md` is kept alongside the code. Each entry is a date, a decision, and one sentence on why the decision was made. Example: "2026-08-19. Dropped the 100 meter demand grid in favor of a 400 meter grid, because the 80,000 point problem does not solve in reasonable time and the difference in mean travel time is under 6 seconds."
- Licensing: MIT for code, CC BY 4.0 for text and figures. `LICENSE` and `LICENSE-text` are added at repository creation.
- `CITATION.cff` allows the work to be cited correctly and takes five minutes to write.

### 1.2 Data provenance

`DATA_SOURCES.md` is filled in as each source is downloaded. For every source it records: full name, publishing organization, exact URL, date downloaded, license, file size, and SHA-256 checksum. The checksum is a one line command and proves the file was not silently altered later.

```
sha256sum data/raw/kontur_population_KZ.gpkg >> DATA_SOURCES.md
```

`data/raw` is never edited after download. Any processing writes new files into `data/processed`. This single rule prevents the most common and least visible error in projects like this one: a source file gets quietly patched somewhere along the way, and the result can no longer be reproduced.

### 1.3 Reproducibility

- Library versions are pinned exactly in `requirements.txt`, not given as ranges.
- Every stochastic process is given a fixed seed, and the seed is recorded in configuration, not buried in code.
- The full analysis runs from a single command. Jupyter notebooks are fine for exploration, but the numbers and figures that appear in the report must be produced by scripts that can be re-run end to end.
- Pre-submission check: delete everything in `data/processed` and `results`, re-run the pipeline on a clean machine, and confirm the numbers match. If a single number has shifted, something was not properly fixed.

### 1.4 What counts as a result

A negative result is still a result. If it turns out the current placement of Astana's ambulance stations is already close to optimal, that is a complete finding and should be reported honestly. If it turns out the available data cannot distinguish between two explanations for the measles coverage gap, that is also a finding, and it has a name: an identifiability boundary.

What is never acceptable, under any circumstances: adjusting the question to match the answer obtained, dropping inconvenient regions, rounding confidence intervals in a favorable direction, or describing a modeling assumption as a measured fact.

### 1.5 Structure of the written report

Both reports follow the IMRaD structure, 10 to 15 pages of main text, in English, with a one page summary in Russian. Sections: Abstract, Introduction, Data, Methods, Results, Sensitivity analysis, Limitations, Conclusion, References, Appendix.

Limitations is drafted immediately after Methods, not at the end, and is added to as work proceeds. Limitations written on the last night tend to be perfunctory. Limitations written early change the method itself, and that is the point.

Every figure and table is numbered, carries a caption that reads independently of the surrounding text, and is produced by code rather than drawn by hand. A screenshot from a spreadsheet is not acceptable in this kind of work.

### 1.6 Citation checking

The literature list in Appendix B has been assembled in advance. Before submission, every entry must be checked against the publisher's own page for year, volume, page numbers, and DOI.

---

## Part 2. Project A: optimal ambulance station placement in Astana

**Working title.** Optimal ambulance station placement in Astana: a covering location analysis under the national ten minute response standard.

### A.1 The one sentence the work must prove

Holding the number of stations fixed at today's count, the placement of Astana's ambulance stations can be changed so that the share of the population reachable within the mandated ten minute standard increases by a measurable amount, and that increase is robust to how demand is modeled.

Two features of this sentence matter. First, the number of stations is fixed. The study does not argue for building more stations, because that improvement would be trivial and would prove nothing. It asks whether the stations that already exist are placed well. That is a stronger and more defensible claim. Second, robustness is built into the claim itself. A single number produced under a single set of assumptions is worth little. What has value is a claim that survives when the assumptions change.

### A.2 Research questions and hypotheses

**RQ1.** What share of Astana's population is reachable by an ambulance crew within 10, 15, and 30 minutes under the current station placement, computed on the real road network?

**RQ2.** What placement of the same number of stations maximizes the share of the population within the ten minute standard, and by how much does it improve on the current placement?

**RQ3.** How robust is the answer to RQ2 to three factors: the demand modeling approach, the assumed travel speed, and crew busy fraction?

**Hypothesis H1.** The current placement achieves less than 95 percent ten minute coverage. Disconfirmed if computed coverage is 95 percent or higher.

**Hypothesis H2.** There exists a rearrangement of the same number of stations that increases coverage by at least 3 percentage points. Disconfirmed if the optimum differs from the current placement by less than 3 percentage points.

**Hypothesis H3.** The set of stations in the optimal solution agrees across all three demand scenarios in at least 70 percent of sites. Disconfirmed if agreement is lower.

The thresholds of 95 percent, 3 percentage points, and 70 percent are fixed now, before any computation. They are not to be changed after results are obtained. If a threshold turns out to have been chosen poorly, that goes in Limitations, not into a rewrite of the threshold.

### A.3 Scope

- **Geography.** The administrative boundary of Astana city. Suburbs in the surrounding Akmola region are excluded, and this exclusion is stated explicitly, because some suburban calls are served by a city station.
- **Call type.** Category 1 urgency, that is, emergency calls with an immediate threat to life, for which the mandated response time is 10 minutes. Categories 2 through 4 are used only as a sensitivity check.
- **Time of day.** The base calculation uses free flow travel. A separate scenario applies a peak hour congestion factor.
- **Out of scope.** Real time dispatch, reassignment of crews between stations, crew mobilization time, call handling time, and hospital transfer time are not modeled. The study answers a question about placement, not about the operation of the service as a whole.

### A.4 Formal specification

**Notation**

| Symbol | Meaning |
|---|---|
| I | set of demand points i, centroids of a 400 meter hexagon grid |
| J | set of candidate sites j |
| d_i | demand weight at point i, the expected number of emergency calls |
| t_ij | travel time from site j to point i on the road network, in minutes |
| S | response standard, S = 10 minutes for category 1 |
| N_i | set of sites from which point i is reachable within S minutes: N_i = { j : t_ij <= S } |
| p | number of stations to place, equal to the current count |
| x_j | binary variable, 1 if a station is placed at site j |
| y_ij | binary variable, 1 if point i is served by site j |
| z_i | binary variable, 1 if point i is covered under the standard |
| q | crew busy fraction, the share of time a crew is occupied |

**Model 1. p-median (Hakimi, 1964)**

Minimizes the population weighted mean travel time across the city.

```
min   sum_i sum_j  d_i * t_ij * y_ij

s.t.  sum_j y_ij = 1                for all i
      y_ij <= x_j                   for all i, j
      sum_j x_j = p
      x_j, y_ij in {0, 1}
```

This model answers "what does the average look like," and it is useful, but it has a known weakness: it is indifferent to a few outlying districts waiting a very long time, so long as that is offset by fast service to the center. It is not sufficient on its own.

**Model 2. MCLP, maximal covering location problem (Church and ReVelle, 1974)**

Maximizes the share of demand covered within the standard.

```
max   sum_i  d_i * z_i

s.t.  z_i <= sum_{j in N_i} x_j     for all i
      sum_j x_j = p
      x_j, z_i in {0, 1}
```

This is the primary model of the study, because it is stated in exactly the terms of Kazakhstan's regulatory standard. The standard does not say "the average response time should be low." It says that for category 1 urgency, response time must not exceed 10 minutes. MCLP is the mathematical statement of that sentence. This match between the optimization formulation and the text of the regulation should be named explicitly in the report, because it turns an abstract optimization exercise into a check on whether a government commitment is being met.

**Model 3. MEXCLP, maximum expected covering location problem (Daskin, 1983)**

The first two models silently assume the nearest station is always free. In practice a crew is often already on another call, in which case the next nearest station responds instead. MEXCLP corrects for this.

```
max   sum_i sum_{k=1..p}  d_i * (1 - q) * q^(k-1) * z_ik

s.t.  sum_{k=1..p} z_ik <= sum_{j in N_i} x_j    for all i
      sum_j x_j = p
      z_ik in {0, 1}
```

Here z_ik equals one if point i is covered by at least k stations, and the factor (1 - q) * q^(k-1) is the probability that the first k-1 nearest crews are busy while the k-th is free. The busy fraction q is estimated as q = (lambda * tau) / m, where lambda is the number of calls per hour, tau is the mean time a crew is occupied per call in hours, and m is the number of crews on shift.

This third model is what separates a serious study from a classroom exercise. The first two are in any textbook. The third requires understanding that coverage is a probabilistic quantity, not a geometric one. If time only allows two of the three models, the priority is MCLP and MEXCLP, with p-median kept as a reference calculation.

**Constrained and unconstrained variants**

Candidate sites J are defined two ways, and both are computed.

- **Unconstrained.** J is every node of the road network, or a thinned subset of it. This gives an upper bound on what is achievable in principle. As a recommendation it is unrealistic, since a station cannot be placed in the middle of an intersection.
- **Constrained.** J is the set of existing healthcare facilities from the medical organization registry: clinics, hospitals, and current substations. This gives a feasible recommendation.

The gap between the two optima is itself a finding: it shows how much coverage is lost to real estate constraints. This distinction is not common in student work of this kind, and it holds up well in an interview.

### A.5 Data

All sources were checked for availability on 12 August 2026.

| Source | Provides | Access | License |
|---|---|---|---|
| OpenStreetMap via the OSMnx library | Astana's road network with road types and speed limits, directed graph | Programmatic, no registration | ODbL, attribution required |
| Kontur Population, 400 meter H3 hexagons | Population distribution within the city, Kazakhstan layer available separately | data.humdata.org, organization Kontur | CC BY 4.0 |
| Kazakhstan open data portal, medorg dataset | Names, addresses, and coordinates of Kazakhstan's medical organizations | data.egov.kz/datasets/view?index=medorg, API available | Open data, Republic of Kazakhstan |
| Astana city ambulance service website, 103-astana.kz | Official list of substations and their addresses | Public website | Reference use, with citation |
| 2GIS, organization listing with branches | Cross check of the substation list | Public website | Cross check only, not for redistribution of the underlying dataset |
| Bureau of National Statistics, stat.gov.kz | Astana population by district and age group | Public statistical releases | Open data, Republic of Kazakhstan |
| Government of Kazakhstan Resolution, 2025, Medical Care Guarantee Program 2026 to 2028, adilet.zan.kz | Response time standard: 10, 15, 30, and 60 minutes by urgency category | Open legal database | Official source |
| Ministry of Health press releases, gov.kz | National mean category 1 response time, call category breakdown, crews per shift | Public website | Official source |

**A note on the standard.** The values of 10, 15, 30, and 60 minutes are fixed in a government resolution, not taken from news coverage. The report should cite the resolution directly, and use press material only where operational figures are needed that do not appear in the regulation itself. This is the difference between a primary and a secondary source, and a reviewer will notice it.

### A.6 Demand modeling: the most honest part of the work

De-identified data on actual call volumes is not publicly available. This is not a flaw in the study, it is a feature of the domain, and dozens of published studies on other cities are built the same way. Several demand scenarios are constructed, and whether the answer depends on the choice of scenario is reported directly.

**Scenario 1, baseline.** Demand is proportional to population in each hexagon. The simplest assumption, and the weakest.

**Scenario 2, age weighted.** Emergency calls are distributed very unevenly by age. Ministry of Health figures for 2025 show circulatory disease accounting for about 19 percent of all calls and respiratory disease for about 24 percent. The former concentrates in older age groups, the latter in children. Age structure by Astana district is published by the Bureau of National Statistics. Weights are built so that d_i is proportional to the sum, over age groups, of group population multiplied by an age specific call rate. The call rates are taken from published emergency services literature and are explicitly flagged as external estimates.

**Scenario 3, daytime mobility adjustment.** During the day, population redistributes toward business districts. A rough but defensible approximation: shift a portion of demand into hexagons with a high density of non-residential buildings, using OpenStreetMap land use data. This scenario is flagged as the most speculative of the three.

**The main scientific output of this section** is the answer to one question: does the recommendation change across scenarios. If the optimal set of sites agrees across all three scenarios by 80 percent or more, the finding is robust, and that should be stated prominently. If it does not hold together, the finding is stated differently: "the available open data are not sufficient to give an unambiguous recommendation, and here is exactly what would need to be published to make one possible." That second outcome is a complete finding in its own right, and in some respects a more mature one.

### A.7 Travel time model

Travel time is computed on the directed road graph, respecting one way streets. Edge speeds are taken from the OpenStreetMap `maxspeed` tag where present, and imputed by road type where absent.

An ambulance running lights and sirens travels faster than general traffic, but not proportionally: the gain comes mainly from clearing intersections rather than from a higher cruising speed. Published estimates put the adjustment factor at roughly 1.1 to 1.5 times free flow speed. The correct approach is to take a base factor, test sensitivity across the range, and calibrate against an external benchmark.

**External calibration benchmark.** The Ministry of Health reported that over the first 11 months of 2025, the national mean category 1 response time was 8.8 minutes. This is a national average including rural areas, so the urban figure should be lower. If a model for Astana produces a mean response time around 12 to 15 minutes, something is wrong, most likely in the speed assumptions or a graph that has fractured into disconnected components. If the model produces 4 minutes, that is also an error, most likely a unit conversion problem. A reasonable range is roughly 5 to 9 minutes, and any deviation from it should be explained rather than ignored.

An additional manual check: pick three pairs of points, compute travel time from the model, and compare against the estimate from any public route planner. Three comparisons, recorded in an appendix table, are worth more than a paragraph arguing for validity.

### A.8 Computational pipeline

Nine steps. Each produces a result that can be inspected directly.

1. **Load the network.** Pull Astana's driving graph via OSMnx (the `osmnx.graph` module), save as GraphML in `data/raw`. Check: node and edge counts, share of edges in the largest strongly connected component. Estimated time: 1 hour.
2. **Speeds and travel time.** Apply `osmnx.routing.add_edge_speeds` and `osmnx.routing.add_edge_travel_times`, then apply the ambulance speed factor. Check: a histogram of speeds by road type contains no absurd values. Estimated time: 1 hour.
3. **Demand.** Load the Kontur layer for Kazakhstan, clip to the city boundary, take hexagon centroids, snap each centroid to the nearest graph node via `osmnx.distance.nearest_nodes`. Check: total population across hexagons compared against the official Astana population figure, with the discrepancy recorded in the text. Estimated time: 3 hours.
4. **Sites.** Compile current substations from the three sources, reconcile into one table, resolve discrepancies, geocode addresses, manually verify each point against satellite imagery. Separately compile candidate sites for the constrained variant. Check: no station falls in a river or outside city limits. Estimated time: 5 hours. This is the least glamorous step and the most consistently underestimated.
5. **Travel time matrix.** Compute t_ij with Dijkstra's algorithm from each site to every demand node. This is many thousands of paths, so computation should run from sites outward rather than from demand points, with results cached to disk. Check: the matrix contains no infinities other than explainable ones. Estimated time: 4 hours.
6. **Baseline calculation.** Evaluate coverage under the current placement: share of demand within 10, 15, and 30 minutes, mean, median, 90th percentile, maximum. This answers RQ1 and is the first real result of the study. Estimated time: 2 hours.
7. **Optimization.** Formulate and solve MCLP, then p-median, then MEXCLP, for both the constrained and unconstrained site sets. Use the PuLP library with the CBC solver, or `scipy.optimize.milp` with HiGHS, both free and both installable with one command. Check: optimality gap is zero, and the solution reproduces on a repeat run. Estimated time: 8 hours.
8. **Sensitivity.** Run all models across the three demand scenarios, three values of the speed factor, three values of q, and p equal to the current count minus one, the current count, and plus one. Compile into tables. Estimated time: 5 hours.
9. **Maps and writing.** Coverage maps before and after, a map of the gain by hexagon, a plot of coverage against number of stations. Then the report text. Estimated time: 12 hours.

Total: roughly 41 hours.

### A.9 Sanity checks

These seven checks are mandatory, and the results are reported in an appendix table. A report that contains this table reads very differently from one that does not.

1. The largest strongly connected component of the graph covers at least 99 percent of edges. If less, part of the city is artificially unreachable and the result is compromised.
2. Total population summed across hexagons is compared against Astana's official population, and the discrepancy is stated as a percentage and explained.
3. Mean modeled response time falls within the range discussed in A.7, and is compared against the published national figure.
4. Coverage under the optimal placement cannot be lower than under the current placement, since the current placement is itself a feasible solution to the optimization problem. If the model returns a lower figure, the formulation contains an error. This check catches more errors than any other.
5. Monotonicity in p: coverage at p+1 is not lower than coverage at p. A violation means the solver did not reach the optimum.
6. Degeneracy check: do multiple distinct solutions achieve the same objective value. If so, this is reported rather than silently resolved by picking one.
7. Manual recomputation: for three randomly chosen hexagons, travel time to the nearest station is computed by hand from a map and checked against the matrix.

### A.10 Risks and fallback plans

| Risk | Likelihood | Response |
|---|---|---|
| OpenStreetMap's road network is incomplete in newer Astana districts | Medium. The city is growing quickly and data entry is volunteer driven | Visually compare network coverage against satellite imagery by district, document gaps found in Limitations, and if needed contribute corrections to OpenStreetMap directly and note this as a separate contribution |
| The substation list disagrees across sources | High | Publish a comparison table showing what each source claims, and send a request to the city ambulance service. The discrepancy itself becomes an appendix |
| The travel time matrix takes too long to compute | Medium | Thin the candidate sites, aggregate demand to an 800 meter grid, or bound the computation to a radius beyond which the standard is clearly unmet |
| The solver fails to converge on the unconstrained variant | Low at a 400 meter grid | Cluster candidate nodes, use a greedy solution as a warm start, and report the optimality gap honestly if one remains |
| No data available on crew counts to estimate q | Medium | Estimate q from the national ratio of calls to crews, run a range of q values, and show how the conclusion changes |
| Not enough time for all three models | Medium | Priority order: MCLP, then MEXCLP, then p-median. One model with a strong sensitivity analysis is worth more than three models without one |

### A.11 What this study does not prove

This list belongs in Limitations. Naming the boundaries of one's own work is read as a sign of maturity.

- The study does not measure actual response time. It models response time on the road network under stated speed assumptions.
- The study does not know the true spatial distribution of calls, and substitutes scenarios for it.
- The study does not account for time of day traffic variation, apart from a single fixed factor scenario.
- The study does not account for the cost of relocating a station, building availability, staffing constraints, or contractual obligations.
- The study is not a recommendation to a health authority. It is an academic study, and should be described that way in the text.

The last point matters most. A sentence like "based on this work, the city should relocate station number X" is not appropriate. The correct phrasing is closer to: "under the stated assumptions, placement X yields coverage N percentage points higher than the current arrangement, indicating a potential for improvement that would need to be checked against operational data."

### A.12 Deliverables

- A report of 10 to 15 pages in English plus a Russian summary.
- A public repository with code, pipeline, and this protocol as the first commit.
- Figure 1: map of current 10 minute coverage. Figure 2: map of optimal coverage. Figure 3: map of the gain by hexagon. Figure 4: coverage as a function of station count. Figure 5: sensitivity analysis results.
- Table 1: baseline figures. Table 2: model comparison. Table 3: sensitivity. Table 4: sanity checks.
- An archival copy on Zenodo with a permanent DOI. This takes fifteen minutes, produces a citable, dated link, and reads as more serious than a GitHub link alone.

---

## Part 3. Project B: measles, reported coverage versus implied susceptibility

**Working title.** Reported coverage versus implied susceptibility: reconstructing regional measles immunity gaps in Kazakhstan, 2023 to 2026.

### B.1 Why this question

In 2024, Kazakhstan recorded 28,147 measles cases, more than any other country in the WHO European Region. Incidence fell in 2025, reported by the Ministry of Health as roughly a sixfold decline. From November 2025, a renewed rise began and continued through the winter and spring of 2026. Meanwhile, official administrative vaccination coverage for 2025 was reported at around 96 percent among one year olds and around 95 percent among six year olds.

These two statements do not sit comfortably together. If coverage is genuinely 96 percent, a large outbreak is unlikely. If an outbreak occurred, and then recurred a year later, susceptibility in the population is meaningfully higher than administrative reporting implies. That is the question this study asks.

**Final formulation.** What share of the population was actually susceptible to measles on the eve of the outbreak, reconstructed from the size of the outbreak itself, and how far does that figure diverge from the administratively reported coverage, nationally and by region?

This is a strong question for four reasons. It is testable: two independently derived numbers are compared against each other. It is anchored to a completed epidemic rather than an ongoing one, so standard reconstruction methods apply. It carries a built in check: a model calibrated on the 2024 outbreak either predicts the 2026 recurrence or it does not, and that is directly observable. And it requires no accusation of underreporting from anyone: the gap may be explained by heterogeneity, migration, accumulation of unvaccinated cohorts, or reporting quality, and the work is obligated to list every explanation rather than pick the most dramatic one.

### B.2 Research questions and hypotheses

**RQ1.** What share of the population was susceptible, implied by the size of the 2024 outbreak, under reasonable values of the basic reproduction number and reporting completeness?

**RQ2.** How far does this reconstructed figure diverge from administratively reported coverage, nationally and by region?

**RQ3.** Is the rate of accumulation of new susceptibles sufficient to explain the return of cases in winter 2025 and 2026, and what does the model predict for 2027?

**RQ4.** At what combination of basic reproduction number and vaccine efficacy is the official target of 95 percent coverage actually sufficient for herd immunity?

**Hypothesis H1.** The reconstructed susceptible share on the eve of the 2024 outbreak exceeds the figure implied by reported coverage by at least 2 percentage points. Disconfirmed if the gap is smaller than 2 points, or if the confidence interval spans zero.

**Hypothesis H2.** The size of the regional gap varies more than reported coverage itself does. That is, the coefficient of variation of the gap exceeds the coefficient of variation of coverage. Disconfirmed by direct calculation.

**Hypothesis H3.** The official 95 percent coverage target is sufficient only when vaccine efficacy exceeds 0.97 and the basic reproduction number is below 15. Tested analytically, disconfirmed by calculation.

### B.3 Mathematical framework

**Base model**

An SEIR model with vital dynamics, since measles' long latent period makes an SIR model inadequate, and births cannot be ignored because they are the source of new susceptibles.

```
dS/dt = mu * N * (1 - v)  -  beta * S * I / N  -  mu * S
dE/dt = beta * S * I / N  -  sigma * E  -  mu * E
dI/dt = sigma * E  -  gamma * I  -  mu * I
dR/dt = gamma * I  +  mu * N * v  -  mu * R
```

Here v is the share of newborns receiving effective protection, that is, coverage multiplied by vaccine efficacy. Parameter relationship: beta = R0 * gamma, ignoring mortality relative to the recovery rate, which is reasonable for measles.

| Parameter | Value | Basis and use |
|---|---|---|
| 1 / sigma, latent period | about 10 days | Standard value for measles. Take from Anderson and May, or Keeling and Rohani, with a page citation |
| 1 / gamma, infectious period | about 8 days | Infectiousness runs roughly 4 days before rash onset and 4 days after. Cross check against WHO surveillance guidance |
| Serial interval | mean about 14 days | Needed to estimate the reproduction number from a time series |
| R0 | a range, not a single number | The central methodological point of this project, see below |
| Vaccine efficacy | about 0.93 for one dose, about 0.97 for two | Take from the WHO measles vaccine position paper, with citation |
| Reporting completeness, rho | range 0.3 to 1.0 | Unknown. Carried through the entire analysis as a parameter |

**On the basic reproduction number: do not take 12 to 18 on faith**

The range 12 to 18 is cited almost everywhere, but the 2017 systematic review by Guerra and colleagues in Lancet Infectious Diseases found published R0 estimates for measles spread considerably wider, with only about 13 percent of studies giving medians inside that range. The authors explicitly recommend that countries estimate R0 from local data or from comparable populations rather than assume the textbook range.

This is an advantage for the study, not a complication. A study that takes R0 = 15 because that is the commonly cited figure reads as introductory. A study that says "R0 for Kazakhstan is not known, so every conclusion is reported as a function of R0 across a stated interval, and here is where the conclusions flip" reads as a research study. The computational effort is the same. The level is not.

**Herd immunity threshold with an imperfect vaccine**

The classical threshold formula is:

```
HIT = 1 - 1 / R0
```

This assumes the vaccine works in everyone who receives it. Accounting for vaccine efficacy E, the required coverage becomes:

```
V* = (1 - 1 / R0) / E
```

At E = 0.97 and R0 = 12, required coverage is about 94.5 percent. At R0 = 15, about 96.2 percent. At R0 = 18, about 97.4 percent.

The conclusion that follows: the official 95 percent target is sufficient only at a comparatively low R0 with a near ideal vaccine. Kazakhstan's reported coverage of about 96 percent sits squarely in the middle of this range, meaning the country is at the margin, not comfortably above it, before regional heterogeneity is even considered, and outbreaks ignite locally, not on the national average. This is exactly where the case for regional analysis arises, not by authorial preference but by the logic of the problem.

**Reconstructing the susceptible share from outbreak size**

The final size relation for a closed population links the initial and final susceptible shares:

```
ln( s0 / s_inf )  =  R0 * ( s0 - s_inf )
```

The observed share that fell ill, A = s0 - s_inf, is obtained from reported cases adjusted for reporting completeness: A = C / (rho * N), where C is reported cases and N is population. The equation is then solved numerically for s0, and reconstructed coverage equals 1 - s0.

Estimate the order of magnitude now, before any code, because this is itself the check that the question is well posed. Take 28,147 cases, a population of about 20 million, reporting completeness of 0.3, and R0 = 15. The result is a susceptible share on the order of 7 percent, that is, reconstructed coverage of about 93 percent against a reported 96 percent. A gap of about 3 percentage points, above the H1 threshold. The problem is well posed.

Three caveats belong directly in the text. First, the final size relation assumes a closed, homogeneous population with no births and no interventions, while catch up immunization campaigns ran in 2024 and 2025, which violates that assumption. Second, the result is sensitive to rho, which is exactly why rho is carried through the analysis as an explicit parameter rather than a convenient assumption. Third, heterogeneity biases the estimate downward, because an outbreak burns through the most susceptible groups first. All three points need to be worked through in the text, not hidden.

**Estimating the reproduction number from a time series**

If monthly or weekly series can be obtained, the Cori et al. method based on the renewal equation is applied, estimating the effective reproduction number in a moving window. If only monthly data is available, that window is too coarse, and it is more appropriate to estimate the exponential growth rate r during the rising phase, then convert to a reproduction number via the Wallinga and Lipsitch relation for a gamma distributed generation interval:

```
R = ( 1 + r / b ) ^ a,   where the generation interval ~ Gamma(a, b), mean a / b
```

The susceptible share is then estimated as S(t) approximately equal to R(t) / R0. This gives a **second, independent** way of estimating the same quantity as the final size relation. Agreement between the two estimates is a strong argument. Disagreement is also a result, and needs to be explained rather than smoothed over.

**Accumulation of susceptibles: why outbreaks return**

The most direct calculation in the whole study, done on a single page. If coverage is v and efficacy is E, each annual birth cohort adds N_births * (1 - v * E) new susceptibles. Time to accumulate a critical mass:

```
T  =  ( S_crit - S_0 ) / ( N_births * (1 - v * E) )
```

Substitute real numbers: roughly 400,000 births per year, coverage 0.96, efficacy 0.97. About 27,000 susceptible children are added annually. Compare this against the number of cases in 2024, and calculate how many years it takes to rebuild pre-outbreak susceptibility. The answer explains why the 2025 decline was followed by a 2026 rise, and supports a forecast for 2027.

A forecast in this kind of study is both a strength and a risk. The strength is that a prediction made in advance and dated by commit history is verifiable. The risk is that it may not come true. Both points belong in the text, plainly stated: what the model predicts, when the prediction was made, and what data will be used to check it. That is what makes it science rather than narrative.

### B.4 Data

Sources checked for availability on 12 August 2026.

| Source | Provides | Granularity | Risk |
|---|---|---|---|
| WHO provisional monthly measles and rubella data | Monthly suspected and confirmed case counts by country, xls export | Country, month | Low. Reporting lag of one to two months, noted on the page itself |
| WHO Immunization Data portal, Kazakhstan page | WUENIC MCV1 and MCV2 estimates from 1980, plus Joint Reporting Form data | Country, year | Low |
| National Center for Public Health (Salidat Kairbekova), annual statistical digest, nrchd.kz | Incidence and immunization indicators by region and by city of republican significance. The 2025 edition was released in May 2026 | Region, year | Medium. **This is the key source for the entire regional component** |
| Bureau of National Statistics, stat.gov.kz | Population by region and age, birth counts | Region, age, year | Low |
| adilet.zan.kz | National immunization schedule, dose timing | Legal act | Low |
| Ministry of Health and Sanitary Epidemiological Control Committee press office, gov.kz | 2026 operational figures, list of regions with rising incidence | Region, operational | High as a source of figures. Use for context and dating, not as the basis for calculations |
| Formal information request to the relevant authority | Monthly regional series, if not otherwise published | Region, month | Medium. Template in Appendix C of the internal planning document, submit no later than 20 August |

**The main data risk, and the fallback ladder**

Everything hinges on one question: are incidence series available broken down by region, and at what frequency. WHO data gives monthly granularity, but only at the country level. Kazakhstani statistical digests give regional granularity, but only annually. The ideal combination, region and month together, may not be publicly available at all.

Four fallback tiers are set out in advance, and moving down a tier is not treated as a failure.

1. **Tier 1, best case.** Monthly regional series obtained. Full analysis: effective reproduction number by region, susceptibility reconstruction, regional gap map.
2. **Tier 2, likely case.** Annual regional series from the statistical digest plus monthly national series from WHO. The dynamic component runs at national level, the regional component is built on annual incidence. The study is fully preserved, only the regional reproduction number estimate is lost.
3. **Tier 3.** Regional data available for only some years. The analysis is bounded to those years, with the gaps stated explicitly. A section is added on exactly what data would need to be published to make a fuller analysis possible. This is, on its own, a publishable finding.
4. **Tier 4, worst case.** No regional data at all. The study reorients to the national level plus a comparison of Kazakhstan against Central Asian neighbors for whom WHO data is available on the same terms. The question shifts to a comparative one, and the title should reflect that honestly.

Requests are sent in August precisely because a reply can take weeks. Kazakhstan's access to information law sets formal deadlines, but actual response time tends to run longer, and planning should follow the actual figure.

**A separate technical trap: regional boundaries have changed**

In June 2022, Kazakhstan created three new regions: Abai, Zhetysu, and Ulytau, carved out of existing ones. This means regional series before and after 2022 are not directly comparable. This cannot be ignored: comparing Karaganda region before and after Ulytau was split off compares two different territories with different populations.

The correct options are either to bound the regional analysis to 2023 onward, or to aggregate the new regions back into their parent regions for comparability with earlier years. Whichever option is chosen, it is justified in the text. This detail takes three sentences in an article and says a great deal about the author: it shows he looked at the data itself, not only at someone else's summary tables.

### B.5 What can, and cannot, be concluded

This is the most important section of the protocol, because the topic is sensitive.

**Can be concluded:** that outbreak size is inconsistent with the susceptibility level implied by reported coverage, under stated assumptions about R0 and reporting completeness. That the regional gap is distributed unevenly. That under stated parameters, the official 95 percent target is insufficient.

**Cannot be concluded:** that anyone falsified reporting. The gap between administrative coverage and reconstructed susceptibility has at least five competing explanations, and the study is obligated to list all of them:

1. Heterogeneity: a regional average can be high even where dense pockets of unvaccinated people exist, and an outbreak ignites in the pocket, not the average.
2. The denominator: administrative coverage is calculated against a planned child count, and internal and international migration makes that denominator imprecise.
3. Primary and secondary vaccine failure, including cold chain breaks.
4. Age structure: some cases may be younger than the age of the first dose, and coverage figures do not apply to them at all.
5. Quality of case reporting itself, separate from coverage reporting.

The phrasing in the text should read close to: "the observed gap is consistent with several mechanisms, and the available open data do not allow them to be distinguished; distinguishing them would require the following." This is called an identifiability boundary, and the ability to name it is worth more than a loud conclusion.

One further point. No sentence in this study should be readable as an argument against vaccination. The conclusion runs in exactly the opposite direction: coverage is insufficient precisely where it looks sufficient. This matters substantively, and it matters because the text will be read by an admissions committee.

### B.6 Step by step analysis plan

1. Collect and fix all series, compute checksums, fill in `DATA_SOURCES.md`. Estimated time: 4 hours.
2. Build the descriptive picture: national monthly series from 2019, annual regional series, incidence per 100,000, age structure of cases. Three figures. Estimated time: 5 hours.
3. Analytical section, no code required: compute V* = (1 - 1/R0)/E across a grid of R0 and E values, plot as a heat map, mark against reported coverage. This answers RQ4 and can be produced on day one. Estimated time: 3 hours.
4. Reconstruct the susceptible share via the final size relation, nationally and by region, across a grid of R0 and rho. Estimated time: 6 hours.
5. Estimate the growth rate and reproduction number from the time series, obtain a second independent susceptibility estimate, compare to the first. Estimated time: 6 hours.
6. Implement the SEIR model, calibrate it against the 2024 outbreak, check whether it reproduces the 2026 rise. Estimated time: 8 hours.
7. Compute susceptible accumulation and produce a dated forecast for 2027 with an interval. Estimated time: 3 hours.
8. Compile the regional gap table with intervals, build the map. Estimated time: 4 hours.
9. Build an interactive simulator: a single HTML page with sliders for R0, coverage, and vaccine efficacy, plotting the resulting dynamics. Published via GitHub Pages, at zero cost and lasting indefinitely. Estimated time: 5 hours.
10. Write the report. Estimated time: 12 hours.

Total: roughly 56 hours. If this exceeds the time available, the priority order is: the core finding (the reported versus reconstructed coverage gap, produced at steps 4 and 5) comes first. Steps 6 and 9, the full SEIR model and the interactive simulator, are the first candidates to defer to a later extension.

### B.7 Sanity checks

1. Summed regional cases for a year equal the national total for that year, within an explainable margin. If not, the series from different sources do not reconcile, and this must be resolved before, not after, computation.
2. The reconstructed susceptible share lies between 0 and 1 under every admissible parameter combination. A value outside that range means an error in the equation or an inadmissible combination of R0 and rho, which is itself informative.
3. The SEIR model at v = 0 reproduces the classical epidemic curve with a known final outbreak size. This is a standard check of the numerical scheme.
4. The sum of S, E, I, and R remains constant, up to births and deaths, across the full integration horizon. A violation indicates an error on the right hand side of the equations.
5. At R0 below 1 the epidemic dies out, at R0 above 1 it grows. Trivial, but it catches sign errors.
6. Population totals from demographic data agree with those used in the model.
7. The reproduction number estimated from the time series during the early outbreak phase agrees in order of magnitude with the product of R0 and the reconstructed susceptible share.

### B.8 Risks

| Risk | Likelihood | Response |
|---|---|---|
| Regional data unavailable | Medium | The four tier fallback ladder in B.4, the study is preserved at every tier |
| Reporting completeness is unknown and the result is highly sensitive to it | High, and irreducible | Carry rho as an explicit parameter through the entire analysis, present results as a surface rather than a single number, and name this as the central limitation |
| Catch up campaigns violate the assumptions of the final size relation | High | Model campaigns as a separate flow from S to R if volumes are known, otherwise state the direction of the resulting bias explicitly |
| The topic is read as politically sensitive | Low, if phrased correctly | No accusations, only a list of competing explanations and a clearly named identifiability boundary |
| Workload exceeds the time budget | High | Steps 6 and 9 are pre-designated as optional, decision point at the midpoint of the work period |

### B.9 Deliverables

- A report of 10 to 15 pages in English plus a Russian summary.
- A regional gap table with confidence intervals. This is the central result of the study.
- A heat map of required coverage as a function of R0 and vaccine efficacy, with Kazakhstan's actual reported coverage marked on it.
- A dated forecast for 2027 with an explicit interval and an explicit method for checking it.
- An interactive simulator on GitHub Pages, time permitting.
- A repository and an archival Zenodo copy with a DOI.

### B.10 Extension: allocation of a limited vaccine supply

This is the part of the project with the strongest mathematical content. The formulation:

Let there be R regions, each with reconstructed susceptible share s_r, population N_r, and a supply of B available doses. Allocate doses a_r to minimize expected total cases:

```
min   sum_r  F_r ( s_r - E * a_r / N_r )

s.t.  sum_r a_r <= B
      0 <= a_r <= number eligible for vaccination in region r
```

Here F_r is the outbreak size function for region r, as a function of susceptible share, derived from the final size relation calibrated in the main study. The function is separable across regions but not convex, which is what makes the problem interesting: the naive intuition of "send more doses where things are worst" is not correct here, because near the herd immunity threshold the marginal return on an additional dose is sharply nonlinear.

**Solution approach.** Start with a greedy algorithm on marginal return: at each step, allocate a batch of doses to whichever region has the largest magnitude derivative of the objective function. Then check with random restarts or simulated annealing to see whether the greedy algorithm finds the same solution. If it does, that is worth stating. If it does not, the gap between the greedy and the best found solution is itself a substantive result.

This extension is what connects the two projects into a single line of work. Project A is the allocation of a limited resource, stations, across space to minimize expected harm, with a probabilistic layer from crew busy fraction. This extension to Project B is the allocation of a limited resource, doses, across space to minimize expected harm, with an epidemiological layer. It is the same mathematical problem in two domains.

---

## Part 4. Working schedule

### Weekly plan, Project A

| Week | Tasks | Deliverable by end of week |
|---|---|---|
| Week 1 | Repository, protocol, pipeline steps 1 and 2 | Astana graph loaded, edge travel times computed, first commit in place |
| Week 2 | Steps 3 and 4 | Demand layer ready, substation list compiled and satellite verified |
| Week 3 | Steps 5 and 6 | Travel time matrix computed, RQ1 answered, first map produced |
| Week 4 | Step 7 | MCLP solved, RQ2 answered |
| Week 5 | Steps 7 and 8 | MEXCLP solved, sensitivity analysis run |
| Week 6 | Step 9 and writing | Full draft report, all figures produced |

### Phased plan, Project B

| Phase | Focus | Approximate hours |
|---|---|---|
| Data collection and provenance | Steps 1 to 2 above | 9 |
| Core reconstruction | Steps 3 to 5 above | 14 |
| Dynamic model | Step 6 above | 8 |
| Forecast and regional synthesis | Steps 7 to 8 above | 7 |
| Optional: simulator | Step 9 above | 5 |
| Writing | Step 10 above | 12 |

The two projects are sequenced with Project A first, because it runs entirely on data that can be downloaded immediately (road network, population grid, facility registry), while Project B depends on a Kazakhstani health statistics request that may take two to six weeks to answer. Requests for Project B data are therefore sent at the start of the work period, while Project A proceeds in parallel, so that waiting time is not idle time.

Project A also front loads the heaviest engineering: geospatial data handling in Python, git discipline, an integer programming solver, and the discipline of a written report. Project B reuses all of these tools rather than introducing them under time pressure.

---

## Appendix A. Repository structure

```
astana-ems-measles/
  README.md               overview, how to run, links to the reports
  PROTOCOL.md              this document, first commit
  DECISIONS.md            dated decision log
  DATA_SOURCES.md         sources, URL, date, license, sha256
  LICENSE                  MIT for code
  LICENSE-text             CC BY 4.0 for text and figures
  CITATION.cff             how to cite the work
  requirements.txt        pinned library versions
  Makefile                 the full pipeline, run with one command
  data/raw/                downloaded data, never edited
  data/processed/          derived data, safe to delete and rebuild
  src/                      pipeline scripts, numbered in run order
  notebooks/                exploration only, never the source of final numbers
  results/figures/          figures, generated by code
  results/tables/           tables, in csv
  paper/                    report text and bibliography
  tests/                    sanity checks, written as automated tests
```

On the `tests/` folder: the sanity checks in A.9 and B.7 are worth writing as small automated tests that run with a single command, rather than as one off manual actions. This costs an extra hour and is a very visible detail. It means the checks run every time, not once at the start and then forgotten.

## Appendix B. Literature

Sorted by purpose. Required entries are marked. Every entry should be checked against the publisher's page before citing, per section 1.6.

**Facility location and emergency services**

- **Required.** Church, R., ReVelle, C. The maximal covering location problem. Papers of the Regional Science Association, 1974, volume 32, pages 101 to 118. The original paper for the model that anchors Project A.
- **Required.** Daskin, M. S. A maximum expected covering location model: formulation, properties and heuristic solution. Transportation Science, 1983, volume 17, number 1, pages 48 to 70. The model that accounts for crew busy fraction.
- Hakimi, S. L. Optimum locations of switching centers and the absolute centers and medians of a graph. Operations Research, 1964, volume 12, number 3. The original p-median formulation.
- Toregas, C., Swain, R., ReVelle, C., Bergman, L. The location of emergency service facilities. Operations Research, 1971, volume 19, number 6. The set covering problem, the precursor to MCLP.
- Brotcorne, L., Laporte, G., Semet, F. Ambulance location and relocation models. European Journal of Operational Research, 2003, volume 147, number 3. A survey of the whole field, the best entry point into the topic.
- Boeing, G. OSMnx: new methods for acquiring, constructing, analyzing, and visualizing complex street networks. Computers, Environment and Urban Systems, 2017, volume 65. The paper for the software tool used throughout. Citation required whenever the tool is used.

**Epidemiology and modeling**

- **Required.** Guerra, F. M. et al. The basic reproduction number (R0) of measles: a systematic review. Lancet Infectious Diseases, 2017, volume 17, number 12. The basis for not taking the 12 to 18 range as given.
- **Required.** Keeling, M. J., Rohani, P. Modeling Infectious Diseases in Humans and Animals. Princeton University Press, 2008. The chapters on SEIR and herd immunity threshold. This is the reference to work through directly, not a summary sourced online.
- Anderson, R. M., May, R. M. Infectious Diseases of Humans: Dynamics and Control. Oxford University Press, 1991. The classic reference for standard measles parameters.
- Fine, P., Eames, K., Heymann, D. L. "Herd immunity": a rough guide. Clinical Infectious Diseases, 2011, volume 52, number 7. A short, clear account of why the herd immunity threshold is more complicated than the simple formula.
- Cori, A., Ferguson, N. M., Fraser, C., Cauchemez, S. A new framework and software to estimate time varying reproduction numbers during epidemics. American Journal of Epidemiology, 2013, volume 178, number 9. The method for estimating the effective reproduction number.
- Wallinga, J., Lipsitch, M. How generation intervals shape the relationship between growth rates and reproductive numbers. Proceedings of the Royal Society B, 2007, volume 274. The conversion from growth rate to reproduction number, needed when data is coarse.
- Diekmann, O., Heesterbeek, J. A. P., Metz, J. A. J. On the definition and the computation of the basic reproduction ratio R0. Journal of Mathematical Biology, 1990, volume 28. A rigorous definition via the next generation matrix, useful if the analysis extends into age structure.

**Methodology and reporting standards**

- WHO guidance on measles and rubella surveillance, the section on case definitions and reporting completeness. Needed to discuss rho correctly.
- WHO measles vaccine position paper, latest revision. The source for vaccine efficacy values and the rationale for the two dose schedule.
- Government of Kazakhstan Resolution on the Medical Care Guarantee Program 2026 to 2028, adilet.zan.kz. The source for the response time standard.

## Appendix C. Glossary

Plain language explanations for the core terms, kept to two sentences each with no formulas. Useful for an interview setting.

| Term | Plain explanation |
|---|---|
| Basic reproduction number, R0 | How many people one infected person infects on average, if nobody around them is protected. |
| Effective reproduction number | The same idea, but in a real population where some people are already protected. It changes over time. |
| Herd immunity threshold | The share of the population that needs to be protected before each new infected person, on average, infects fewer than one other person, so the outbreak dies out on its own. |
| Final size relation | A relationship between how infectious a disease is and the total share of the population that ends up infected. It lets the share of people unprotected before an outbreak be reconstructed from the number of people infected during it. |
| Reporting completeness | The share of real cases that made it into official statistics. Usually unknown, and therefore carried through the calculation as a parameter rather than assumed away. |
| Maximal covering location problem | Place a fixed number of facilities so that as many people as possible fall within a set travel time standard. |
| p-median problem | Place a fixed number of facilities to minimize the average distance or time to the population. Unlike the covering problem, it is indifferent to any fixed standard. |
| Integer programming | Optimization where the variables can only take whole number values. Here that means zero or one: a station either exists at a site or it does not. |
| Crew busy fraction | The share of time a crew is occupied on a call. When it is high, the nearest station is often unavailable, and a coverage model that ignores this overstates real coverage. |
| Sensitivity analysis | Checking whether a conclusion changes when the underlying assumptions change. If it does, the conclusion needs to be restated, not the assumption hidden. |
| Identifiability boundary | A situation where several different explanations produce the same observed data, and the available data cannot distinguish between them. |
