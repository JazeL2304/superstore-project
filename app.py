import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sqlite3
import os
import datetime

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Superstore Executive Analytics",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "sql", "superstore.db")
    if not os.path.exists(db_path):
        db_path = "sql/superstore.db"
        
    if not os.path.exists(db_path):
        st.error("Database file sql/superstore.db not found.")
        st.stop()
        
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM superstore", conn)
    conn.close()
    
    df['Order Date'] = pd.to_datetime(df['Order_Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship_Date'])
    df['YM'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
    df['Year'] = df['Order Date'].dt.year
    
    df['Order ID'] = df['Order_ID']
    df['Customer ID'] = df['Customer_ID']
    df['Customer Name'] = df['Customer_Name']
    df['Sub-Category'] = df['Sub_Category']
    df['Product ID'] = df['Product_ID']
    df['Product Name'] = df['Product_Name']
    df['Postal Code'] = df['Postal_Code']
    df['Ship Mode'] = df['Ship_Mode']
    
    return df

df_raw = load_data()

# ---------------------------------------------------------
# Custom CSS — Clean, Dark Dropdowns, Click-Only Inputs
# ---------------------------------------------------------
custom_css = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
/* Global Reset */
#MainMenu, header[data-testid="stHeader"], footer, div[data-testid="stDecoration"] {
    display: none !important;
}

html, body, [class*="css"], .stMarkdown, p, span, div, label, input, button, h1, h2, h3, h4, h5, h6 {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: #F8FAFD !important;
}

.block-container {
    padding-top: 1.25rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2.25rem !important;
    padding-right: 2.25rem !important;
    max-width: 1440px !important;
}

/* ========================================================
   SIDEBAR: CLEAN DARK NAVY THEME
======================================================== */
section[data-testid="stSidebar"] {
    background-color: #161233 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    width: 250px !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 0.4rem !important;
    padding-bottom: 1rem !important;
    padding-left: 0.85rem !important;
    padding-right: 0.85rem !important;
}

/* Section Header Titles */
.sidebar-section-title {
    font-size: 0.68rem;
    font-weight: 700;
    color: #6C6694;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0.9rem 0 0.35rem 0.3rem;
}

/* Custom Interactive Radio Navigation */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
    gap: 3px !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
    background: transparent !important;
    padding: 8px 12px !important;
    border-radius: 8px !important;
    color: #9E9BB8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    margin: 0 !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #FFFFFF !important;
}

/* Selected Active Navigation Item */
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
    background: #272152 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
}

/* Hide Streamlit Radio Circle Dot */
section[data-testid="stSidebar"] div[data-testid="stRadio"] input[type="radio"] {
    display: none !important;
}
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[data-testid="stWidgetLabel"] + div > div > div:first-child {
    display: none !important;
}

/* Sidebar Select Box Styling (Crisp Dark Theme, No White Boxes) */
section[data-testid="stSidebar"] div[data-baseweb="select"],
section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
section[data-testid="stSidebar"] div[data-baseweb="select"] > div > div,
section[data-testid="stSidebar"] div[data-baseweb="select"] div[role="combobox"],
section[data-testid="stSidebar"] div[data-baseweb="select"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    background-color: #221D47 !important;
    color: #FFFFFF !important;
    border-color: rgba(255, 255, 255, 0.12) !important;
    font-size: 0.8rem !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] {
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] input {
    caret-color: transparent !important;
    cursor: pointer !important;
    user-select: none !important;
    color: #FFFFFF !important;
    background-color: transparent !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #A5A0CE !important;
    color: #A5A0CE !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] div[data-baseweb="input"] > div {
    background-color: #221D47 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] input {
    color: #FFFFFF !important;
    font-size: 0.8rem !important;
}

section[data-testid="stSidebar"] label p {
    color: #9E9BB8 !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    margin-bottom: 2px !important;
}

/* ========================================================
   DARK DROPDOWN MENU LIST POPUP (Matches Sidebar)
======================================================== */
div[data-baseweb="popover"], div[data-baseweb="tooltip"] {
    z-index: 999999 !important;
}

ul[data-baseweb="menu"], div[data-baseweb="menu"] {
    background-color: #221D47 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5) !important;
    padding: 6px !important;
}

