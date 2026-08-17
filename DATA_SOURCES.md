# Data sources

Every dataset used in this project is logged here at the time it is downloaded, per protocol section 1.2. `data/raw/` is never edited after download; if a source needs correcting, download it again as a new dated entry rather than editing the existing file in place.

To generate a checksum after downloading a file:

```bash
sha256sum data/raw/<filename> >> DATA_SOURCES.md
```

then move the resulting line into the matching row below and format it properly.

## Template for a new entry

```
### <short name>
- **Provides:** what the file contains
- **Organization:** who publishes it
- **URL:** exact source URL
- **Date downloaded:** YYYY-MM-DD
- **License:** license or usage terms
- **File size:**
- **SHA-256:**
```

---

## Project A: ambulance station placement

### Road network
- **Provides:** Astana's driving network with road types and speed limits, directed graph
- **Organization:** OpenStreetMap contributors, accessed via the OSMnx library
- **URL:** retrieved programmatically via OSMnx, not a single fixed URL. Record the OSMnx query parameters used and the extraction date instead.
- **Date downloaded:**
- **License:** ODbL, attribution required
- **File size:**
- **SHA-256:**

### Population grid (Kontur)
- **Provides:** population distribution in 400 meter H3 hexagons
- **Organization:** Kontur
- **URL:** data.humdata.org, Kazakhstan population layer
- **Date downloaded:**
- **License:** CC BY 4.0
- **File size:**
- **SHA-256:**

### Medical organizations registry
- **Provides:** names, addresses, and coordinates of registered medical organizations
- **Organization:** Kazakhstan open data portal
- **URL:** data.egov.kz/datasets/view?index=medorg
- **Date downloaded:**
- **License:** Open data, Republic of Kazakhstan
- **File size:**
- **SHA-256:**

### Ambulance substation list (primary)
- **Provides:** official list of Astana ambulance substations and addresses
- **Organization:** Astana city ambulance service
- **URL:** 103-astana.kz
- **Date downloaded:**
- **License:** reference use, cite the source
- **File size:**
- **SHA-256:**

### Ambulance substation list (cross check)
- **Provides:** secondary listing used to cross check the primary substation list
- **Organization:** 2GIS
- **URL:**
- **Date downloaded:**
- **License:** cross check only, do not redistribute the underlying dataset
- **File size:**
- **SHA-256:**

### Population by district
- **Provides:** Astana population by district and age group
- **Organization:** Bureau of National Statistics
- **URL:** stat.gov.kz
- **Date downloaded:**
- **License:** open data, Republic of Kazakhstan
- **File size:**
- **SHA-256:**

### Response time standard
- **Provides:** the 10, 15, 30, and 60 minute response standards by urgency category
- **Organization:** Government of Kazakhstan, Medical Care Guarantee Program 2026 to 2028
- **URL:** adilet.zan.kz
- **Date downloaded:**
- **License:** official public legal text
- **File size:**
- **SHA-256:**

## Project B: measles

### WHO monthly measles and rubella data
- **Provides:** monthly suspected and confirmed case counts by country
- **Organization:** World Health Organization
- **URL:**
- **Date downloaded:**
- **License:**
- **File size:**
- **SHA-256:**

### WHO Immunization Data portal, Kazakhstan
- **Provides:** WUENIC MCV1 and MCV2 coverage estimates, Joint Reporting Form data
- **Organization:** World Health Organization
- **URL:**
- **Date downloaded:**
- **License:**
- **File size:**
- **SHA-256:**

### National statistical digest on public health
- **Provides:** incidence and immunization indicators by region, 2025 edition
- **Organization:** National Center for Public Health
- **URL:** nrchd.kz
- **Date downloaded:**
- **License:**
- **File size:**
- **SHA-256:**

### Population and births by region
- **Provides:** population by region and age, birth counts
- **Organization:** Bureau of National Statistics
- **URL:** stat.gov.kz
- **Date downloaded:**
- **License:** open data, Republic of Kazakhstan
- **File size:**
- **SHA-256:**

### National immunization schedule
- **Provides:** the official schedule and dose timing for childhood vaccination
- **Organization:** Government of Kazakhstan
- **URL:** adilet.zan.kz
- **Date downloaded:**
- **License:** official public legal text
- **File size:**
- **SHA-256:**

### Formal information request, regional monthly measles data
- **Provides:** regional monthly incidence series, if not otherwise published
- **Organization:** submitted to the relevant Kazakhstani health authority
- **URL:** n/a, submitted through the official government correspondence portal
- **Date submitted:**
- **Reference / tracking number:**
- **Date of response:**
- **Outcome:** (record the outcome even if it is a refusal or partial answer. A documented refusal is itself citable in the Limitations section.)
