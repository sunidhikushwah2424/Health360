"""
Health360: Comprehensive Healthcare Risk & Disease Analysis
Main Flask Application & Web Controller
"""

import os
import json
import time
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for

from utils.data_processor import DataProcessor
from utils.insights_generator import generate_healthcare_insights
from visualizations.charts import (
    generate_all_charts,
    create_kpi_indicators,
    create_chart_avg_bp_by_age,
    create_chart_alcohol_smoking_by_age,
    create_chart_exercise_distribution,
    create_chart_age_distribution,
    create_chart_hd_vs_diabetes_by_bmi,
    create_chart_bmi_vs_hd_rate,
    create_chart_heatmap_bmi_exercise,
    create_chart_age_by_fatigue,
    THEME, AGE_ORDER, BMI_ORDER, EXERCISE_ORDER
)
from data.generate_dataset import generate_health360_dataset

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'health360-clinical-analytics-secret-key-2026'

# Custom Jinja Template Filters
@app.template_filter('number_format')
def number_format_filter(value):
    try:
        if isinstance(value, float):
            return f"{value:,.1f}"
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value

# Data Processor Instance
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
raw_csv_path = os.path.join(BASE_DIR, 'data', 'healthcare_dataset.csv')
cleaned_csv_path = os.path.join(BASE_DIR, 'data', 'cleaned_healthcare_dataset.csv')

# Ensure dataset exists
if not os.path.exists(raw_csv_path):
    print(f"Dataset not found at {raw_csv_path}. Generating synthetic dataset...")
    generate_health360_dataset(raw_csv_path)

dp = DataProcessor(raw_csv_path, cleaned_csv_path)
df_clean = dp.load_and_clean()

# ============================================================================
# PAGE ROUTES
# ============================================================================

@app.route('/')
@app.route('/overview')
def index():
    """Main Smart Healthcare & Risk Factor Analysis Dashboard (Overview)."""
    df = dp.get_dataframe()
    kpis = dp.calculate_kpis(df)
    charts, json_charts = generate_all_charts(df)
    
    return render_template(
        'index.html',
        active_page='overview',
        kpis=kpis,
        initial_chart_json=json.dumps(json_charts)
    )

@app.route('/patient-analytics')
def patient_analytics():
    """Patient Demographics and Anthropometrics Analysis."""
    df = dp.get_dataframe()
    total = len(df)
    
    # 1. Age distribution pie
    age_pie = create_chart_age_distribution(df)
    
    # 2. BMI category bar
    bmi_counts = df['BMI_Category'].value_counts().reindex(BMI_ORDER, fill_value=0)
    fig_bmi = go.Figure(go.Bar(
        x=BMI_ORDER,
        y=bmi_counts.values,
        marker_color=['#94a3b8', '#38bdf8', '#fb923c', '#f43f5e'],
        text=bmi_counts.values,
        textposition='outside'
    ))
    fig_bmi.update_layout(
        title="<b>Patient Count by BMI Category</b>",
        paper_bgcolor=THEME['paper_bg'],
        plot_bgcolor=THEME['bg'],
        height=380,
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(gridcolor=THEME['grid']),
        yaxis=dict(gridcolor=THEME['grid'])
    )
    
    # 3. Scatter: Age vs BMI colored by Health Risk Score
    sample_df = df.sample(min(1200, len(df)), random_state=42)
    fig_scatter = px.scatter(
        sample_df,
        x='Age',
        y='BMI',
        color='Overall_Health_Risk_Score',
        color_continuous_scale='Viridis',
        hover_data=['Gender', 'Blood_Pressure', 'Heart_Disease'],
        title="<b>Patient Bivariate Distribution: Age vs BMI (Colored by Risk Score)</b>"
    )
    fig_scatter.update_layout(
        paper_bgcolor=THEME['paper_bg'],
        plot_bgcolor=THEME['bg'],
        height=420,
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(gridcolor=THEME['grid']),
        yaxis=dict(gridcolor=THEME['grid'])
    )
    
    chart_json = {
        'age_pie': json.loads(age_pie.to_json()),
        'bmi_bar': json.loads(fig_bmi.to_json()),
        'scatter_risk': json.loads(fig_scatter.to_json())
    }
    
    male_count = (df['Gender'] == 'Male').sum()
    return render_template(
        'patient_analytics.html',
        active_page='patient_analytics',
        total_patients=total,
        avg_age=round(df['Age'].mean(), 1),
        male_pct=round((male_count / total) * 100, 1),
        female_pct=round(((total - male_count) / total) * 100, 1),
        avg_bmi=round(df['BMI'].mean(), 1),
        chart_json=json.dumps(chart_json)
    )

