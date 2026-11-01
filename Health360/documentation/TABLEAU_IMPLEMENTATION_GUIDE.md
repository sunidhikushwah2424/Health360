# Health360: Tableau Desktop & Tableau Public Implementation Guide
## Step-by-Step Instructions for Connecting, Designing, Storytelling & Publishing

---

### 1. Introduction
This guide provides complete instructions for replicating the Health360 analytics dashboards and guided narrative story inside **Tableau Desktop** or **Tableau Public**, matching the specifications and visual layouts from the project blueprint.

A pre-processed, Tableau-optimized dataset is included in the project at:
`data/tableau_healthcare_dataset.csv`

---

### 2. Connecting the Dataset in Tableau Desktop

1. Launch **Tableau Desktop** (or **Tableau Public Desktop Edition**).
2. On the left start pane, under **Connect**, click **Text File**.
3. Navigate to `Health360/data/tableau_healthcare_dataset.csv` and click **Open**.
4. Tableau will load the schema with 5,000 records.
5. Review the Data Source tab and verify data types:
   - `Patient_ID` → String (Abc)
   - `Age` → Number (Whole) (#)
   - `Gender` → String (Abc)
   - `BMI` → Number (Decimal) (#)
   - `Exercise_Level` → String (Abc)
   - `Smoking_Habits` → String (Abc)
   - `Alcohol_Consumption` → String (Abc)
   - `Blood_Pressure` → Number (Decimal) (#)
   - `Cholesterol` → Number (Whole) (#)
   - `Glucose_Levels` → Number (Whole) (#)
   - `Fatigue` → String (Abc)
   - `Heart_Disease` → String (Abc)
   - `Diabetes` → String (Abc)
   - `Stroke_History` → String (Abc)
   - `Overall_Health_Risk_Score` → Number (Decimal) (#)
   - `Age_Group` → String (Abc)
   - `BMI_Category` → String (Abc)

---

### 3. Authoring Calculated Fields in Tableau

Although `tableau_healthcare_dataset.csv` includes pre-materialized categorical columns, you can also author them as calculated fields in Tableau (as illustrated on page 37 of the project PDF):

#### Calculated Field 1: `[Age Group]`
1. Click the dropdown arrow next to the Search bar in the Data pane and select **Create Calculated Field...**
2. Name the field: `Age Group`
3. Enter the following formula:
```tableau
IF [Age] <= 30 THEN "Teenager"
ELSEIF [Age] <= 40 THEN "Young Adult"
ELSEIF [Age] <= 50 THEN "Adult"
ELSEIF [Age] <= 60 THEN "Middle Age"
ELSEIF [Age] <= 70 THEN "Senior"
ELSE "Old"
END
```
4. Click **OK**.

#### Calculated Field 2: `[BMI Category]`
```tableau
IF [BMI] < 18.5 THEN "Underweight"
ELSEIF [BMI] <= 24.9 THEN "Normal"
ELSEIF [BMI] <= 29.9 THEN "Overweight"
ELSE "Obese"
END
```

#### Calculated Field 3: `[Heart Disease Rate]`
```tableau
SUM(IF [Heart_Disease] = "Yes" THEN 1 ELSE 0 END) / COUNT([Patient_ID])
```

#### Calculated Field 4: `[Diabetes Rate]`
```tableau
SUM(IF [Diabetes] = "Yes" THEN 1 ELSE 0 END) / COUNT([Patient_ID])
```

---

### 4. Creating the 9 Individual Worksheets

#### Sheet 1: KPI Overview
- Drag `Number of Records` / `COUNT(Patient_ID)` to **Text**.
- Add calculated KPI tiles for Heart Disease Count, Diabetes Count, Average Blood Pressure, and Average BMI.

#### Sheet 2: Average Blood Pressure Across Age Groups (Bar Chart)
- Drag `Age Group` to **Columns**.
- Drag `Blood_Pressure` to **Rows**; change aggregation to **Average**.
- Drag `Age Group` to **Color**.
- Add reference line at `130 mmHg` on the Blood Pressure axis.

#### Sheet 3: Alcohol and Smoking Consumption Across Age Groups (Grouped Bar Chart)
- Drag `Age Group` to **Columns**.
- Create a measure for Smokers count and Alcohol consumers count.
- Place `Measure Names` on **Columns** and **Color**, and `Measure Values` on **Rows**.
- Select **Side-by-side Bars**.

#### Sheet 4: Exercise Level Distribution (Donut Chart)
- Change Marks type to **Pie**.
- Drag `Exercise_Level` to **Color** and **Label**.
- Drag `COUNT(Patient_ID)` to **Angle** and **Label** (Quick Table Calculation: Percent of Total).
- Create a dual-axis with a synchronized circle mark to form the donut hole.

#### Sheet 5: Patient Distribution by Age Group (Pie Chart)
- Change Marks type to **Pie**.
- Drag `Age Group` to **Color** and **Label**.
- Drag `COUNT(Patient_ID)` to **Angle** and **Label** (Percent of Total).

#### Sheet 6: Heart Disease vs Diabetes Prevalence by BMI Category (Grouped Bar Chart)
- Drag `BMI Category` to **Columns**.
- Place `Measure Names` (Heart Disease Count & Diabetes Count) on **Columns** and **Color**.
- Place `Measure Values` on **Rows**.

#### Sheet 7: BMI Category vs Heart Disease Rate (Bar Chart)
- Drag `BMI Category` to **Columns** (Sort: Obese, Overweight, Normal, Underweight).
- Drag `[Heart Disease Rate]` to **Rows**.
- Format axis as **Percentage**.

#### Sheet 8: Heart Disease by BMI Category and Exercise Level (Heat Map)
- Drag `Exercise_Level` to **Columns** (Active, Moderate, Sedentary).
- Drag `BMI Category` to **Rows** (Normal, Obese, Overweight, Underweight).
- Change Marks type to **Square**.
- Drag `[Heart Disease Rate]` to **Color** and **Label**.
- Select **Red-Yellow Colormap**.

#### Sheet 9: Age Group Distribution by Fatigue Condition (Stacked Bar Chart)
- Drag `Age Group` to **Rows**.
- Drag `COUNT(Patient_ID)` to **Columns**.
- Drag `Fatigue` to **Color** (Yes = Dark Blue, No = Light Blue).

---

### 5. Assembling the 4 Required Dashboards

1. **Dashboard 1: Healthcare Overview Dashboard**
   - Canvas Size: `Automatic` or `1200 x 800`.
   - Layout: Top KPI summary row, followed by Exercise Level Donut, Blood Pressure Bar Chart, and Alcohol/Smoking Grouped Bar Chart.
   - Add interactive filters for `Age Group`, `Gender`, and `BMI Category` set to apply to all related worksheets.

2. **Dashboard 2: Disease Analysis Dashboard**
   - Layout: BMI vs Heart Disease Rate, Heart Disease vs Diabetes Prevalence, and the BMI × Exercise Level Heat Map.

3. **Dashboard 3: Lifestyle Analysis Dashboard**
   - Layout: Exercise Level Distribution, Substance consumption by Age, and Age Group by Fatigue Condition.

4. **Dashboard 4: Patient Demographics Dashboard**
   - Layout: Age Group Pie Chart, BMI Tier Breakdown, and Gender Stratification.

---

### 6. Constructing the 5-Scene Tableau Story
*(Matching PDF Pages 23, 25, 53: "Smart Healthcare Analytics: Patient Risk & Lifestyle Insights")*

1. Click the **New Story** icon at the bottom of Tableau Desktop.
2. Title the story header: `Smart Healthcare Analytics: Patient Risk & Lifestyle Insights`.
3. Build the 5 story points (scenes):
   - **Scene 1 (Blank point title: "Patient Distribution By Age Group"):** Drag the Age Group Pie Chart into the canvas. Add caption describing the 5,000-patient demographic baseline.
   - **Scene 2 (Blank point title: "Age Group Distribution by Fatigue Condition"):** Drag the Fatigue Condition stacked bar chart. Add caption explaining the pervasive nature of fatigue across age tiers.
   - **Scene 3 (Blank point title: "Exercise Level Distribution"):** Drag the Exercise Donut chart. Add caption detailing the tripartite exertion split.
   - **Scene 4 (Blank point title: "Average Blood Pressure Across Age Groups"):** Drag the Blood Pressure bar chart. Add caption highlighting early-onset hypertension in young adults.
   - **Scene 5 (Blank point title: "Heart Disease by BMI Category and Exercise Level"):** Drag the Heat Map. Add caption synthesizing the compounding impact of obesity and inactivity, concluding with exercise recommendations.

---

### 7. Publishing to Tableau Public

1. In Tableau Desktop, go to **Server > Tableau Public > Save to Tableau Public As...** (or **File > Save to Tableau Public**).
2. If prompted, sign in with your **Tableau Public** account credentials (create a free account at [public.tableau.com](https://public.tableau.com) if you do not have one).
3. Name your workbook: `Health360 – Comprehensive Healthcare Risk & Disease Analysis`.
4. Click **Save**. Tableau will package the data extract and upload the workbook.
5. Your default web browser will automatically open to your published Tableau Public dashboard URL.
6. Click the **Share** icon at the bottom of your Tableau Public page and copy the **Link** or **Embed Code**.
7. In the Health360 web application, navigate to the **Tableau Hub** page (`/tableau`), paste your URL, and click **Load Embed** to display your live Tableau workbook!
