"""
Health360 Visualizations Engine
Generates interactive Plotly charts adhering to clinical healthcare standards
and exact specifications from the Health360 project guide.
"""

import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Professional Healthcare Color Palette
THEME = {
    'bg': '#ffffff',
    'paper_bg': '#ffffff',
    'text': '#1e293b',
    'muted': '#64748b',
    'grid': '#f1f5f9',
    'primary': '#0284c7',       # Ocean Blue
    'secondary': '#0ea5e9',     # Sky Blue
    'teal': '#0d9488',          # Health Teal
    'coral': '#f43f5e',         # Warning Rose/Coral
    'amber': '#f59e0b',         # Warning Amber
    'emerald': '#10b981',       # Success Green
    'indigo': '#6366f1',        # Deep Indigo
    'purple': '#8b5cf6',        # Lilac Purple
    'categories': ['#0284c7', '#0ea5e9', '#0d9488', '#f59e0b', '#f43f5e', '#8b5cf6']
}

AGE_ORDER = ['Teenager', 'Young Adult', 'Adult', 'Middle Age', 'Senior', 'Old']
BMI_ORDER = ['Underweight', 'Normal', 'Overweight', 'Obese']
EXERCISE_ORDER = ['Active', 'Moderate', 'Sedentary']

def _base_layout(title="", height=380):
    """Returns a standardized professional layout config for Plotly figures."""
    return dict(
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(family='Inter, sans-serif', size=15, color=THEME['text']),
            x=0.03,
            y=0.95
        ),
        paper_bgcolor=THEME['paper_bg'],
        plot_bgcolor=THEME['bg'],
        font=dict(family='Inter, sans-serif', color=THEME['text'], size=12),
        margin=dict(l=45, r=25, t=55, b=45),
        height=height,
        autosize=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=11)
        ),
        xaxis=dict(
            gridcolor=THEME['grid'],
            zerolinecolor=THEME['grid'],
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            gridcolor=THEME['grid'],
            zerolinecolor=THEME['grid'],
            tickfont=dict(size=11)
        ),
        hoverlabel=dict(
            bgcolor='#0f172a',
            font_size=12,
            font_family='Inter, sans-serif',
            font_color='#ffffff'
        )
    )