@app.route('/disease-analysis')
def disease_analysis():
    """Chronic Disease, Morbidity, and Vascular Analysis."""
    df = dp.get_dataframe()
    kpis = dp.calculate_kpis(df)
    
    chart_bmi_hd = create_chart_bmi_vs_hd_rate(df)
    chart_hd_diab = create_chart_hd_vs_diabetes_by_bmi(df)
    chart_heatmap = create_chart_heatmap_bmi_exercise(df)
    
    # Multi-morbidity breakdown
    both_hd_diab = ((df['Heart_Disease'] == 'Yes') & (df['Diabetes'] == 'Yes')).sum()
    only_hd = ((df['Heart_Disease'] == 'Yes') & (df['Diabetes'] == 'No')).sum()
    only_diab = ((df['Heart_Disease'] == 'No') & (df['Diabetes'] == 'Yes')).sum()
    neither = ((df['Heart_Disease'] == 'No') & (df['Diabetes'] == 'No')).sum()
    
    fig_comorbid = go.Figure(go.Pie(
        labels=['Neither', 'Heart Disease Only', 'Diabetes Only', 'Both HD & Diabetes'],
        values=[neither, only_hd, only_diab, both_hd_diab],
        marker=dict(colors=['#94a3b8', '#f43f5e', '#f59e0b', '#8b5cf6'], line=dict(color='#ffffff', width=2)),
        hole=0.45,
        textinfo='label+percent'
    ))
    fig_comorbid.update_layout(
        title="<b>Chronic Disease Co-Morbidity Clustering</b>",
        paper_bgcolor=THEME['paper_bg'],
        height=380,
        margin=dict(l=30, r=30, t=50, b=30)
    )
    
    chart_json = {
        'chart_bmi_hd_rate': json.loads(chart_bmi_hd.to_json()),
        'chart_hd_vs_diabetes': json.loads(chart_hd_diab.to_json()),
        'chart_heatmap': json.loads(chart_heatmap.to_json()),
        'comorbidity': json.loads(fig_comorbid.to_json())
    }
    
    return render_template(
        'disease_analysis.html',
        active_page='disease_analysis',
        kpis=kpis,
        chart_json=json.dumps(chart_json)
    )

@app.route('/lifestyle-analysis')
def lifestyle_analysis():
    """Lifestyle & Behavioral Factors (Exercise, Smoking, Alcohol, Fatigue)."""
    df = dp.get_dataframe()
    kpis = dp.calculate_kpis(df)
    
    # Additional KPI metrics for lifestyle
    ex_counts = df['Exercise_Level'].value_counts()
    kpis['exercise_active_count'] = int(ex_counts.get('Active', 0))
    kpis['exercise_active_pct'] = round((kpis['exercise_active_count'] / len(df)) * 100, 1)
    kpis['exercise_sedentary_count'] = int(ex_counts.get('Sedentary', 0))
    kpis['exercise_sedentary_pct'] = round((kpis['exercise_sedentary_count'] / len(df)) * 100, 1)
    
    chart_donut = create_chart_exercise_distribution(df)
    chart_alc_smoke = create_chart_alcohol_smoking_by_age(df)
    chart_fatigue = create_chart_age_by_fatigue(df)
    
    # Heart disease rate across exercise tiers
    ex_rates = df.groupby('Exercise_Level', observed=True)['Heart_Disease_Num'].mean() * 100
    fig_ex_hd = go.Figure(go.Bar(
        x=EXERCISE_ORDER,
        y=[ex_rates.get(ex, 0) for ex in EXERCISE_ORDER],
        marker_color=['#10b981', '#0ea5e9', '#f59e0b'],
        text=[f"{ex_rates.get(ex, 0):.1f}%" for ex in EXERCISE_ORDER],
        textposition='outside'
    ))
    fig_ex_hd.update_layout(
        title="<b>Heart Disease Prevalence by Exercise Routine</b>",
        paper_bgcolor=THEME['paper_bg'],
        plot_bgcolor=THEME['bg'],
        height=380,
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(title="Exercise Level", gridcolor=THEME['grid']),
        yaxis=dict(title="Heart Disease Rate (%)", range=[0, 50], gridcolor=THEME['grid'])
    )
    
    chart_json = {
        'chart_exercise_donut': json.loads(chart_donut.to_json()),
        'chart_alcohol_smoking': json.loads(chart_alc_smoke.to_json()),
        'chart_age_fatigue': json.loads(chart_fatigue.to_json()),
        'ex_hd_bar': json.loads(fig_ex_hd.to_json())
    }
    
    return render_template(
        'lifestyle_analysis.html',
        active_page='lifestyle_analysis',
        kpis=kpis,
        chart_json=json.dumps(chart_json)
    )

@app.route('/visualizations')
def visualizations():
    """All 9 Required Project Visualizations with full descriptions & data."""
    df = dp.get_dataframe()
    kpis = dp.calculate_kpis(df)
    charts, json_charts = generate_all_charts(df)
    
    # Add KPI gauge
    kpi_gauges = create_kpi_indicators(kpis)
    json_charts['kpi_gauges'] = json.loads(kpi_gauges.to_json())
    
    return render_template(
        'visualizations.html',
        active_page='visualizations',
        kpis=kpis,
        chart_json=json.dumps(json_charts)
    )

