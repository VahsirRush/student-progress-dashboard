import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

# Version check
VERSION = "1.0.1"
st.set_page_config(
    page_title="Student Progress Dashboard",
    page_icon="📚",
    layout="wide"
)

# Display version in sidebar
with st.sidebar:
    st.markdown(f"**Version:** {VERSION}")
    st.markdown("---")

# Custom CSS
st.markdown("""
    <style>
    /* Design System Variables */
    :root {
        /* Color Palette */
        --primary: #2196F3;
        --primary-light: #64B5F6;
        --primary-dark: #1976D2;
        --secondary: #FFC107;
        --secondary-light: #FFD54F;
        --secondary-dark: #FFA000;
        --success: #4CAF50;
        --warning: #FF9800;
        --danger: #F44336;
        --info: #00BCD4;
        --neutral: #9E9E9E;
        
        /* Typography */
        --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        --font-size-xs: 0.75rem;
        --font-size-sm: 0.875rem;
        --font-size-md: 1rem;
        --font-size-lg: 1.125rem;
        --font-size-xl: 1.25rem;
        
        /* Text Colors */
        --text-primary: #000000;
        --text-secondary: #333333;
        --text-muted: #666666;
        
        /* Spacing */
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
        
        /* Border Radius */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        
        /* Shadows */
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        --shadow-md: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
        --shadow-lg: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
        
        /* Transitions */
        --transition-fast: 150ms ease;
        --transition-normal: 250ms ease;
        --transition-slow: 350ms ease;
    }
    
    /* Global Styles */
    * {
        font-family: var(--font-family);
        transition: all var(--transition-normal);
        color: var(--text-primary);
    }
    
    /* Streamlit specific overrides */
    .stApp {
        background-color: white;
    }
    
    .stMarkdown {
        color: var(--text-primary);
    }
    
    .stMetric {
        color: var(--text-primary);
    }
    
    .stMetric > div > div {
        color: var(--text-primary);
    }
    
    .stMetric > div > div > div {
        color: var(--text-primary);
    }
    
    .stSelectbox > div > div {
        color: var(--text-primary);
    }
    
    .stTextInput > div > div > input {
        border-radius: var(--radius-md);
        border: 1px solid rgba(0,0,0,0.1);
        padding: var(--spacing-sm) var(--spacing-md);
        background-color: white;
        color: black;
    }
    
    /* Chart specific overrides */
    .js-plotly-plot .plotly .modebar {
        background-color: white;
    }
    
    .js-plotly-plot .plotly .modebar-btn {
        color: var(--text-primary);
    }
    
    .js-plotly-plot .plotly .modebar-btn:hover {
        background-color: rgba(0,0,0,0.1);
    }
    
    /* Card Styles */
    .student-box {
        background: white;
        border-radius: 0;
        box-shadow: none;
        padding: 1rem;
        margin-bottom: 0;
        border: none;
        border-bottom: 1px solid #000000;
        transition: all 0.3s ease;
    }

    .student-box:hover {
        transform: none;
        box-shadow: none;
        background-color: rgba(0, 0, 0, 0.02);
    }

    .student-box.selected {
        border-left: none;
        background: none;
        border-bottom: 1px solid #000000;
    }

    .student-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0;
        padding: 0.5rem 0;
    }

    .student-info {
        flex: 1;
        margin: 0;
        padding: 0;
    }

    .student-name {
        margin: 0;
        padding: 0;
    }

    .student-details {
        margin: 0;
        padding: 0;
    }

    .student-actions {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
        padding: 0;
    }

    .select-button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: var(--spacing-sm) var(--spacing-md);
        cursor: pointer;
        font-weight: 500;
        transition: all var(--transition-normal);
    }

    .select-button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
    }

    .select-button.selected {
        background: var(--success);
    }
    
    /* Status Indicators */
    .status-indicator {
        margin: 0;
        padding: 0.25rem 0.5rem;
    }
    
    .status-active {
        background: rgba(76,175,80,0.1);
        color: var(--success);
    }
    
    .status-warning {
        background: rgba(255,152,0,0.1);
        color: var(--warning);
    }
    
    .status-alert {
        background: rgba(244,67,54,0.1);
        color: var(--danger);
    }
    
    /* Preview Dropdown */
    .preview-dropdown {
        margin-top: var(--spacing-md);
        border-radius: var(--radius-lg);
        overflow: hidden;
        background: white;
        box-shadow: var(--shadow-sm);
        border: 1px solid #000000;
    }
    
    .preview-header {
        margin: 0;
        padding: 0.5rem 0;
    }
    
    .preview-content {
        margin: 0;
        padding: 0.5rem;
    }
    
    .preview-section {
        margin: 0;
        padding: 0.5rem 0;
    }
    
    .preview-section-title {
        font-size: var(--font-size-md);
        font-weight: 600;
        color: var(--primary-dark);
        margin-bottom: var(--spacing-md);
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
    }
    
    .preview-metric {
        display: flex;
        justify-content: space-between;
        padding: var(--spacing-sm) 0;
        border-bottom: 1px solid #000000;
        font-size: var(--font-size-sm);
    }
    
    .preview-metric:last-child {
        border-bottom: none;
    }
    
    /* Alerts */
    .preview-alert {
        padding: var(--spacing-md);
        border-radius: var(--radius-md);
        margin-top: var(--spacing-sm);
        font-size: var(--font-size-sm);
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .alert-warning {
        background: rgba(255,152,0,0.1);
        color: var(--warning);
        border-left: 4px solid var(--warning);
    }
    
    .alert-success {
        background: rgba(76,175,80,0.1);
        color: var(--success);
        border-left: 4px solid var(--success);
    }
    
    .alert-danger {
        background: rgba(244,67,54,0.1);
        color: var(--danger);
        border-left: 4px solid var(--danger);
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
        border-radius: var(--radius-sm);
        height: 8px !important;
    }

    /* Buttons */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        padding: var(--spacing-sm) var(--spacing-lg);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all var(--transition-normal);
    }

    .stButton > button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    /* Metrics */
    .stMetric {
        background: white;
        padding: var(--spacing-md);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
    }
    
    .stMetric > div {
        padding: 0 !important;
    }

    /* Charts */
    .js-plotly-plot {
        background: white !important;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: white;
        border-radius: var(--radius-md);
        padding: var(--spacing-md);
        margin: var(--spacing-sm) 0;
        box-shadow: var(--shadow-sm);
    }

    .streamlit-expanderHeader:hover {
        background: rgba(33,150,243,0.05);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
    }
    
    /* Search Input */
    .stTextInput > div > div > input {
        border-radius: var(--radius-md);
        border: 1px solid rgba(0,0,0,0.1);
        padding: var(--spacing-sm) var(--spacing-md);
        background-color: white;
        color: black;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(33,150,243,0.1);
        background-color: white;
        color: black;
    }

    /* Comparison View Styles */
    .comparison-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin-top: 2rem;
    }

    .comparison-card {
        background: white;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        padding: var(--spacing-lg);
        border: 1px solid #000000;
    }

    .comparison-header {
        border-bottom: 1px solid #000000;
        padding-bottom: var(--spacing-md);
        margin-bottom: var(--spacing-md);
    }

    .comparison-section {
        margin: 0;
        padding: 0.5rem;
    }

    .comparison-metric {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-sm) 0;
        border-bottom: 1px solid #000000;
    }

    .comparison-metric:last-child {
        border-bottom: none;
    }

    .metric-label {
        color: var(--neutral);
        font-size: var(--font-size-sm);
    }

    .metric-value {
        font-weight: 600;
        color: var(--primary-dark);
    }

    .trend-indicator {
        display: inline-flex;
        align-items: center;
        gap: var(--spacing-xs);
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--radius-sm);
        font-size: var(--font-size-sm);
    }

    .trend-up {
        background: rgba(76,175,80,0.1);
        color: var(--success);
    }

    .trend-down {
        background: rgba(244,67,54,0.1);
        color: var(--danger);
    }

    .trend-neutral {
        background: rgba(158,158,158,0.1);
        color: var(--neutral);
    }

    /* Timeline Styles */
    .timeline-container {
        margin: 0;
        padding: 0.5rem;
    }

    .timeline-header {
        margin: 0;
        padding: 0.5rem 0;
    }

    .timeline-controls {
        display: flex;
        gap: var(--spacing-md);
        align-items: center;
    }

    .timeline-legend {
        display: flex;
        flex-wrap: wrap;
        gap: var(--spacing-sm);
        margin-top: var(--spacing-md);
        padding: var(--spacing-sm);
        background: rgba(0,0,0,0.02);
        border-radius: var(--radius-sm);
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: var(--spacing-xs);
        font-size: var(--font-size-sm);
        color: var(--neutral);
    }

    .legend-color {
        width: 12px;
        height: 12px;
        border-radius: 2px;
    }

    /* Remove spacing between students */
    .student-box {
        background: white;
        border-radius: 0;
        box-shadow: none;
        padding: 1rem;
        margin-bottom: 0;
        border: none;
        border-bottom: 1px solid #000000;
        transition: all 0.3s ease;
    }

    .student-box:hover {
        transform: none;
        box-shadow: none;
        background-color: rgba(0, 0, 0, 0.02);
    }

    .student-box.selected {
        border-left: none;
        background: none;
        border-bottom: 1px solid #000000;
    }

    /* Remove container spacing */
    .student-list-container {
        margin: 0;
        padding: 0;
    }

    /* Remove spacing from student header */
    .student-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0;
        padding: 0.5rem 0;
    }

    /* Remove spacing from student info */
    .student-info {
        flex: 1;
        margin: 0;
        padding: 0;
    }

    .student-name {
        margin: 0;
        padding: 0;
    }

    .student-details {
        margin: 0;
        padding: 0;
    }

    /* Remove spacing from student actions */
    .student-actions {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0;
        padding: 0;
    }

    /* Remove spacing from status indicators */
    .status-indicator {
        margin: 0;
        padding: 0.25rem 0.5rem;
    }

    /* Remove spacing from preview sections */
    .preview-section {
        margin: 0;
        padding: 0.5rem 0;
    }

    .preview-header {
        margin: 0;
        padding: 0.5rem 0;
    }

    .preview-content {
        margin: 0;
        padding: 0.5rem;
    }

    /* Remove spacing from subject breakdown */
    .subject-breakdown {
        margin: 0;
        padding: 0.5rem 0;
    }

    .subject-item {
        margin: 0;
        padding: 0.25rem 0;
    }

    /* Remove spacing from metric cards */
    .metric-card {
        margin: 0;
        padding: 0.5rem;
    }

    /* Remove spacing from alerts */
    .alert-item {
        margin: 0;
        padding: 0.25rem 0.5rem;
    }

    /* Remove spacing from comparison sections */
    .comparison-section {
        margin: 0;
        padding: 0.5rem;
    }

    /* Remove spacing from timeline sections */
    .timeline-container {
        margin: 0;
        padding: 0.5rem;
    }

    .timeline-header {
        margin: 0;
        padding: 0.5rem 0;
    }

    .timeline-metrics {
        margin: 0;
        padding: 0.5rem 0;
    }

    .timeline-chart {
        margin: 0;
        padding: 0.5rem;
    }

    /* Student Selection Dropdown */
    .stSelectbox > div > div > div[data-baseweb="select"] {
        color: white;
    }

    .stSelectbox > div > div > div[data-baseweb="select"]:hover {
        color: white;
    }

    .stSelectbox > div > div > div[data-baseweb="select"] > div {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions
def calculate_progress(row):
    if row['skills_practiced'] == 0:
        return 0
    return round((row['skills_mastered'] / row['skills_practiced']) * 100)

def get_progress_color(progress):
    if progress >= 80: return '#7ba7c2'  # Lazy Blue Light
    if progress >= 60: return '#5d8aa8'  # Lazy Blue
    if progress >= 40: return '#d1b280'  # Lazy Sand
    if progress >= 20: return '#c19a6b'  # Lazy Sand Dark
    return '#b76e79'  # Lazy Rose

def get_progress_emoji(progress):
    if progress >= 80: return '🌟'
    if progress >= 60: return '⭐'
    if progress >= 40: return '✨'
    if progress >= 20: return '💫'
    return '🌱'

def get_student_summary(df, student_id, date_filter=None):
    student_data = df[df['student_id'] == student_id]
    
    # Apply date filter if specified
    if date_filter and date_filter != "All":
        try:
            filter_date = pd.to_datetime(date_filter)
            student_data = student_data[student_data['date'].dt.date == filter_date.date()]
        except:
            st.warning("Invalid date format. Showing all data.")
    
    if student_data.empty:
        return None
    
    # Calculate overall totals
    total_questions = student_data['questions_answered'].sum()
    total_skills_practiced = student_data['skills_practiced'].sum()
    total_skills_mastered = student_data['skills_mastered'].sum()
    
    # Calculate subject breakdown
    subject_breakdown = {}
    for subject in student_data['subject'].unique():
        subject_data = student_data[student_data['subject'] == subject]
        
        # Calculate subject totals
        subject_questions = subject_data['questions_answered'].sum()
        subject_skills_practiced = subject_data['skills_practiced'].sum()
        subject_skills_mastered = subject_data['skills_mastered'].sum()
        
        # Calculate progress
        progress = 0
        if subject_skills_practiced > 0:
            progress = round((subject_skills_mastered / subject_skills_practiced) * 100)
        
        # Calculate predictive growth
        mastery_rate = round((subject_skills_mastered / max(1, subject_skills_practiced)) * 100, 1)
        efficiency = round((subject_skills_mastered / max(1, subject_questions)) * 100, 1)
        questions_per_day = round(subject_questions / max(1, len(subject_data)), 1)
        
        # Weighted growth calculation
        predicted_growth = round(
            (mastery_rate * 0.4) +  # 40% weight on mastery rate
            (efficiency * 0.4) +    # 40% weight on efficiency
            (min(questions_per_day, 20) * 0.2)  # 20% weight on questions per day, capped at 20
        )
        
        # Adjust growth based on current progress
        if progress < 30:
            predicted_growth *= 1.2  # 20% boost for students who need more help
        elif progress > 80:
            predicted_growth *= 0.8  # 20% reduction for already high-performing students
        
        subject_breakdown[subject] = {
            'questions': subject_questions,
            'skills_practiced': subject_skills_practiced,
            'skills_mastered': subject_skills_mastered,
            'progress': progress,
            'questions_per_day': questions_per_day,
            'mastery_rate': mastery_rate,
            'efficiency': efficiency,
            'predicted_growth': predicted_growth
        }
    
    return {
        'name': f"{student_data['first_name'].iloc[0]} {student_data['last_name'].iloc[0]}",
        'teacher': student_data['teacher_name'].iloc[0],
        'subjects': student_data['subject'].unique(),
        'total_questions': total_questions,
        'total_skills_practiced': total_skills_practiced,
        'total_skills_mastered': total_skills_mastered,
        'latest_date': student_data['date'].max(),
        'subject_breakdown': subject_breakdown,
        'timeline_data': student_data.sort_values('date')[['date', 'subject', 'questions_answered', 'skills_mastered']].to_dict('records')
    }

def draw_donut_chart(subject, start_val, end_val, term):
    """Create a donut chart showing start vs end percentiles."""
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        values=[start_val, end_val],
        labels=["Start", "End"],
        marker=dict(colors=["#FFA15A", "#00CC96"]),
        hole=0.6,
        textinfo='label+value',
        hoverinfo='label+value+percent',
        texttemplate='%{label}<br>%{value:.0f}',
        insidetextorientation='horizontal',
        sort=False,
        direction='clockwise',
        rotation=180,
        textfont=dict(
            color='black',
            size=14,
            family='Arial'
        ),
        textposition='inside'
    ))
    
    fig.update_layout(
        title={
            'text': f"<b>{subject} Percentile ({term})</b><br><span style='font-size:12px'>Start vs. End</span>",
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.95,
            'yanchor': 'top',
            'font': dict(
                color='black',
                size=20,
                family='Arial'
            )
        },
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(
            color='black',
            size=12,
            family='Arial'
        ),
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    return fig

def get_percentile(series, value):
    """Calculate percentile for a given value in a series."""
    if pd.isna(value): return None
    return round(series.rank(pct=True)[series.index[series == value][0]] * 100)

def display_ixl_progress(student_id, df):
    """Display IXL progress charts for a specific student."""
    st.markdown("### IXL Progress")
    
    # Filter data for the specific student
    student_data = df[df['student_id'] == student_id].copy()
    
    if student_data.empty:
        st.warning("No IXL data available for this student.")
        return
    
    # Check if required columns exist
    required_columns = ['End date', 'Starting diagnostic level - Math', 
                       'Ending diagnostic level - Math', 'Starting diagnostic level - ELA', 
                       'Ending diagnostic level - ELA', 'questions_answered']
    
    missing_columns = [col for col in required_columns if col not in student_data.columns]
    if missing_columns:
        st.warning(f"Missing required columns: {', '.join(missing_columns)}")
        with st.expander("Debug Information", expanded=False):
            st.write("Available columns:", student_data.columns.tolist())
            st.write("Sample data:", student_data.head())
        return
    
    # Convert Date column to datetime
    student_data['End date'] = pd.to_datetime(student_data['End date'])
    student_data = student_data.sort_values('End date')
    
    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Progress Over Time", "Term Performance"])
    
    with tab1:
        # Create two columns for the charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Math Progress Chart
            fig_math = go.Figure()
            try:
                # Check if required columns exist
                if 'End date' not in student_data.columns or 'Ending diagnostic level - Math' not in student_data.columns:
                    st.warning("Required columns for Math progress visualization are missing.")
                else:
                    fig_math.add_trace(go.Bar(
                        x=student_data['End date'].dt.strftime('%Y-%m-%d'),
                        y=student_data['Ending diagnostic level - Math'],
                        name='Math Level',
                        marker_color='#2196F3',
                        text=student_data['Ending diagnostic level - Math'],
                        textposition='outside',
                        textfont=dict(
                            color='black',
                            size=12,
                            family='Arial'
                        ),
                        hovertemplate='Date: %{x}<br>Level: %{y}<extra></extra>'
                    ))
                    fig_math.update_layout(
                        title={
                            'text': 'Math Diagnostic Level Over Time',
                            'x': 0.5,
                            'xanchor': 'center',
                            'y': 0.95,
                            'yanchor': 'top',
                            'font': dict(
                                color='black',
                                size=18,
                                family='Arial'
                            )
                        },
                        xaxis_title='Date',
                        yaxis_title='Diagnostic Level',
                        template='plotly_white',
                        height=400,
                        font=dict(
                            color='black',
                            size=12,
                            family='Arial'
                        ),
                        xaxis=dict(
                            title_font=dict(
                                color='black',
                                size=12,
                                family='Arial'
                            ),
                            tickfont=dict(
                                color='black',
                                size=10,
                                family='Arial'
                            ),
                            tickangle=45
                        ),
                        yaxis=dict(
                            title_font=dict(
                                color='black',
                                size=12,
                                family='Arial'
                            ),
                            tickfont=dict(
                                color='black',
                                size=10,
                                family='Arial'
                            )
                        ),
                        margin=dict(t=50, b=50, l=50, r=50),
                        plot_bgcolor='white',
                        paper_bgcolor='white'
                    )
                    st.plotly_chart(fig_math, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating Math progress chart: {str(e)}")
        
        with col2:
            # ELA Progress Chart
            fig_ela = go.Figure()
            try:
                # Check if required columns exist
                if 'End date' not in student_data.columns or 'Ending diagnostic level - ELA' not in student_data.columns:
                    st.warning("Required columns for ELA progress visualization are missing.")
                else:
                    fig_ela.add_trace(go.Bar(
                        x=student_data['End date'].dt.strftime('%Y-%m-%d'),
                        y=student_data['Ending diagnostic level - ELA'],
                        name='ELA Level',
                        marker_color='#FFC107',
                        text=student_data['Ending diagnostic level - ELA'],
                        textposition='outside',
                        textfont=dict(
                            color='black',
                            size=12,
                            family='Arial'
                        ),
                        hovertemplate='Date: %{x}<br>Level: %{y}<extra></extra>'
                    ))
                    fig_ela.update_layout(
                        title={
                            'text': 'ELA Diagnostic Level Over Time',
                            'x': 0.5,
                            'xanchor': 'center',
                            'y': 0.95,
                            'yanchor': 'top',
                            'font': dict(
                                color='black',
                                size=18,
                                family='Arial'
                            )
                        },
                        xaxis_title='Date',
                        yaxis_title='Diagnostic Level',
                        template='plotly_white',
                        height=400,
                        font=dict(
                            color='black',
                            size=12,
                            family='Arial'
                        ),
                        xaxis=dict(
                            title_font=dict(
                                color='black',
                                size=12,
                                family='Arial'
                            ),
                            tickfont=dict(
                                color='black',
                                size=10,
                                family='Arial'
                            ),
                            tickangle=45
                        ),
                        yaxis=dict(
                            title_font=dict(
                                color='black',
                                size=12,
                                family='Arial'
                            ),
                            tickfont=dict(
                                color='black',
                                size=10,
                                family='Arial'
                            )
                        ),
                        margin=dict(t=50, b=50, l=50, r=50),
                        plot_bgcolor='white',
                        paper_bgcolor='white'
                    )
                    st.plotly_chart(fig_ela, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating ELA progress chart: {str(e)}")
    
    with tab2:
        # Term selection
        selected_term = st.selectbox("Select Term", ["Fall", "Spring"])
        term_data = student_data[student_data['Term'] == selected_term]
        
        if term_data.empty:
            st.warning(f"No data available for {selected_term} term.")
            st.stop()
        
        # Get the most recent diagnostic for this term
        latest_data = term_data.sort_values(by="End date", ascending=False).iloc[0]
        
        # Calculate percentiles
        math_start_pct = get_percentile(
            df[df['Term'] == selected_term]['Starting diagnostic level - Math'],
            latest_data['Starting diagnostic level - Math']
        )
        
        math_end_pct = get_percentile(
            df[df['Term'] == selected_term]['Ending diagnostic level - Math'],
            latest_data['Ending diagnostic level - Math']
        )
        
        ela_start_pct = get_percentile(
            df[df['Term'] == selected_term]['Starting diagnostic level - ELA'],
            latest_data['Starting diagnostic level - ELA']
        )
        
        ela_end_pct = get_percentile(
            df[df['Term'] == selected_term]['Ending diagnostic level - ELA'],
            latest_data['Ending diagnostic level - ELA']
        )
        
        # Create two columns for the donut charts
        col1, col2 = st.columns(2)
        
        with col1:
            if math_start_pct is not None and math_end_pct is not None:
                st.plotly_chart(draw_donut_chart("Math", math_start_pct, math_end_pct, selected_term), use_container_width=True)
            else:
                st.info("Student Has Not Completed Enough Math Training-Sets To Receive a Score")
        
        with col2:
            if ela_start_pct is not None and ela_end_pct is not None:
                st.plotly_chart(draw_donut_chart("ELA", ela_start_pct, ela_end_pct, selected_term), use_container_width=True)
            else:
                st.info("Student Has Not Completed Enough ELA Training-Sets To Receive a Score")
    
    # Display additional metrics
    st.markdown("### IXL Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            math_questions = student_data[student_data['subject'] == 'Mathematics']['questions_answered'].sum()
            st.metric(
                "Total Math Questions",
                f"{math_questions:,}",
                help="Total math questions answered by the student"
            )
        except Exception as e:
            st.warning("Could not calculate total math questions")
    
    with col2:
        try:
            ela_questions = student_data[student_data['subject'] == 'English Language Arts']['questions_answered'].sum()
            st.metric(
                "Total ELA Questions",
                f"{ela_questions:,}",
                help="Total ELA questions answered by the student"
            )
        except Exception as e:
            st.warning("Could not calculate total ELA questions")
    
    with col3:
        try:
            if 'Ending diagnostic level - Math' in student_data.columns:
                latest_math = student_data['Ending diagnostic level - Math'].iloc[-1]
                previous_math = student_data['Ending diagnostic level - Math'].iloc[-2] if len(student_data) > 1 else latest_math
                math_change = latest_math - previous_math
                st.metric(
                    "Math Level Change",
                    f"{math_change:+.1f}",
                    help="Change in math diagnostic level from previous assessment"
                )
        except Exception as e:
            st.warning("Could not calculate math level change")

def display_student_dashboard(student_id, date_filter=None):
    student_data = df[df['student_id'] == student_id]
    
    # Apply date filter if specified
    if date_filter and date_filter != "All":
        try:
            filter_date = pd.to_datetime(date_filter)
            student_data = student_data[student_data['date'].dt.date == filter_date.date()]
        except:
            st.warning("Invalid date format. Showing all data.")
    
    summary = get_student_summary(df, student_id, date_filter)
    
    if summary is None:
        st.warning("No data available for the selected date.")
        return
    
    st.title(f"Student Dashboard: {summary['name']}")
    st.write(f"Teacher: {summary['teacher']}")
    
    # Add date filter information
    if date_filter and date_filter != "All":
        st.info(f"Showing data for: {date_filter}")
    else:
        st.info("Showing all available data")
    
    # Timeline Chart
    st.markdown('<div class="timeline-chart">', unsafe_allow_html=True)
    st.subheader("Progress Timeline")
    timeline_df = pd.DataFrame(summary['timeline_data'])
    timeline_df['date'] = pd.to_datetime(timeline_df['date'])
    
    # Create a more detailed timeline chart
    fig = go.Figure()
    
    for subject in timeline_df['subject'].unique():
        subject_data = timeline_df[timeline_df['subject'] == subject]
        fig.add_trace(go.Scatter(
            x=subject_data['date'],
            y=subject_data['skills_mastered'],
            name=f'{subject} Skills Mastered',
            mode='lines+markers',
            line=dict(width=2),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title={
            'text': 'Progress Over Time',
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.95,
            'yanchor': 'top',
            'font': dict(
                color='black',
                size=18,
                family='Arial'
            )
        },
        xaxis_title='Date',
        yaxis_title='Skills Mastered',
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.1)',
            borderwidth=1,
            font=dict(
                color='black',
                size=12,
                family='Arial'
            ),
            orientation='h'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(
            color='black',
            size=12,
            family='Arial'
        ),
        xaxis=dict(
            title_font=dict(
                color='black',
                size=12,
                family='Arial'
            ),
            tickfont=dict(
                color='black',
                size=10,
                family='Arial'
            )
        ),
        yaxis=dict(
            title_font=dict(
                color='black',
                size=12,
                family='Arial'
            ),
            tickfont=dict(
                color='black',
                size=10,
                family='Arial'
            )
        ),
        margin=dict(t=50, b=100, l=50, r=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Overall Progress
    st.subheader("Overall Progress")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Questions", summary['total_questions'])
    with col2:
        st.metric("Skills Practiced", summary['total_skills_practiced'])
    with col3:
        st.metric("Skills Mastered", summary['total_skills_mastered'])
    with col4:
        avg_growth = round(sum(data['predicted_growth'] for data in summary['subject_breakdown'].values()) / len(summary['subject_breakdown']))
        st.metric("Predicted Growth", f"+{avg_growth}%", 
                 delta=f"+{avg_growth - 50}%" if avg_growth > 50 else None)
    
    # Subject Comparison Chart
    st.subheader("Subject Comparison")
    subjects = list(summary['subject_breakdown'].keys())
    progress_values = [data['progress'] for data in summary['subject_breakdown'].values()]
    mastery_rates = [data['mastery_rate'] for data in summary['subject_breakdown'].values()]
    efficiency_scores = [data['efficiency'] for data in summary['subject_breakdown'].values()]
    
    fig = go.Figure(data=[
        go.Bar(name='Progress', x=subjects, y=progress_values, marker_color='#7ba7c2'),
        go.Bar(name='Mastery Rate', x=subjects, y=mastery_rates, marker_color='#5d8aa8'),
        go.Bar(name='Efficiency', x=subjects, y=efficiency_scores, marker_color='#d1b280')
    ])
    
    fig.update_layout(
        barmode='group',
        title={
            'text': 'Subject Performance Comparison',
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.95,
            'yanchor': 'top',
            'font': dict(
                color='black',
                size=18,
                family='Arial'
            )
        },
        xaxis_title='Subject',
        yaxis_title='Percentage',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(
            color='black',
            size=12,
            family='Arial'
        ),
        xaxis=dict(
            title_font=dict(
                color='black',
                size=12,
                family='Arial'
            ),
            tickfont=dict(
                color='black',
                size=10,
                family='Arial'
            )
        ),
        yaxis=dict(
            title_font=dict(
                color='black',
                size=12,
                family='Arial'
            ),
            tickfont=dict(
                color='black',
                size=10,
                family='Arial'
            )
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Subject Breakdown
    st.subheader("Subject Breakdown")
    
    # Get list of subjects and their data
    subjects = list(summary['subjects'])
    num_subjects = len(subjects)
    
    if num_subjects <= 4:
        # Create a 2x2 grid for up to 4 subjects
        cols = st.columns(2)
        for i, subject in enumerate(subjects):
            col_idx = i % 2
            row_idx = i // 2
            subject_data = student_data[student_data['subject'] == subject].iloc[0]
            progress = round((subject_data['skills_mastered'] / max(1, subject_data['skills_practiced'])) * 100)
            
            with cols[col_idx]:
                # Calculate metrics
                mastery_rate = round((subject_data['skills_mastered'] / max(1, subject_data['skills_practiced'])) * 100, 1)
                efficiency = round((subject_data['skills_mastered'] / max(1, subject_data['questions_answered'])) * 100, 1)
                questions_per_day = round(subject_data['questions_answered'] / max(1, len(student_data)), 1)
                
                # Create a container for the subject card
                with st.container():
                    st.markdown(f"### {subject} - {progress}%")
                    
                    # Display metrics in a grid
                    metric_cols = st.columns(2)
                    with metric_cols[0]:
                        st.metric("Mastery Rate", f"{mastery_rate}%")
                        st.metric("Questions/Day", questions_per_day)
                    with metric_cols[1]:
                        st.metric("Efficiency", f"{efficiency}%")
                        st.metric("Skills Mastered", subject_data['skills_mastered'])
                    
                    # Progress bar
                    st.progress(progress/100)
                    
                    # Additional details in a container
                    with st.container():
                        st.markdown("#### Activity Details")
                        st.write(f"Total Questions: {subject_data['questions_answered']}")
                        st.write(f"Skills Practiced: {subject_data['skills_practiced']}")
                        
                        # Check for diagnostic levels based on subject
                        if subject == 'Mathematics':
                            start_col = 'Starting diagnostic level - Math'
                            end_col = 'Ending diagnostic level - Math'
                            growth_col = 'Diagnostic growth - Math'
                        elif subject == 'English Language Arts':
                            start_col = 'Starting diagnostic level - ELA'
                            end_col = 'Ending diagnostic level - ELA'
                            growth_col = 'Diagnostic growth - ELA'
                        else:
                            start_col = end_col = growth_col = None
                        
                        # Only show diagnostic information if the columns exist
                        if start_col in subject_data and end_col in subject_data:
                            st.write(f"Starting Level: {subject_data[start_col]}")
                            st.write(f"Ending Level: {subject_data[end_col]}")
                            if growth_col in subject_data:
                                st.write(f"Growth: {subject_data[growth_col]}")
    else:
        # Create a triangular layout for more than 4 subjects
        st.markdown(
            '<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0;">',
            unsafe_allow_html=True
        )
        
        for i, subject in enumerate(subjects):
            subject_data = student_data[student_data['subject'] == subject].iloc[0]
            progress = round((subject_data['skills_mastered'] / max(1, subject_data['skills_practiced'])) * 100)
            
            # Calculate position in triangular grid
            row = i // 3
            col = i % 3
            if row == 1 and col == 1:  # Center position
                col = 2
            elif row == 1 and col == 2:  # Right position
                col = 1
            
            # Create a container for the subject card
            with st.container():
                st.markdown(f"### {subject} - {progress}%")
                
                # Calculate metrics
                mastery_rate = round((subject_data['skills_mastered'] / max(1, subject_data['skills_practiced'])) * 100, 1)
                efficiency = round((subject_data['skills_mastered'] / max(1, subject_data['questions_answered'])) * 100, 1)
                questions_per_day = round(subject_data['questions_answered'] / max(1, len(student_data)), 1)
                
                # Display metrics in a grid
                metric_cols = st.columns(2)
                with metric_cols[0]:
                    st.metric("Mastery Rate", f"{mastery_rate}%")
                    st.metric("Questions/Day", questions_per_day)
                with metric_cols[1]:
                    st.metric("Efficiency", f"{efficiency}%")
                    st.metric("Skills Mastered", subject_data['skills_mastered'])
                
                # Progress bar
                st.progress(progress/100)
                
                # Additional details in a container
                with st.container():
                    st.markdown("#### Activity Details")
                    st.write(f"Total Questions: {subject_data['questions_answered']}")
                    st.write(f"Skills Practiced: {subject_data['skills_practiced']}")
                    
                    # Check for diagnostic levels based on subject
                    if subject == 'Mathematics':
                        start_col = 'Starting diagnostic level - Math'
                        end_col = 'Ending diagnostic level - Math'
                        growth_col = 'Diagnostic growth - Math'
                    elif subject == 'English Language Arts':
                        start_col = 'Starting diagnostic level - ELA'
                        end_col = 'Ending diagnostic level - ELA'
                        growth_col = 'Diagnostic growth - ELA'
                    else:
                        start_col = end_col = growth_col = None
                    
                    # Only show diagnostic information if the columns exist
                    if start_col in subject_data and end_col in subject_data:
                        st.write(f"Starting Level: {subject_data[start_col]}")
                        st.write(f"Ending Level: {subject_data[end_col]}")
                        if growth_col in subject_data:
                            st.write(f"Growth: {subject_data[growth_col]}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Add IXL Progress section after other metrics
    display_ixl_progress(student_id, df)

def get_student_status_indicators(student_id, df):
    student_data = df[df['student_id'] == student_id]
    if student_data.empty:
        return None
    
    # Calculate overall progress
    total_skills_practiced = student_data['skills_practiced'].sum()
    total_skills_mastered = student_data['skills_mastered'].sum()
    overall_progress = round((total_skills_mastered / max(1, total_skills_practiced)) * 100)
    
    # Get latest activity date
    latest_date = student_data['date'].max()
    days_since_activity = (pd.Timestamp.now() - latest_date).days
    
    # Calculate subject completion
    subjects = student_data['subject'].unique()
    total_subjects = len(df['subject'].unique())
    subject_completion = len(subjects) / total_subjects * 100
    
    # Calculate growth trend
    growth_trend = 0
    for subject in subjects:
        subject_data = student_data[student_data['subject'] == subject]
        if not subject_data.empty:
            mastery_rate = round((subject_data['skills_mastered'].sum() / max(1, subject_data['skills_practiced'].sum())) * 100, 1)
            efficiency = round((subject_data['skills_mastered'].sum() / max(1, subject_data['questions_answered'].sum())) * 100, 1)
            growth_trend += (mastery_rate * 0.6 + efficiency * 0.4)
    growth_trend = round(growth_trend / len(subjects))
    
    return {
        'overall_progress': overall_progress,
        'days_since_activity': days_since_activity,
        'subject_completion': subject_completion,
        'growth_trend': growth_trend,
        'subjects': list(subjects)
    }

def get_status_icon(progress):
    if progress >= 80: return '<i class="fas fa-star" style="color: #f1c40f;"></i>'
    if progress >= 60: return '<i class="fas fa-star-half-alt" style="color: #f1c40f;"></i>'
    if progress >= 40: return '<i class="fas fa-star" style="color: #bdc3c7;"></i>'
    if progress >= 20: return '<i class="far fa-star" style="color: #bdc3c7;"></i>'
    return '<i class="far fa-circle" style="color: #bdc3c7;"></i>'

def get_activity_status(days):
    if days <= 1:
        return '<i class="fas fa-circle" style="color: #2ecc71;"></i>', 'Active Today', 'status-active'
    if days <= 3:
        return '<i class="fas fa-circle" style="color: #f1c40f;"></i>', 'Active This Week', 'status-warning'
    if days <= 7:
        return '<i class="fas fa-circle" style="color: #e67e22;"></i>', 'Active This Month', 'status-warning'
    return '<i class="fas fa-circle" style="color: #e74c3c;"></i>', 'Inactive', 'status-alert'

def get_growth_indicator(trend):
    if trend >= 80:
        return '<i class="fas fa-chart-line" style="color: #2ecc71;"></i>', 'High Growth', 'status-active'
    if trend >= 60:
        return '<i class="fas fa-arrow-up" style="color: #2ecc71;"></i>', 'Moderate Growth', 'status-active'
    if trend >= 40:
        return '<i class="fas fa-equals" style="color: #f1c40f;"></i>', 'Stable', 'status-warning'
    return '<i class="fas fa-arrow-down" style="color: #e74c3c;"></i>', 'Needs Attention', 'status-alert'

def get_student_alerts(status):
    alerts = []
    
    # Activity alerts
    if status['days_since_activity'] > 7:
        alerts.append({
            'type': 'danger',
            'icon': '<i class="fas fa-exclamation-circle"></i>',
            'message': 'No activity in the last 7 days'
        })
    elif status['days_since_activity'] > 3:
        alerts.append({
            'type': 'warning',
            'icon': '<i class="fas fa-clock"></i>',
            'message': 'Limited activity this week'
        })
    
    # Progress alerts
    if status['overall_progress'] < 40:
        alerts.append({
            'type': 'danger',
            'icon': '<i class="fas fa-chart-line"></i>',
            'message': 'Overall progress below target'
        })
    elif status['overall_progress'] < 60:
        alerts.append({
            'type': 'warning',
            'icon': '<i class="fas fa-chart-line"></i>',
            'message': 'Progress needs improvement'
        })
    
    # Subject completion alerts
    if status['subject_completion'] < 50:
        alerts.append({
            'type': 'warning',
            'icon': '<i class="fas fa-book"></i>',
            'message': 'Low subject participation'
        })
    
    # Growth alerts
    if status['growth_trend'] < 40:
        alerts.append({
            'type': 'danger',
            'icon': '<i class="fas fa-arrow-down"></i>',
            'message': 'Growth trend declining'
        })
    
    return alerts

# Add debug mode toggle at the top of the app
debug_mode = st.sidebar.checkbox("Debug Mode", value=False)

# Load and process data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/combined_data.csv')
        
        # Create a list to store processed records
        records = []
        
        for _, row in df.iterrows():
            student_id = row['Student ID']
            if pd.isna(student_id):
                continue
                
            # Convert date to datetime
            try:
                end_date = pd.to_datetime(row['End date'])
            except:
                end_date = pd.NaT  # Not a Time
                
            # Calculate term based on date
            def get_term(date):
                if pd.isna(date): return None
                month = date.month
                if 8 <= month <= 12: return "Fall"
                elif 1 <= month <= 6: return "Spring"
                return None
            
            term = get_term(end_date)
                
            # Process Math records
            if not pd.isna(row['Math questions answered']) and int(row['Math questions answered']) > 0:
                record = {
                    'student_id': student_id,
                    'first_name': row['Student first name'],
                    'last_name': row['Student last name'],
                    'teacher_name': row['Teacher names'],
                    'date': end_date,
                    'End date': end_date,
                    'Term': term,
                    'subject': 'Mathematics',
                    'questions_answered': int(row['Math questions answered']),
                    'skills_practiced': int(row['Math skills practiced']),
                    'skills_proficient': int(row['Math skills proficient']),
                    'skills_mastered': int(row['Math skills mastered'])
                }
                
                # Add diagnostic levels if they exist
                if 'Starting diagnostic level - Math' in row:
                    record['Starting diagnostic level - Math'] = row['Starting diagnostic level - Math']
                if 'Ending diagnostic level - Math' in row:
                    record['Ending diagnostic level - Math'] = row['Ending diagnostic level - Math']
                if 'Diagnostic growth - Math' in row:
                    record['Diagnostic growth - Math'] = row['Diagnostic growth - Math']
                
                records.append(record)
            
            # Process ELA records
            if not pd.isna(row['ELA questions answered']) and int(row['ELA questions answered']) > 0:
                record = {
                    'student_id': student_id,
                    'first_name': row['Student first name'],
                    'last_name': row['Student last name'],
                    'teacher_name': row['Teacher names'],
                    'date': end_date,
                    'End date': end_date,
                    'Term': term,
                    'subject': 'English Language Arts',
                    'questions_answered': int(row['ELA questions answered']),
                    'skills_practiced': int(row['ELA skills practiced']),
                    'skills_proficient': int(row['ELA skills proficient']),
                    'skills_mastered': int(row['ELA skills mastered'])
                }
                
                # Add diagnostic levels if they exist
                if 'Starting diagnostic level - Overall ELA' in row:
                    record['Starting diagnostic level - ELA'] = row['Starting diagnostic level - Overall ELA']
                if 'Ending diagnostic level - Overall ELA' in row:
                    record['Ending diagnostic level - ELA'] = row['Ending diagnostic level - Overall ELA']
                if 'Diagnostic growth - ELA' in row:
                    record['Diagnostic growth - ELA'] = row['Diagnostic growth - ELA']
                
                records.append(record)
            
            # Process Science records
            if not pd.isna(row['Science questions answered']) and int(row['Science questions answered']) > 0:
                records.append({
                    'student_id': student_id,
                    'first_name': row['Student first name'],
                    'last_name': row['Student last name'],
                    'teacher_name': row['Teacher names'],
                    'date': end_date,
                    'End date': end_date,
                    'Term': term,
                    'subject': 'Science',
                    'questions_answered': int(row['Science questions answered']),
                    'skills_practiced': int(row['Science skills practiced']),
                    'skills_proficient': int(row['Science skills proficient']),
                    'skills_mastered': int(row['Science skills mastered'])
                })
            
            # Process Social Studies records
            if not pd.isna(row['Social studies questions answered']) and int(row['Social studies questions answered']) > 0:
                records.append({
                    'student_id': student_id,
                    'first_name': row['Student first name'],
                    'last_name': row['Student last name'],
                    'teacher_name': row['Teacher names'],
                    'date': end_date,
                    'End date': end_date,
                    'Term': term,
                    'subject': 'Social Studies',
                    'questions_answered': int(row['Social studies questions answered']),
                    'skills_practiced': int(row['Social studies skills practiced']),
                    'skills_proficient': int(row['Social studies skills proficient']),
                    'skills_mastered': int(row['Social studies skills mastered'])
                })
        
        # Create DataFrame and sort by date
        df = pd.DataFrame(records)
        df = df.sort_values('date', ascending=False)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load the data
df = load_data()

if df is not None:
    # Initialize session state
    if 'active_tab' not in st.session_state:
        st.session_state['active_tab'] = "Student Dashboard"
    if 'selected_students' not in st.session_state:
        st.session_state['selected_students'] = set()
    if 'selected_student' not in st.session_state:
        st.session_state['selected_student'] = None
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Student Dashboard", "Student List", "Comparison View", "Raw Data"])
    
    # Student Dashboard Tab
    with tab1:
        st.title("Student Progress Dashboard")
        
        # Search and filter section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("Search by Name or ID", key="dashboard_search")
        
        with col2:
            subject_filter = st.selectbox(
                "Filter by Subject",
                ["All"] + list(df['subject'].unique()),
                key="dashboard_subject"
            )
        
        with col3:
            date_filter = st.selectbox(
                "Filter by Date",
                ["All"] + [d.strftime('%Y-%m-%d') if pd.notnull(d) else 'Unknown' for d in df['date'].unique()],
                key="dashboard_date"
            )
        
        # Filter data based on search and filters
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[
                filtered_df['first_name'].str.contains(search_term, case=False) |
                filtered_df['last_name'].str.contains(search_term, case=False) |
                filtered_df['student_id'].astype(str).str.contains(search_term, case=False)
            ]
        
        if subject_filter != "All":
            filtered_df = filtered_df[filtered_df['subject'] == subject_filter]
        
        if date_filter != "All":
            filtered_df = filtered_df[filtered_df['date'].dt.strftime('%Y-%m-%d') == date_filter]
        
        # Student selection
        if not filtered_df.empty:
            students = filtered_df['student_id'].unique()
            
            # If a student was selected from the list, use that student
            selected_student = None
            if st.session_state['selected_student'] is not None:
                selected_student = st.session_state['selected_student']
                # Clear the selection after using it
                st.session_state['selected_student'] = None
            
            # If no student was selected from the list, use the selectbox
            if selected_student is None:
                selected_student = st.selectbox(
                    "Select Student",
                    options=students,
                    format_func=lambda x: f"{filtered_df[filtered_df['student_id'] == x]['first_name'].iloc[0]} {filtered_df[filtered_df['student_id'] == x]['last_name'].iloc[0]}",
                    key="dashboard_student_select"
                )
            
            if st.button("Analyze Student", key="dashboard_analyze"):
                display_student_dashboard(selected_student, date_filter)
        else:
            st.warning("No students found matching the search criteria.")
    
    # Student List Tab
    with tab2:
        st.title("Student List")
        
        # Group students by ID and get unique students
        unique_students = df.groupby('student_id').agg({
            'first_name': 'first',
            'last_name': 'first',
            'teacher_name': 'first',
            'date': 'max'
        }).reset_index()
        
        # Add search functionality for the student list
        search_term = st.text_input("Search students", "", key="student_search")
        
        # Filter students based on search
        if search_term:
            unique_students = unique_students[
                unique_students['first_name'].str.contains(search_term, case=False) |
                unique_students['last_name'].str.contains(search_term, case=False) |
                unique_students['student_id'].astype(str).str.contains(search_term, case=False)
            ]
        
        # Add filter and sort options
        col1, col2 = st.columns(2)
        with col1:
            filter_option = st.selectbox(
                "Filter by",
                ["All", "Teacher", "Subject", "Progress Level"],
                key="student_filter"
            )
            
            if filter_option == "Teacher":
                teacher_filter = st.selectbox(
                    "Select Teacher",
                    ["All"] + list(unique_students['teacher_name'].unique()),
                    key="teacher_filter"
                )
                if teacher_filter != "All":
                    unique_students = unique_students[unique_students['teacher_name'] == teacher_filter]
            
            elif filter_option == "Subject":
                subject_filter = st.selectbox(
                    "Select Subject",
                    ["All"] + list(df['subject'].unique()),
                    key="subject_filter"
                )
                if subject_filter != "All":
                    student_ids_with_subject = df[df['subject'] == subject_filter]['student_id'].unique()
                    unique_students = unique_students[unique_students['student_id'].isin(student_ids_with_subject)]
            
            elif filter_option == "Progress Level":
                progress_level = st.selectbox(
                    "Select Progress Level",
                    ["All", "High (80%+)", "Medium (40-79%)", "Low (<40%)"],
                    key="progress_filter"
                )
                if progress_level != "All":
                    student_progress = {}
                    for student_id in unique_students['student_id']:
                        student_data = df[df['student_id'] == student_id]
                        progress = calculate_progress(student_data)
                        student_progress[student_id] = progress
                    
                    if progress_level == "High (80%+)":
                        filtered_ids = [sid for sid, prog in student_progress.items() if prog >= 80]
                    elif progress_level == "Medium (40-79%)":
                        filtered_ids = [sid for sid, prog in student_progress.items() if 40 <= prog < 80]
                    else:  # Low (<40%)
                        filtered_ids = [sid for sid, prog in student_progress.items() if prog < 40]
                    
                    unique_students = unique_students[unique_students['student_id'].isin(filtered_ids)]
        
        with col2:
            sort_option = st.selectbox(
                "Sort by",
                ["Name", "Progress (High to Low)", "Progress (Low to High)", "Last Activity", "Teacher"],
                key="student_sort"
            )
        
        if sort_option == "Name":
            unique_students = unique_students.sort_values(['first_name', 'last_name'])
        elif sort_option == "Progress (High to Low)":
            student_progress = {}
            for student_id in unique_students['student_id']:
                student_data = df[df['student_id'] == student_id]
                progress = calculate_progress(student_data)
                student_progress[student_id] = progress
            unique_students['progress'] = unique_students['student_id'].map(student_progress)
            unique_students = unique_students.sort_values('progress', ascending=False)
        elif sort_option == "Progress (Low to High)":
            student_progress = {}
            for student_id in unique_students['student_id']:
                student_data = df[df['student_id'] == student_id]
                progress = calculate_progress(student_data)
                student_progress[student_id] = progress
            unique_students['progress'] = unique_students['student_id'].map(student_progress)
            unique_students = unique_students.sort_values('progress')
        elif sort_option == "Last Activity":
            unique_students = unique_students.sort_values('date', ascending=False)
        elif sort_option == "Teacher":
            unique_students = unique_students.sort_values('teacher_name')
        
        # Add buttons for selection actions
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("Clear Selection", key="clear_selection"):
                st.session_state['selected_students'] = set()
                st.experimental_rerun()
        with col2:
            if st.button("View Selected Students", key="view_selected"):
                if len(st.session_state['selected_students']) > 0:
                    st.session_state['active_tab'] = "Comparison View"
                    st.experimental_rerun()
                else:
                    st.warning("Please select at least one student to compare")
        with col3:
            if len(st.session_state['selected_students']) > 0:
                # Create a report for selected students
                report_data = []
                for student_id in st.session_state['selected_students']:
                    summary = get_student_summary(df, student_id)
                    if summary:
                        report_data.append({
                            'student_name': summary['name'],
                            'teacher': summary['teacher'],
                            'total_questions': summary['total_questions'],
                            'total_skills_practiced': summary['total_skills_practiced'],
                            'total_skills_mastered': summary['total_skills_mastered'],
                            'latest_date': summary['latest_date'].strftime('%Y-%m-%d') if pd.notnull(summary['latest_date']) else 'Unknown'
                        })
                
                if report_data:
                    report_df = pd.DataFrame(report_data)
                    csv = report_df.to_csv(index=False)
                    st.download_button(
                        label="Download Selected Report",
                        data=csv,
                        file_name="selected_students_report.csv",
                        mime="text/csv",
                        key="download_selected"
                    )
            else:
                st.button("Download Selected Report", key="download_selected_disabled", disabled=True)
        with col4:
            st.write(f"Selected: {len(st.session_state['selected_students'])} students")
        
        # Display students in cards
        for _, student in unique_students.iterrows():
            status = get_student_status_indicators(student['student_id'], df)
            if status is None:
                continue
            
            with st.container():
                box_class = "student-box selected" if student['student_id'] in st.session_state['selected_students'] else "student-box"
                st.markdown(f'<div class="{box_class}">', unsafe_allow_html=True)
                
                # Student header with name and selection button
                activity_icon, activity_text, status_class = get_activity_status(status['days_since_activity'])
                total_subjects = len(df['subject'].unique())
                student_data = df[df['student_id'] == student['student_id']]
                
                st.markdown(
                    f'<div class="student-header">'
                    f'<div class="student-info">'
                    f'<h3 class="student-name">{student["first_name"]} {student["last_name"]}</h3>'
                    f'<p class="student-details">ID: {student["student_id"]}</p>'
                    f'<p class="student-details">Teacher: {student["teacher_name"]}</p>'
                    f'</div>'
                    f'<div class="student-actions">'
                    f'<div class="status-indicator {status_class}">'
                    f'{activity_icon} {activity_text}'
                    f'</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Selection checkbox
                is_selected = st.checkbox(
                    "Select for comparison",
                    key=f"select_{student['student_id']}",
                    value=student['student_id'] in st.session_state['selected_students']
                )
                
                if is_selected:
                    st.session_state['selected_students'].add(student['student_id'])
                else:
                    st.session_state['selected_students'].discard(student['student_id'])
                
                # Quick actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("View Dashboard", key=f"list_dashboard_btn_{student['student_id']}"):
                        st.session_state['selected_student'] = student['student_id']
                        st.session_state['active_tab'] = "Student Dashboard"
                        st.experimental_rerun()
                with col2:
                    summary = get_student_summary(df, student['student_id'])
                    report_data = [{
                        'student_name': summary['name'],
                        'teacher': summary['teacher'],
                        'total_questions': summary['total_questions'],
                        'total_skills_practiced': summary['total_skills_practiced'],
                        'total_skills_mastered': summary['total_skills_mastered'],
                        'latest_date': summary['latest_date'].strftime('%Y-%m-%d') if pd.notnull(summary['latest_date']) else 'Unknown'
                    }]
                    report_df = pd.DataFrame(report_data)
                    csv = report_df.to_csv(index=False)
                    st.download_button(
                        label="Download Report",
                        data=csv,
                        file_name=f"student_report_{student['student_id']}.csv",
                        mime="text/csv",
                        key=f"list_report_btn_{student['student_id']}"
                    )
                with col3:
                    if st.button("Compare with Class", key=f"list_compare_btn_{student['student_id']}"):
                        st.session_state['selected_students'].add(student['student_id'])
                        st.session_state['active_tab'] = "Comparison View"
                        st.experimental_rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Comparison View Tab
    with tab3:
        st.title("Student Comparison")
        if len(st.session_state['selected_students']) == 0:
            st.warning("No students selected for comparison. Please select students from the Student List tab.")
        else:
            # Display comparison view for selected students
            for student_id in st.session_state['selected_students']:
                summary = get_student_summary(df, student_id)
                if summary:
                    with st.expander(f"{summary['name']} - {summary['teacher']}", expanded=True):
                        # Overall Progress
                        st.subheader("Overall Progress")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Questions", summary['total_questions'])
                        with col2:
                            st.metric("Skills Practiced", summary['total_skills_practiced'])
                        with col3:
                            st.metric("Skills Mastered", summary['total_skills_mastered'])
                        with col4:
                            avg_growth = round(sum(data['predicted_growth'] for data in summary['subject_breakdown'].values()) / len(summary['subject_breakdown']))
                            st.metric("Predicted Growth", f"+{avg_growth}%", 
                                    delta=f"+{avg_growth - 50}%" if avg_growth > 50 else None)
                        
                        # Subject Comparison Chart
                        st.subheader("Subject Comparison")
                        subjects = list(summary['subject_breakdown'].keys())
                        progress_values = [data['progress'] for data in summary['subject_breakdown'].values()]
                        mastery_rates = [data['mastery_rate'] for data in summary['subject_breakdown'].values()]
                        efficiency_scores = [data['efficiency'] for data in summary['subject_breakdown'].values()]
                        
                        fig = go.Figure(data=[
                            go.Bar(name='Progress', x=subjects, y=progress_values, marker_color='#7ba7c2'),
                            go.Bar(name='Mastery Rate', x=subjects, y=mastery_rates, marker_color='#5d8aa8'),
                            go.Bar(name='Efficiency', x=subjects, y=efficiency_scores, marker_color='#d1b280')
                        ])
                        
                        fig.update_layout(
                            barmode='group',
                            title='Subject Performance Comparison',
                            xaxis_title='Subject',
                            yaxis_title='Percentage',
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Metric Breakdown Charts
                        st.subheader("Metric Breakdown")
                        
                        # Create tabs for different metric visualizations
                        metric_tabs = st.tabs(["Skills Progress", "IXL Progress", "IXL Term Performance"])
                        
                        with metric_tabs[0]:
                            # Skills Progress Chart
                            fig = go.Figure()
                            
                            for subject in subjects:
                                subject_data = summary['subject_breakdown'][subject]
                                fig.add_trace(go.Bar(
                                    name=subject,
                                    x=['Skills Practiced', 'Skills Mastered'],
                                    y=[subject_data['skills_practiced'], subject_data['skills_mastered']],
                                    text=[subject_data['skills_practiced'], subject_data['skills_mastered']],
                                    textposition='auto',
                                    textfont=dict(
                                        color='black',
                                        size=12,
                                        family='Arial'
                                    )
                                ))
                            
                            fig.update_layout(
                                title={
                                    'text': 'Skills Progress by Subject',
                                    'font': dict(
                                        color='black',
                                        size=18,
                                        family='Arial'
                                    ),
                                    'x': 0.5,
                                    'y': 0.95
                                },
                                barmode='group',
                                xaxis_title='Metric',
                                yaxis_title='Count',
                                plot_bgcolor='white',
                                paper_bgcolor='white',
                                font=dict(
                                    color='black',
                                    size=12,
                                    family='Arial'
                                ),
                                xaxis=dict(
                                    tickfont=dict(
                                        color='black',
                                        size=10,
                                        family='Arial'
                                    )
                                ),
                                yaxis=dict(
                                    tickfont=dict(
                                        color='black',
                                        size=10,
                                        family='Arial'
                                    )
                                ),
                                margin=dict(t=50, b=50, l=50, r=50)
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with metric_tabs[1]:
                            # IXL Progress Over Time
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Math Progress Chart
                                fig_math = go.Figure()
                                try:
                                    # Check if required columns exist
                                    if 'End date' not in student_data.columns or 'Ending diagnostic level - Math' not in student_data.columns:
                                        st.warning("Required columns for Math progress visualization are missing.")
                                    else:
                                        fig_math.add_trace(go.Bar(
                                            x=student_data['End date'].dt.strftime('%Y-%m-%d'),
                                            y=student_data['Ending diagnostic level - Math'],
                                            name='Math Level',
                                            marker_color='#2196F3',
                                            text=student_data['Ending diagnostic level - Math'],
                                            textposition='outside',
                                            textfont=dict(
                                                color='black',
                                                size=12,
                                                family='Arial'
                                            ),
                                            hovertemplate='Date: %{x}<br>Level: %{y}<extra></extra>'
                                        ))
                                        fig_math.update_layout(
                                            title={
                                                'text': 'Math Diagnostic Level Over Time',
                                                'x': 0.5,
                                                'xanchor': 'center',
                                                'y': 0.95,
                                                'yanchor': 'top',
                                                'font': dict(
                                                    color='black',
                                                    size=18,
                                                    family='Arial'
                                                )
                                            },
                                            xaxis_title='Date',
                                            yaxis_title='Diagnostic Level',
                                            template='plotly_white',
                                            height=400,
                                            font=dict(
                                                color='black',
                                                size=12,
                                                family='Arial'
                                            ),
                                            xaxis=dict(
                                                tickfont=dict(
                                                    color='black',
                                                    size=10,
                                                    family='Arial'
                                                ),
                                                tickangle=45
                                            ),
                                            yaxis=dict(
                                                tickfont=dict(
                                                    color='black',
                                                    size=10,
                                                    family='Arial'
                                                )
                                            ),
                                            margin=dict(t=50, b=50, l=50, r=50),
                                            plot_bgcolor='white',
                                            paper_bgcolor='white'
                                        )
                                        st.plotly_chart(fig_math, use_container_width=True)
                                except Exception as e:
                                    st.error(f"Error creating Math progress chart: {str(e)}")
                            
                            with col2:
                                # ELA Progress Chart
                                fig_ela = go.Figure()
                                try:
                                    # Check if required columns exist
                                    if 'End date' not in student_data.columns or 'Ending diagnostic level - ELA' not in student_data.columns:
                                        st.warning("Required columns for ELA progress visualization are missing.")
                                    else:
                                        fig_ela.add_trace(go.Bar(
                                            x=student_data['End date'].dt.strftime('%Y-%m-%d'),
                                            y=student_data['Ending diagnostic level - ELA'],
                                            name='ELA Level',
                                            marker_color='#FFC107',
                                            text=student_data['Ending diagnostic level - ELA'],
                                            textposition='outside',
                                            textfont=dict(
                                                color='black',
                                                size=12,
                                                family='Arial'
                                            ),
                                            hovertemplate='Date: %{x}<br>Level: %{y}<extra></extra>'
                                        ))
                                        fig_ela.update_layout(
                                            title={
                                                'text': 'ELA Diagnostic Level Over Time',
                                                'x': 0.5,
                                                'xanchor': 'center',
                                                'y': 0.95,
                                                'yanchor': 'top',
                                                'font': dict(
                                                    color='black',
                                                    size=18,
                                                    family='Arial'
                                                )
                                            },
                                            xaxis_title='Date',
                                            yaxis_title='Diagnostic Level',
                                            template='plotly_white',
                                            height=400,
                                            font=dict(
                                                color='black',
                                                size=12,
                                                family='Arial'
                                            ),
                                            xaxis=dict(
                                                tickfont=dict(
                                                    color='black',
                                                    size=10,
                                                    family='Arial'
                                                ),
                                                tickangle=45
                                            ),
                                            yaxis=dict(
                                                tickfont=dict(
                                                    color='black',
                                                    size=10,
                                                    family='Arial'
                                                )
                                            ),
                                            margin=dict(t=50, b=50, l=50, r=50),
                                            plot_bgcolor='white',
                                            paper_bgcolor='white'
                                        )
                                        st.plotly_chart(fig_ela, use_container_width=True)
                                except Exception as e:
                                    st.error(f"Error creating ELA progress chart: {str(e)}")
                        
                        with metric_tabs[2]:
                            # IXL Term Performance
                            try:
                                # Check if required columns exist
                                if 'End date' not in student_data.columns:
                                    st.warning("Required date column for term performance visualization is missing.")
                                    st.stop()
                                
                                # Add term information
                                def get_term(date):
                                    if pd.isna(date): return None
                                    month = date.month
                                    if 8 <= month <= 12: return "Fall"
                                    elif 1 <= month <= 6: return "Spring"
                                    return None
                                
                                student_data['Term'] = student_data['End date'].apply(get_term)
                                
                                # Term selection
                                selected_term = st.selectbox("Select Term", ["Fall", "Spring"])
                                term_data = student_data[student_data['Term'] == selected_term]
                                
                                if term_data.empty:
                                    st.warning(f"No data available for {selected_term} term.")
                                    st.stop()
                                
                                # Get the most recent diagnostic for this term
                                latest_data = term_data.sort_values(by="End date", ascending=False).iloc[0]
                                
                                # Calculate percentiles
                                math_start_pct = get_percentile(
                                    df[df['Term'] == selected_term]['Starting diagnostic level - Math'],
                                    latest_data['Starting diagnostic level - Math']
                                )
                                
                                math_end_pct = get_percentile(
                                    df[df['Term'] == selected_term]['Ending diagnostic level - Math'],
                                    latest_data['Ending diagnostic level - Math']
                                )
                                
                                ela_start_pct = get_percentile(
                                    df[df['Term'] == selected_term]['Starting diagnostic level - ELA'],
                                    latest_data['Starting diagnostic level - ELA']
                                )
                                
                                ela_end_pct = get_percentile(
                                    df[df['Term'] == selected_term]['Ending diagnostic level - ELA'],
                                    latest_data['Ending diagnostic level - ELA']
                                )
                                
                                # Create two columns for the donut charts
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    if math_start_pct is not None and math_end_pct is not None:
                                        st.plotly_chart(draw_donut_chart("Math", math_start_pct, math_end_pct, selected_term), use_container_width=True)
                                    else:
                                        st.info("Student Has Not Completed Enough Math Training-Sets To Receive a Score")
                                
                                with col2:
                                    if ela_start_pct is not None and ela_end_pct is not None:
                                        st.plotly_chart(draw_donut_chart("ELA", ela_start_pct, ela_end_pct, selected_term), use_container_width=True)
                                    else:
                                        st.info("Student Has Not Completed Enough ELA Training-Sets To Receive a Score")
                            except Exception as e:
                                st.error(f"Error creating term performance visualization: {str(e)}")
    
    # Raw Data Tab
    with tab4:
        st.title("Raw Data")
        st.dataframe(df)
        
        # Download button for raw data
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Raw Data",
            data=csv,
            file_name="student_data.csv",
            mime="text/csv"
        )
else:
    st.error("Failed to load data. Please check if the data file exists and is properly formatted.") 