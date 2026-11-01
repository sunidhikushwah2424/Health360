"""
Health360 Data Processing & Cleaning Engine
Handles dataset ingestion, validation, cleaning, feature engineering,
categorical binning, filtering, and metric aggregations.
"""

import os
import pandas as pd
import numpy as np

# Age group categorization logic matching PDF specs
def categorize_age(age):
    if age <= 30:
        return 'Teenager'
    elif age <= 40:
        return 'Young Adult'
    elif age <= 50:
        return 'Adult'
    elif age <= 60:
        return 'Middle Age'
    elif age <= 70:
        return 'Senior'
    else:
        return 'Old'

# BMI category logic matching clinical standards & PDF specs
def categorize_bmi(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif bmi <= 24.9:
        return 'Normal'
    elif bmi <= 29.9:
        return 'Overweight'
    else:
        return 'Obese'

# Blood pressure clinical classification
def categorize_bp(bp):
    if bp < 120:
        return 'Normal (<120)'
    elif bp < 130:
        return 'Elevated (120-129)'
    elif bp < 140:
        return 'Stage 1 HTN (130-139)'
    else:
        return 'Stage 2 HTN (>=140)'

class DataProcessor:
    def __init__(self, raw_path=None, cleaned_path=None):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.raw_path = raw_path or os.path.join(base_dir, 'data', 'healthcare_dataset.csv')
        self.cleaned_path = cleaned_path or os.path.join(base_dir, 'data', 'cleaned_healthcare_dataset.csv')
        self.tableau_path = os.path.join(base_dir, 'data', 'tableau_healthcare_dataset.csv')
        self.df = None
        self.cleaning_stats = {}
        
    def load_and_clean(self):
        """Loads, cleans, validates, and enhances the dataset with calculated fields."""
        if not os.path.exists(self.raw_path):
            raise FileNotFoundError(f"Source dataset not found at {self.raw_path}")
            
        df = pd.read_csv(self.raw_path)
        initial_count = len(df)
        
        # 1. Missing Values & Duplicate checks
        duplicates = df.duplicated().sum()
        df = df.drop_duplicates()
        
        null_counts = df.isnull().sum().to_dict()
        
        # Handle potential missing values cleanly
        if df['Age'].isnull().any():
            df['Age'] = df['Age'].fillna(df['Age'].median()).astype(int)
        if df['BMI'].isnull().any():
            df['BMI'] = df['BMI'].fillna(df['BMI'].median()).round(1)
        if df['Blood_Pressure'].isnull().any():
            df['Blood_Pressure'] = df['Blood_Pressure'].fillna(df['Blood_Pressure'].median()).round(1)
        if df['Cholesterol'].isnull().any():
            df['Cholesterol'] = df['Cholesterol'].fillna(df['Cholesterol'].median()).astype(int)
        if df['Glucose_Levels'].isnull().any():
            df['Glucose_Levels'] = df['Glucose_Levels'].fillna(df['Glucose_Levels'].median()).astype(int)
            
        # Fill categorical nulls with mode
        cat_cols = ['Gender', 'Exercise_Level', 'Smoking_Habits', 'Alcohol_Consumption',
                    'Fatigue', 'Chest_Pain', 'Dizziness', 'Heart_Disease', 'Diabetes', 'Stroke_History']
        for col in cat_cols:
            if col in df.columns and df[col].isnull().any():
                df[col] = df[col].fillna(df[col].mode()[0])
                
        # 2. Type Corrections
        df['Age'] = df['Age'].astype(int)
        df['BMI'] = df['BMI'].astype(float).round(1)
        df['Blood_Pressure'] = df['Blood_Pressure'].astype(float).round(1)
        df['Cholesterol'] = df['Cholesterol'].astype(int)
        df['Glucose_Levels'] = df['Glucose_Levels'].astype(int)
        df['Overall_Health_Risk_Score'] = df['Overall_Health_Risk_Score'].astype(float).round(1)
        
        # 3. Calculated Fields
        df['Age_Group'] = df['Age'].apply(categorize_age)
        df['BMI_Category'] = df['BMI'].apply(categorize_bmi)
        df['BP_Category'] = df['Blood_Pressure'].apply(categorize_bp)
        
        # Risk score grouping
        df['Risk_Level'] = pd.cut(
            df['Overall_Health_Risk_Score'],
            bins=[0, 40, 70, 100],
            labels=['Low Risk', 'Moderate Risk', 'High Risk']
        )
        
        # Numeric binary flags (useful for aggregations)
        df['Heart_Disease_Num'] = (df['Heart_Disease'] == 'Yes').astype(int)
        df['Diabetes_Num'] = (df['Diabetes'] == 'Yes').astype(int)
        df['Stroke_History_Num'] = (df['Stroke_History'] == 'Yes').astype(int)
        df['Fatigue_Num'] = (df['Fatigue'] == 'Yes').astype(int)
        df['Smoking_Num'] = (df['Smoking_Habits'] == 'Yes').astype(int)
        df['Alcohol_Num'] = (df['Alcohol_Consumption'] == 'Yes').astype(int)
        
        # Categorical ordering for charts & tables
        age_order = ['Teenager', 'Young Adult', 'Adult', 'Middle Age', 'Senior', 'Old']
        bmi_order = ['Underweight', 'Normal', 'Overweight', 'Obese']
        exercise_order = ['Active', 'Moderate', 'Sedentary']
        
        df['Age_Group'] = pd.Categorical(df['Age_Group'], categories=age_order, ordered=True)
        df['BMI_Category'] = pd.Categorical(df['BMI_Category'], categories=bmi_order, ordered=True)
        df['Exercise_Level'] = pd.Categorical(df['Exercise_Level'], categories=exercise_order, ordered=True)
        
        self.cleaning_stats = {
            'initial_records': initial_count,
            'final_records': len(df),
            'duplicates_removed': int(duplicates),
            'missing_values_handled': sum(null_counts.values())
        }
        
        # Persist cleaned datasets
        os.makedirs(os.path.dirname(self.cleaned_path), exist_ok=True)
        df.to_csv(self.cleaned_path, index=False)
        
        # Tableau export: formatted cleanly without categorical datatypes
        df_tableau = df.copy()
        df_tableau['Age_Group'] = df_tableau['Age_Group'].astype(str)
        df_tableau['BMI_Category'] = df_tableau['BMI_Category'].astype(str)
        df_tableau['Exercise_Level'] = df_tableau['Exercise_Level'].astype(str)
        df_tableau.to_csv(self.tableau_path, index=False)
        
        self.df = df
        return df

    def get_dataframe(self):
        if self.df is None:
            self.load_and_clean()
        return self.df

    def filter_dataframe(self, filters=None):
        """Applies dynamic multi-select or single filters to the dataset."""
        df = self.get_dataframe().copy()
        if not filters:
            return df
            
        # Age Group filter
        if 'age_group' in filters and filters['age_group']:
            val = filters['age_group']
            if isinstance(val, list):
                if 'All' not in val:
                    df = df[df['Age_Group'].astype(str).isin(val)]
            elif val != 'All':
                df = df[df['Age_Group'].astype(str) == val]
                
        # Gender filter
        if 'gender' in filters and filters['gender']:
            val = filters['gender']
            if isinstance(val, list):
                if 'All' not in val:
                    df = df[df['Gender'].isin(val)]
            elif val != 'All':
                df = df[df['Gender'] == val]
                
        # BMI Category filter
        if 'bmi_category' in filters and filters['bmi_category']:
            val = filters['bmi_category']
            if isinstance(val, list):
                if 'All' not in val:
                    df = df[df['BMI_Category'].astype(str).isin(val)]
            elif val != 'All':
                df = df[df['BMI_Category'].astype(str) == val]
                
        # Exercise Level filter
        if 'exercise_level' in filters and filters['exercise_level']:
            val = filters['exercise_level']
            if isinstance(val, list):
                if 'All' not in val:
                    df = df[df['Exercise_Level'].astype(str).isin(val)]
            elif val != 'All':
                df = df[df['Exercise_Level'].astype(str) == val]
                
        # Smoking Habits filter
        if 'smoking' in filters and filters['smoking'] and filters['smoking'] != 'All':
            df = df[df['Smoking_Habits'] == filters['smoking']]
            
        # Alcohol Consumption filter
        if 'alcohol' in filters and filters['alcohol'] and filters['alcohol'] != 'All':
            df = df[df['Alcohol_Consumption'] == filters['alcohol']]
            
        # Heart Disease filter
        if 'heart_disease' in filters and filters['heart_disease'] and filters['heart_disease'] != 'All':
            df = df[df['Heart_Disease'] == filters['heart_disease']]
            
        # Diabetes filter
        if 'diabetes' in filters and filters['diabetes'] and filters['diabetes'] != 'All':
            df = df[df['Diabetes'] == filters['diabetes']]
            
        # Stroke History filter
        if 'stroke' in filters and filters['stroke'] and filters['stroke'] != 'All':
            df = df[df['Stroke_History'] == filters['stroke']]

        # Fatigue filter
        if 'fatigue' in filters and filters['fatigue'] and filters['fatigue'] != 'All':
            df = df[df['Fatigue'] == filters['fatigue']]
            
        return df

    def calculate_kpis(self, df=None):
        """Calculates dynamic KPI metrics from the dataset."""
        if df is None:
            df = self.get_dataframe()
            
        total_patients = len(df)
        if total_patients == 0:
            return {
                'total_patients': 0,
                'heart_disease_count': 0,
                'heart_disease_pct': 0.0,
                'diabetes_count': 0,
                'diabetes_pct': 0.0,
                'stroke_count': 0,
                'stroke_pct': 0.0,
                'avg_bp': 0.0,
                'avg_bmi': 0.0,
                'avg_risk_score': 0.0,
                'fatigue_count': 0,
                'fatigue_pct': 0.0,
                'smoking_count': 0,
                'alcohol_count': 0
            }
            
        hd_count = int(df['Heart_Disease_Num'].sum())
        diab_count = int(df['Diabetes_Num'].sum())
        stroke_count = int(df['Stroke_History_Num'].sum())
        fatigue_count = int(df['Fatigue_Num'].sum())
        smoking_count = int(df['Smoking_Num'].sum())
        alcohol_count = int(df['Alcohol_Num'].sum())
        
        return {
            'total_patients': total_patients,
            'heart_disease_count': hd_count,
            'heart_disease_pct': round((hd_count / total_patients) * 100, 1),
            'diabetes_count': diab_count,
            'diabetes_pct': round((diab_count / total_patients) * 100, 1),
            'stroke_count': stroke_count,
            'stroke_pct': round((stroke_count / total_patients) * 100, 1),
            'avg_bp': round(float(df['Blood_Pressure'].mean()), 2),
            'avg_bmi': round(float(df['BMI'].mean()), 1),
            'avg_risk_score': round(float(df['Overall_Health_Risk_Score'].mean()), 1),
            'fatigue_count': fatigue_count,
            'fatigue_pct': round((fatigue_count / total_patients) * 100, 1),
            'smoking_count': smoking_count,
            'smoking_pct': round((smoking_count / total_patients) * 100, 1),
            'alcohol_count': alcohol_count,
            'alcohol_pct': round((alcohol_count / total_patients) * 100, 1)
        }