# -------------------------------------------------------------
# Chart 1: KPI Indicator Figure (for visual KPI component)
# -------------------------------------------------------------
def create_kpi_indicators(kpis):
    """Generates an aesthetic Plotly KPI overview figure."""
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="number+gauge",
        value=kpis.get('avg_bp', 134.7),
        domain={'x': [0, 0.48], 'y': [0, 1]},
        title={'text': "<b>Avg Blood Pressure</b><br><span style='font-size:0.8em;color:gray'>Systolic mmHg</span>"},
        gauge={
            'axis': {'range': [90, 180]},
            'bar': {'color': THEME['primary']},
            'steps': [
                {'range': [90, 120], 'color': '#d1fae5'},
                {'range': [120, 139], 'color': '#fef3c7'},
                {'range': [139, 180], 'color': '#fee2e2'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 3},
                'thickness': 0.75,
                'value': 140
            }
        }
    ))
    
    fig.add_trace(go.Indicator(
        mode="number+gauge",
        value=kpis.get('avg_risk_score', 52.9),
        domain={'x': [0.52, 1], 'y': [0, 1]},
        title={'text': "<b>Avg Health Risk Score</b><br><span style='font-size:0.8em;color:gray'>Scale 0-100</span>"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': THEME['coral']},
            'steps': [
                {'range': [0, 40], 'color': '#d1fae5'},
                {'range': [40, 70], 'color': '#fef3c7'},
                {'range': [70, 100], 'color': '#fee2e2'}
            ],
            'threshold': {
                'line': {'color': "darkred", 'width': 3},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    layout = _base_layout("Clinical Vitals & Risk Score Overview", height=240)
    layout['margin'] = dict(l=25, r=25, t=40, b=25)
    fig.update_layout(layout)
    return fig

# -------------------------------------------------------------
# Chart 2: Bar Chart – Average Blood Pressure Across Age Groups
# -------------------------------------------------------------
def create_chart_avg_bp_by_age(df):
    """Chart 2: Bar Chart showing Average Blood Pressure Across Age Groups."""
    grouped = df.groupby('Age_Group', observed=True)['Blood_Pressure'].mean().reindex(AGE_ORDER).reset_index()
    grouped['Blood_Pressure'] = grouped['Blood_Pressure'].round(2)
    
    colors = ['#f43f5e', '#f97316', '#cbd5e1', '#a8a29e', '#f472b6', '#a78bfa']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped['Age_Group'],
        y=grouped['Blood_Pressure'],
        text=[f"{v:.2f} mmHg" if pd.notnull(v) else "" for v in grouped['Blood_Pressure']],
        textposition='outside',
        marker=dict(
            color=colors[:len(grouped)],
            line=dict(color='#334155', width=1)
        ),
        hovertemplate="<b>%{x}</b><br>Average BP: %{y:.2f} mmHg<extra></extra>"
    ))
    
    # Add Hypertension Stage 1 reference line at 130 mmHg
    fig.add_hline(
        y=130, line_dash="dash", line_color="#ef4444",
        annotation_text="Hypertension Threshold (130 mmHg)",
        annotation_position="bottom right",
        annotation_font=dict(color='#ef4444', size=11)
    )
    
    layout = _base_layout("Average Blood Pressure Across Age Groups", height=380)
    layout['yaxis']['range'] = [0, max(160, (grouped['Blood_Pressure'].max() or 140) + 15)]
    layout['yaxis']['title'] = "Blood Pressure (mmHg)"
    layout['xaxis']['title'] = "Age Group"
    fig.update_layout(layout)
    return fig

# -------------------------------------------------------------
# Chart 3: Grouped Bar Chart – Alcohol & Smoking Across Age Groups
# -------------------------------------------------------------
def create_chart_alcohol_smoking_by_age(df):
    """Chart 3: Grouped Bar Chart – Alcohol and Smoking Consumption Across Age Groups."""
    grp_smoke = df[df['Smoking_Habits'] == 'Yes'].groupby('Age_Group', observed=True)['Patient_ID'].count().reindex(AGE_ORDER, fill_value=0)
    grp_alcohol = df[df['Alcohol_Consumption'] == 'Yes'].groupby('Age_Group', observed=True)['Patient_ID'].count().reindex(AGE_ORDER, fill_value=0)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=AGE_ORDER,
        y=grp_alcohol.values,
        name='Alcohol Consumers',
        marker_color='#f59e0b',
        text=grp_alcohol.values,
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Alcohol Consumers: %{y}<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=AGE_ORDER,
        y=grp_smoke.values,
        name='Smokers',
        marker_color='#ec4899',
        text=grp_smoke.values,
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Smokers: %{y}<extra></extra>"
    ))
    
    layout = _base_layout("Alcohol and Smoking Consumption Across Age Groups", height=380)
    layout['barmode'] = 'group'
    layout['xaxis']['title'] = "Age Group"
    layout['yaxis']['title'] = "Patient Count"
    max_val = max(max(grp_alcohol.values, default=10), max(grp_smoke.values, default=10))
    layout['yaxis']['range'] = [0, max_val * 1.25]
    fig.update_layout(layout)
    return fig

# -------------------------------------------------------------
# Chart 4: Donut Chart – Exercise Level Distribution
# -------------------------------------------------------------
def create_chart_exercise_distribution(df):
    """Chart 4: Donut Chart – Exercise Level Distribution."""
    counts = df['Exercise_Level'].value_index = df['Exercise_Level'].value_counts().reindex(EXERCISE_ORDER, fill_value=0)
    
    colors = ['#10b981', '#0ea5e9', '#f59e0b']
    
    fig = go.Figure(data=[go.Pie(
        labels=counts.index.tolist(),
        values=counts.values.tolist(),
        hole=0.55,
        marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
        textinfo='label+percent',
        insidetextorientation='radial',
        hovertemplate="<b>%{label}</b><br>Patients: %{value:,} (%{percent})<extra></extra>"
    )])
    
    layout = _base_layout("Exercise Level Distribution", height=380)
    layout['showlegend'] = True
    fig.update_layout(layout)
    return fig

