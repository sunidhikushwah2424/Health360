"""
Health360 Integration Tests: Flask Application Endpoints & Routes
"""

import unittest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_overview_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Health360", response.data)
        self.assertIn(b"Smart Healthcare & Risk Factor Analysis Dashboard", response.data)

    def test_patient_analytics_page(self):
        response = self.client.get('/patient-analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Patient Demographics", response.data)

    def test_disease_analysis_page(self):
        response = self.client.get('/disease-analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Chronic Disease", response.data)

    def test_lifestyle_analysis_page(self):
        response = self.client.get('/lifestyle-analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Lifestyle", response.data)

    def test_visualizations_page(self):
        response = self.client.get('/visualizations')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All 9 Required Visualizations", response.data)

    def test_insights_page(self):
        response = self.client.get('/insights')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Healthcare Insights", response.data)

    def test_story_page(self):
        response = self.client.get('/story')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Smart Healthcare Analytics: Patient Risk", response.data)

    def test_data_explorer_page(self):
        response = self.client.get('/data-explorer')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Patient Dataset Explorer", response.data)

    def test_tableau_hub_page(self):
        response = self.client.get('/tableau')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Tableau Desktop", response.data)

    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Methodology", response.data)

    def test_api_filter_data(self):
        payload = {'age_group': 'Adult', 'smoking': 'Yes'}
        response = self.client.post(
            '/api/filter-data',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('kpis', data)
        self.assertIn('charts', data)
        self.assertIn('filter_latency_ms', data)

    def test_api_kpis(self):
        response = self.client.get('/api/kpis')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['kpis']['total_patients'], 5000)

    def test_api_performance(self):
        response = self.client.get('/api/performance')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['dataset_records'], 5000)
        self.assertIn('benchmarks_ms', data)

    def test_export_cleaned(self):
        response = self.client.get('/api/export-cleaned')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response.content_type)

    def test_export_tableau(self):
        response = self.client.get('/api/export-tableau')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/csv', response.content_type)

if __name__ == '__main__':
    unittest.main()
