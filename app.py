import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Superstore Sales & Profit Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic styling
st.markdown("""
<style>
    /* Hide top padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    
    /* Header Container */
    .main-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .main-header p {
        margin: 0.4rem 0 0 0;
        color: #94A3B8;
        font-size: 0.95rem;
    }

    /* Custom Metric Styling */
    div[data-testid="stMetric"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 1rem 1.25rem;
        border-radius: 10px;
        color: #F8FAFC;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stMetric"] label {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
    }
    div[data-testid="stMetricValue"] {
        font-weight: 700 !important;
        color: #38BDF8 !important;
    }

    /* Container Card styling for charts */
    .chart-card {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

import sqlite3

# ---------------------------------------------------------
# Load Data (Cached from SQLite Database)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "sql", "superstore.db")
    if not os.path.exists(db_path):
        db_path = "sql/superstore.db"
        
    if not os.path.exists(db_path):
        st.error("❌ File database `sql/superstore.db` tidak ditemukan. Pastikan database SQLite sudah dibangun.")
        st.stop()
        
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM superstore", conn)
    conn.close()
    
    # Standardize & parse dates
    df['Order Date'] = pd.to_datetime(df['Order_Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship_Date'])
    df['Year-Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
    
    # Aliasing column names for app compatibility
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
# Sidebar Filter Controls
# ---------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60)
st.sidebar.title("🔍 Filter Dashboard")
st.sidebar.markdown("Filter data berdasarkan kebutuhan analisis Anda:")

# Date Range Filter
min_date = df_raw['Order Date'].min().date()
max_date = df_raw['Order Date'].max().date()

start_date, end_date = st.sidebar.date_input(
    "Periode Tanggal (Order Date):",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Region Filter
all_regions = sorted(df_raw['Region'].unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Pilih Region:",
    options=all_regions,
    default=all_regions
)

# Category Filter
all_categories = sorted(df_raw['Category'].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Pilih Kategori Product:",
    options=all_categories,
    default=all_categories
)

# Segment Filter
all_segments = sorted(df_raw['Segment'].unique().tolist())
selected_segments = st.sidebar.multiselect(
    "Pilih Segment Konsumen:",
    options=all_segments,
    default=all_segments
)

# ---------------------------------------------------------
# Data Filtering Logic
# ---------------------------------------------------------
df_filtered = df_raw[
    (df_raw['Order Date'].dt.date >= start_date) &
    (df_raw['Order Date'].dt.date <= end_date) &
    (df_raw['Region'].isin(selected_regions)) &
    (df_raw['Category'].isin(selected_categories)) &
    (df_raw['Segment'].isin(selected_segments))
]

# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>📊 Executive Dashboard Superstore</h1>
    <p>Analisis Kinerja Penjualan, Profitabilitas, Tren Bulanan, dan Dampak Diskon Produk</p>
</div>
""", unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("⚠️ Tidak ada data yang sesuai dengan kombinasi filter terpilih.")
    st.stop()

# ---------------------------------------------------------
# Key Performance Indicators (KPIs)
# ---------------------------------------------------------
total_sales = df_filtered['Sales'].sum()
total_profit = df_filtered['Profit'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = df_filtered['Order ID'].nunique()
avg_discount = df_filtered['Discount'].mean() * 100

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Penjualan", f"${total_sales:,.0f}")
with col2:
    st.metric("Total Profit", f"${total_profit:,.0f}", delta=f"{profit_margin:.1f}% Margin")
with col3:
    st.metric("Profit Margin", f"{profit_margin:.1f}%")
with col4:
    st.metric("Jumlah Transaksi", f"{total_orders:,}")
with col5:
    st.metric("Rata-rata Diskon", f"{avg_discount:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Visualizations Grid (2 x 2)
# ---------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)

# ---------------------------------------------------------
# Visual 1: Profit per Sub-Kategori (Highlight Rugi)
# ---------------------------------------------------------
with row1_col1:
    st.subheader("1. Profit per Sub-Kategori (Highlight Kerugian)")
    
    subcat_profit = df_filtered.groupby('Sub-Category')['Profit'].sum().reset_index()
    subcat_profit = subcat_profit.sort_values(by='Profit', ascending=True)
    subcat_profit['Status'] = subcat_profit['Profit'].apply(lambda x: 'Rugi (Loss)' if x < 0 else 'Untung (Profit)')
    
    fig_subcat = px.bar(
        subcat_profit,
        x='Profit',
        y='Sub-Category',
        orientation='h',
        color='Status',
        color_discrete_map={
            'Untung (Profit)': '#00CC96',  # Mint Green / Teal
            'Rugi (Loss)': '#EF553B'      # Coral Red / Highlight
        },
        text='Profit',
        title="Profitability per Sub-Kategori Produk"
    )
    
    fig_subcat.update_traces(
        texttemplate='%{text:$.0f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Profit: %{x:$.2f}<extra></extra>'
    )
    
    fig_subcat.update_layout(
        xaxis_title="Total Profit ($)",
        yaxis_title="Sub-Kategori",
        legend_title_text="Keterangan",
        height=450,
        margin=dict(l=20, r=40, t=50, b=20),
        xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='#64748B')
    )
    
    st.plotly_chart(fig_subcat, use_container_width=True)

# ---------------------------------------------------------
# Visual 2: Tren Sales & Profit Bulanan (Line Chart)
# ---------------------------------------------------------
with row1_col2:
    st.subheader("2. Tren Sales & Profit Bulanan")
    
    monthly_df = df_filtered.groupby('Year-Month')[['Sales', 'Profit']].sum().reset_index()
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly_df['Year-Month'],
        y=monthly_df['Sales'],
        mode='lines+markers',
        name='Sales',
        line=dict(color='#3B82F6', width=3),
        marker=dict(size=6),
        hovertemplate='Sales: $%{y:,.2f}<extra></extra>'
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly_df['Year-Month'],
        y=monthly_df['Profit'],
        mode='lines+markers',
        name='Profit',
        line=dict(color='#10B981', width=3),
        marker=dict(size=6),
        hovertemplate='Profit: $%{y:,.2f}<extra></extra>'
    ))
    
    fig_trend.update_layout(
        title="Perkembangan Sales dan Profit Sepanjang Waktu",
        xaxis_title="Bulan & Tahun",
        yaxis_title="Jumlah ($)",
        hovermode="x unified",
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns(2)

# ---------------------------------------------------------
# Visual 3: Profit per Region (Bar Chart)
# ---------------------------------------------------------
with row2_col1:
    st.subheader("3. Profit per Region")
    
    region_profit = df_filtered.groupby('Region')['Profit'].sum().reset_index()
    region_profit = region_profit.sort_values(by='Profit', ascending=False)
    
    fig_region = px.bar(
        region_profit,
        x='Region',
        y='Profit',
        color='Region',
        color_discrete_sequence=px.colors.qualitative.Bold,
        text='Profit',
        title="Perbandingan Profitabilitas Berdasarkan Region"
    )
    
    fig_region.update_traces(
        texttemplate='%{text:$.0f}',
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Profit: %{y:$.2f}<extra></extra>'
    )
    
    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Total Profit ($)",
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig_region, use_container_width=True)

