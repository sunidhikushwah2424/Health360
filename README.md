# Health360: Comprehensive Healthcare Risk & Disease Analysis

<div align="center">

![Health360 Logo](https://img.shields.io/badge/Health360-Healthcare%20Analytics-0284c7?style=for-the-badge&logo=heartbeat&logoColor=white)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Framework - Flask 3.1](https://img.shields.io/badge/Framework-Flask%203.1-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Visualization - Plotly 7.1](https://img.shields.io/badge/Visualization-Plotly%207.1-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/python/)
[![Data - Pandas & NumPy](https://img.shields.io/badge/Data%20Engine-Pandas%20%26%20NumPy-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![UI - Bootstrap 5.3](https://img.shields.io/badge/UI-Bootstrap%205.3-7952B3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![BI - Tableau Ready](https://img.shields.io/badge/BI%20Integration-Tableau%20Desktop%20%26%20Public-E97627.svg?logo=tableau&logoColor=white)](https://public.tableau.com)
[![Tests - 26 Passing](https://img.shields.io/badge/Unit%20%26%20Integration%20Tests-26%2F26%20Passing%20(100%25)-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**An interactive, full-stack healthcare risk analytics platform analyzing patient records, epidemiological patterns, and chronic disease prevalence across demographic, anthropometric, and lifestyle factors.**

*Developed in strict accordance with the SkillWallet Smart Healthcare & Risk Factor Analysis project specification.*

[Explore Dashboards](#-core-dashboards--web-pages) • [All 9 Visualizations](#-all-9-required-visualizations) • [Quick Start](#-quick-start--installation) • [Tableau Integration](#-tableau-integration--story) • [Documentation](#-project-documentation)

</div>

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Highlights & Architecture](#-key-highlights--architecture)
3. [Dataset & Clinical Data Dictionary](#-dataset--clinical-data-dictionary)
4. [All 9 Required Visualizations](#-all-9-required-visualizations)
5. [Core Dashboards & Web Pages](#-core-dashboards--web-pages)
6. [Technology Stack](#-technology-stack)
7. [Project Directory Structure](#-project-directory-structure)
8. [Quick Start & Installation](#-quick-start--installation)
9. [Running Tests & Benchmarks](#-running-tests--benchmarks)
10. [Tableau Desktop & Public Integration](#-tableau-integration--story)
11. [5-7 Minute Video Demonstration Guide](#-5-7-minute-video-demonstration-guide)
12. [Medical & Scientific Disclaimer](#-medical--scientific-disclaimer)

---

## 🩺 Project Overview

Modern healthcare organizations face the critical challenge of synthesizing high-dimensional patient records into actionable clinical intelligence. **Health360** bridges this gap by unifying:
- **Epidemiological Risk Modeling:** Evaluating blood pressure progression, obesity-related cardiac escalation, and glycemic disorders across 6 standardized life stages.
- **Dynamic Asynchronous Filtering:** Enabling sub-second cohort slicing without page reloads using vector calculations and `Plotly.react()`.
- **Tableau Business Intelligence:** Full dataset compatibility with Tableau Desktop and Tableau Public, featuring 4 core dashboards and a 5-scene guided narrative data story (*"Smart Healthcare Analytics: Patient Risk & Lifestyle Insights"*).
- **Automated Clinical Insights Engine:** Algorithmically generating human-readable observations from current cohort selections while strictly upholding that **correlation is not causation**.

---

## ⚡ Key Highlights & Architecture

```
                                  [ RAW DATA SOURCE ]
                       5,000 Records · 17 Clinical Attributes (Seed: 42)
                                           │
                                           ▼
                              [ UTILS / DATA PROCESSOR ]
                 - Null & Duplicate Validation (0 Nulls, 0 Dups)
                 - Age Group Bins (Teenager, Young Adult, Adult, Middle Age, Senior, Old)
                 - BMI Bins (Underweight, Normal, Overweight, Obese)
                 - Blood Pressure & Risk Score Categorization
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
          [ FLASK 3.1 BACKEND ]                       [ TABLEAU DATASET EXPORT ]
      - REST API Endpoints (/api/...)               tableau_healthcare_dataset.csv
      - In-Memory High-Speed Slicing                              │
      - Automated Healthcare Insights                             ▼
                    │                                   [ TABLEAU DESKTOP / PUBLIC ]
                    ▼                                   - 4 Specialized Dashboards
          [ RESPONSIVE FRONTEND ]                       - 5-Scene Narrative Story
      - Navy Blue & Teal Healthcare Theme               - Public Web Embedding
      - 6 Dynamic Animated KPI Cards
      - 9 Reactive Plotly 7.1 Charts
```

---

## 📊 Dataset & Clinical Data Dictionary

The project utilizes a validated 5,000-record synthetic clinical dataset (`data/healthcare_dataset.csv` and `data/cleaned_healthcare_dataset.csv`) generated with a fixed random seed (`seed=42`) for 100% reproducibility.

### Ingested Clinical Attributes (17 Fields)
| Field Name | Type | Range / Domain | Clinical Context & Purpose |
| :--- | :--- | :--- | :--- |
| `Patient_ID` | String | `PID-10001` to `PID-15000` | De-identified synthetic patient identifier |
| `Age` | Integer | 18 – 85 years | Basis for 6 life-stage calculated age cohorts |
| `Gender` | Categorical | Male (50.5%), Female (49.5%) | Demographic stratification |
| `BMI` | Float | 15.2 – 44.8 kg/m² | Anthropometric measure of body fat |
| `Exercise_Level` | Categorical | Active, Moderate, Sedentary | Self-reported weekly cardiovascular activity |
| `Smoking_Habits` | Binary | Yes, No | Tobacco smoke exposure |
| `Alcohol_Consumption`| Binary | Yes, No | Regular alcohol consumption |
| `Blood_Pressure` | Float | 98.0 – 185.0 mmHg | Resting systolic blood pressure |
| `Cholesterol` | Integer | 120 – 320 mg/dL | Total serum cholesterol level |
| `Glucose_Levels` | Integer | 65 – 275 mg/dL | Fasting blood glucose concentration |
| `Fatigue` | Binary | Yes, No | Persistent unrefreshing exhaustion symptom |
| `Chest_Pain` | Binary | Yes, No | Reported thoracic or anginal discomfort |
| `Dizziness` | Binary | Yes, No | Vertiginous or orthostatic lightheadedness |
| `Heart_Disease` | Binary | Yes, No | Confirmed history of coronary artery disease |
| `Diabetes` | Binary | Yes, No | Confirmed Type 2 Diabetes Mellitus |
| `Stroke_History` | Binary | Yes, No | Prior ischemic or hemorrhagic stroke |
| `Overall_Health_Risk_Score`| Float | 10.0 – 98.0 | Multivariate weighted clinical risk index |

### Standardized Calculated Categorical Fields
1. **Age Groups (Matching Project Specification):**
   - `18–30`: **Teenager** (~20.4%)
   - `31–40`: **Young Adult** (~16.0%)
   - `41–50`: **Adult** (~16.3%)
   - `51–60`: **Middle Age** (~16.1%)
   - `61–70`: **Senior** (~16.4%)
   - `>70`: **Old** (~14.9%)
2. **BMI Categories:**
   - `<18.5`: **Underweight**
   - `18.5–24.9`: **Normal**
   - `25.0–29.9`: **Overweight**
   - `≥30.0`: **Obese**
3. **Blood Pressure Categories:** Normal (<120), Elevated (120-129), Stage 1 HTN (130-139), Stage 2 HTN (≥140).

---

## 📈 All 9 Required Visualizations

All nine visualizations specified in the project specification are fully implemented using Plotly 7.1 and rendered via `visualizations/charts.py`:

| # | Visualization Name | Chart Type | Key Metrics & Dimensions | Analytical & Clinical Finding |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Patient Health & Disease Overview** | KPI Cards & Dual Gauges | Total Patients (5,000), HD Cases, Diabetes Cases, Stroke Cases, Mean BP, Mean Risk | Provides foundational baseline denominators for population health assessment. |
| **2** | **Average Blood Pressure Across Age Groups** | Bar Chart + Reference Line | X: 6 Age Groups; Y: Mean Systolic BP (mmHg); 130 mmHg HTN line | Reveals that average BP exceeds the 130 mmHg hypertension threshold across youth and adulthood alike. |
| **3** | **Alcohol and Smoking Across Age Groups** | Grouped Bar Chart | X: Age Groups; Y: Patient Counts; Color: Smokers vs Alcohol Consumers | Shows alcohol consumption peaks in youth while tobacco use persists through middle and senior age. |
| **4** | **Exercise Level Distribution** | Donut Chart (Hole = 0.55) | Slices: Active (33.5%), Moderate (33.5%), Sedentary (32.9%) | Validates balanced physical exertion baselines across the patient cohort. |
| **5** | **Patient Distribution by Age Group** | Pie Chart | Slices: Teenager, Young Adult, Adult, Middle Age, Senior, Old | Demonstrates balanced demographic representation across adult development stages. |
| **6** | **Heart Disease vs Diabetes Prevalence by BMI** | Grouped Bar Chart | X: BMI Category; Y: Patient Counts for Heart Disease vs Diabetes | Illustrates the parallel escalation of cardiovascular and endocrine morbidities with body mass. |
| **7** | **BMI Category vs Heart Disease Rate** | Gradient Bar Chart | X: BMI Category; Y: Heart Disease Prevalence (%) | Quantifies the steep risk gradient: 20.64% (Underweight) → 25.97% (Normal) → 32.91% (Overweight) → 39.98% (Obese). |
| **8** | **Heart Disease by BMI & Exercise Level** | 4×3 Matrix Heat Map | Y: BMI Category; X: Exercise Level; Cells: Exact Heart Disease Rate | Identifies the highest-risk group: **Obese + Sedentary (42.86%)** and shows exercise buffers risk in all BMI tiers. |
| **9** | **Age Group Distribution by Fatigue Condition**| Stacked Horizontal Bar | Y: Age Groups; X: Patient Counts (Fatigue: Yes vs Fatigue: No) | Demonstrates persistent fatigue affects ~44% across all age groups, linking strongly to inactivity. |

---

## 💻 Core Dashboards & Web Pages

The web application contains 9 dedicated interfaces:
1. **Overview Dashboard (`/`):** The primary command center containing 6 dynamic KPI cards, the global multi-factor filter bar, all 9 required charts, and real-time AJAX reactivity.
2. **Patient Analytics (`/patient-analytics`):** Anthropometrics, demographic ratios, and continuous Bivariate Scatter (Age vs BMI vs Risk Score).
3. **Chronic Disease Analysis (`/disease-analysis`):** Multi-morbidity breakdown (Heart Disease, Diabetes, and Stroke co-occurrence).
4. **Lifestyle Analysis (`/lifestyle-analysis`):** Deep dive into physical exertion, tobacco habits, alcohol intake, and symptomatic fatigue.
5. **All 9 Visualizations Gallery (`/visualizations`):** Complete chart catalog with full descriptions, clinical rationale, and raw data summaries.
6. **Automated Healthcare Insights (`/insights`):** Automated statistical synthesis engine calculating dominant patterns and preventive takeaways.
7. **Tableau Data Story (`/story`):** 5-scene guided narrative presentation (*"Smart Healthcare Analytics: Patient Risk & Lifestyle Insights"*).
8. **Patient Dataset Explorer (`/data-explorer`):** Tabular data viewer with search, filtering, and instant CSV download.
9. **Tableau Integration Hub (`/tableau`):** Step-by-step instructions for Tableau Desktop, publishing to Tableau Public, and a live Tableau web embedder.
10. **About & Methodology (`/about`):** Architecture overview, clinical data dictionary, and developer credentials.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.14, Flask 3.1.3, Werkzeug, Jinja2
- **Data Engineering:** Pandas 3.1.0, NumPy 2.5.4
- **Visualization:** Plotly 7.1.0, Plotly.js 2.35.2
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3.3, Bootstrap Icons 1.11.3
- **Business Intelligence:** Tableau Desktop, Tableau Public
- **Quality Assurance:** Python `unittest`, Custom Performance Stress Test Suite

---

## 📁 Project Directory Structure

```
Health360/
├── app.py                            # Main Flask server & web application controller
├── run.py                            # Production-ready application launcher
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation and quick-start guide
├── .gitignore                        # Git ignore rules
│
├── data/
│   ├── generate_dataset.py           # 5,000-record synthetic data generator (seed: 42)
│   ├── healthcare_dataset.csv        # Primary synthetic clinical dataset (17 attributes)
│   ├── cleaned_healthcare_dataset.csv# Preprocessed & validated dataset (0 nulls)
│   └── tableau_healthcare_dataset.csv# Pre-formatted for Tableau Desktop & Public
│
├── utils/
│   ├── __init__.py
│   ├── data_processor.py             # Data ingestion, cleaning, binning & dynamic filtering
│   └── insights_generator.py         # Dynamic clinical insights generation engine
│
├── visualizations/
│   ├── __init__.py
│   └── charts.py                     # All 9 required Plotly charts & layout configurations
│
├── templates/
│   ├── base.html                     # Master layout with navy sidebar & top navigation
│   ├── index.html                    # Main Overview Dashboard (All 9 charts & KPIs)
│   ├── patient_analytics.html        # Demographics, age cohorts & BMI distributions
│   ├── disease_analysis.html         # Heart Disease, Diabetes, Stroke co-morbidities
│   ├── lifestyle_analysis.html       # Physical activity, smoking, alcohol & fatigue
│   ├── visualizations.html           # Full gallery of all 9 charts with data tables
│   ├── insights.html                 # Automated healthcare insights & observations
│   ├── story.html                    # Tableau-style 5-Scene Interactive Story
│   ├── data_explorer.html            # Tabular dataset browser with search & pagination
│   ├── tableau_hub.html              # Tableau integration hub, embed viewer & guide
│   └── about.html                    # Project methodology, data dictionary & architecture
│
├── static/
│   ├── css/
│   │   └── style.css                 # Custom healthcare theme CSS
│   ├── js/
│   │   └── dashboard.js              # Real-time AJAX dynamic filtering & Plotly updates
│   └── images/
│
├── tests/
│   ├── test_data_pipeline.py         # Unit tests for preprocessing & calculated fields
│   ├── test_visualizations.py        # Unit tests for chart rendering
│   ├── test_app.py                   # Integration tests for Flask routes & endpoints
│   └── performance_test.py           # Latency, stress & memory benchmarking suite
│
└── documentation/
    ├── PROJECT_DOCUMENTATION.md      # Comprehensive technical engineering report
    ├── TABLEAU_IMPLEMENTATION_GUIDE.md # Step-by-step Tableau Desktop & Public guide
    ├── PERFORMANCE_TEST_REPORT.md    # Performance stress test results
    └── DEMONSTRATION_GUIDE.md        # 5–7 min video presentation script & defense Q&A
```

---

## 🚀 Quick Start & Installation

### 1. Clone or Open the Repository
```bash
git clone https://github.com/<your-username>/Health360.git
cd Health360
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Web Application
```bash
python run.py
```
*Or directly via Flask:*
```bash
python app.py
```

### 5. Access the Platform
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 🧪 Running Tests & Benchmarks

### Execute Unit & Integration Tests (26 Tests)
```bash
python -m unittest discover -s tests
```
*Expected Result:* `Ran 26 tests in ~3.0s ... OK (100% Passed)`

### Run the Performance Stress & Latency Suite
```bash
python tests/performance_test.py
```

### Measured Performance Benchmarks:
| Operation | Measured Latency | Standard Target | Status |
| :--- | :--- | :--- | :--- |
| **Dataset Ingestion & Validation (5,000 rows)** | **66.90 ms** | < 500 ms | **EXCELLENT** |
| **Dynamic KPI Recalculation** | **0.166 ms** | < 25 ms | **OPTIMAL** |
| **Batch Generation of All 9 Charts** | **131.53 ms** | < 300 ms | **OPTIMAL** |
| **Average Per-Chart Render Time** | **14.61 ms** | < 50 ms | **OPTIMAL** |
| **Multi-Dimensional Filter Queries** | **< 2.50 ms** | < 20 ms | **INSTANT** |
| **In-Memory Memory Footprint** | **3.37 MB** | < 50 MB | **ULTRA-LIGHT** |

---

## 📊 Tableau Integration & Story

A pre-formatted Tableau dataset is included in `data/tableau_healthcare_dataset.csv`.

### Step-by-Step Tableau Workflow:
1. Open **Tableau Desktop** (or Tableau Public Desktop).
2. Connect to `data/tableau_healthcare_dataset.csv`.
3. Create Calculated Fields (as detailed in `documentation/TABLEAU_IMPLEMENTATION_GUIDE.md`):
   ```tableau
   // [Age Group]
   IF [Age] <= 30 THEN "Teenager"
   ELSEIF [Age] <= 40 THEN "Young Adult"
   ELSEIF [Age] <= 50 THEN "Adult"
   ELSEIF [Age] <= 60 THEN "Middle Age"
   ELSEIF [Age] <= 70 THEN "Senior"
   ELSE "Old"
   END
   ```
4. Build the 4 Dashboards:
   - **Healthcare Overview Dashboard**
   - **Disease Analysis Dashboard**
   - **Lifestyle Analysis Dashboard**
   - **Patient Demographics Dashboard**
5. Construct the 5-Scene Story:
   - **Point 1:** Patient Distribution by Age Group
   - **Point 2:** Age Group Distribution by Fatigue Condition
   - **Point 3:** Exercise Level Distribution
   - **Point 4:** Average Blood Pressure Across Age Groups
   - **Point 5:** Heart Disease by BMI Category & Exercise Level
6. Publish to **Tableau Public** (**File > Save to Tableau Public**) and paste your live URL into the Health360 **Tableau Hub** (`/tableau`) to embed it.

---

## 🎥 5-7 Minute Video Demonstration Guide

For project presentations, capstone defense, or video recordings (matching Page 57 of the project guide), a detailed script is provided in [`documentation/DEMONSTRATION_GUIDE.md`](documentation/DEMONSTRATION_GUIDE.md):

- **0:00 – 1:00:** Problem Statement, Platform Purpose & Technology Stack.
- **1:00 – 2:15:** Data Pipeline, 5,000-Record Ingestion, Validation & Engineered Fields.
- **2:15 – 4:00:** Interactive Walkthrough of All 9 Visualizations & Live Multi-Filter Reactivity.
- **4:00 – 5:15:** Tableau Data Story: *"Patient Risk & Lifestyle Insights"* (5 Scenes).
- **5:15 – 6:30:** Automated Healthcare Insights Engine, Performance Benchmarks & Defense Q&A.

---

## ⚕️ Medical & Scientific Disclaimer

**Health360 is an analytical and educational platform, NOT a medical diagnosis system.**

All synthetic patient records and epidemiological analyses are generated for educational demonstration, public health research, and academic evaluation. Observed relationships represent statistical correlations and must never be interpreted as clinical proof of causation or used to guide individual medical diagnosis or treatment decisions.

---

## 📜 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Health360 Healthcare Analytics Platform · Engineered with Flask, Pandas, Plotly & Tableau · 2026</sub>
</div>
