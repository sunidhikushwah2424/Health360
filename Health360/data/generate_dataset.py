"""
Health360 Synthetic Healthcare Dataset Generator
Generates a realistic 5,000-record synthetic healthcare dataset for educational and analytical purposes.
Includes 17 standard clinical and lifestyle attributes with clinical correlations matching project specifications.
"""

import numpy as np
import pandas as pd
import os

def generate_health360_dataset(output_path, num_records=5000, seed=42):
    np.random.seed(seed)
    
    # 1. Patient ID
    patient_ids = [f"PID-{10001 + i}" for i in range(num_records)]
    
    # 2. Age (18 to 85)
    # Calibrated distribution across age brackets:
    # 18-30 (Teenager ~20.4%), 31-40 (Young Adult ~16%), 41-50 (Adult ~16.3%),
    # 51-60 (Middle Age ~16.1%), 61-70 (Senior ~16.4%), 71-85 (Old ~16.0%)
    bracket_probs = [0.2038, 0.1596, 0.1626, 0.1608, 0.1638, 0.1494]
    bracket_choices = np.random.choice(6, size=num_records, p=bracket_probs)
    
    ages = []
    for b in bracket_choices:
        if b == 0:
            ages.append(np.random.randint(18, 31))
        elif b == 1:
            ages.append(np.random.randint(31, 41))
        elif b == 2:
            ages.append(np.random.randint(41, 51))
        elif b == 3:
            ages.append(np.random.randint(51, 61))
        elif b == 4:
            ages.append(np.random.randint(61, 71))
        else:
            ages.append(np.random.randint(71, 86))
            
    ages = np.array(ages)
    
    # 3. Gender
    genders = np.random.choice(['Male', 'Female'], size=num_records, p=[0.505, 0.495])
    
    # 4. Exercise Level (~33% Sedentary, ~33.5% Moderate, ~33.5% Active)
    exercise_levels = np.random.choice(['Sedentary', 'Moderate', 'Active'], size=num_records, p=[0.3294, 0.3354, 0.3352])
    
    # 5. Smoking Habits & Alcohol Consumption (~28% Smoker, ~38% Drinker)
    smoking_probs = np.where(genders == 'Male', 0.31, 0.24)
    smoking_habits = np.where(np.random.rand(num_records) < smoking_probs, 'Yes', 'No')
    
    alcohol_probs = np.where(genders == 'Male', 0.42, 0.34)
    alcohol_consumption = np.where(np.random.rand(num_records) < alcohol_probs, 'Yes', 'No')
    
    # 6. BMI calculation (15.5 to 44.5)
    # Influenced slightly by age and exercise
    base_bmi = np.random.normal(26.8, 5.2, num_records)
    # Adjust for exercise
    exercise_bmi_adj = np.where(exercise_levels == 'Active', -1.8, 
                               np.where(exercise_levels == 'Moderate', -0.5, 1.8))
    bmis = np.clip(np.round(base_bmi + exercise_bmi_adj, 1), 15.2, 44.8)
    
    # Derive BMI categories to calibrate disease prevalence according to PDF benchmarks:
    # Obese: ~40% Heart Disease, Overweight: ~33%, Normal: ~26%, Underweight: ~20%
    bmi_cats = []
    for b in bmis:
        if b < 18.5:
            bmi_cats.append('Underweight')
        elif b <= 24.9:
            bmi_cats.append('Normal')
        elif b <= 29.9:
            bmi_cats.append('Overweight')
        else:
            bmi_cats.append('Obese')
    bmi_cats = np.array(bmi_cats)
    
    # 7. Blood Pressure (Systolic mmHg)
    # PDF benchmarks: Old: ~135.67, Young Adult: ~134.67, Teenager: ~134.50, Senior: ~134.34, Middle Age: ~133.97, Adult: ~133.61
    bp_base = np.random.normal(134.2, 12.5, num_records)
    # Adjust slightly by age group
    age_bp_adj = np.zeros(num_records)
    for i, a in enumerate(ages):
        if a <= 30:
            age_bp_adj[i] = 0.3
        elif a <= 40:
            age_bp_adj[i] = 0.5
        elif a <= 50:
            age_bp_adj[i] = -0.6
        elif a <= 60:
            age_bp_adj[i] = -0.2
        elif a <= 70:
            age_bp_adj[i] = 0.1
        else:
            age_bp_adj[i] = 1.5
            
    # Add lifestyle effects
    lifestyle_bp_adj = np.where(smoking_habits == 'Yes', 2.0, 0) + np.where(exercise_levels == 'Sedentary', 1.5, -1.0)
    blood_pressure = np.round(np.clip(bp_base + age_bp_adj + lifestyle_bp_adj, 98.0, 185.0), 1)
    
    # 8. Cholesterol (mg/dL) - Normal ~160-199, Borderline 200-239, High 240+
    chol_base = np.random.normal(195, 32, num_records)
    chol_adj = (ages - 45) * 0.4 + (bmis - 25) * 0.9
    cholesterol = np.round(np.clip(chol_base + chol_adj, 120, 320)).astype(int)
    
    # 9. Glucose Levels (mg/dL) - Normal 70-99, Prediabetes 100-125, Diabetes 126+
    glucose_base = np.random.normal(105, 28, num_records)
    glucose_adj = (bmis - 25) * 1.5 + (ages - 40) * 0.3
    glucose_levels = np.round(np.clip(glucose_base + glucose_adj, 65, 275)).astype(int)
    
    # 10. Chronic Conditions: Heart Disease, Diabetes, Stroke History
    # Heart disease calibrated precisely with BMI category and exercise level
    hd_prob = np.zeros(num_records)
    for i in range(num_records):
        cat = bmi_cats[i]
        ex = exercise_levels[i]
        if cat == 'Obese':
            p = 0.3768 if ex == 'Active' else (0.3993 if ex == 'Moderate' else 0.4286)
        elif cat == 'Overweight':
            p = 0.3068 if ex == 'Active' else (0.3450 if ex == 'Moderate' else 0.3395)
        elif cat == 'Normal':
            p = 0.2529 if ex == 'Active' else (0.2609 if ex == 'Moderate' else 0.2579)
        else: # Underweight
            p = 0.2222 if ex == 'Active' else (0.2046 if ex == 'Moderate' else 0.1879)
        
        # Age adjustment
        if ages[i] > 60:
            p += 0.04
        if smoking_habits[i] == 'Yes':
            p += 0.03
        hd_prob[i] = np.clip(p, 0.05, 0.85)
        
    heart_disease = np.where(np.random.rand(num_records) < hd_prob, 'Yes', 'No')
    
    # Diabetes: strongly related to glucose levels and BMI
    diab_prob = 0.10 + 0.012 * (bmis - 20) + np.where(glucose_levels > 125, 0.35, 0.02)
    diabetes = np.where(np.random.rand(num_records) < np.clip(diab_prob, 0.04, 0.75), 'Yes', 'No')
    
    # Stroke History: related to age, blood pressure, heart disease, smoking
    stroke_prob = 0.04 + (ages - 40) * 0.002 + np.where(blood_pressure > 140, 0.08, 0.0) + \
                  np.where(heart_disease == 'Yes', 0.09, 0.0) + np.where(smoking_habits == 'Yes', 0.03, 0.0)
    stroke_history = np.where(np.random.rand(num_records) < np.clip(stroke_prob, 0.02, 0.40), 'Yes', 'No')
    
    # 11. Symptoms: Fatigue, Chest Pain, Dizziness
    # Fatigue: matches PDF screenshot (~390-440 per age group, higher in sedentary and chronic illness)
    fatigue_prob = 0.38 + np.where(exercise_levels == 'Sedentary', 0.12, -0.05) + \
                   np.where(diabetes == 'Yes', 0.10, 0.0) + np.where(heart_disease == 'Yes', 0.08, 0.0)
    fatigue = np.where(np.random.rand(num_records) < np.clip(fatigue_prob, 0.15, 0.80), 'Yes', 'No')
    
    chest_pain_prob = 0.12 + np.where(heart_disease == 'Yes', 0.30, 0.0) + np.where(blood_pressure > 145, 0.10, 0.0)
    chest_pain = np.where(np.random.rand(num_records) < np.clip(chest_pain_prob, 0.05, 0.70), 'Yes', 'No')
    
    dizziness_prob = 0.15 + np.where(blood_pressure > 140, 0.12, 0.0) + np.where(ages > 65, 0.08, 0.0)
    dizziness = np.where(np.random.rand(num_records) < np.clip(dizziness_prob, 0.05, 0.65), 'Yes', 'No')
    
    # 12. Overall Health Risk Score (10.0 to 98.0)
    # Composite formula reflecting clinical weighted risk factors
    risk_score = (
        (ages / 85.0) * 20.0 +
        ((bmis - 18.5) / 25.0) * 18.0 +
        ((blood_pressure - 100.0) / 80.0) * 16.0 +
        (cholesterol / 300.0) * 12.0 +
        (glucose_levels / 250.0) * 12.0 +
        np.where(smoking_habits == 'Yes', 8.0, 0.0) +
        np.where(alcohol_consumption == 'Yes', 4.0, 0.0) +
        np.where(exercise_levels == 'Sedentary', 6.0, np.where(exercise_levels == 'Moderate', 2.0, 0.0)) +
        np.where(heart_disease == 'Yes', 12.0, 0.0) +
        np.where(diabetes == 'Yes', 8.0, 0.0) +
        np.where(stroke_history == 'Yes', 10.0, 0.0)
    )
    # Normalize and clip to 10.0 - 98.0
    risk_score = np.clip(np.round((risk_score / 106.0) * 88.0 + 10.0, 1), 10.0, 98.0)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Patient_ID': patient_ids,
        'Age': ages,
        'Gender': genders,
        'BMI': bmis,
        'Exercise_Level': exercise_levels,
        'Smoking_Habits': smoking_habits,
        'Alcohol_Consumption': alcohol_consumption,
        'Blood_Pressure': blood_pressure,
        'Cholesterol': cholesterol,
        'Glucose_Levels': glucose_levels,
        'Fatigue': fatigue,
        'Chest_Pain': chest_pain,
        'Dizziness': dizziness,
        'Heart_Disease': heart_disease,
        'Diabetes': diabetes,
        'Stroke_History': stroke_history,
        'Overall_Health_Risk_Score': risk_score
    })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records at {output_path}")
    print("\nSummary of Generated Dataset:")
    print(f"Age range: {df['Age'].min()} - {df['Age'].max()} (Mean: {df['Age'].mean():.1f})")
    print(f"BMI range: {df['BMI'].min()} - {df['BMI'].max()} (Mean: {df['BMI'].mean():.1f})")
    print(f"Blood Pressure Mean: {df['Blood_Pressure'].mean():.2f}")
    print(f"Heart Disease prevalence: {(df['Heart_Disease'] == 'Yes').mean()*100:.1f}%")
    print(f"Diabetes prevalence: {(df['Diabetes'] == 'Yes').mean()*100:.1f}%")
    print(f"Stroke History prevalence: {(df['Stroke_History'] == 'Yes').mean()*100:.1f}%")
    return df

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "healthcare_dataset.csv")
    generate_health360_dataset(out)
