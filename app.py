import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import textwrap
from data_loader import (
    get_google_trends,
    get_bps_provinsi_2025,
    get_bps_nasional_2024,
    get_spklu_targets,
    get_spklu_list,
    get_gaikindo_sales
)

# Set Page Config
st.set_page_config(
    page_title="Transisi Energi & Ekosistem EV Indonesia",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_all_data():
    trends = get_google_trends()
    bps_prov, bps_tot = get_bps_provinsi_2025()
    bps_nas_2024 = get_bps_nasional_2024()
    spklu_target = get_spklu_targets()
    spklu_list = get_spklu_list()
    gaik_ann, gaik_mon, gaik_bev_brand, gaik_hev_brand, gaik_phev_brand = get_gaikindo_sales()
    return trends, bps_prov, bps_tot, bps_nas_2024, spklu_target, spklu_list, gaik_ann, gaik_mon, gaik_bev_brand, gaik_hev_brand, gaik_phev_brand

trends, bps_prov, bps_tot, bps_nas_2024, spklu_target, spklu_list, gaik_ann, gaik_mon, gaik_bev_brand, gaik_hev_brand, gaik_phev_brand = load_all_data()

# Inject Custom CSS for Premium Styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* Main App Layout */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #0f172a !important;
    }
    
    /* Premium Cards & Containers */
    .premium-card, div[data-testid="stVerticalBlockBorder"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .premium-card:hover, div[data-testid="stVerticalBlockBorder"]:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Accent borders */
    .border-teal { border-top: 4px solid #0f766e !important; }
    .border-blue { border-top: 4px solid #0284c7 !important; }
    .border-orange { border-top: 4px solid #ea580c !important; }
    .border-indigo { border-top: 4px solid #4f46e5 !important; }
    
    .section-title {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.25rem;
        margin-bottom: 15px;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 8px;
    }
    
    /* Metrics Box */
    .metric-box {
        background: #f8fafc;
        border-left: 4px solid #0284c7;
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 12px;
    }
    
    .metric-title {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    
    /* Segmented Control Tabs (iOS/macOS style) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 6px;
        background-color: #e2e8f0;
        border-radius: 10px;
        border: none;
        margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        white-space: nowrap;
        background-color: transparent;
        border: none !important;
        border-radius: 8px;
        color: #475569;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 6px 16px;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #0f172a;
        background-color: rgba(255,255,255,0.4);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0f766e !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
    }
    
    /* Sidebar selector styles */
    .sidebar-widget {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 16px;
    }
    
    /* Footer */
    .creator-footer {
        font-size: 0.75rem;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
        padding-top: 15px;
        margin-top: 25px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("<h2 style='color:#0f766e; margin-bottom: 5px; font-weight:800;'>⚡ Transisi EV</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:0.85rem; margin-top:0;'>Satria Data SIC 2026</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Global Interactive Year Filter
    st.write("**📅 Filter Analisis Halaman**")
    selected_year = st.selectbox(
        "Pilih Tahun Data:",
        ["Semua Tahun", "Tahun 2024", "Tahun 2025"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Dynamic calculations for sidebar metrics
    if selected_year == "Tahun 2024":
        bev_sales_kpi = "43.188 Unit"
        xev_sales_kpi = "103.227 Unit"
        spklu_count_kpi = "803 Titik"
        total_veh_val = f"{bps_nas_2024['Jumlah'].sum() / 1_000_000:.1f} Juta"
    elif selected_year == "Tahun 2025":
        bev_sales_kpi = "103.931 Unit"
        xev_sales_kpi = "175.144 Unit"
        spklu_count_kpi = "937 Titik"
        total_veh_val = "172,9 Juta"
    else:
        # Semua Tahun cumulative
        bev_sales_kpi = "147.119 Unit"
        xev_sales_kpi = "278.371 Unit"
        spklu_count_kpi = "937 Titik"
        total_veh_val = "172,9 Juta"
        
    st.subheader("📊 Statistik Ringkas")
    st.markdown(f"""
    <div class='metric-box' style='border-left-color: #0f766e;'>
        <div class='metric-title'>Total Kendaraan (BPS)</div>
        <div class='metric-value'>{total_veh_val}</div>
    </div>
    <div class='metric-box' style='border-left-color: #0284c7;'>
        <div class='metric-title'>Penjualan BEV (Gaikindo)</div>
        <div class='metric-value'>{bev_sales_kpi}</div>
    </div>
    <div class='metric-box' style='border-left-color: #f59e0b;'>
        <div class='metric-title'>Sebaran SPKLU DKI</div>
        <div class='metric-value'>{spklu_count_kpi}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Creator info
    st.markdown("""
    <div class='creator-footer'>
        <b>Kreator:</b><br>
        Zaky Muhammad Fauzi & Brama Hartoyo<br>
        <i>DS-48-03 Bachelor of Data Science</i><br>
        School of Computing, Telkom University
    </div>
    """, unsafe_allow_html=True)

# ----------------- MAIN CONTENT -----------------

# Header Banner
st.markdown("""
<div style='background-color: #ffffff; padding: 30px; border-radius: 12px; border: 1px solid #e2e8f0; border-left: 6px solid #0f766e; margin-bottom: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
    <div style='font-size: 0.8rem; font-weight: 700; color: #0f766e; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 5px;'>Dashboard Analitik Transisi Energi</div>
    <h1 style='margin: 0; font-size: 2.1rem; font-weight: 800; color: #0f172a; line-height: 1.2;'>
        MENGAKSELERASI EKOSISTEM KENDARAAN LISTRIK (EV) DI INDONESIA
    </h1>
    <p style='margin: 10px 0 0 0; color: #475569; font-size: 1rem; line-height: 1.5;'>
        Sebuah visualisasi data interaktif untuk mengukur tren adopsi pasar, pemetaan sebaran spasial SPKLU, serta tantangan sosial-ekonomi industri hijau nasional.
    </p>
</div>
""", unsafe_allow_html=True)

# Create Tabs (Tab 4 Removed)
tab1, tab2, tab3 = st.tabs([
    "📈 Tren Pasar & Populasi xEV", 
    "⚡ Infrastruktur SPKLU (Jakarta)", 
    "🌱 Peluang, Tantangan & Kerja Hijau"
])

# ----------------- TAB 1: TREN PASAR & POPULASI -----------------
with tab1:
    st.markdown("<h3 style='color:#0f766e; font-weight:700; margin-bottom:5px;'>📈 Tren Adopsi dan Transisi Pasar</h3>", unsafe_allow_html=True)
    st.write("Bagian ini menampilkan dinamika pertumbuhan kendaraan listrik di Indonesia, baik dari segi penjualan nasional maupun minat pencarian masyarakat.")
    
    # 1. Dynamic Headline Statistics
    if selected_year == "Tahun 2024":
        kpi_bev_val = "43.188 Unit"
        kpi_bev_sub = "Awal Adopsi Masif"
        kpi_hev_val = "59.903 Unit"
        kpi_hev_sub = "Pangsa Dominan HEV"
        kpi_share_val = "11,9%"
        kpi_share_sub = "Dari Total Mobil Terjual"
        kpi_target_val = "98.764 Unit"
        kpi_target_sub = "Target ESDM Thn 2025"
    elif selected_year == "Tahun 2025":
        kpi_bev_val = "103.931 Unit"
        kpi_bev_sub = "🚀 +141% YoY vs 2024"
        kpi_hev_val = "65.943 Unit"
        kpi_hev_sub = "+10% YoY vs 2024"
        kpi_share_val = "21,8%"
        kpi_share_sub = "Melampaui Pangsa HEV"
        kpi_target_val = "163.764 Unit"
        kpi_target_sub = "Target ESDM Thn 2026"
    else:
        # Semua Tahun
        kpi_bev_val = "147.119 Unit"
        kpi_bev_sub = "Total BEV Terjual (24-25)"
        kpi_hev_val = "125.846 Unit"
        kpi_hev_sub = "Total HEV Terjual (24-25)"
        kpi_share_val = "16,8% (Rerata)"
        kpi_share_sub = "Akselerasi Eksponensial"
        kpi_target_val = "943.764 Unit"
        kpi_target_sub = "Target Akhir Peta Jalan 2030"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='premium-card border-teal' style='margin-bottom:0;'>
            <div style='color: #64748b; font-size: 0.8rem; font-weight:500; text-transform:uppercase;'>BEV Wholesales</div>
            <div style='font-size: 1.6rem; font-weight: 800; color: #0f766e; margin-top:5px;'>{kpi_bev_val}</div>
            <div style='font-size: 0.8rem; color: #475569; margin-top:5px;'>{kpi_bev_sub}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='premium-card border-blue' style='margin-bottom:0;'>
            <div style='color: #64748b; font-size: 0.8rem; font-weight:500; text-transform:uppercase;'>Hybrid (HEV) Wholesales</div>
            <div style='font-size: 1.6rem; font-weight: 800; color: #0284c7; margin-top:5px;'>{kpi_hev_val}</div>
            <div style='font-size: 0.8rem; color: #475569; margin-top:5px;'>{kpi_hev_sub}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='premium-card border-indigo' style='margin-bottom:0;'>
            <div style='color: #64748b; font-size: 0.8rem; font-weight:500; text-transform:uppercase;'>Pangsa Pasar xEV</div>
            <div style='font-size: 1.6rem; font-weight: 800; color: #4f46e5; margin-top:5px;'>{kpi_share_val}</div>
            <div style='font-size: 0.8rem; color: #475569; margin-top:5px;'>{kpi_share_sub}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='premium-card border-orange' style='margin-bottom:0;'>
            <div style='color: #64748b; font-size: 0.8rem; font-weight:500; text-transform:uppercase;'>Target KBLBB ESDM</div>
            <div style='font-size: 1.6rem; font-weight: 800; color: #e056fd; margin-top:5px;' style='color:#ea580c;'>{kpi_target_val}</div>
            <div style='font-size: 0.8rem; color: #475569; margin-top:5px;'>{kpi_target_sub}</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Main charts grid
    st.markdown("<br>", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns([3, 2])
    
    # Filter sales data based on year
    if selected_year == "Tahun 2024":
        filtered_sales_df = gaik_ann[gaik_ann["Tahun"] == "2024"]
    elif selected_year == "Tahun 2025":
        filtered_sales_df = gaik_ann[gaik_ann["Tahun"] == "2025"]
    else:
        filtered_sales_df = gaik_ann

    with chart_col1:
        with st.container(border=True):
            st.markdown("<div class='section-title'>📊 Perkembangan Penjualan Kendaraan Listrik (Gaikindo)</div>", unsafe_allow_html=True)
            
            fig_sales = px.bar(
                filtered_sales_df,
                x="Tahun",
                y="Penjualan",
                color="Kategori",
                barmode="group",
                color_discrete_map={"BEV": "#0f766e", "HEV": "#0284c7", "PHEV": "#f97316"},
                text_auto='.3s',
                height=350
            )
            fig_sales.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#0f172a',
                xaxis=dict(gridcolor='#e2e8f0', title="Tahun"),
                yaxis=dict(gridcolor='#e2e8f0', title="Penjualan (Unit)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_sales, use_container_width=True)
        
    with chart_col2:
        with st.container(border=True):
            st.markdown("<div class='section-title'>🎯 Target vs Realisasi Populasi KBLBB</div>", unsafe_allow_html=True)
            
            roadmap_years = [2025, 2026, 2027, 2028, 2029, 2030]
            roadmap_targets = [98764, 163764, 243764, 393764, 633764, 943764]
            
            fig_target = go.Figure()
            fig_target.add_trace(go.Scatter(
                x=roadmap_years, y=roadmap_targets,
                mode='lines+markers',
                name='Target Nasional (ESDM)',
                line=dict(color='#ea580c', width=3, dash='dash'),
                marker=dict(size=8)
            ))
            
            if selected_year == "Tahun 2024":
                fig_target.add_trace(go.Bar(
                    x=[2024], y=[43324],
                    name='Realisasi Populasi (2024)',
                    marker_color='#0f766e',
                    width=0.3
                ))
            elif selected_year == "Tahun 2025":
                fig_target.add_trace(go.Bar(
                    x=[2025], y=[147119],
                    name='Realisasi Populasi (2025)',
                    marker_color='#0f766e',
                    width=0.3
                ))
            else:
                fig_target.add_trace(go.Bar(
                    x=[2024, 2025], y=[43324, 147119],
                    name='Realisasi Populasi',
                    marker_color='#0f766e',
                    width=0.3
                ))
                
            fig_target.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#0f172a',
                xaxis=dict(gridcolor='#e2e8f0', tickmode='linear'),
                yaxis=dict(gridcolor='#e2e8f0', title="Populasi (Unit)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=350
            )
            st.plotly_chart(fig_target, use_container_width=True)

    # 3. Google Trends & BPS Vehicle population
    col_trends, col_pop = st.columns([1, 1])
    
    with col_trends:
        with st.container(border=True):
            st.markdown("<div class='section-title'>📈 Minat Penelusuran Masyarakat (Google Trends)</div>", unsafe_allow_html=True)
            
            trends_df = trends.copy()
            fig_trends = px.line(
                trends_df,
                x="Time",
                y=["ev", "kendaraan listrik", "SPKLU"],
                labels={"value": "Indeks Minat (0-100)", "variable": "Kata Kunci"},
                color_discrete_sequence=["#0284c7", "#0f766e", "#f97316"],
                height=350
            )
            fig_trends.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#0f172a',
                xaxis=dict(gridcolor='#e2e8f0', title="Tahun"),
                yaxis=dict(gridcolor='#e2e8f0'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_trends, use_container_width=True)
            
    with col_pop:
        with st.container(border=True):
            st.markdown("<div class='section-title'>⚖️ Jurang Transisi: Populasi Kendaraan Nasional</div>", unsafe_allow_html=True)
            
            # Calculate dynamic pie chart values
            if selected_year == "Tahun 2024":
                total_ice = bps_nas_2024['Jumlah'].sum()
                total_ev = 43324
                labels_year = "2024"
            else:
                total_ice = 172938093
                total_ev = 147119
                labels_year = "2025"
                
            categories = ["Konvensional (BBM)", "KBLBB (Listrik murni)"]
            values = [total_ice, total_ev]
            
            fig_gap = go.Figure(data=[go.Pie(
                labels=categories,
                values=values,
                hole=.4,
                marker_colors=["#cbd5e1", "#0f766e"]
            )])
            fig_gap.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#0f172a',
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                height=350
            )
            st.plotly_chart(fig_gap, use_container_width=True)

    # 4. Wide Insight Panel (Tab 1 Summary)
    st.markdown(f"""
    <div class='premium-card border-teal'>
        <div class='section-title'>💡 Analisis Temuan Lanskap Pasar & Transisi EV ({selected_year})</div>
        <ul style='margin: 0; padding-left: 20px; color: #475569; line-height:1.6;'>
            <li><b>Akselerasi Pasar BEV:</b> Penjualan BEV nasional melonjak signifikan dari <b>43.188 unit (2024)</b> menjadi <b>103.931 unit (2025)</b>. Hal ini menunjukkan peningkatan adopsi hingga <b>+141% YoY</b>, melampaui pertumbuhan mobil Hybrid (HEV) yang hanya tumbuh 10%.</li>
            <li><b>Melampaui Target Awal:</b> Akumulasi realisasi KBLBB hingga tahun 2025 mencapai <b>147.119 unit</b>, mengungguli target awal peta jalan Kemen ESDM 24/2025 untuk tahun 2025 sebesar <b>98.764 unit</b>.</li>
            <li><b>Skala Jurang Transisi:</b> Meskipun pertumbuhan persentase EV sangat masif, proporsinya terhadap total armada kendaraan nasional (BPS) masih di kisaran <b>0,08%</b> dari total <b>{total_veh_val}</b> kendaraan konvensional berbahan bakar fosil. Hal ini menandakan transisi penuh membutuhkan waktu dan strategi konversi jangka panjang.</li>
            <li><b>Kesadaran Publik:</b> Minat pencarian Google Trends untuk kata kunci <i>"kendaraan listrik"</i> dan <i>"SPKLU"</i> menunjukkan peningkatan konsisten sejak pertengahan 2022, membuktikan penerimaan masyarakat dan kesadaran infrastruktur mulai meluas secara nasional.</li>
    </div>
    """, unsafe_allow_html=True)

# ----------------- TAB 2: INFRASTRUKTUR SPKLU (JAKARTA) -----------------
with tab2:
    st.markdown("<h3 style='color:#0f766e; font-weight:700; margin-bottom:5px;'>⚡ Analisis Sebaran SPKLU di DKI Jakarta</h3>", unsafe_allow_html=True)
    st.write("Visualisasi sebaran stasiun pengisian daya kendaraan listrik umum (SPKLU) sampel untuk wilayah DKI Jakarta, memetakan kepadatan dan jenis pengisian daya.")
    
    # Load spklu data
    df_spklu = spklu_list
    
    col_map, col_stats = st.columns([3, 2])
    
    with col_map:
        with st.container(border=True):
            st.markdown("<div class='section-title'>🗺️ Peta Interaktif Sebaran Lokasi SPKLU</div>", unsafe_allow_html=True)
            
            # Filter map by operator
            operators_list = ["Semua"] + list(df_spklu['clean_operator'].unique())
            selected_op = st.selectbox("Saring berdasarkan Operator:", operators_list)
            
            filtered_spklu = df_spklu
            if selected_op != "Semua":
                filtered_spklu = df_spklu[df_spklu['clean_operator'] == selected_op]
                
            fig_map = px.scatter_mapbox(
                filtered_spklu,
                lat="latitude",
                lon="longitude",
                hover_name="nama_spklu",
                hover_data=["owner_operator", "jumlah_unit", "teknologi", "lokasi"],
                color="teknologi",
                size="jumlah_unit",
                color_discrete_map={
                    "MEDIUM CHARGING": "#0284c7",
                    "ULTRA FAST CHARGING": "#be123c",
                    "STANDART CHARGING": "#64748b",
                    "FAST CHARGING": "#0f766e"
                },
                zoom=10.2,
                mapbox_style="carto-positron",
                height=370
            )
            fig_map.update_layout(
                margin={"r":0,"t":0,"l":0,"b":0},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#0f172a'
            )
            st.plotly_chart(fig_map, use_container_width=True)
            st.markdown("<span style='font-size:0.8rem; color:#64748b;'>*Ukuran titik melambangkan jumlah charger di lokasi tersebut. Seret dan perbesar peta.*</span>", unsafe_allow_html=True)
        
    with col_stats:
        with st.container(border=True):
            st.markdown("<div class='section-title'>🔌 Statistik Infrastruktur Pengisian</div>", unsafe_allow_html=True)
            
            # 1. Target vs Realisasi SPKLU
            st.markdown("<span style='font-size:0.85rem; font-weight:600; color:#475569;'>Target vs Realisasi SPKLU DKI Jakarta (Unit)</span>", unsafe_allow_html=True)
            df_target_spklu = spklu_target
            fig_target_spklu = px.bar(
                df_target_spklu,
                x="periode_data",
                y=["target_spklu", "realisasi_spklu"],
                barmode="group",
                labels={"value": "Jumlah", "periode_data": "Tahun", "variable": "Status"},
                color_discrete_map={"target_spklu": "#cbd5e1", "realisasi_spklu": "#0284c7"},
                height=180
            )
            fig_target_spklu.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#0f172a',
                xaxis=dict(gridcolor='#e2e8f0', tickmode='linear'),
                yaxis=dict(gridcolor='#e2e8f0', title=None),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_target_spklu, use_container_width=True)
            
            # 2. Technology distribution
            tech_counts = df_spklu['teknologi'].value_counts().reset_index()
            tech_counts.columns = ['Teknologi', 'Jumlah']
            
            st.markdown("<span style='font-size:0.85rem; font-weight:600; color:#475569; margin-top:10px;'>Komposisi Teknologi Pengisian</span>", unsafe_allow_html=True)
            fig_tech = px.bar(
                tech_counts,
                y='Teknologi',
                x='Jumlah',
                orientation='h',
                color='Teknologi',
                color_discrete_map={
                    "MEDIUM CHARGING": "#0284c7",
                    "ULTRA FAST CHARGING": "#be123c",
                    "STANDART CHARGING": "#64748b",
                    "FAST CHARGING": "#0f766e"
                },
                height=160
            )
            fig_tech.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#0f172a',
                xaxis=dict(gridcolor='#e2e8f0', title=None),
                yaxis=dict(gridcolor='rgba(0,0,0,0)', title=None)
            )
            st.plotly_chart(fig_tech, use_container_width=True)
        
    # Operator share row
    with st.container(border=True):
        st.markdown("<div style='height: 4px; background-color: #0284c7; border-radius: 2px; margin-bottom: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🏢 Dominasi Operator Swasta vs BUMN dalam Penyediaan Charger</div>", unsafe_allow_html=True)
        
        op_counts = df_spklu['clean_operator'].value_counts().reset_index()
        op_counts.columns = ['Operator', 'Jumlah SPKLU']
        # Keep top 5 and group others
        top_n = 5
        top_ops = op_counts.head(top_n).copy()
        others_sum = op_counts.iloc[top_n:]['Jumlah SPKLU'].sum()
        if others_sum > 0:
            others_df = pd.DataFrame([{'Operator': 'LAINNYA / PRIVATE BRAND', 'Jumlah SPKLU': others_sum}])
            top_ops = pd.concat([top_ops, others_df], ignore_index=True)
            
        fig_op = px.pie(
            top_ops,
            names='Operator',
            values='Jumlah SPKLU',
            color_discrete_sequence=px.colors.qualitative.Safe,
            hole=0.4,
            height=280
        )
        fig_op.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#0f172a',
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1)
        )
        op_col1, op_col2 = st.columns([1, 2])
        with op_col1:
            st.plotly_chart(fig_op, use_container_width=True)
        with op_col2:
            st.markdown("""
            <div style='color: #475569; line-height: 1.6; font-size: 0.95rem;'>
                <ul style='margin: 0; padding-left: 20px;'>
                    <li><b>Peran Swasta Sangat Besar:</b> Operator swasta seperti <b>Voltron</b> mendominasi penyediaan infrastruktur pengisian daya dengan <b>447 lokasi sampel</b>, melampaui operator negara <b>PLN (250 lokasi)</b>. Hal ini menunjukkan ekosistem investasi SPKLU di DKI Jakarta berjalan agresif dan menarik minat swasta secara riil.</li>
                    <li><b>Kesenjangan Wilayah Spasial:</b> Terjadi ketimpangan persebaran SPKLU. Wilayah komersial seperti <b>Jakarta Selatan (286 lokasi)</b> dan <b>Jakarta Pusat (169 lokasi)</b> memiliki densitas stasiun tertinggi, sedangkan wilayah penyangga pemukiman padat masih sangat minim akses pengisian.</li>
                    <li><b>Urgensi Peningkatan Teknologi:</b> Mayoritas colokan pengisi daya masih berjenis <i>Medium Charging</i> (551 unit). Untuk menunjang mobilitas cepat antar kota, akselerasi ke tipe <i>Fast Charging</i> dan <i>Ultra Fast Charging</i> mutlak dipercepat oleh para operator.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ----------------- TAB 3: PELUANG, TANTANGAN & KERJA HIJAU -----------------
with tab3:
    st.markdown("<h3 style='color:#0f766e; font-weight:700; margin-bottom:5px;'>🌱 Peluang & Tantangan Transisi Energi</h3>", unsafe_allow_html=True)
    st.write("Analisis dampak transisi energi terhadap struktur perdagangan otomotif nasional dan peta jalan pembukaan lapangan kerja baru (*green jobs*).")
    
    # Trade trajectory data
    with st.container(border=True):
        st.markdown("<div style='height: 4px; background-color: #4f46e5; border-radius: 2px; margin-bottom: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>🚗 Lintasan Perdagangan Otomotif Indonesia (CBU Exports vs Imports)</div>", unsafe_allow_html=True)
        
        trade_years = ["2020", "2022", "2025"]
        cbu_exports = [232175, 473802, 518212]
        cbu_imports = [35173, 83298, 97010]
        
        fig_trade = go.Figure()
        fig_trade.add_trace(go.Bar(
            x=trade_years, y=cbu_exports,
            name="Ekspor CBU (Unit)",
            marker_color="#0f766e"
        ))
        fig_trade.add_trace(go.Bar(
            x=trade_years, y=cbu_imports,
            name="Impor CBU (Unit)",
            marker_color="#ea580c"
        ))
        fig_trade.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#0f172a',
            xaxis=dict(gridcolor='#e2e8f0', title="Tahun"),
            yaxis=dict(gridcolor='#e2e8f0', title="Jumlah Kendaraan (Unit)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=320
        )
        
        trade_col1, trade_col2 = st.columns([3, 2])
        with trade_col1:
            st.plotly_chart(fig_trade, use_container_width=True)
        with trade_col2:
            st.markdown("""
            <div style='color: #475569; line-height: 1.6; font-size: 0.95rem; padding-top: 10px;'>
                <b>Hilirisasi & Penguatan Manufaktur Lokal:</b>
                <ul style='margin-top: 10px; padding-left: 20px;'>
                    <li><b>Rasio Ekspor-Impor 5:1:</b> Indonesia berhasil mengekspor kendaraan utuh (CBU) lima kali lipat lebih banyak daripada impor CBU pada tahun 2025 (<b>518.212 ekspor</b> vs <b>97.010 impor</b>).</li>
                    <li><b>Akselerasi CKD Lokal:</b> Kebijakan TKDN mendorong produsen EV asing mendirikan pabrik perakitan (CKD) lokal di Indonesia (seperti BYD, Wuling, Chery, Hyundai).</li>
                    <li><b>Rantai Pasok Baterai:</b> Hilirisasi nikel mentah menjadi sel baterai terintegrasi (smelter HPAL) mengamankan posisi tawar Indonesia di kancah otomotif hijau global.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
    # Paradox & Green Jobs
    col_para, col_jobs = st.columns(2)
    with col_para:
        with st.container(border=True):
            st.markdown("<div style='height: 4px; background-color: #ea580c; border-radius: 2px; margin-bottom: 15px;'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>⚖️ Paradoks Listrik Bersih & Hilirisasi Nikel</div>", unsafe_allow_html=True)
            st.markdown("""
            <div style='color: #475569; line-height: 1.6; font-size: 0.95rem;'>
                <ul style='margin: 0; padding-left: 20px;'>
                    <li><b>Ketergantungan Batubara:</b> Lebih dari <b>60%</b> listrik pengisi daya EV di Indonesia masih dipasok dari pembangkit listrik batubara (PLTU). Transisi ke EBT pada grid nasional harus berjalan beriringan dengan adopsi EV.</li>
                    <li><b>Dampak Lingkungan Tambang:</b> Ekstraksi nikel skala besar memicu kekhawatiran deforestasi dan pencemaran pesisir. Penerapan standar penambangan bertanggung jawab (<i>responsible mining</i>) sangat krusial agar transisi energi tetap lestari secara lokal.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
    with col_jobs:
        with st.container(border=True):
            st.markdown("<div style='height: 4px; background-color: #0f766e; border-radius: 2px; margin-bottom: 15px;'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>💼 Potensi Lapangan Kerja Hijau (Green Jobs)</div>", unsafe_allow_html=True)
            st.markdown("""
            <div style='color: #475569; line-height: 1.6; font-size: 0.95rem;'>
                <ul style='margin: 0; padding-left: 20px;'>
                    <li><b>Penciptaan Lapangan Kerja:</b> Proyeksi penciptaan <b>500.000 pekerjaan hijau baru pada 2030</b> dan berpotensi mencapai 1.7 juta pada 2045 di sektor manufaktur baterai, servis EV, dan daur ulang baterai.</li>
                    <li><b>Kesenjangan Keterampilan:</b> Indonesia memerlukan program pelatihan ulang (<i>reskilling</i>) berskala besar bagi jutaan mekanik bengkel konvensional agar siap menguji dan merawat sistem bertegangan tinggi (<i>high-voltage</i>).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