# -------------------------------------------------------------
# Chart 5: Pie Chart – Patient Distribution by Age Group
# -------------------------------------------------------------
def create_chart_age_distribution(df):
    """Chart 5: Pie Chart – Patient Distribution by Age Group."""
    counts = df['Age_Group'].value_counts().reindex(AGE_ORDER, fill_value=0)
    
    colors = ['#cbd5e1', '#f97316', '#a855f7', '#f472b6', '#a8a29e', '#f43f5e']
    
    fig = go.Figure(data=[go.Pie(
        labels=counts.index.tolist(),
        values=counts.values.tolist(),
        marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
        textinfo='label+percent',
        hovertemplate="<b>%{label}</b><br>Patients: %{value:,} (%{percent})<extra></extra>"
    )])
    
    layout = _base_layout("Patient Distribution by Age Group", height=380)
    layout['showlegend'] = True
    fig.update_layout(layout)
    return fig

# -------------------------------------------------------------
# Chart 6: Grouped Bar Chart – Heart Disease vs Diabetes Prevalence by BMI Category
# -------------------------------------------------------------
def create_chart_hd_vs_diabetes_by_bmi(df):
    """Chart 6: Grouped Bar Chart – Heart Disease vs Diabetes Prevalence by BMI Category."""
    hd_counts = df[df['Heart_Disease'] == 'Yes'].groupby('BMI_Category', observed=True)['Patient_ID'].count().reindex(BMI_ORDER, fill_value=0)
    diab_counts = df[df['Diabetes'] == 'Yes'].groupby('BMI_Category', observed=True)['Patient_ID'].count().reindex(BMI_ORDER, fill_value=0)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=BMI_ORDER,
        y=hd_counts.values,
        name='Heart Disease',
        marker_color='#f43f5e',
        text=hd_counts.values,
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Heart Disease: %{y:,} patients<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=BMI_ORDER,
        y=diab_counts.values,
        name='Diabetes',
        marker_color='#f59e0b',
        text=diab_counts.values,
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Diabetes: %{y:,} patients<extra></extra>"
    ))
    
    layout = _base_layout("Heart Disease vs Diabetes Prevalence by BMI Category", height=380)
    layout['barmode'] = 'group'
    layout['xaxis']['title'] = "BMI Category"
    layout['yaxis']['title'] = "Patient Count"
    max_val = max(max(hd_counts.values, default=10), max(diab_counts.values, default=10))
    layout['yaxis']['range'] = [0, max_val * 1.25]
    fig.update_layout(layout)
    return fig

# -------------------------------------------------------------
# Chart 7: Bar Chart – BMI Category vs Heart Disease Rate
# -------------------------------------------------------------
def create_chart_bmi_vs_hd_rate(df):
    """Chart 7: Bar Chart – BMI Category vs Heart Disease Rate (percentage)."""
    # Group by BMI category and compute rate
    order_chart = ['Obese', 'Overweight', 'Normal', 'Underweight']
    rates = []
    texts = []
    
    for cat in order_chart:
        sub = df[df['BMI_Category'] == cat]
        if len(sub) > 0:
            rate = (sub['Heart_Disease'] == 'Yes').mean() * 100
        else:
            rate = 0.0
        rates.append(round(rate, 2))
        texts.append(f"{rate:.2f}%")
        
    colors = ['#f43f5e', '#fb923c', '#38bdf8', '#94a3b8']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=order_chart,
        y=rates,
        text=texts,
        textposition='outside',
        marker=dict(
            color=colors,
            line=dict(color='#334155', width=1)
        ),
        hovertemplate="<b>%{x}</b><br>Heart Disease Rate: %{y:.2f}%<extra></extra>"
    ))
    
    layout = _base_layout("BMI Category vs Heart Disease Rate", height=380)
    layout['xaxis']['title'] = "BMI Category"
    layout['yaxis']['title'] = "Heart Disease Rate (%)"
    layout['yaxis']['range'] = [0, max(50, (max(rates, default=40) + 10))]
    fig.update_layout(layout)
    return fig

