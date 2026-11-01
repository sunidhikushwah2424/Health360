"""
Health360 Unit Tests: Data Processing, Cleaning & KPI Calculations
"""

import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_processor import DataProcessor, categorize_age, categorize_bmi

class TestDataPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dp = DataProcessor()
        cls.df = cls.dp.load_and_clean()

    def test_record_count(self):
        """Verifies dataset has at least 1,000 records (here 5,000 as per PDF)."""
        self.assertGreaterEqual(len(self.df), 1000)
        self.assertEqual(len(self.df), 5000)

    def test_required_columns_exist(self):
        """Verifies presence of all 17 clinical and demographic columns."""
        required_cols = [
            'Patient_ID', 'Age', 'Gender', 'BMI', 'Exercise_Level',
            'Smoking_Habits', 'Alcohol_Consumption', 'Blood_Pressure',
            'Cholesterol', 'Glucose_Levels', 'Fatigue', 'Chest_Pain',
            'Dizziness', 'Heart_Disease', 'Diabetes', 'Stroke_History',
            'Overall_Health_Risk_Score'
        ]
        for col in required_cols:
            self.assertIn(col, self.df.columns)

    def test_no_null_values(self):
        """Verifies that cleaned dataset has 0 missing/null entries."""
        self.assertEqual(self.df.isnull().sum().sum(), 0)

    def test_no_duplicate_patient_ids(self):
        """Verifies Patient_ID uniqueness."""
        self.assertEqual(self.df['Patient_ID'].duplicated().sum(), 0)

    def test_age_group_classification(self):
        """Tests Age Group categorization logic."""
        self.assertEqual(categorize_age(20), 'Teenager')
        self.assertEqual(categorize_age(30), 'Teenager')
        self.assertEqual(categorize_age(35), 'Young Adult')
        self.assertEqual(categorize_age(45), 'Adult')
        self.assertEqual(categorize_age(55), 'Middle Age')
        self.assertEqual(categorize_age(65), 'Senior')
        self.assertEqual(categorize_age(75), 'Old')

    def test_bmi_category_classification(self):
        """Tests BMI categorization logic."""
        self.assertEqual(categorize_bmi(17.5), 'Underweight')
        self.assertEqual(categorize_bmi(22.0), 'Normal')
        self.assertEqual(categorize_bmi(27.5), 'Overweight')
        self.assertEqual(categorize_bmi(34.0), 'Obese')

    def test_kpi_calculation(self):
        """Verifies KPI computation returns valid numerical metrics."""
        kpis = self.dp.calculate_kpis(self.df)
        self.assertEqual(kpis['total_patients'], len(self.df))
        self.assertGreater(kpis['heart_disease_count'], 0)
        self.assertGreater(kpis['diabetes_count'], 0)
        self.assertGreater(kpis['stroke_count'], 0)
        self.assertGreater(kpis['avg_bp'], 100)
        self.assertGreater(kpis['avg_bmi'], 15)

    def test_dynamic_filtering(self):
        """Verifies filter_dataframe correctly subsets records."""
        filtered = self.dp.filter_dataframe({'age_group': 'Adult', 'gender': 'Female'})
        self.assertTrue((filtered['Age_Group'] == 'Adult').all())
        self.assertTrue((filtered['Gender'] == 'Female').all())
        self.assertLess(len(filtered), len(self.df))

if __name__ == '__main__':
    unittest.main()