@app.route('/insights')
def insights():
    """Dynamic Healthcare Insights Engine."""
    df = dp.get_dataframe()
    insights_data = generate_healthcare_insights(df)
    
    return render_template(
        'insights.html',
        active_page='insights',
        total_analyzed=insights_data['total_analyzed'],
        insights=insights_data['insights'],
        disclaimer=insights_data['disclaimer']
    )

@app.route('/story')
def story():
    """Tableau-Style 5-Scene Interactive Story Player."""
    df = dp.get_dataframe()
    charts, json_charts = generate_all_charts(df)
    
    return render_template(
        'story.html',
        active_page='story',
        chart_json=json.dumps(json_charts)
    )

@app.route('/data-explorer')
def data_explorer():
    """Tabular Patient Dataset Explorer."""
    df = dp.get_dataframe()
    preview_df = df.head(100)
    
    return render_template(
        'data_explorer.html',
        active_page='data_explorer',
        total_records=len(df),
        preview_rows=preview_df.to_dict(orient='records')
    )

@app.route('/tableau')
@app.route('/tableau-hub')
def tableau_hub():
    """Tableau Desktop & Public Integration Hub and Publishing Guide."""
    return render_template('tableau_hub.html', active_page='tableau_hub')

@app.route('/about')
def about():
    """System Architecture, Technology Stack, and Methodology."""
    return render_template('about.html', active_page='about')

# ============================================================================
# API ENDPOINTS (Dynamic Filtering, KPIs, Exports, Performance)
# ============================================================================

@app.route('/api/filter-data', methods=['POST', 'GET'])
def api_filter_data():
    """
    Primary dynamic filtering endpoint.
    Receives filter criteria, filters dataset, recalculates KPIs,
    re-renders all 9 charts in Plotly JSON, and generates updated insights summary.
    """
    filters = request.get_json(silent=True) or request.args.to_dict()
    
    start_time = time.time()
    filtered_df = dp.filter_dataframe(filters)
    filter_time = round((time.time() - start_time) * 1000, 2)
    
    kpis = dp.calculate_kpis(filtered_df)
    _, json_charts = generate_all_charts(filtered_df)
    
    # Generate quick summary sentence
    total_f = len(filtered_df)
    if total_f > 0:
        summary_text = (
            f"Filtered cohort consists of {total_f:,} patients. "
            f"Heart disease prevalence stands at {kpis['heart_disease_pct']}%, "
            f"average blood pressure is {kpis['avg_bp']} mmHg, and average risk score is {kpis['avg_risk_score']}/100."
        )
    else:
        summary_text = "No patient records match the selected filter combination."
        
    return jsonify({
        'status': 'success',
        'kpis': kpis,
        'charts': json_charts,
        'insights_summary': summary_text,
        'filter_latency_ms': filter_time
    })

@app.route('/api/kpis', methods=['GET'])
def api_kpis():
    """Returns raw KPI metrics for current active dataset."""
    df = dp.get_dataframe()
    kpis = dp.calculate_kpis(df)
    return jsonify({'status': 'success', 'kpis': kpis})

@app.route('/api/export-cleaned', methods=['GET'])
def export_cleaned_dataset():
    """Serves the cleaned healthcare CSV dataset."""
    if os.path.exists(dp.cleaned_path):
        return send_file(dp.cleaned_path, as_attachment=True, download_name="cleaned_healthcare_dataset.csv", mimetype="text/csv")
    return jsonify({'error': 'Cleaned dataset not found'}), 404

@app.route('/api/export-tableau', methods=['GET'])
def export_tableau_dataset():
    """Serves the Tableau-optimized CSV dataset."""
    if os.path.exists(dp.tableau_path):
        return send_file(dp.tableau_path, as_attachment=True, download_name="tableau_healthcare_dataset.csv", mimetype="text/csv")
    return jsonify({'error': 'Tableau dataset not found'}), 404

@app.route('/api/performance', methods=['GET'])
def api_performance():
    """Performance benchmarking route assessing rendering and filtering speeds."""
    df = dp.get_dataframe()
    
    # Test 1: Full KPI calculation
    t0 = time.time()
    kpis = dp.calculate_kpis(df)
    kpi_ms = round((time.time() - t0) * 1000, 2)
    
    # Test 2: Chart generation
    t0 = time.time()
    _, _ = generate_all_charts(df)
    charts_ms = round((time.time() - t0) * 1000, 2)
    
    # Test 3: Complex Multi-filter
    t0 = time.time()
    test_filter = {'age_group': 'Adult', 'exercise_level': 'Sedentary', 'smoking': 'Yes'}
    filtered = dp.filter_dataframe(test_filter)
    filter_ms = round((time.time() - t0) * 1000, 2)
    
    return jsonify({
        'status': 'healthy',
        'dataset_records': len(df),
        'attributes_count': len(df.columns),
        'memory_usage_mb': round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        'benchmarks_ms': {
            'kpi_calculation_latency': kpi_ms,
            'all_9_charts_generation_latency': charts_ms,
            'complex_filter_latency': filter_ms
        }
    })

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', active_page='404'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Health360 Healthcare Analytics Platform initializing on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True)