# -------------------------------------------------------------
# Chart 8: Heat Map – Heart Disease by BMI Category and Exercise Level
# -------------------------------------------------------------
def create_chart_heatmap_bmi_exercise(df):
    """Chart 8: Heat Map – Heart Disease Rate by BMI Category and Exercise Level."""
    y_categories = ['Normal', 'Obese', 'Overweight', 'Underweight']
    x_categories = ['Active', 'Moderate', 'Sedentary']
    
    # Calculate matrix
    matrix = []
    text_matrix = []
    
    for bmi in y_categories:
        row = []
        text_row = []
        for ex in x_categories:
            sub = df[(df['BMI_Category'] == bmi) & (df['Exercise_Level'] == ex)]
            if len(sub) > 0:
                rate = (sub['Heart_Disease'] == 'Yes').mean()
            else:
                rate = 0.0
            row.append(round(rate, 4))
            text_row.append(f"{rate:.4f}<br>({rate*100:.1f}%)")
        matrix.append(row)
        text_matrix.append(text_row)
        
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=x_categories,
        y=y_categories,
        text=text_matrix,
        texttemplate="%{text}",
        colorscale='YlOrRd',
        reversescale=False,
        showscale=True,
        colorbar=dict(title=dict(text="Prevalence", side="right")),
        hovertemplate="BMI: <b>%{y}</b><br>Exercise: <b>%{x}</b><br>HD Prevalence: <b>%{z:.4f}</b><extra></extra>"
    ))
    
    layout = _base_layout("Heart Disease by BMI Category and Exercise Level", height=380)
    layout['xaxis']['title'] = "Exercise Level Category"
    layout['yaxis']['title'] = "BMI Category"
    fig.update_layout(layout)
    return fig

# -------------------------------------------------------------
# Chart 9: Bar Chart – Age Group Distribution by Fatigue Condition
# -------------------------------------------------------------
def create_chart_age_by_fatigue(df):
    """Chart 9: Bar Chart – Age Group Distribution by Fatigue Condition."""
    # Matches horizontal/grouped layout from PDF
    fatigue_yes = df[df['Fatigue'] == 'Yes'].groupby('Age_Group', observed=True)['Patient_ID'].count().reindex(AGE_ORDER, fill_value=0)
    fatigue_no = df[df['Fatigue'] == 'No'].groupby('Age_Group', observed=True)['Patient_ID'].count().reindex(AGE_ORDER, fill_value=0)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=AGE_ORDER,
        x=fatigue_yes.values,
        name='Fatigue: Yes',
        orientation='h',
        marker_color='#0284c7',
        text=fatigue_yes.values,
        textposition='inside',
        hovertemplate="<b>%{y}</b><br>Fatigue Present: %{x:,}<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        y=AGE_ORDER,
        x=fatigue_no.values,
        name='Fatigue: No',
        orientation='h',
        marker_color='#bae6fd',
        text=fatigue_no.values,
        textposition='inside',
        hovertemplate="<b>%{y}</b><br>Fatigue Absent: %{x:,}<extra></extra>"
    ))
    
    layout = _base_layout("Age Group Distribution by Fatigue Condition", height=380)
    layout['barmode'] = 'stack'
    layout['xaxis']['title'] = "Patient Count"
    layout['yaxis']['title'] = "Age Group"
    fig.update_layout(layout)
    return fig

# -------------------------------------------------------------
# Helper: Generate all 9 charts in one unified bundle
# -------------------------------------------------------------
def generate_all_charts(df):
    """Returns a dictionary containing all 9 chart objects and their JSON payloads."""
    charts = {
        'chart_bp_by_age': create_chart_avg_bp_by_age(df),
        'chart_alcohol_smoking': create_chart_alcohol_smoking_by_age(df),
        'chart_exercise_donut': create_chart_exercise_distribution(df),
        'chart_age_pie': create_chart_age_distribution(df),
        'chart_hd_vs_diabetes': create_chart_hd_vs_diabetes_by_bmi(df),
        'chart_bmi_hd_rate': create_chart_bmi_vs_hd_rate(df),
        'chart_heatmap': create_chart_heatmap_bmi_exercise(df),
        'chart_age_fatigue': create_chart_age_by_fatigue(df),
    }
    
    # Also create JSON representations for AJAX dynamic loading
    json_charts = {}
    for k, fig in charts.items():
        json_charts[k] = json.loads(fig.to_json())
        
    return charts, json_charts
