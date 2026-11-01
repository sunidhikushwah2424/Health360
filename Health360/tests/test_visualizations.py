"""
Health360 Unit Tests: Visualizations & Chart Engines
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_processor import DataProcessor
from visualizations.charts import (
    generate_all_charts,
    create_chart_avg_bp_by_age,
    create_chart_alcohol_smoking_by_age,
    create_chart_exercise_distribution,
    create_chart_age_distribution,
    create_chart_hd_vs_diabetes_by_bmi,
    create_chart_bmi_vs_hd_rate,
    create_chart_heatmap_bmi_exercise,
    create_chart_age_by_fatigue
)

class TestVisualizations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dp = DataProcessor()
        cls.df = cls.dp.load_and_clean()

    def test_chart_generation_all_9(self):
        """Verifies all charts generate without exception and contain traces."""
        charts, jsons = generate_all_charts(self.df)
        expected_keys = [
            'chart_bp_by_age',
            'chart_alcohol_smoking',
            'chart_exercise_donut',
            'chart_age_pie',
            'chart_hd_vs_diabetes',
            'chart_bmi_hd_rate',
            'chart_heatmap',
            'chart_age_fatigue'
        ]
        for key in expected_keys:
            self.assertIn(key, charts)
            self.assertIn(key, jsons)
            fig = charts[key]
            self.assertGreater(len(fig.data), 0, f"Chart {key} has no data traces")

    def test_heatmap_dimensions(self):
        """Verifies heatmap has 4 BMI tiers on Y and 3 Exercise tiers on X."""
        fig = create_chart_heatmap_bmi_exercise(self.df)
        heatmap_trace = fig.data[0]
        self.assertEqual(len(heatmap_trace.y), 4) # Normal, Obese, Overweight, Underweight
        self.assertEqual(len(heatmap_trace.x), 3) # Active, Moderate, Sedentary

    def test_donut_hole(self):
        """Verifies exercise level chart has donut hole."""
        fig = create_chart_exercise_distribution(self.df)
        self.assertGreater(fig.data[0].hole, 0.4)

if __name__ == '__main__':
    unittest.main()