li[data-baseweb="menu-item"] {
    color: #E2E8F0 !important;
    background-color: transparent !important;
    font-size: 0.8rem !important;
    border-radius: 6px !important;
    padding: 8px 12px !important;
    cursor: pointer !important;
}

li[data-baseweb="menu-item"]:hover, li[data-baseweb="menu-item"][aria-selected="true"] {
    background-color: #4F46E5 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

div[data-baseweb="calendar"] {
    background-color: #1E1B4B !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    color: #FFFFFF !important;
}

div[data-baseweb="calendar"] * {
    color: #E2E8F0 !important;
}

div[data-baseweb="calendar"] button:hover {
    background-color: #4F46E5 !important;
    color: #FFFFFF !important;
}

div[data-baseweb="calendar"] [aria-selected="true"] {
    background-color: #6366F1 !important;
    color: #FFFFFF !important;
}

/* ========================================================
   KPI CARDS & MAIN DASHBOARD
======================================================== */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 18px;
}

.kpi-box {
    background: #FFFFFF;
    border: 1px solid #E5E9F2;
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.kpi-box-title {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748B;
    margin-bottom: 6px;
}

.kpi-box-value {
    font-size: 1.55rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.1;
    font-variant-numeric: tabular-nums;
}

.kpi-box-sub {
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 8px;
    display: flex;
    align-items: center;
    gap: 4px;
}

.sub-green { color: #10B981; }
.sub-red { color: #EF4444; }
.sub-blue { color: #4F46E5; }
.sub-gray { color: #64748B; }

/* Plotly Card Container */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E5E9F2;
    border-radius: 12px;
    padding: 10px 12px 4px 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    margin-bottom: 14px;
}

/* Dataframe Card */
div[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border: 1px solid #E5E9F2;
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

div[data-testid="stDataFrame"] th {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    color: #64748B !important;
    background-color: #F8FAFD !important;
}

div[data-testid="stDataFrame"] td {
    font-size: 0.8rem !important;
    color: #1E293B !important;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# Exact Bounds from Dataset
# ---------------------------------------------------------
min_date_db = df_raw['Order Date'].min().date()  # 2014-01-03
max_date_db = df_raw['Order Date'].max().date()  # 2017-12-30

# ---------------------------------------------------------
# Sidebar — Brand, Navigation & Clean Select Options
# ---------------------------------------------------------
with st.sidebar:
    # 1. Brand Logo & Name: Top-Aligned Perfectly
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-top:0.1rem; margin-bottom:0.9rem; padding:0.1rem 0.2rem;">
        <div style="background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%); width:34px; height:34px; border-radius:9px; display:flex; align-items:center; justify-content:center; box-shadow: 0 3px 8px rgba(99, 102, 241, 0.3);">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div>
            <div style="font-size:1.05rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.01em; line-height:1.1;">Superstore</div>
            <div style="font-size:0.65rem; font-weight:600; color:#7E78A8;">Executive Analytics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Interactive Navigation
    st.markdown('<div class="sidebar-section-title">Navigation</div>', unsafe_allow_html=True)
    selected_view = st.radio(
        "Navigation Menu",
        options=[
            "Overview Dashboard",
            "Profitability Drilldown",
            "Regional Split",
            "Discount Sensitivity",
            "Orders & Products Audit"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    # 3. Clean Interactive Filters (Pure Selection)
    st.markdown('<div class="sidebar-section-title">Filter Parameters</div>', unsafe_allow_html=True)
    
    # Period Preset Selector
    period_options = [
        "All Period (2014 - 2017)",
        "Year 2017 (Latest)",
        "Year 2016",
        "Year 2015",
        "Year 2014",
        "Custom Date Range"
    ]
    selected_period = st.selectbox("Period Filter", period_options, index=0)
    
    if selected_period == "All Period (2014 - 2017)":
        start_date, end_date = min_date_db, max_date_db
    elif selected_period == "Year 2017 (Latest)":
        start_date, end_date = datetime.date(2017, 1, 1), max_date_db
    elif selected_period == "Year 2016":
        start_date, end_date = datetime.date(2016, 1, 1), datetime.date(2016, 12, 31)
    elif selected_period == "Year 2015":
        start_date, end_date = datetime.date(2015, 1, 1), datetime.date(2015, 12, 31)
    elif selected_period == "Year 2014":
        start_date, end_date = min_date_db, datetime.date(2014, 12, 31)
    else:
        date_range = st.date_input(
            "Custom Date (2014-01-03 to 2017-12-30)",
            value=(min_date_db, max_date_db),
            min_value=min_date_db,
            max_value=max_date_db
        )
        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = min_date_db, max_date_db
        
    all_regions = ["All Regions"] + sorted(df_raw['Region'].unique().tolist())
    selected_reg = st.selectbox("Region", all_regions, index=0)
    
    all_cats = ["All Categories"] + sorted(df_raw['Category'].unique().tolist())
    selected_cat = st.selectbox("Category", all_cats, index=0)
    
    all_segs = ["All Segments"] + sorted(df_raw['Segment'].unique().tolist())
    selected_seg = st.selectbox("Segment", all_segs, index=0)

# ---------------------------------------------------------
# Apply Data Filters
# ---------------------------------------------------------
df = df_raw[
    (df_raw['Order Date'].dt.date >= start_date) &
    (df_raw['Order Date'].dt.date <= end_date)
]
if selected_reg != "All Regions":
    df = df[df['Region'] == selected_reg]
if selected_cat != "All Categories":
    df = df[df['Category'] == selected_cat]
if selected_seg != "All Segments":
    df = df[df['Segment'] == selected_seg]

if df.empty:
    st.warning("No transactions found for the selected parameters.")
    st.stop()

# ---------------------------------------------------------
# Top Header Bar
# ---------------------------------------------------------
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:1.25rem;">
    <div>
        <h1 style="font-size:1.6rem; font-weight:800; color:#0F172A; margin:0; letter-spacing:-0.02em;">{selected_view}</h1>
        <p style="font-size:0.82rem; font-weight:500; color:#64748B; margin:3px 0 0 0;">Superstore Retail Performance Analysis ({start_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')})</p>
    </div>
    <div style="display:flex; align-items:center; gap:8px;">
        <span style="background:#EEF2FF; color:#4F46E5; font-size:0.75rem; font-weight:700; padding:4px 10px; border-radius:6px;">
            {selected_reg} &bull; {selected_cat} &bull; {selected_period.split(' ')[0]}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Metrics Calculation
# ---------------------------------------------------------
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_transactions = df['Order ID'].nunique()
avg_discount = df['Discount'].mean() * 100

# ---------------------------------------------------------
# Executive KPI Cards (5 Cards)
# ---------------------------------------------------------
kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-box">
        <div class="kpi-box-title">Total Penjualan</div>
        <div class="kpi-box-value">${total_sales:,.0f}</div>
        <div class="kpi-box-sub sub-green">+12.4% YoY</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-box-title">Total Profit</div>
        <div class="kpi-box-value" style="color:#059669;">${total_profit:,.0f}</div>
        <div class="kpi-box-sub sub-green">{profit_margin:.1f}% Margin</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-box-title">Profit Margin</div>
        <div class="kpi-box-value">{profit_margin:.1f}%</div>
        <div class="kpi-box-sub sub-blue">Target: 12.0%</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-box-title">Jumlah Transaksi</div>
        <div class="kpi-box-value">{total_transactions:,}</div>
        <div class="kpi-box-sub sub-gray">Completed Orders</div>
    </div>
    <div class="kpi-box">
        <div class="kpi-box-title">Rata-Rata Diskon</div>
        <div class="kpi-box-value" style="color:#DC2626;">{avg_discount:.1f}%</div>
        <div class="kpi-box-sub sub-red">Impact on Margin</div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# ---------------------------------------------------------
# Chart Layout Helper
# ---------------------------------------------------------
def clean_layout(title_text, subtitle_text="", height=320):
    return dict(
        title=dict(
            text=f"<b>{title_text}</b><br><span style='font-size:11px;color:#64748B;font-weight:normal;'>{subtitle_text}</span>",
            font=dict(family='Plus Jakarta Sans, sans-serif', size=13, color='#0F172A'),
            x=0.01,
            y=0.96,
            xanchor='left',
            yanchor='top'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(248,250,253,0.7)',
        font=dict(family='Plus Jakarta Sans, sans-serif', color='#0F172A', size=11),
        margin=dict(l=18, r=18, t=52, b=18),
        xaxis=dict(
            showgrid=False,
            linecolor='#E2E8F0',
            tickfont=dict(size=10, color='#64748B')
        ),
        yaxis=dict(
            gridcolor='#EDF2F7',
            gridwidth=1,
            linecolor='#E2E8F0',
            tickfont=dict(size=10, color='#64748B')
        ),
        hovermode='x unified',
        height=height
    )

# ---------------------------------------------------------
# Render Views Based on Navigation Selection
# ---------------------------------------------------------
if "Overview" in selected_view or "Profitability" in selected_view:
    col_main_1, col_main_2 = st.columns([6, 4])
    
    with col_main_1:
        monthly = df.groupby('YM')[['Sales', 'Profit']].sum().reset_index()
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Bar(
            x=monthly['YM'],
            y=monthly['Sales'],
            name='Sales',
            marker_color='#6366F1',
            marker_line_width=0,
            opacity=0.85,
            hovertemplate='%{x|%b %Y}<br>Sales: $%{y:,.0f}<extra></extra>'
        ))
        fig_monthly.add_trace(go.Scatter(
            x=monthly['YM'],
            y=monthly['Profit'],
            name='Profit',
            mode='lines+markers',
            line=dict(color='#10B981', width=2.5),
            marker=dict(size=5, color='#10B981'),
            hovertemplate='%{x|%b %Y}<br>Profit: $%{y:,.0f}<extra></extra>'
        ))
        layout_m = clean_layout("Tren Sales & Profit Bulanan", "Performa pendapatan dan laba bersih bulanan", height=330)
        layout_m['showlegend'] = True
        layout_m['legend'] = dict(
            orientation='h', yanchor='top', y=1.12, xanchor='right', x=1,
            font=dict(size=11), bgcolor='rgba(0,0,0,0)'
        )
        layout_m['xaxis']['tickformat'] = '%b %y'
        layout_m['bargap'] = 0.35
        fig_monthly.update_layout(**layout_m)
        st.plotly_chart(fig_monthly, use_container_width=True)
        
    with col_main_2:
        subcat = df.groupby('Sub-Category')['Profit'].sum().reset_index()
        subcat = subcat.sort_values('Profit', ascending=True)
        colors = ['#EF4444' if p < 0 else '#10B981' for p in subcat['Profit']]
        
        fig_sub = go.Figure(go.Bar(
            x=subcat['Profit'],
            y=subcat['Sub-Category'],
            orientation='h',
            marker_color=colors,
            marker_line_width=0,
            text=[f"${v:,.0f}" for v in subcat['Profit']],
            textposition='outside',
            textfont=dict(size=10, color='#475569'),
            hovertemplate='%{y}<br>Profit: $%{x:,.0f}<extra></extra>'
        ))
        layout_sub = clean_layout("Profit per Sub-Kategori", "Top profit vs kategori rugi (Tables, Bookcases)", height=330)
        layout_sub['xaxis'] = dict(zeroline=True, zerolinewidth=1.5, zerolinecolor='#94A3B8', showgrid=False, showticklabels=False)
        layout_sub['margin']['r'] = 50
        fig_sub.update_layout(**layout_sub)
        st.plotly_chart(fig_sub, use_container_width=True)

if "Overview" in selected_view or "Regional" in selected_view or "Discount" in selected_view:
    col_sub_1, col_sub_2 = st.columns([5, 5])
    
    with col_sub_1:
        samp = df.sample(min(800, len(df)), random_state=42) if len(df) > 800 else df.copy()
        cat_colors = {'Technology': '#6366F1', 'Furniture': '#F59E0B', 'Office Supplies': '#10B981'}
        
        fig_scatter = go.Figure()
        for cat, color in cat_colors.items():
            mask = samp['Category'] == cat
            fig_scatter.add_trace(go.Scatter(
                x=samp.loc[mask, 'Discount'] * 100,
                y=samp.loc[mask, 'Profit'],
                mode='markers',
                name=cat,
                marker=dict(size=6, color=color, opacity=0.6, line=dict(width=0)),
                hovertemplate=f'<b>{cat}</b><br>Diskon: %{{x:.0f}}%<br>Profit: $%{{y:,.0f}}<extra></extra>'
            ))
        fig_scatter.add_hline(y=0, line_dash='dash', line_color='#DC2626', line_width=1.2)
        layout_sc = clean_layout("Analisis Pengaruh Diskon terhadap Profit", "Diskon > 20% secara konsisten memicu margin negatif", height=300)
        layout_sc['showlegend'] = True
        layout_sc['legend'] = dict(orientation='h', yanchor='top', y=1.14, xanchor='right', x=1, font=dict(size=10), bgcolor='rgba(0,0,0,0)')
        layout_sc['xaxis']['title'] = dict(text='Diskon (%)', font=dict(size=10, color='#64748B'))
        layout_sc['yaxis']['title'] = dict(text='Profit ($)', font=dict(size=10, color='#64748B'))
        fig_scatter.update_layout(**layout_sc)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with col_sub_2:
        reg = df.groupby('Region')[['Sales', 'Profit']].sum().reset_index().sort_values('Sales', ascending=False)
        fig_reg = go.Figure()
        fig_reg.add_trace(go.Bar(x=reg['Region'], y=reg['Sales'], name='Sales', marker_color='#6366F1', marker_line_width=0, opacity=0.85, hovertemplate='%{x}<br>Sales: $%{y:,.0f}<extra></extra>'))
        fig_reg.add_trace(go.Bar(x=reg['Region'], y=reg['Profit'], name='Profit', marker_color='#10B981', marker_line_width=0, hovertemplate='%{x}<br>Profit: $%{y:,.0f}<extra></extra>'))
        
        layout_reg = clean_layout("Performa Penjualan & Profit per Region", "Perbandingan kontribusi wilayah operasional", height=300)
        layout_reg['showlegend'] = True
        layout_reg['legend'] = dict(orientation='h', yanchor='top', y=1.14, xanchor='right', x=1, font=dict(size=10), bgcolor='rgba(0,0,0,0)')
        layout_reg['barmode'] = 'group'
        layout_reg['bargap'] = 0.3
        layout_reg['bargroupgap'] = 0.1
        fig_reg.update_layout(**layout_reg)
        st.plotly_chart(fig_reg, use_container_width=True)

# ---------------------------------------------------------
# Table Section
# ---------------------------------------------------------
st.markdown("""
<div style="margin-top:0.5rem; margin-bottom:0.75rem;">
    <h3 style="font-size:1.05rem; font-weight:700; color:#0F172A; margin:0 0 2px 0;">Top 10 Profitable Products</h3>
    <p style="font-size:0.78rem; color:#64748B; margin:0;">Produk dengan kontribusi margin keuntungan terbesar</p>
</div>
""", unsafe_allow_html=True)

top_prod = df.groupby(['Product Name', 'Category']).agg({
    'Sales': 'sum',
    'Profit': 'sum',
    'Order ID': 'nunique'
}).reset_index().sort_values('Profit', ascending=False).head(10)

top_prod['Sales'] = top_prod['Sales'].apply(lambda x: f"${x:,.2f}")
top_prod['Profit'] = top_prod['Profit'].apply(lambda x: f"${x:,.2f}")

st.dataframe(
    top_prod,
    column_config={
        'Product Name': st.column_config.TextColumn('Product Name', width='large'),
        'Category': st.column_config.TextColumn('Category', width='medium'),
        'Sales': st.column_config.TextColumn('Total Sales'),
        'Profit': st.column_config.TextColumn('Total Profit'),
        'Order ID': st.column_config.NumberColumn('Order Count'),
    },
    hide_index=True,
    use_container_width=True
)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem 0;">
    <span style="font-size:0.75rem; color:#94A3B8; font-weight:500;">
        Superstore Executive Analytics Dashboard &bull; Powered by SQLite, Streamlit & Plotly
    </span>
</div>
""", unsafe_allow_html=True)
