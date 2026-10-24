# Healthcare Facility Analytics — Dataset Documentation & Data Dictionary

## 1. Official Dataset Provenance
- **Dataset Name:** Hospital Quarterly Financial & Utilization Report – Complete Data Set
- **Publisher:** State of California Department of Health Care Access and Information (HCAI), formerly OSHPD
- **Host Portal:** HealthData.gov
- **Official URL:** [https://healthdata.gov/State/Hospital-Quarterly-Financial-Utilization-Report-Co/8j3z-qxvr](https://healthdata.gov/State/Hospital-Quarterly-Financial-Utilization-Report-Co/8j3z-qxvr)
- **Harvest Source:** [https://data.chhs.ca.gov/dataset/hospital-quarterly-financial-utilization-report-complete-data-set](https://data.chhs.ca.gov/dataset/hospital-quarterly-financial-utilization-report-complete-data-set)
- **License:** Open Data Commons Open Database License (ODC-ODbL)
- **Reporting Frequency:** Quarterly (Every three months)

---

## 2. Reporting Unit & Multi-Period Structure
Each raw record submitted to HCAI represents a **Hospital-Quarter observation**, indexed by:
- `FAC_NO`: Unique facility license number
- `YEAR_QTR`: Year and quarter code (e.g., `20231` for 2023 Q1, `20234` for 2023 Q4)

### Distinction: Quarterly Filings vs. Annual Facility Profiles
- **Hospital-Quarter Observations:** Captures dynamic seasonal shifts (e.g., winter inpatient spikes, respiratory virus season, periodic billing reconciliations). The multi-quarter raw ingest comprises **2,192 quarterly filings** across 5 reporting periods (2023 Q1 through 2024 Q1).
- **Annualized Facility Profiles:** For the primary unsupervised clustering task, all four quarters of calendar year 2023 (`20231`, `20232`, `20233`, `20234`) were aggregated for facilities reporting continuously across all four quarters (**N = 428 facilities**). Capacity metrics were averaged, while financial flows and patient volumes were summed across the full 365.25-day operating cycle. This prevents autocorrelation, eliminates seasonal distortion, and creates a stable peer-group benchmark.

---

## 3. Data Cleaning, Exclusions & Quality Audit
1. **Operating Status Filter:** Facilities marked with `OP_STATUS == 'Closed'` (3 records) were excluded.
2. **Zero Capacity / Inactive Facilities:** Records with zero available beds (`AVL_BEDS <= 0`), zero patient discharges (`DIS_TOT <= 0`), or non-positive operational expenses (`TOT_OP_EXP <= 0`) were pruned (6 records).
3. **Safe Division Formulation:** All ratio calculations implement zero-division protection to avoid infinity errors.
4. **Outlier Mitigation:** Highly skewed financial ratios (`OP_MARGIN`, `EXP_REV_RATIO`, `ALOS`, `OUTPATIENT_RATIO`) were winsorized between the 1st and 99th percentiles before distance-based clustering.
5. **Missing Value Rate:** 0.0% missingness across all 8 engineered analytical indicators in the final analytical cohort ($N = 428$).

---

## 4. Complete Data Dictionary

| Variable Code | Canonical Name | Conceptual Definition | Measurement Unit | Aggregation Method |
| :--- | :--- | :--- | :--- | :--- |
| `FAC_NO` | Facility Number | Unique state regulatory license identifier | Categorical ID | Primary Key |
| `FAC_NAME` | Facility Name | Official registered name of the hospital | Text String | Identifier |
| `COUNTY_NAME` | County | California county where facility operates | Text String | Geographic grouping |
| `TYPE_CNTRL` | Control Type | Institutional ownership (Non-profit, Investor-owned, County, City, State) | Categorical | Governance grouping |
| `TYPE_HOSP` | Hospital Type | Functional classification (General Acute, Psychiatric, Acute Specialty) | Categorical | Clinical scope |
| `LIC_BEDS` | Licensed Beds | State-authorized bed capacity | Integer count | Annual Mean |
| `AVL_BEDS` | Available Beds | Physically operational beds immediately ready for occupancy | Integer count | Annual Mean |
| `STF_BEDS` | Staffed Beds | Beds staffed with qualified nursing/clinical personnel | Integer count | Annual Mean |
| `DIS_TOT` | Total Discharges | Total formalized inpatient patient discharges | Count | Annual Sum |
| `DAY_TOT` | Total Patient Days | Total inpatient care bed-days delivered | Count | Annual Sum |
| `VIS_TOT` | Total Outpatient Visits | Total outpatient clinical, surgical, and emergency visits | Count | Annual Sum |
| `NET_TOT` | Net Patient Revenue | Net patient billing revenue post-contractual allowances | US Dollars (\$) | Annual Sum |
| `OTH_OP_REV` | Other Operating Revenue | Ancillary operating income (cafeteria, research, clinics) | US Dollars (\$) | Annual Sum |
| `TOT_OP_EXP` | Total Operating Expenses | Total audited operating expenses (salaries, supplies, facility) | US Dollars (\$) | Annual Sum |
| `OP_MARGIN` | Operating Margin | `(Total Operating Revenue - Operating Expenses) / Total Operating Revenue` | Ratio | Engineered Indicator |
| `EXP_REV_RATIO` | Expense-to-Revenue Ratio | `Total Operating Expenses / Total Operating Revenue` | Ratio | Engineered Indicator |
| `REV_PER_BED` | Revenue per Available Bed | `Total Operating Revenue / Available Beds` | \$ / Bed | Engineered Indicator |
| `EXP_PER_BED` | Expense per Available Bed | `Total Operating Expenses / Available Beds` | \$ / Bed | Engineered Indicator |
| `OCCUPANCY_RATE` | Bed Occupancy Rate | `Total Inpatient Days / (Available Beds * 365.25)` | Percentage | Engineered Indicator |
| `STF_AVL_RATIO` | Staffed Bed Ratio | `Staffed Beds / Available Beds` | Ratio | Engineered Indicator |
| `ALOS` | Average Length of Stay | `Total Inpatient Days / Total Discharges` | Days | Engineered Indicator |
| `OUTPATIENT_RATIO`| Outpatient Intensity | `Total Outpatient Visits / Total Inpatient Days` | Ratio | Engineered Indicator |

---

## 5. Instructions for Manual Dataset Download
If downloading programmatically via `python scripts/fetch_quarterly_data.py` is restricted on your network:
1. Navigate to the official HCAI data portal: [https://data.chhs.ca.gov/dataset/hospital-quarterly-financial-utilization-report-complete-data-set](https://data.chhs.ca.gov/dataset/hospital-quarterly-financial-utilization-report-complete-data-set)
2. Locate the resources:
   - `2023 Quarter 1 - Complete Data Set` -> Download `2023_q1.xlsx`
   - `2023 Quarter 2 - Complete Data Set` -> Download `2023_q2.xlsx`
   - `2023 Quarter 3 - Complete Data Set` -> Download `2023_q3.xlsx`
   - `2023 Quarter 4 - Complete Data Set` -> Download `2023_q4.xlsx`
   - `2024 Quarter 1 - Complete Data Set` -> Download `2024_q1.xlsx`
3. Place all five `.xlsx` files into the `data/raw/` directory.
4. Execute `python scripts/fetch_quarterly_data.py` to compile `combined_quarterly_raw.csv`.