# ---------------------------------------------------------
# Visual 4: Scatter Diskon vs Profit
# ---------------------------------------------------------
with row2_col2:
    st.subheader("4. Analisis Diskon vs Profit")
    
    # Format discount into percentage for hover clarity
    df_filtered_scatter = df_filtered.copy()
    df_filtered_scatter['Discount_Pct'] = df_filtered_scatter['Discount'] * 100
    
    fig_scatter = px.scatter(
        df_filtered_scatter,
        x='Discount_Pct',
        y='Profit',
        color='Category',
        size='Sales',
        size_max=25,
        hover_data=['Sub-Category', 'Sales', 'Profit', 'Discount_Pct'],
        color_discrete_map={
            'Technology': '#8B5CF6',
            'Furniture': '#F59E0B',
            'Office Supplies': '#06B6D4'
        },
        title="Dampak Tingkat Diskon (%) Terhadap Profitabilitas Order"
    )
    
    # Add horizontal reference line at profit = 0
    fig_scatter.add_hline(y=0, line_dash="dash", line_color="#EF4444", opacity=0.8, annotation_text="Titik Impas (Profit = 0)")
    
    fig_scatter.update_traces(
        hovertemplate='<b>Sub-Kategori: %{customdata[0]}</b><br>Diskon: %{x:.0f}%<br>Profit: %{y:$.2f}<br>Sales: %{customdata[1]:$.2f}<extra></extra>'
    )
    
    fig_scatter.update_layout(
        xaxis_title="Diskon (%)",
        yaxis_title="Profit ($)",
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B;'>Superstore Streamlit Interactive Dashboard &bull; Built with Streamlit & Plotly</p>", unsafe_allow_html=True)
