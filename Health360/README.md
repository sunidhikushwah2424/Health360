# Health360: Comprehensive Healthcare Risk & Disease Analysis

[![Python Version](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.1-green.svg)](https://flask.palletsprojects.com/)
[![Visualization](https://img.shields.io/badge/Visualization-Plotly%207.1-orange.svg)](https://plotly.com/python/)
[![BI Integration](https://img.shields.io/badge/Tableau-Desktop%20%26%20Public-red.svg)](https://public.tableau.com)
[![Build Status](https://img.shields.io/badge/Tests-26%20Passing-brightgreen.svg)]()

> **Health360** is a full-stack healthcare analytics platform designed to analyze patient health records, examine epidemiological relationships, and visualize multi-morbidity risks across demographic, lifestyle, and clinical factors.

Developed in strict adherence to the **SkillWallet Smart Healthcare & Risk Factor Analysis** project specification.

---

## 🌟 Key Platform Features

- **Dynamic Interactive Dashboard:** Real-time multi-dimensional cohort filtering across Age Group, Gender, BMI Category, Exercise Level, Smoking Habits, Alcohol Intake, and Disease Status without page reloads.
- **All 9 Required Project Visualizations:**
  1. **KPI Overview:** Dynamic patient counts, disease prevalence rates, mean blood pressure, and health risk scores.
  2. **Bar Chart:** Average Blood Pressure Across Age Groups with 130 mmHg Hypertension reference line.
  3. **Grouped Bar Chart:** Alcohol and Smoking Consumption Across Age Groups.
  4. **Donut Chart:** Exercise Level Distribution (Active, Moderate, Sedentary).
  5. **Pie Chart:** Patient Distribution by Age Group (Teenager, Young Adult, Adult, Middle Age, Senior, Old).
  6. **Grouped Bar Chart:** Heart Disease vs Diabetes Prevalence by BMI Category.
  7. **Bar Chart:** BMI Category vs Heart Disease Rate (20.64% to 39.98%).
  8. **Heat Map:** Heart Disease Rate by BMI Category (Y) and Exercise Level (X).
  9. **Bar Chart:** Age Group Distribution by Fatigue Condition.
- **Tableau-Style Guided Story Player:** 5-scene interactive data presentation (*"Smart Healthcare Analytics: Patient Risk & Lifestyle Insights"*).
- **Automated Healthcare Insights Engine:** Algorithmically generates statistical summaries and clinical observations directly from the active cohort.
- **Dataset Management & Explorer:** Ingests and inspects 5,000 synthetic patient records across 17 clinical attributes with zero missing values and zero duplicates.
- **Tableau Integration Hub:** Ready-to-use dataset (`tableau_healthcare_dataset.csv`), calculated field formulas, and Tableau Public live web embedding container.

---

## 🏗️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend & Web Integration** | Python 3.14, Flask 3.1, Jinja2 |
| **Data Processing & Analytics** | Pandas 3.1, NumPy 2.5 |
| **Interactive Visualizations** | Plotly 7.1, Plotly.js 2.35.2 |
| **Frontend UI/UX** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons |
| **Business Intelligence** | Tableau Desktop, Tableau Public |
| **Quality Assurance** | Python `unittest` (26 passing tests), Performance Benchmark Suite |

---

## 📂 Project Structure

```
Health360/
├── app.py                            # Main Flask server & web application controller
├── run.py                            # Convenience server launcher
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation and quick-start guide
├── data/
│   ├── generate_dataset.py           # Synthetic dataset generator (5,000 records, seed=42)
│   ├── healthcare_dataset.csv        # Primary synthetic patient dataset
│   ├── cleaned_healthcare_dataset.csv# Preprocessed & validated dataset
│   └── tableau_healthcare_dataset.csv# Pre-formatted for Tableau Desktop & Public
├── utils/
│   ├── __init__.py
│   ├── data_processor.py             # Data ingestion, validation, cleaning & filtering engine
│   └── insights_generator.py         # Dynamic clinical insights generation engine
├── visualizations/
│   ├── __init__.py
│   └── charts.py                     # All 9 required Plotly charts & layout configurations
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
├── static/
│   ├── css/
│   │   └── style.css                 # Custom healthcare theme CSS
│   ├── js/
│   │   └── dashboard.js              # Real-time AJAX dynamic filtering & Plotly updates
│   └── images/
├── tests/
│   ├── test_data_pipeline.py         # Unit tests for data cleaning & feature logic
│   ├── test_visualizations.py        # Unit tests for chart rendering
│   ├── test_app.py                   # Integration tests for Flask routes & endpoints
│   └── performance_test.py           # Latency, stress & memory benchmarking suite
└── documentation/
    ├── PROJECT_DOCUMENTATION.md      # Comprehensive technical documentation
    ├── TABLEAU_IMPLEMENTATION_GUIDE.md # Step-by-step Tableau Desktop & Public guide
    ├── PERFORMANCE_TEST_REPORT.md    # Performance stress test results
    └── DEMONSTRATION_GUIDE.md        # 5-7 minute video presentation script & Q&A prep
```

---

## 🚀 Quick Start & Execution

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Installation
Open your terminal in the `Health360` directory and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Running the Application
Launch the Flask development server:
```bash
python run.py
```
*Or:*
```bash
python app.py
```

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

### Run Performance Stress Benchmarking Suite
```bash
python tests/performance_test.py
```

**Measured Benchmarks:**
- Dataset Ingestion (5,000 records): **66.9 ms**
- Dynamic KPI Recalculation: **0.166 ms**
- Batch Generation of All 9 Charts: **131.5 ms** (14.6 ms/chart)
- Multi-Filter Latency: **~2.1 ms**
- In-Memory Footprint: **3.37 MB**

---

## 📊 Tableau Integration

1. In Tableau Desktop, connect to `data/tableau_healthcare_dataset.csv`.
2. Follow the calculated field formulas provided in `documentation/TABLEAU_IMPLEMENTATION_GUIDE.md`:
   - `[Age Group]`: Teenager (18–30), Young Adult (31–40), Adult (41–50), Middle Age (51–60), Senior (61–70), Old (>70).
   - `[BMI Category]`: Underweight (<18.5), Normal (18.5–24.9), Overweight (25–29.9), Obese (≥30.0).
3. Build the 4 core dashboards and the 5-scene story *"Smart Healthcare Analytics: Patient Risk & Lifestyle Insights"*.
4. Publish to Tableau Public (**File > Save to Tableau Public**) and paste the link into the **Tableau Hub** (`/tableau`) for seamless web embedding.

---

## ⚕️ Scientific & Medical Disclaimer

**Health360 is an analytical and educational platform, NOT a medical diagnosis system.**

All analyses and synthetic patient records are intended for public health researchers, data scientists, and students exploring epidemiological methodologies. Observed relationships represent statistical correlations and must never be interpreted as clinical proof of causation or utilized for individual medical diagnosis or treatment decisions.
