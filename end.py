import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

st.set_page_config(layout="wide", page_title="لوحة معلومات هيئة الصحة العامة بنجران", page_icon="images/R (1).png")
# Initialize session state for health data if not already set
if 'health_df' not in st.session_state:
    st.session_state.health_df = pd.DataFrame({
        'الشهر': ['يناير 2025', 'فبراير 2025', 'مارس 2025', 'أبريل 2025', 'مايو 2025', 'يونيو 2025',
                  'يوليو 2025', 'أغسطس 2025', 'سبتمبر 2025', 'أكتوبر 2025', 'نوفمبر 2025', 'ديسمبر 2025'],
        'عدد العابرين': [185726, 200682, 163291, 106674, 86673, 104816, 0, 0, 0, 0, 0, 0],
        'عدد المعتمرين': [88806, 120930, 96027, 4316, 0, 17697, 0, 0, 0, 0, 0, 0],
        'عدد الحجاج': [0, 0, 0, 0, 12951, 0, 0, 0, 0, 0, 0, 0],
        'زيارات العيادة': [2490, 2129, 1640, 1362, 1223, 1015, 0, 0, 0, 0, 0, 0],
        'حالات النقل الإسعافي وحالات الإشتباه': [7, 8, 3, 5, 21, 11, 0, 0, 0, 0, 0, 0],
        'الجولات الإشرافية': [2, 3, 2, 1, 2, 2, 0, 0, 0, 0, 0, 0],
        'شلل الأطفال': [185726, 200682, 163291, 106674, 86673, 104816, 0, 0, 0, 0, 0, 0],
        'مخية شوكية': [88806, 120930, 96027, 4316, 0, 17697, 0, 0, 0, 0, 0, 0],
        'ثلاثي فيروسي': [2490, 2129, 1640, 1362, 1223, 1015, 0, 0, 0, 0, 0, 0],
        'مجموع التطعيمات': [104730, 109856, 67885, 53470, 62147, 62745, 0, 0, 0, 0, 0, 0],
        'المجموع الكلي': [381761, 433606, 328847, 165829, 163017, 186286, 0, 0, 0, 0, 0, 0]
    })
# Initialize session state for auto-refresh settings
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'refresh_rate' not in st.session_state:
    st.session_state.refresh_rate = 30
# Define default analysis settings
analysis_type = "شامل"
time_period = "جميع الأشهر"
viz_type = ["خطي", "أعمدة", "دائري"]
show_predictions = True
show_correlations = True
show_clusters = False
# Function to update quarterly data in the DataFrame
def update_quarter_data(quarter, index, new_data):
    st.session_state.health_df.at[index, 'عدد العابرين'] = new_data['عدد العابرين']
    st.session_state.health_df.at[index, 'عدد المعتمرين'] = new_data['عدد المعتمرين']
    st.session_state.health_df.at[index, 'عدد الحجاج'] = new_data['عدد الحجاج']
    st.session_state.health_df.at[index, 'زيارات العيادة'] = new_data['زيارات العيادة']
    st.session_state.health_df.at[index, 'حالات النقل الإسعافي وحالات الإشتباه'] = new_data['حالات النقل الإسعافي وحالات الإشتباه']
    st.session_state.health_df.at[index, 'الجولات الإشرافية'] = new_data['الجولات الإشرافية']
    st.session_state.health_df.at[index, 'شلل الأطفال'] = new_data['شلل الأطفال']
    st.session_state.health_df.at[index, 'مخية شوكية'] = new_data['مخية شوكية']
    st.session_state.health_df.at[index, 'ثلاثي فيروسي'] = new_data['ثلاثي فيروسي']
    total_vaccinations = new_data['شلل الأطفال'] + new_data['مخية شوكية'] + new_data['ثلاثي فيروسي']
    st.session_state.health_df.at[index, 'مجموع التطعيمات'] = total_vaccinations
    st.session_state.health_df.at[index, 'المجموع الكلي'] = (
        new_data['عدد العابرين'] + new_data['عدد المعتمرين'] + new_data['عدد الحجاج'] +
        new_data['زيارات العيادة'] + new_data['حالات النقل الإسعافي وحالات الإشتباه'] +
        new_data['الجولات الإشرافية'] + total_vaccinations
    )
#custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@200;300;400;600;700;800&family=Amiri:wght@400;700&display=swap');
:root {
    --primary-gradient: linear-gradient(135deg, #22577A 0%, #38A3A5 100%);
    --secondary-gradient: linear-gradient(135deg, #57CC99 0%, #80ED99 100%);
    --tertiary-gradient: linear-gradient(135deg, #2794EB 0%, #BFF8D4 100%);
    --success-gradient: linear-gradient(135deg, #80ED99 0%, #BFF8D4 100%);
    --warning-gradient: linear-gradient(135deg, #57CC99 0%, #80ED99 100%);
    --danger-gradient: linear-gradient(135deg, #22577A 0%, #38A3A5 100%);
    --glass-bg: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.1);
    --dark-glass: rgba(0, 0, 0, 0.5);
    --shadow-glow: 0 8px 32px rgba(34, 87, 122, 0.37);
    --shadow-premium: 0 15px 35px rgba(0, 0, 0, 0.4);
    --text-primary: #BFF8D4;
    --text-secondary: rgba(255, 255, 255, 0.7);
    --text-accent: #80ED99;
    --radius-lg: 16px;
    --radius-md: 12px;
    --radius-sm: 8px;
    --transition-main: all 0.3s ease;
}
.stApp {
    background: 
        radial-gradient(circle at 20% 80%, #22577A 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, #38A3A5 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, #57CC99 0%, transparent 50%),
        linear-gradient(135deg, #0A0A0A 0%, #121212 50%, #1C2526 100%);
    background-size: 400% 400%;
    animation: backgroundShift 20s ease infinite;
    color: var(--text-primary);
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    min-height: 100vh;
    padding: 0 !important;
    margin: 0 !important;
}
@keyframes backgroundShift {
    0%, 100% { background-position: 0% 50%; }
    33% { background-position: 100% 0%; }
    66% { background-position: 100% 100%; }
}
.main-header {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: 2rem 1rem;
    margin: 1rem 0;
    text-align: center;
    box-shadow: var(--shadow-glow);
    position: relative;
    overflow: hidden;
    animation: headerFloat 6s ease-in-out infinite;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.05), transparent);
    animation: shimmer 3s linear infinite;
}
@keyframes headerFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
@keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}
.metric-card {
    background: var(--glass-bg);
    backdrop-filter: blur(15px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    padding: 1rem;
    margin: 0.5rem 0;
    min-height: 180px;
    text-align: center;
    box-shadow: var(--shadow-glow);
    transition: var(--transition-main);
    position: relative;
    animation: cardSlideIn 0.8s ease-out;
}
.metric-card:hover {
    transform: translateY(-15px) scale(1.02);
    box-shadow: 0 20px 40px rgba(34, 87, 122, 0.5);
    border-color: var(--text-accent);
}
.metric-card.updated {
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0% { box-shadow: var(--shadow-glow); }
    50% { box-shadow: 0 0 20px rgba(128, 237, 153, 0.8); }
    100% { box-shadow: var(--shadow-glow); }
}
.metric-value {
    font-size: 2.5rem;
    font-weight: 800;
    background: var(--secondary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    animation: valueCount 2s ease-out;
}
.metric-label {
    font-size: 1.3rem;
    color: var(--text-secondary);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.metric-status {
    font-size: 0.9rem;
    padding: 0.4rem 1rem;
    border-radius: var(--radius-sm);
    display: inline-block;
}
.insight-badge, .warning-badge, .danger-badge {
    margin: 0.25rem;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    padding: 0.4rem 1rem;
    font-weight: 600;
    transition: var(--transition-main);
}
.insight-badge { background: var(--success-gradient); color: #0A0A0A; }
.warning-badge { background: var(--warning-gradient); color: #0A0A0A; }
.danger-badge { background: var(--danger-gradient); color: #0A0A0A; }
.insight-badge:hover, .warning-badge:hover, .danger-badge:hover {
    transform: scale(1.1);
}
.chart-title {
    color: var(--text-primary);
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-align: center;
    border-bottom: 2px solid var(--text-accent);
    padding-bottom: 0.5rem;
}
.analysis-card {
    background: var(--dark-glass);
    backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    padding: 1rem;
    margin: 0.5rem 0;
    border-right: 4px solid var(--text-accent);
    box-shadow: var(--shadow-premium);
    animation: fadeInLeft 0.8s ease-out;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.analysis-title {
    font-size: 1.2rem;
    color: var(--text-accent);
    font-weight: 600;
}
.analysis-text {
    font-size: 1.1rem;
    color: var(--text-secondary);
    line-height: 1.6;
    flex-grow: 1;
    max-height: 100px;
    overflow-y: auto;
}
.stButton > button {
    background: var(--primary-gradient);
    color: #0A0A0A;
    border: none;
    border-radius: var(--radius-md);
    padding: 0.8rem 1.5rem;
    font-weight: 600;
    transition: var(--transition-main);
    box-shadow: var(--shadow-premium);
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 30px rgba(34, 87, 122, 0.4);
}
.section-divider {
    height: 2px;
    background: var(--primary-gradient);
    border: none;
    margin: 1rem 0;
    animation: dividerGlow 3s ease-in-out infinite;
}
/* Custom styling for Streamlit tabs */
.stTabs [data-baseweb="tab"] {
    background-color: #1C2526; /* Default tab background */
    color: var(--text-secondary); /* Default text color */
    border: none; /* Remove any border */
    padding: 10px 20px;
    margin: 0 5px;
    border-radius: var(--radius-md);
    transition: all 0.3s ease;
    text-decoration: none; /* Remove underline */
}

/* Style for the active tab */
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #80ED99; /* Green color for active tab */
    color: #0A0A0A; /* Dark text for contrast */
    font-weight: 600;
    box-shadow: var(--shadow-glow);
    border: none; /* Ensure no border */
    outline: none; /* Remove outline */
    text-decoration: none; /* Remove underline */
}

/* Optional: Use off-white for active tab (uncomment to use instead of green) */
/*
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #F5F5F5; /* Off-white color */
    color: #1C2526; /* Dark text for contrast */
    font-weight: 600;
    box-shadow: var(--shadow-glow);
    border: none; /* Ensure no border */
    outline: none; /* Remove outline */
    text-decoration: none; /* Remove underline */
}
*/

/* Remove any default Streamlit red underline or border */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: none; /* Remove bottom border */
}
.stTabs [data-baseweb="tab-panel"] {
    border: none; /* Remove panel border */
}
@keyframes dividerGlow {
    0%, 100% { box-shadow: 0 0 5px rgba(34, 87, 122, 0.5); }
    50% { box-shadow: 0 0 20px rgba(34, 87, 122, 0.8); }
}
@keyframes cardSlideIn {
    from { transform: translateY(50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
@keyframes fadeInLeft {
    from { transform: translateX(-30px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes valueCount {
    from { transform: scale(0); }
    to { transform: scale(1); }
}
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: var(--dark-glass);
    border-radius: var(--radius-sm);
}
::-webkit-scrollbar-thumb {
    background: var(--primary-gradient);
    border-radius: var(--radius-sm);
}
::-webkit-scrollbar-thumb:hover {
    background: var(--secondary-gradient);
}
.gauge-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 0.001rem;
}
.gauge-container .plotly {
    max-height: 300px;
    transition: var(--transition-main);
}
.gauge-container:hover .plotly {
    transform: scale(1.05);
}
@media (max-width: 768px) {
    .main-header, .chart-container, .metric-card, .analysis-card {
        padding: 0.8rem;
        margin: 0.8rem 0;
    }
    .metric-value { font-size: 2rem; }
    .metric-label { font-size: 1.1rem; }
    .analysis-text { font-size: 0.95rem; max-height: 80px; }
    .gauge-container .plotly { max-height: 200px; }
}
@media (max-width: 480px) {
    .metric-value { font-size: 1.8rem; }
    .insight-badge, .warning-badge, .danger-badge {
        font-size: 0.8rem;
        padding: 0.3rem 0.8rem;
    }
}
</style>
""", unsafe_allow_html=True)
#header section
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3rem; font-weight: 800; color: white;">
         لوحة معلومات هيئة الصحة العامة بنجران
    </h1>
    <p style="font-size: 1.5rem; color: var(--text-secondary);">
        تحليلات متقدمة للأداء الصحي في المنافذ - 2025
    </p>
</div>
""", unsafe_allow_html=True)
# Auto-refresh toggle
st.markdown(f"""
<div class="floating-stats" style="position: fixed; top: 100px; right: 20px; background: var(--glass-bg); backdrop-filter: blur(15px); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 1.5rem; box-shadow: var(--shadow-glow); z-index: 1000; animation: floatUpDown 4s ease-in-out infinite; font-size: 1rem; color: var(--text-secondary);">
     إحصائيات سريعة<br>
     المجموع الكلي: {st.session_state.health_df['المجموع الكلي'].sum():,}<br>
     التطعيمات: {st.session_state.health_df['مجموع التطعيمات'].sum():,}<br>
     العابرين: {st.session_state.health_df['عدد العابرين'].sum():,}
</div>
<style>
@keyframes floatUpDown {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }}
}}
</style>
""", unsafe_allow_html=True)
# Analysis settings
filtered_df = st.session_state.health_df
if time_period != "جميع الأشهر":
    if time_period == "الربع الأول":
        filtered_df = st.session_state.health_df.iloc[0:3]
    elif time_period == "الربع الثاني":
        filtered_df = st.session_state.health_df.iloc[3:6]
    elif time_period == "الربع الثالث":
        filtered_df = st.session_state.health_df.iloc[6:9]
    elif time_period == "الربع الرابع":
        filtered_df = st.session_state.health_df.iloc[9:12]
    elif time_period == "شهر واحد":
        month = st.selectbox("اختر الشهر:", st.session_state.health_df['الشهر'].unique())
        filtered_df = st.session_state.health_df[st.session_state.health_df['الشهر'] == month]
# Display analysis type
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> المؤشرات الرئيسية</div>', unsafe_allow_html=True)
# Create columns for key metrics
col1, col2, col3, col4 = st.columns(4)
# Displaying key metrics
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['عدد العابرين'].sum():,}</div>
        <div class="metric-label">إجمالي العابرين</div>
        <div class="metric-status insight-badge">مستقر</div>
    </div>
    """, unsafe_allow_html=True)
# Displaying total pilgrims and umrah performers
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['عدد المعتمرين'].sum() + filtered_df['عدد الحجاج'].sum():,}</div>
        <div class="metric-label">إجمالي المعتمرين والحجاج</div>
        <div class="metric-status warning-badge">موسمي</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['زيارات العيادة'].sum():,}</div>
        <div class="metric-label">زيارات العيادة</div>
        <div class="metric-status insight-badge">مستقر</div>
    </div>
    """, unsafe_allow_html=True)
# Displaying emergency cases
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['حالات النقل الإسعافي وحالات الإشتباه'].sum():,}</div>
        <div class="metric-label">حالات الطوارئ</div>
        <div class="metric-status danger-badge">يحتاج متابعة</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
# Displaying total pilgrims and umrah performers
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> تحليل المجموع الكلي</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
# Displaying total monthly sum
with col1:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> المجموع الكلي لكل شهر</h4>', unsafe_allow_html=True)
    fig_total_monthly = go.Figure()
    fig_total_monthly.add_trace(go.Bar(
        x=filtered_df['الشهر'],
        y=filtered_df['المجموع الكلي'],
        name='المجموع الكلي',
        marker_color='#22577A',
        text=filtered_df['المجموع الكلي'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>المجموع الكلي: %{y:,}<extra></extra>'
    ))
    fig_total_monthly.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        yaxis_title='المجموع الكلي',
        height=600,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    st.plotly_chart(fig_total_monthly, use_container_width=True)
# Displaying total quarterly sum
with col2:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> المجموع الكلي لكل ربع</h4>', unsafe_allow_html=True)
    quarters_data = {
        'الربع': ['الربع الأول', 'الربع الثاني', 'الربع الثالث', 'الربع الرابع'],
        'المجموع الكلي': [
            st.session_state.health_df.iloc[0:3]['المجموع الكلي'].sum(),
            st.session_state.health_df.iloc[3:6]['المجموع الكلي'].sum(),
            st.session_state.health_df.iloc[6:9]['المجموع الكلي'].sum(),
            st.session_state.health_df.iloc[9:12]['المجموع الكلي'].sum()
        ]
    }
    quarters_data['المجموع الكلي'] = [max(1, val) for val in quarters_data['المجموع الكلي']]
    fig_total_quarterly = go.Figure(data=[go.Pie(
        labels=quarters_data['الربع'],
        values=quarters_data['المجموع الكلي'],
        hole=0.4,
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(
            colors=['#22577A', '#38A3A5', '#57CC99', '#80ED99'],
            line=dict(color='#0A0A0A', width=2)
        ),
        hovertemplate='الربع: %{label}<br>المجموع الكلي: %{value:,}<br>النسبة: %{percent}<extra></extra>',
        pull=[0.1, 0, 0, 0]
    )])
    fig_total_quarterly.add_annotation(
        text=f"إجمالي<br>{sum(quarters_data['المجموع الكلي']):,}",
        x=0.5, y=0.5,
        font_size=18,
        font_color='var(--text-primary)',
        showarrow=False
    )
    fig_total_quarterly.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600
    )
    st.plotly_chart(fig_total_quarterly, use_container_width=True)
# Displaying total monthly sum
st.markdown('</div>', unsafe_allow_html=True)

# تحليل التطعيمات
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> تحليل التطعيمات</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
# Displaying vaccination trends, distribution, and heatmap
with col1:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> اتجاهات التطعيمات</h4>', unsafe_allow_html=True)
    filtered_vacc_df = filtered_df[filtered_df['شلل الأطفال'].notnull()]
    fig_vacc_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_vacc_trend.add_trace(
        go.Scatter(
            x=filtered_vacc_df['الشهر'], 
            y=filtered_vacc_df['شلل الأطفال'],
            mode='lines+markers',
            name='شلل الأطفال',
            line=dict(color='#22577A', width=4),
            marker=dict(size=12),
            fill='tonexty',
            text=filtered_vacc_df['شلل الأطفال'].apply(lambda x: f'{x:,}'),
            textposition='top center'
        ),
        secondary_y=False,
    )
    fig_vacc_trend.add_trace(
        go.Scatter(
            x=filtered_vacc_df['الشهر'], 
            y=filtered_vacc_df['مخية شوكية'],
            mode='lines+markers',
            name='مخية شوكية',
            line=dict(color='#38A3A5', width=4),
            marker=dict(size=12),
            text=filtered_vacc_df['مخية شوكية'].apply(lambda x: f'{x:,}'),
            textposition='bottom center'
        ),
        secondary_y=True,
    )
    fig_vacc_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        showlegend=True,
        height=600,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    fig_vacc_trend.update_yaxes(title_text="شلل الأطفال", secondary_y=False, title_font_color='var(--text-primary)')
    fig_vacc_trend.update_yaxes(title_text="مخية شوكية", secondary_y=True, title_font_color='var(--text-primary)')
    st.plotly_chart(fig_vacc_trend, use_container_width=True)
# Displaying vaccination distribution pie chart
with col2:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> توزيع التطعيمات</h4>', unsafe_allow_html=True)
    vaccine_data = {
        'النوع': ['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
        'الإجمالي': [
            filtered_vacc_df['شلل الأطفال'].sum(),
            filtered_vacc_df['مخية شوكية'].sum(),
            filtered_vacc_df['ثلاثي فيروسي'].sum()
        ]
    }
    vaccine_data['الإجمالي'] = [max(1, val) for val in vaccine_data['الإجمالي']]
    fig_vacc_pie = go.Figure(data=[go.Pie(
        labels=vaccine_data['النوع'],
        values=vaccine_data['الإجمالي'],
        hole=0.4,
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(
            colors=['#22577A', '#38A3A5', '#57CC99'],
            line=dict(color='#0A0A0A', width=2)
        ),
        hovertemplate='%{label}<br>العدد: %{value:,}<br>النسبة: %{percent}<extra></extra>',
        pull=[0.1, 0, 0]
    )])
    fig_vacc_pie.add_annotation(
        text=f"إجمالي<br>{sum(vaccine_data['الإجمالي']):,}",
        x=0.5, y=0.5,
        font_size=18,
        font_color='var(--text-primary)',
        showarrow=False
    )
    fig_vacc_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600
    )
    st.plotly_chart(fig_vacc_pie, use_container_width=True)
# Displaying vaccination heatmap
with col3:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> خريطة حرارية للتطعيمات</h4>', unsafe_allow_html=True)
    vacc_matrix = np.array([
        filtered_vacc_df['شلل الأطفال'].values,
        filtered_vacc_df['مخية شوكية'].values,
        filtered_vacc_df['ثلاثي فيروسي'].values
    ])
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=vacc_matrix,
        x=filtered_vacc_df['الشهر'],
        y=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
        colorscale=[[0, '#BFF8D4'], [0.5, '#57CC99'], [1, '#22577A']],
        text=vacc_matrix,
        texttemplate="%{text:,}",
        textfont={"size": 16, "color": "white"},
        hoverongaps=False,
        hovertemplate='الشهر: %{x}<br>التطعيم: %{y}<br>العدد: %{z:,}<extra></extra>'
    ))
    fig_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">تحليل الطوارئ والزيارات الطبية</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
# Displaying clinic visits and emergency cases
with col1:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> زيارات العيادة</h4>', unsafe_allow_html=True)
    filtered_clinic_df = filtered_df[filtered_df['زيارات العيادة'].notnull()]
    fig_clinic = go.Figure()
    fig_clinic.add_trace(go.Bar(
        x=filtered_clinic_df['الشهر'],
        y=filtered_clinic_df['زيارات العيادة'],
        name='زيارات العيادة',
        marker_color='#2794EB',
        text=filtered_clinic_df['زيارات العيادة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>الزيارات: %{y:,}<extra></extra>'
    ))
    fig_clinic.add_trace(go.Scatter(
        x=filtered_clinic_df['الشهر'],
        y=filtered_clinic_df['زيارات العيادة'],
        mode='lines+markers',
        name='الاتجاه',
        line=dict(color='#80ED99', width=3),
        marker=dict(size=8)
    ))
    fig_clinic.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        yaxis_title='عدد الزيارات',
        height=600,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    st.plotly_chart(fig_clinic, use_container_width=True)
# Displaying emergency cases
with col2:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> حالات النقل الإسعافي</h4>', unsafe_allow_html=True)
    filtered_emergency_df = filtered_df[filtered_df['حالات النقل الإسعافي وحالات الإشتباه'].notnull()]
    fig_emergency = go.Figure()
    fig_emergency.add_trace(go.Scatter(
        x=filtered_emergency_df['الشهر'],
        y=filtered_emergency_df['حالات النقل الإسعافي وحالات الإشتباه'],
        mode='lines+markers',
        fill='tonexty',
        name='النقل الإسعافي',
        line=dict(color='#BFF8D4', width=4),
        marker=dict(size=15, color='#57CC99'),
        text=filtered_emergency_df['حالات النقل الإسعافي وحالات الإشتباه'].apply(lambda x: f'{x}' if x > 0 else '0'),
        textposition='top center',
        hovertemplate='الشهر: %{x}<br>الحالات: %{y}<extra></extra>'
    ))
    fig_emergency.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600,
        yaxis=dict(range=[0, max(25, filtered_emergency_df['حالات النقل الإسعافي وحالات الإشتباه'].max() * 1.2)])
    )
    st.plotly_chart(fig_emergency, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
# Quarterly analysis
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> تحليلات الأرباع</div>', unsafe_allow_html=True)

q1_tab, q2_tab, q3_tab, q4_tab = st.tabs(["الربع الأول", "الربع الثاني", "الربع الثالث", "الربع الرابع"])
# Quarter 1 analysis
with q1_tab:
    q1_df = filtered_df[filtered_df['الشهر'].isin(['يناير 2025', 'فبراير 2025', 'مارس 2025'])]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> تطور عدد العابرين والمعتمرين - الربع الأول</h4>', unsafe_allow_html=True)
        fig_q1_travelers = go.Figure()
        fig_q1_travelers.add_trace(go.Scatter(
            x=q1_df['الشهر'], 
            y=q1_df['عدد العابرين'],
            mode='lines+markers+text',
            name='العابرين',
            line=dict(color='#22577A', width=4),
            marker=dict(size=12, color='#38A3A5'),
            text=q1_df['عدد العابرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='top center',
            hovertemplate='الشهر: %{x}<br>العابرين: %{y:,}<br>المعتمرين: %{customdata:,}<extra></extra>',
            customdata=q1_df['عدد المعتمرين']
        ))
        fig_q1_travelers.add_trace(go.Scatter(
            x=q1_df['الشهر'], 
            y=q1_df['عدد المعتمرين'],
            mode='lines+markers+text',
            name='المعتمرين',
            line=dict(color='#57CC99', width=4),
            marker=dict(size=12, color='#80ED99'),
            text=q1_df['عدد المعتمرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='bottom center',
            hovertemplate='الشهر: %{x}<br>المعتمرين: %{y:,}<br>العابرين: %{customdata:,}<extra></extra>',
            customdata=q1_df['عدد العابرين']
        ))
        fig_q1_travelers.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=600,
            transition={'duration': 1000, 'easing': 'cubic-in-out'}
        )
        st.plotly_chart(fig_q1_travelers, use_container_width=True)
    
    with col2:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> زيارات العيادة والنقل الإسعافي - الربع الأول</h4>', unsafe_allow_html=True)
        fig_q1_medical = make_subplots(specs=[[{"secondary_y": True}]])
        fig_q1_medical.add_trace(
            go.Bar(x=q1_df['الشهر'], y=q1_df['زيارات العيادة'], 
                   name='زيارات العيادة', 
                   marker_color='#2794EB',
                   text=q1_df['زيارات العيادة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
                   textposition='auto'),
            secondary_y=False,
        )
        fig_q1_medical.add_trace(
            go.Scatter(x=q1_df['الشهر'], y=q1_df['حالات النقل الإسعافي وحالات الإشتباه'], 
                      mode='lines+markers',
                      name='النقل الإسعافي',
                      line=dict(color='#BFF8D4', width=3),
                      marker=dict(size=10, color='#80ED99'),
                      text=q1_df['حالات النقل الإسعافي وحالات الإشتباه'].apply(lambda x: f'{x}' if x > 0 else '0'),
                      textposition='top center'),
            secondary_y=True,
        )
        fig_q1_medical.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600,
            transition={'duration': 1000, 'easing': 'cubic-in-out'}
        )
        fig_q1_medical.update_yaxes(title_text="زيارات العيادة", secondary_y=False, title_font_color='var(--text-primary)')
        fig_q1_medical.update_yaxes(title_text="النقل الإسعافي", secondary_y=True, title_font_color='var(--text-primary)')
        st.plotly_chart(fig_q1_medical, use_container_width=True)
    
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;">تحليل التطعيمات حسب النوع - الربع الأول</h4>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_q1_vacc_3d = go.Figure()
        months = q1_df['الشهر']
        fig_q1_vacc_3d.add_trace(go.Scatter3d(
            x=months,
            y=['شلل الأطفال'] * len(months),
            z=q1_df['شلل الأطفال'],
            mode='markers+lines',
            marker=dict(size=8, color='#22577A', opacity=0.8),
            line=dict(color='#38A3A5', width=6),
            name='شلل الأطفال'
        ))
        fig_q1_vacc_3d.add_trace(go.Scatter3d(
            x=months,
            y=['مخية شوكية'] * len(months),
            z=q1_df['مخية شوكية'],
            mode='markers+lines',
            marker=dict(size=8, color='#57CC99', opacity=0.8),
            line=dict(color='#80ED99', width=6),
            name='مخية شوكية'
        ))
        fig_q1_vacc_3d.add_trace(go.Scatter3d(
            x=months,
            y=['ثلاثي فيروسي'] * len(months),
            z=q1_df['ثلاثي فيروسي'],
            mode='markers+lines',
            marker=dict(size=8, color='#2794EB', opacity=0.8),
            line=dict(color='#BFF8D4', width=6),
            name='ثلاثي فيروسي'
        ))
        fig_q1_vacc_3d.update_layout(
            scene=dict(
                xaxis_title='الشهر',
                yaxis_title='نوع التطعيم',
                zaxis_title='العدد',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600
        )
        st.plotly_chart(fig_q1_vacc_3d, use_container_width=True)
    
    with col2:
        total_vacc_q1 = q1_df['مجموع التطعيمات'].sum()
        fig_q1_pie = go.Figure(data=[go.Pie(
            labels=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
            values=[max(1, q1_df['شلل الأطفال'].sum()), max(1, q1_df['مخية شوكية'].sum()), max(1, q1_df['ثلاثي فيروسي'].sum())],
            hole=0.4,
            textinfo='percent+label',
            textfont_size=14,
            marker=dict(colors=['#22577A', '#38A3A5', '#57CC99'], line=dict(color='#0A0A0A', width=2)),
            hovertemplate='%{label}<br>العدد: %{value:,}<br>النسبة: %{percent}<extra></extra>',
            rotation=90,
            pull=[0.1, 0, 0]
        )])
        fig_q1_pie.add_annotation(
            text=f"إجمالي<br>{total_vacc_q1:,}",
            x=0.5, y=0.5,
            font_size=18,
            font_color='var(--text-primary)',
            showarrow=False
        )
        fig_q1_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600
        )
        st.plotly_chart(fig_q1_pie, use_container_width=True)
    
    st.markdown('<h3 style="color: var(--text-accent); text-align: center;"> تحليلات الربع الأول</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> اتجاه العابرين</div>
            <div class="analysis-text">
                وصل عدد العابرين إلى ذروته في فبراير (200,682) ثم انخفض في مارس إلى 163,291. 
                يشير هذا إلى نشاط موسمي قوي في منتصف الربع الأول.
            </div>
            <span class="insight-badge">نمو 8.1% في فبراير</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title">🕌 موسم العمرة</div>
            <div class="analysis-text">
                شهد فبراير أعلى معدل للمعتمرين (120,930) بزيادة 36% عن يناير، 
                مما يعكس الذروة الموسمية لأداء العمرة في هذه الفترة.
            </div>
            <span class="warning-badge">ذروة موسمية</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> برنامج التطعيم</div>
            <div class="analysis-text">
                تم تطعيم 282,471 جرعة في الربع الأول، مع تركيز كبير على تطعيم شلل الأطفال (62% من المجموع).
            </div>
            <span class="insight-badge">هدف محقق</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title"> المجموع الكلي للربع الأول</div>
        <div class="analysis-text">
            المجموع الكلي: {q1_df['المجموع الكلي'].sum():,}
        </div>
    </div>
    """, unsafe_allow_html=True)
# Quarter 2 analysis
with q2_tab:
    q2_df = filtered_df[filtered_df['الشهر'].isin(['أبريل 2025', 'مايو 2025', 'يونيو 2025'])]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> مقارنة العابرين والمعتمرين - الربع الثاني</h4>', unsafe_allow_html=True)
        fig_q2_comparison = go.Figure()
        fig_q2_comparison.add_trace(go.Bar(
            x=q2_df['الشهر'],
            y=q2_df['عدد العابرين'],
            name='العابرين',
            marker_color='#22577A',
            text=q2_df['عدد العابرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='auto',
            hovertemplate='الشهر: %{x}<br>العابرين: %{y:,}<br>المعتمرين والحجاج: %{customdata:,}<extra></extra>',
            customdata=q2_df['عدد المعتمرين'] + q2_df['عدد الحجاج']
        ))
        fig_q2_comparison.add_trace(go.Bar(
            x=q2_df['الشهر'],
            y=q2_df['عدد المعتمرين'] + q2_df['عدد الحجاج'],
            name='المعتمرين والحجاج',
            marker_color='#38A3A5',
            text=(q2_df['عدد المعتمرين'] + q2_df['عدد الحجاج']).apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='auto',
            hovertemplate='الشهر: %{x}<br>المعتمرين والحجاج: %{y:,}<br>العابرين: %{customdata:,}<extra></extra>',
            customdata=q2_df['عدد العابرين']
        ))
        fig_q2_comparison.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600,
            transition={'duration': 1500, 'easing': 'cubic-in-out'}
        )
        st.plotly_chart(fig_q2_comparison, use_container_width=True)
# Displaying clinic visits and emergency cases
    with col2:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> حالات النقل الإسعافي - الربع الثاني</h4>', unsafe_allow_html=True)
        fig_q2_emergency = go.Figure()
        fig_q2_emergency.add_trace(go.Scatter(
            x=q2_df['الشهر'],
            y=q2_df['حالات النقل الإسعافي وحالات الإشتباه'],
            mode='lines+markers',
            fill='tonexty',
            name='النقل الإسعافي',
            line=dict(color='#57CC99', width=4),
            marker=dict(size=15, color='#80ED99'),
            text=q2_df['حالات النقل الإسعافي وحالات الإشتباه'].apply(lambda x: f'{x}' if x > 0 else '0'),
            textposition='top center',
            hovertemplate='الشهر: %{x}<br>النقل الإسعافي: %{y}<extra></extra>'
        ))
        fig_q2_emergency.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600,
            yaxis=dict(range=[0, max(25, q2_df['حالات النقل الإسعافي وحالات الإشتباه'].max() * 1.2)])
        )
        st.plotly_chart(fig_q2_emergency, use_container_width=True)
# Displaying vaccination matrix
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> خريطة حرارية للتطعيمات - الربع الثاني</h4>', unsafe_allow_html=True)
    vacc_matrix = np.array([
        q2_df['شلل الأطفال'].values,
        q2_df['مخية شوكية'].values,
        q2_df['ثلاثي فيروسي'].values
    ])
    fig_q2_heatmap = go.Figure(data=go.Heatmap(
        z=vacc_matrix,
        x=q2_df['الشهر'],
        y=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
        colorscale=[[0, '#BFF8D4'], [0.5, '#57CC99'], [1, '#22577A']],
        text=vacc_matrix,
        texttemplate="%{text:,}",
        textfont={"size": 16, "color": "white"},
        hoverongaps=False,
        hovertemplate='الشهر: %{x}<br>التطعيم: %{y}<br>العدد: %{z:,}<extra></extra>'
    ))
    fig_q2_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600
    )
    st.plotly_chart(fig_q2_heatmap, use_container_width=True)
# Displaying total vaccinations pie chart    
    st.markdown('<h3 style="color: var(--text-accent); text-align: center;"> تحليلات الربع الثاني</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> انخفاض العابرين</div>
            <div class="analysis-text">
                انخفض عدد العابرين بشكل ملحوظ في مايو إلى 86,673، 
                وهو أدنى معدل في النصف الأول من العام، ثم تعافى جزئياً في يونيو.
            </div>
            <span class="warning-badge">انخفاض 19% في مايو</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> موسم الحج</div>
            <div class="analysis-text">
                ظهرت حالات الحج في مايو (12,951 حاج) مع توقف العمرة، 
                مما يعكس بداية الاستعدادات لموسم الحج الكبير.
            </div>
            <span class="insight-badge">بداية موسم الحج</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> ذروة الطوارئ</div>
            <div class="analysis-text">
                سجل شهر مايو أعلى معدل لحالات النقل الإسعافي (21 حالة)، 
                مما يستدعي تعزيز الخدمات الطبية الطارئة.
            </div>
            <span class="danger-badge">زيادة 320% في مايو</span>
        </div>
        """, unsafe_allow_html=True)
# Displaying total quarterly sum
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title"> المجموع الكلي للربع الثاني</div>
        <div class="analysis-text">
            المجموع الكلي: {q2_df['المجموع الكلي'].sum():,}
        </div>
    </div>
    """, unsafe_allow_html=True)
# Quarter 3 analysis
with q3_tab:
    q3_df = st.session_state.health_df.iloc[6:9]
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> إدخال وتحليل بيانات الربع الثالث</h4>', unsafe_allow_html=True)
    
    for i, month in enumerate(['يوليو 2025', 'أغسطس 2025', 'سبتمبر 2025']):
        with st.form(key=f'q3_form_{month}'):
            st.markdown(f"### بيانات {month}")
            travelers = st.number_input(f"عدد العابرين ({month})", min_value=0, value=int(q3_df.iloc[i]['عدد العابرين']), step=1)
            pilgrims = st.number_input(f"عدد المعتمرين ({month})", min_value=0, value=int(q3_df.iloc[i]['عدد المعتمرين']), step=1)
            hajj = st.number_input(f"عدد الحجاج ({month})", min_value=0, value=int(q3_df.iloc[i]['عدد الحجاج']), step=1)
            clinic_visits = st.number_input(f"زيارات العيادة ({month})", min_value=0, value=int(q3_df.iloc[i]['زيارات العيادة']), step=1)
            emergencies = st.number_input(f"حالات النقل الإسعافي ({month})", min_value=0, value=int(q3_df.iloc[i]['حالات النقل الإسعافي وحالات الإشتباه']), step=1)
            inspections = st.number_input(f"الجولات الإشرافية ({month})", min_value=0, value=int(q3_df.iloc[i]['الجولات الإشرافية']), step=1)
            polio = st.number_input(f"شلل الأطفال ({month})", min_value=0, value=int(q3_df.iloc[i]['شلل الأطفال']), step=1)
            meningitis = st.number_input(f"مخية شوكية ({month})", min_value=0, value=int(q3_df.iloc[i]['مخية شوكية']), step=1)
            triple_viral = st.number_input(f"ثلاثي فيروسي ({month})", min_value=0, value=int(q3_df.iloc[i]['ثلاثي فيروسي']), step=1)
            submit = st.form_submit_button("حفظ بيانات الشهر")
            if submit:
                new_data = {
                    'عدد العابرين': travelers,
                    'عدد المعتمرين': pilgrims,
                    'عدد الحجاج': hajj,
                    'زيارات العيادة': clinic_visits,
                    'حالات النقل الإسعافي وحالات الإشتباه': emergencies,
                    'الجولات الإشرافية': inspections,
                    'شلل الأطفال': polio,
                    'مخية شوكية': meningitis,
                    'ثلاثي فيروسي': triple_viral
                }
                update_quarter_data('Q3', 6 + i, new_data)
                st.success(f"تم تحديث بيانات {month} بنجاح!")
 # Displaying travelers and pilgrims chart   
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> العابرين والمعتمرين - الربع الثالث</h4>', unsafe_allow_html=True)
        fig_q3_chart = go.Figure()
        fig_q3_chart.add_trace(go.Scatter(
            x=q3_df['الشهر'],
            y=q3_df['عدد العابرين'],
            mode='lines+markers+text',
            name='العابرين',
            line=dict(color='#22577A', width=4),
            marker=dict(size=12, color='#38A3A5'),
            text=q3_df['عدد العابرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='top center',
            hovertemplate='الشهر: %{x}<br>العابرين: %{y:,}<br>المعتمرين: %{customdata:,}<extra></extra>',
            customdata=q3_df['عدد المعتمرين']
        ))
        fig_q3_chart.add_trace(go.Scatter(
            x=q3_df['الشهر'],
            y=q3_df['عدد المعتمرين'],
            mode='lines+markers+text',
            name='المعتمرين',
            line=dict(color='#57CC99', width=4),
            marker=dict(size=12, color='#80ED99'),
            text=q3_df['عدد المعتمرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='bottom center',
            hovertemplate='الشهر: %{x}<br>المعتمرين: %{y:,}<br>العابرين: %{customdata:,}<extra></extra>',
            customdata=q3_df['عدد العابرين']
        ))
        fig_q3_chart.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            showlegend=True,
            height=600,
            transition={'duration': 1000, 'easing': 'cubic-in-out'}
        )
        st.plotly_chart(fig_q3_chart, use_container_width=True)
    
    with col2:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> خدمات العيادة والطوارئ - الربع الثالث</h4>', unsafe_allow_html=True)
        fig_q3_medical = make_subplots(specs=[[{"secondary_y": True}]])
        fig_q3_medical.add_trace(
            go.Bar(
                x=q3_df['الشهر'],
                y=q3_df['زيارات العيادة'],
                name='زيارات العيادة',
                marker_color='#2794EB',
                text=q3_df['زيارات العيادة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
                textposition='auto'
            ),
            secondary_y=False,
        )
        fig_q3_medical.add_trace(
            go.Scatter(
                x=q3_df['الشهر'],
                y=q3_df['حالات النقل الإسعافي وحالات الإشتباه'],
                mode='lines+markers',
                name='النقل الإسعافي',
                line=dict(color='#BFF8D4', width=3),
                marker=dict(size=10, color='#80ED99'),
                text=q3_df['حالات النقل الإسعافي وحالات الإشتباه'].apply(lambda x: f'{x}' if x > 0 else '0'),
                textposition='top center'
            ),
            secondary_y=True,
        )
        fig_q3_medical.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600
        )
        fig_q3_medical.update_yaxes(title_text="زيارات العيادة", secondary_y=False, title_font_color='var(--text-primary)')
        fig_q3_medical.update_yaxes(title_text="النقل الإسعافي", secondary_y=True, title_font_color='var(--text-primary)')
        st.plotly_chart(fig_q3_medical, use_container_width=True)
# Displaying vaccination matrix
    q3_total = q3_df['المجموع الكلي'].sum()
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title">المجموع الكلي للربع الثالث</div>
        <div class="analysis-text">
            المجموع الكلي: {q3_total:,}
        </div>
        <span class="insight-badge">يوليو - سبتمبر 2025</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# Quarter 4 analysis
with q4_tab:
    q4_df = st.session_state.health_df.iloc[9:12]
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> إدخال وتحليل بيانات الربع الرابع</h4>', unsafe_allow_html=True)
    
    for i, month in enumerate(['أكتوبر 2025', 'نوفمبر 2025', 'ديسمبر 2025']):
        with st.form(key=f'q4_form_{month}'):
            st.markdown(f"### بيانات {month}")
            travelers = st.number_input(f"عدد العابرين ({month})", min_value=0, value=int(q4_df.iloc[i]['عدد العابرين']), step=1)
            pilgrims = st.number_input(f"عدد المعتمرين ({month})", min_value=0, value=int(q4_df.iloc[i]['عدد المعتمرين']), step=1)
            hajj = st.number_input(f"عدد الحجاج ({month})", min_value=0, value=int(q4_df.iloc[i]['عدد الحجاج']), step=1)
            clinic_visits = st.number_input(f"زيارات العيادة ({month})", min_value=0, value=int(q4_df.iloc[i]['زيارات العيادة']), step=1)
            emergencies = st.number_input(f"حالات النقل الإسعافي ({month})", min_value=0, value=int(q4_df.iloc[i]['حالات النقل الإسعافي وحالات الإشتباه']), step=1)
            inspections = st.number_input(f"الجولات الإشرافية ({month})", min_value=0, value=int(q4_df.iloc[i]['الجولات الإشرافية']), step=1)
            polio = st.number_input(f"شلل الأطفال ({month})", min_value=0, value=int(q4_df.iloc[i]['شلل الأطفال']), step=1)
            meningitis = st.number_input(f"مخية شوكية ({month})", min_value=0, value=int(q4_df.iloc[i]['مخية شوكية']), step=1)
            triple_viral = st.number_input(f"ثلاثي فيروسي ({month})", min_value=0, value=int(q4_df.iloc[i]['ثلاثي فيروسي']), step=1)
            submit = st.form_submit_button("حفظ بيانات الشهر")
            if submit:
                new_data = {
                    'عدد العابرين': travelers,
                    'عدد المعتمرين': pilgrims,
                    'عدد الحجاج': hajj,
                    'زيارات العيادة': clinic_visits,
                    'حالات النقل الإسعافي وحالات الإشتباه': emergencies,
                    'الجولات الإشرافية': inspections,
                    'شلل الأطفال': polio,
                    'مخية شوكية': meningitis,
                    'ثلاثي فيروسي': triple_viral
                }
                update_quarter_data('Q4', 9 + i, new_data)
                st.success(f"تم تحديث بيانات {month} بنجاح!")
# Displaying travelers and pilgrims chart
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> العابرين والمعتمرين - الربع الرابع</h4>', unsafe_allow_html=True)
        fig_q4_chart = go.Figure()
        fig_q4_chart.add_trace(go.Scatter(
            x=q4_df['الشهر'],
            y=q4_df['عدد العابرين'],
            mode='lines+markers+text',
            name='العابرين',
            line=dict(color='#22577A', width=4),
            marker=dict(size=12, color='#38A3A5'),
            text=q4_df['عدد العابرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='top center',
            hovertemplate='الشهر: %{x}<br>العابرين: %{y:,}<br>المعتمرين: %{customdata:,}<extra></extra>',
            customdata=q4_df['عدد المعتمرين']
        ))
        fig_q4_chart.add_trace(go.Scatter(
            x=q4_df['الشهر'],
            y=q4_df['عدد المعتمرين'],
            mode='lines+markers+text',
            name='المعتمرين',
            line=dict(color='#57CC99', width=4),
            marker=dict(size=12, color='#80ED99'),
            text=q4_df['عدد المعتمرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='bottom center',
            hovertemplate='الشهر: %{x}<br>المعتمرين: %{y:,}<br>العابرين: %{customdata:,}<extra></extra>',
            customdata=q4_df['عدد العابرين']
        ))
        fig_q4_chart.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            showlegend=True,
            height=600,
            transition={'duration': 1000, 'easing': 'cubic-in-out'}
        )
        st.plotly_chart(fig_q4_chart, use_container_width=True)
    # Displaying clinic visits and emergency cases 
    with col2:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;">🏥 خدمات العيادة والطوارئ - الربع الرابع</h4>', unsafe_allow_html=True)
        fig_q4_medical = make_subplots(specs=[[{"secondary_y": True}]])
        fig_q4_medical.add_trace(
            go.Bar(
                x=q4_df['الشهر'],
                y=q4_df['زيارات العيادة'],
                name='زيارات العيادة',
                marker_color='#2794EB',
                text=q4_df['زيارات العيادة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
                textposition='auto'
            ),
            secondary_y=False,
        )
        fig_q4_medical.add_trace(
            go.Scatter(
                x=q4_df['الشهر'],
                y=q4_df['حالات النقل الإسعافي وحالات الإشتباه'],
                mode='lines+markers',
                name='النقل الإسعافي',
                line=dict(color='#BFF8D4', width=3),
                marker=dict(size=10, color='#80ED99'),
                text=q4_df['حالات النقل الإسعافي وحالات الإشتباه'].apply(lambda x: f'{x}' if x > 0 else '0'),
                textposition='top center'
            ),
            secondary_y=True,
        )
        fig_q4_medical.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600
        )
        # Update y-axes titles and colors
        fig_q4_medical.update_yaxes(title_text="زيارات العيادة", secondary_y=False, title_font_color='var(--text-primary)')
        fig_q4_medical.update_yaxes(title_text="النقل الإسعافي", secondary_y=True, title_font_color='var(--text-primary)')
        st.plotly_chart(fig_q4_medical, use_container_width=True)
  # Displaying vaccination matrix  
    q4_total = q4_df['المجموع الكلي'].sum()
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title">المجموع الكلي للربع الرابع</div>
        <div class="analysis-text">
            المجموع الكلي: {q4_total:,}
        </div>
        <span class="insight-badge">أكتوبر - ديسمبر 2025</spa>
            </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
#  Displaying vaccination matrix
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> (لوحات القياس)</div>', unsafe_allow_html=True)
# Displaying clinic efficiency, emergency response, vaccination rate, and inspection efficiency
clinic_efficiency = filtered_df['زيارات العيادة'].sum() / max(1, filtered_df['عدد العابرين'].sum()) * 100
emergency_response = filtered_df['حالات النقل الإسعافي وحالات الإشتباه'].sum() / max(1, filtered_df['زيارات العيادة'].sum()) * 100
vaccination_rate = filtered_df['مجموع التطعيمات'].sum() / max(1, filtered_df['عدد العابرين'].sum()) * 100
inspection_efficiency = filtered_df['الجولات الإشرافية'].sum() / 12 * 100
# Displaying the 3D scatter plots for clinic efficiency, emergency response, vaccination rate, and inspection efficiency
col1, col2, col3, col4 = st.columns(4)
# Filter the DataFrame to include only the months in the current year
months = filtered_df['الشهر']
month_indices = list(range(len(months)))
# Create 3D scatter plots for each metric
with col1:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> كفاءة العيادات</h4>', unsafe_allow_html=True)
    fig_clinic_3d = go.Figure()
    fig_clinic_3d.add_trace(go.Scatter3d(
        x=month_indices,
        y=filtered_df['عدد العابرين'],
        z=filtered_df['زيارات العيادة'],
        mode='markers+lines',
        marker=dict(size=8, color='#22577A', opacity=0.8),
        line=dict(color='#38A3A5', width=6),
        name='زيارات العيادة',
        text=[f'الشهر: {m}<br>زيارات: {v:,}<br>عابرين: {t:,}' for m, v, t in zip(months, filtered_df['زيارات العيادة'], filtered_df['عدد العابرين'])],
        hovertemplate='%{text}<extra></extra>'
    ))
    fig_clinic_3d.update_layout(
        scene=dict(
            xaxis_title='الشهر',
            yaxis_title='عدد العابرين',
            zaxis_title='زيارات العيادة',
            xaxis=dict(tickvals=month_indices, ticktext=months),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_clinic_3d, use_container_width=True, config={'displayModeBar': False})
# Displaying emergency response, vaccination rate, and inspection efficiency
with col2:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> كفاءة الاستجابة للطوارئ</h4>', unsafe_allow_html=True)
    fig_emergency_3d = go.Figure()
    fig_emergency_3d.add_trace(go.Scatter3d(
        x=month_indices,
        y=filtered_df['زيارات العيادة'],
        z=filtered_df['حالات النقل الإسعافي وحالات الإشتباه'],
        mode='markers+lines',
        marker=dict(size=8, color='#57CC99', opacity=0.8),
        line=dict(color='#80ED99', width=6),
        name='حالات الطوارئ',
        text=[f'الشهر: {m}<br>حالات طوارئ: {e}<br>زيارات: {v:,}' for m, e, v in zip(months, filtered_df['حالات النقل الإسعافي وحالات الإشتباه'], filtered_df['زيارات العيادة'])],
        hovertemplate='%{text}<extra></extra>'
    ))
    fig_emergency_3d.update_layout(
        scene=dict(
            xaxis_title='الشهر',
            yaxis_title='زيارات العيادة',
            zaxis_title='حالات الطوارئ',
            xaxis=dict(tickvals=month_indices, ticktext=months),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_emergency_3d, use_container_width=True, config={'displayModeBar': False})
# Displaying vaccination rate and inspection efficiency
with col3:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> معدل التطعيمات</h4>', unsafe_allow_html=True)
    fig_vacc_3d = go.Figure()
    fig_vacc_3d.add_trace(go.Scatter3d(
        x=month_indices,
        y=filtered_df['عدد العابرين'],
        z=filtered_df['مجموع التطعيمات'],
        mode='markers+lines',
        marker=dict(size=8, color='#2794EB', opacity=0.8),
        line=dict(color='#BFF8D4', width=6),
        name='التطعيمات',
        text=[f'الشهر: {m}<br>تطعيمات: {v:,}<br>عابرين: {t:,}' for m, v, t in zip(months, filtered_df['مجموع التطعيمات'], filtered_df['عدد العابرين'])],
        hovertemplate='%{text}<extra></extra>'
    ))
    fig_vacc_3d.update_layout(
        scene=dict(
            xaxis_title='الشهر',
            yaxis_title='عدد العابرين',
            zaxis_title='مجموع التطعيمات',
            xaxis=dict(tickvals=month_indices, ticktext=months),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_vacc_3d, use_container_width=True, config={'displayModeBar': False})
#
with col4:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> كفاءة الجولات الإشرافية</h4>', unsafe_allow_html=True)
    fig_inspection_3d = go.Figure()
    fig_inspection_3d.add_trace(go.Scatter3d(
        x=month_indices,
        y=filtered_df['عدد العابرين'],
        z=filtered_df['الجولات الإشرافية'],
        mode='markers+lines',
        marker=dict(size=8, color='#80ED99', opacity=0.8),
        line=dict(color='#57CC99', width=6),
        name='الجولات الإشرافية',
        text=[f'الشهر: {m}<br>جولات: {i}<br>عابرين: {t:,}' for m, i, t in zip(months, filtered_df['الجولات الإشرافية'], filtered_df['عدد العابرين'])],
        hovertemplate='%{text}<extra></extra>'
    ))
    fig_inspection_3d.update_layout(
        scene=dict(
            xaxis_title='الشهر',
            yaxis_title='عدد العابرين',
            zaxis_title='الجولات الإشرافية',
            xaxis=dict(tickvals=month_indices, ticktext=months),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_inspection_3d, use_container_width=True, config={'displayModeBar': False})

st.markdown('</div>', unsafe_allow_html=True)
# Calculating clinic efficiency, emergency response, vaccination rate, and inspection efficiency
clinic_efficiency = min(filtered_df['زيارات العيادة'].mean() / 1000 * 100, 100) if filtered_df['زيارات العيادة'].mean() > 0 else 0
emergency_response = min(filtered_df['حالات النقل الإسعافي وحالات الإشتباه'].mean() / 10 * 100, 100) if filtered_df['حالات النقل الإسعافي وحالات الإشتباه'].mean() > 0 else 0
vaccination_rate = min(filtered_df['مجموع التطعيمات'].mean() / filtered_df['عدد العابرين'].mean() * 100, 100) if filtered_df['عدد العابرين'].mean() > 0 else 0
inspection_efficiency = min(filtered_df['الجولات الإشرافية'].mean() / 12 * 100, 100) if filtered_df['الجولات الإشرافية'].mean() > 0 else 0

col1, col2, col3, col4 = st.columns(4)
# Displaying clinic efficiency gauge
with col1:
    fig_gauge_clinic = go.Figure(go.Indicator(
        mode="gauge+number",
        value=clinic_efficiency,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "كفاءة العيادات (%)", 'font': {'size': 16, 'color': 'var(--text-primary)'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'var(--text-primary)', 'tickfont': {'color': 'var(--text-primary)'}},
            'bar': {'color': '#22577A'},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'var(--text-primary)',
            'steps': [
                {'range': [0, 50], 'color': '#BFF8D4'},
                {'range': [50, 75], 'color': '#57CC99'},
                {'range': [75, 100], 'color': '#38A3A5'}
            ],
            'threshold': {
                'line': {'color': '#80ED99', 'width': 4},
                'value': 80
            }
        }
    ))
    fig_gauge_clinic.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_gauge_clinic, use_container_width=True, config={'displayModeBar': False})
# Displaying emergency response gauge
with col2:
    fig_gauge_emergency = go.Figure(go.Indicator(
        mode="gauge+number",
        value=emergency_response,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "كفاءة الاستجابة للطوارئ (%)", 'font': {'size': 16, 'color': 'var(--text-primary)'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'var(--text-primary)', 'tickfont': {'color': 'var(--text-primary)'}},
            'bar': {'color': '#38A3A5'},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'var(--text-primary)',
            'steps': [
                {'range': [0, 50], 'color': '#BFF8D4'},
                {'range': [50, 75], 'color': '#57CC99'},
                {'range': [75, 100], 'color': '#22577A'}
            ],
            'threshold': {
                'line': {'color': '#80ED99', 'width': 4},
                'value': 90
            }
        }
    ))
    fig_gauge_emergency.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_gauge_emergency, use_container_width=True, config={'displayModeBar': False})
# Displaying vaccination rate and inspection efficiency gauges
with col3:
    fig_gauge_vaccination = go.Figure(go.Indicator(
        mode="gauge+number",
        value=vaccination_rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "معدل التطعيمات (%)", 'font': {'size': 16, 'color': 'var(--text-primary)'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'var(--text-primary)', 'tickfont': {'color': 'var(--text-primary)'}},
            'bar': {'color': '#57CC99'},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'var(--text-primary)',
            'steps': [
                {'range': [0, 50], 'color': '#BFF8D4'},
                {'range': [50, 75], 'color': '#38A3A5'},
                {'range': [75, 100], 'color': '#22577A'}
            ],
            'threshold': {
                'line': {'color': '#80ED99', 'width': 4},
                'value': 85
            }
        }
    ))
    fig_gauge_vaccination.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_gauge_vaccination, use_container_width=True, config={'displayModeBar': False})
# Displaying inspection efficiency gauge
with col4:
    fig_gauge_inspection = go.Figure(go.Indicator(
        mode="gauge+number",
        value=inspection_efficiency,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "كفاءة الجولات الإشرافية (%)", 'font': {'size': 16, 'color': 'var(--text-primary)'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'var(--text-primary)', 'tickfont': {'color': 'var(--text-primary)'}},
            'bar': {'color': '#2794EB'},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'var(--text-primary)',
            'steps': [
                {'range': [0, 50], 'color': '#BFF8D4'},
                {'range': [50, 75], 'color': '#57CC99'},
                {'range': [75, 100], 'color': '#38A3A5'}
            ],
            'threshold': {
                'line': {'color': '#80ED99', 'width': 4},
                'value': 90
            }
        }
    ))
    fig_gauge_inspection.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_gauge_inspection, use_container_width=True, config={'displayModeBar': False})

st.markdown('</div>', unsafe_allow_html=True)
# Displaying advanced analytics
if show_predictions or show_correlations or show_clusters:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> التحليلات المتقدمة</div>', unsafe_allow_html=True)
# Displaying predictions and correlations   
    col1, col2 = st.columns(2)
# Displaying predictions
    with col1:
        if show_predictions:
            st.markdown('<h4 style="color: var(--text-primary); text-align: center;">🔮 توقعات عدد العابرين</h4>', unsafe_allow_html=True)
            months = filtered_df['الشهر']
            travelers = filtered_df['عدد العابرين'].values
            if len(travelers) >= 3:
                future_months = ['المتوقع ' + m for m in months[-3:]]
                predicted_travelers = travelers[-3:] * 1.1  # افتراض زيادة 10%
                fig_predictions = go.Figure()
                fig_predictions.add_trace(go.Scatter(
                    x=months,
                    y=travelers,
                    mode='lines+markers',
                    name='الفعلي',
                    line=dict(color='#22577A', width=4),
                    marker=dict(size=10)
                ))
                fig_predictions.add_trace(go.Scatter(
                    x=future_months,
                    y=predicted_travelers,
                    mode='lines+markers',
                    name='المتوقع',
                    line=dict(color='#80ED99', width=4, dash='dash'),
                    marker=dict(size=10)
                ))
                fig_predictions.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_family='Cairo',
                    font_color='var(--text-primary)',
                    height=600,
                    transition={'duration': 1000, 'easing': 'cubic-in-out'}
                )
                st.plotly_chart(fig_predictions, use_container_width=True)
# Displaying correlations
    with col2:
        if show_correlations:
            st.markdown('<h4 style="color: var(--text-primary); text-align: center;">🔗 تحليل الارتباط</h4>', unsafe_allow_html=True)
            corr_matrix = filtered_df[['عدد العابرين', 'عدد المعتمرين', 'عدد الحجاج', 'زيارات العيادة', 'حالات النقل الإسعافي وحالات الإشتباه', 'مجموع التطعيمات']].corr()
            fig_corr = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.index,
                colorscale=[[0, '#22577A'], [0.5, '#38A3A5'], [1, '#BFF8D4']],
                text=corr_matrix.values.round(2),
                texttemplate="%{text}",
                textfont={"size": 14, "color": "white"},
                hovertemplate='%{x} vs %{y}<br>الارتباط: %{z:.2f}<extra></extra>'
            ))
            fig_corr.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_family='Cairo',
                font_color='var(--text-primary)',
                height=600
            )
            st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
# Displaying clusters
if show_predictions:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> التوقعات</div>', unsafe_allow_html=True)
# Displaying predictions for 2026
    future_months = ['يناير 2026', 'فبراير 2026', 'مارس 2026']
    growth_rate = 0.05 # Assuming a growth rate of 5% per month
    last_known = filtered_df.iloc[-1][['عدد العابرين', 'عدد المعتمرين', 'زيارات العيادة']].to_dict()
    predicted_data = {
        'الشهر': future_months,
        'عدد العابرين': [int(last_known['عدد العابرين'] * (1 + growth_rate) ** (i + 1)) for i in range(3)],
        'عدد المعتمرين': [int(last_known['عدد المعتمرين'] * (1 + growth_rate) ** (i + 1)) for i in range(3)],
        'زيارات العيادة': [int(last_known['زيارات العيادة'] * (1 + growth_rate) ** (i + 1)) for i in range(3)]
    }
    predicted_df = pd.DataFrame(predicted_data)
    # Merging predicted data with the last known data
    fig_predictions = go.Figure()
    fig_predictions.add_trace(go.Scatter(
        x=filtered_df['الشهر'],
        y=filtered_df['عدد العابرين'],
        mode='lines+markers',
        name='العابرين (فعلي)',
        line=dict(color='#22577A', width=3),
        marker=dict(size=8)
    ))
    # Adding predicted data for travelers
    fig_predictions.add_trace(go.Scatter(
        x=predicted_df['الشهر'],
        y=predicted_df['عدد العابرين'],
        mode='lines+markers',
        name='العابرين (متوقع)',
        line=dict(color='#38A3A5', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    # Adding predicted data for pilgrims
    fig_predictions.add_trace(go.Scatter(
        x=filtered_df['الشهر'],
        y=filtered_df['زيارات العيادة'],
        mode='lines+markers',
        name='زيارات العيادة (فعلي)',
        line=dict(color='#57CC99', width=3),
        marker=dict(size=8)
    ))
    # Adding predicted data for pilgrims
    fig_predictions.add_trace(go.Scatter(
        x=predicted_df['الشهر'],
        y=predicted_df['زيارات العيادة'],
        mode='lines+markers',
        name='زيارات العيادة (متوقع)',
        line=dict(color='#80ED99', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    fig_predictions.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600,
        title='توقعات عدد العابرين وزيارات العيادة لعام 2026',
        title_font=dict(size=20, color='var(--text-primary)')
    )
    st.plotly_chart(fig_predictions, use_container_width=True)
    # Displaying insights and predictions
    st.markdown('<h3 style="color: var(--text-accent); text-align: center;"> رؤى التوقعات</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
# Displaying insights for travelers and clinic visits
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> توقعات العابرين</div>
            <div class="analysis-text">
                من المتوقع أن ينمو عدد العابرين بنسبة 5% شهريًا في 2026، 
                مما يتطلب تعزيز الموارد في المنافذ.
            </div>
            <span class="insight-badge">نمو متوقع</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> توقعات زيارات العيادة</div>
            <div class="analysis-text">
                زيارات العيادة ستتبع نموًا مشابهًا بنسبة 5%، 
                مما يشير إلى الحاجة إلى زيادة الطاقم الطبي.
            </div>
            <span class="warning-badge">تخطيط مطلوب</span>
        </div>
        """, unsafe_allow_html=True)
# Displaying clusters
    st.markdown('</div>', unsafe_allow_html=True)
# Footer and session state cleanup
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
# Footer with last update time and credits
st.markdown("""
<div style="text-align: center; padding: 1rem; color: var(--text-secondary);">
    <p>لوحة المعلومات الصحية الشاملة 2025 - مكتب هيئة الصحة العامة بنجران</p>
    <p>تم التطوير بواسطة فريق التحليلات الصحية</p>
</div>
""", unsafe_allow_html=True)
# Footer with last update time and credits
st.markdown("""
<div style="position: fixed; bottom: 20px; left: 20px; background: var(--glass-bg); backdrop-filter: blur(15px); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 1rem; box-shadow: var(--shadow-glow); font-size: 0.9rem; color: var(--text-secondary);">
     آخر تحديث: {}
</div>

""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
# Storing the updated DataFrame in session state
st.session_state.health_df = st.session_state.health_df.fillna(0)

