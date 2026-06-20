import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<style>
    /* Main App Layout */
    .stApp {
        background-color: #090a10;
        color: #e2e8f0;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111320 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Cards / Containers */
    .premium-card {
        background: rgba(25, 28, 48, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    /* Glow effect for headings */
    .glow-text {
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.6);
        color: #00f2fe;
    }
    
    .glow-green {
        text-shadow: 0 0 10px rgba(57, 255, 20, 0.6);
        color: #39ff14;
    }
    
    /* Metrics Box */
    .metric-box {
        background: rgba(13, 14, 25, 0.8);
        border-left: 4px solid #00f2fe;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: rgba(25, 28, 48, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px 8px 0px 0px;
        color: #94a3b8;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #00f2fe;
        background-color: rgba(25, 28, 48, 0.8);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(25, 28, 48, 0.95) !important;
        border-top: 2px solid #00f2fe !important;
        color: #00f2fe !important;
    }
    
    /* Footer */
    .creator-footer {
        font-size: 0.75rem;
        color: #64748b;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        padding-top: 15px;
        margin-top: 30px;
        line-height: 1.4;
    }
    
    /* Print Poster styling */
    @media print {
        body * {
            visibility: hidden;
        }
        #print-section, #print-section * {
            visibility: visible;
        }
        #print-section {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("<h2 class='glow-text'>⚡ Transisi EV</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sub-theme info
    st.markdown("""
    **Tema Besar:**
    *Mengolah Data, Membangun Bangsa*
    
    **Sub-Tema:**
    *Transisi Energi & Tantangan Industri Nasional*
    """)
    
    st.markdown("---")
    
    # Quick Statistics
    st.subheader("📊 Statistik Ringkas")
    st.markdown("""
    <div class='metric-box' style='border-left-color: #39ff14;'>
        <div class='metric-title'>Total Kendaraan (BPS 2025)</div>
        <div class='metric-value'>172,9 Juta</div>
    </div>
    <div class='metric-box' style='border-left-color: #00f2fe;'>
        <div class='metric-title'>Penjualan xEV (2025)</div>
        <div class='metric-value'>175.144 Unit</div>
    </div>
    <div class='metric-box' style='border-left-color: #f1c40f;'>
        <div class='metric-title'>Sebaran SPKLU Jakarta (Sample)</div>
        <div class='metric-value'>937 Titik</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Creator info (As requested)
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
<div style='background: linear-gradient(135deg, #111328 0%, #070913 100%); padding: 30px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 25px;'>
    <h1 style='margin: 0; font-size: 2.3rem; font-weight: 800; background: linear-gradient(to right, #00f2fe, #4facfe, #39ff14); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        TRANSISI ENERGI NASIONAL: MENGAKSELERASI EKOSISTEM KENDARAAN LISTRIK (EV)
    </h1>
    <p style='margin: 10px 0 0 0; color: #94a3b8; font-size: 1.1rem;'>
        Analisis Komprehensif Mengenai Perkembangan, Tren Pasar, Tantangan Infrastruktur, dan Lapangan Kerja Hijau di Indonesia.
    </p>
</div>
""", unsafe_allow_html=True)

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tren Pasar & Populasi xEV", 
    "⚡ Infrastruktur SPKLU (Jakarta)", 
    "🌱 Peluang, Tantangan & Kerja Hijau", 
    "📰 Poster Infografis (Format Poster)"
])

# ----------------- TAB 1: TREN PASAR & POPULASI -----------------
with tab1:
    st.markdown("<h3 class='glow-text'>📈 Tren Adopsi dan Transisi Pasar</h3>", unsafe_allow_html=True)
    st.write("Bagian ini menampilkan dinamika pertumbuhan kendaraan listrik di Indonesia, baik dari segi penjualan nasional maupun minat pencarian masyarakat.")
    
    # 1. Headline Statistics Rows
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='premium-card' style='padding: 15px; margin-bottom: 10px;'>
            <div style='color: #94a3b8; font-size: 0.85rem;'>BEV Wholesales (2025)</div>
            <div style='font-size: 1.7rem; font-weight: 700; color: #39ff14;'>103.931 Unit</div>
            <div style='font-size: 0.8rem; color: #00f2fe;'>+141% YoY (vs 2024)</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='premium-card' style='padding: 15px; margin-bottom: 10px;'>
            <div style='color: #94a3b8; font-size: 0.85rem;'>Hybrid (HEV) Wholesales (2025)</div>
            <div style='font-size: 1.7rem; font-weight: 700; color: #4facfe;'>65.943 Unit</div>
            <div style='font-size: 0.8rem; color: #94a3b8;'>+10% YoY (vs 2024)</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='premium-card' style='padding: 15px; margin-bottom: 10px;'>
            <div style='color: #94a3b8; font-size: 0.85rem;'>Pangsa xEV terhadap Mobil Nasional</div>
            <div style='font-size: 1.7rem; font-weight: 700; color: #ff007f;'>21,8% (2025)</div>
            <div style='font-size: 0.8rem; color: #94a3b8;'>Meningkat drastis dari 11,9% (2024)</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='premium-card' style='padding: 15px; margin-bottom: 10px;'>
            <div style='color: #94a3b8; font-size: 0.85rem;'>Target KBLBB ESDM (2030)</div>
            <div style='font-size: 1.7rem; font-weight: 700; color: #f1c40f;'>943.764 Unit</div>
            <div style='font-size: 0.8rem; color: #f1c40f;'>Peta Jalan Kepmen ESDM 24/2025</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Main charts grid
    st.markdown("<br>", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns([3, 2])
    
    with chart_col1:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("📊 Perkembangan Penjualan Kendaraan Listrik (Gaikindo)")
        
        # Plotly Bar chart for Wholesales (2024 vs 2025)
        annual_sales_df = gaik_ann
        fig_sales = px.bar(
            annual_sales_df,
            x="Tahun",
            y="Penjualan",
            color="Kategori",
            barmode="group",
            color_discrete_map={"BEV": "#39ff14", "HEV": "#4facfe", "PHEV": "#ff007f"},
            text_auto='.3s'
        )
        fig_sales.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Penjualan (Unit)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_sales, use_container_width=True)
        
        # Short insight
        st.markdown("""
        **Analisis Tren:**  
        Tahun 2025 merupakan titik balik bersejarah (*inflection point*) di mana penjualan mobil listrik murni (**BEV**) melonjak hingga **141%** dan melampaui penjualan mobil **Hybrid**. 
        Hal ini didorong oleh membanjirnya merek-merek Tiongkok baru serta perluasan TKDN lokal.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with chart_col2:
        st.markdown("<div class='premium-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.subheader("🎯 Target vs Realisasi Populasi KBLBB")
        
        # Roadmap data
        roadmap_years = [2025, 2026, 2027, 2028, 2029, 2030]
        roadmap_targets = [98764, 163764, 243764, 393764, 633764, 943764]
        # Current realization estimated from accumulated sales + registration
        realization = [147119, 0, 0, 0, 0, 0] # Realization cumulative BEV + PHEV active
        
        fig_target = go.Figure()
        fig_target.add_trace(go.Scatter(
            x=roadmap_years, y=roadmap_targets,
            mode='lines+markers',
            name='Target Nasional (ESDM)',
            line=dict(color='#f1c40f', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        fig_target.add_trace(go.Bar(
            x=[2025], y=[147119],
            name='Realisasi Populasi (2025)',
            marker_color='#39ff14',
            width=0.4
        ))
        fig_target.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickmode='linear'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Populasi Kendaraan (Unit)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_target, use_container_width=True)
        st.markdown("""
        *Realisasi populasi KBLBB kumulatif per tahun 2025 telah melampaui target awal peta jalan pemerintah (98.764 unit vs 147.119 unit aktual), menandakan akselerasi adopsi yang lebih cepat dari perkiraan.*
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Google Trends & BPS Vehicle population
    st.markdown("<br>", unsafe_allow_html=True)
    col_trends, col_pop = st.columns([1, 1])
    
    with col_trends:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("📈 Minat Penelusuran Masyarakat (Google Trends)")
        
        # Filter Google Trends
        trends_df = trends.copy()
        fig_trends = px.line(
            trends_df,
            x="Time",
            y=["ev", "kendaraan listrik", "SPKLU"],
            labels={"value": "Indeks Minat (0-100)", "variable": "Kata Kunci"},
            color_discrete_sequence=["#00f2fe", "#39ff14", "#ff007f"]
        )
        fig_trends.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Tahun"),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trends, use_container_width=True)
        st.markdown("""
        Pencarian terkait *"kendaraan listrik"* dan *"ev"* mulai melonjak signifikan sejak pertengahan tahun 2022, seiring dengan peluncuran model ikonik yang dirakit lokal serta kebijakan subsidi pemerintah.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_pop:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("⚖️ Jurang Transisi: Populasi Kendaraan Nasional")
        
        # General vehicle population (BPS 2025)
        # Total ICE vs EV (98k target vs 172.9M conventional)
        categories = ["Konvensional (BBM)", "KBLBB (Listrik murni)"]
        values = [172938093, 147119] # 2025 numbers
        
        fig_gap = go.Figure(data=[go.Pie(
            labels=categories,
            values=values,
            hole=.4,
            marker_colors=["#e2e8f0", "#39ff14"]
        )])
        fig_gap.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_gap, use_container_width=True)
        st.markdown("""
        **Tantangan Utama:** Meskipun pertumbuhan penjualan mobil listrik melesat ratusan persen, proporsi EV murni terhadap total kendaraan nasional saat ini baru mencapai **0.08%**. Transisi penuh memerlukan waktu, hilirisasi yang kokoh, dan konversi armada yang masif.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 2: INFRASTRUKTUR SPKLU (JAKARTA) -----------------
with tab2:
    st.markdown("<h3 class='glow-text'>⚡ Analisis Sebaran SPKLU di DKI Jakarta</h3>", unsafe_allow_html=True)
    st.write("Visualisasi sebaran stasiun pengisian daya kendaraan listrik umum (SPKLU) sampel untuk wilayah DKI Jakarta, memetakan kepadatan dan jenis pengisian daya.")
    
    # Load spklu data
    df_spklu = spklu_list
    
    col_map, col_stats = st.columns([3, 2])
    
    with col_map:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.subheader("🗺️ Peta Interaktif Sebaran Lokasi SPKLU")
        
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
                "MEDIUM CHARGING": "#4facfe",
                "ULTRA FAST CHARGING": "#ff007f",
                "STANDART CHARGING": "#e2e8f0",
                "FAST CHARGING": "#39ff14"
            },
            zoom=10.5,
            mapbox_style="carto-darkmatter",
            height=500
        )
        fig_map.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown("*Ukuran titik melambangkan jumlah unit colokan (charger) di lokasi tersebut. Seret dan perbesar peta untuk melihat sebaran spasial secara mendalam.*")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_stats:
        st.markdown("<div class='premium-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.subheader("🔌 Statistik Infrastruktur Pengisian")
        
        # 1. Target vs Realisasi SPKLU
        st.write("**Target Pembangunan SPKLU DKI Jakarta (Unit)**")
        df_target_spklu = spklu_target
        fig_target_spklu = px.bar(
            df_target_spklu,
            x="periode_data",
            y=["target_spklu", "realisasi_spklu"],
            barmode="group",
            labels={"value": "Jumlah SPKLU (Unit)", "periode_data": "Tahun", "variable": "Status"},
            color_discrete_map={"target_spklu": "#64748b", "realisasi_spklu": "#00f2fe"}
        )
        fig_target_spklu.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickmode='linear'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_target_spklu, use_container_width=True)
        
        # 2. Technology distribution
        tech_counts = df_spklu['teknologi'].value_counts().reset_index()
        tech_counts.columns = ['Teknologi', 'Jumlah']
        
        st.write("**Komposisi Teknologi Pengisian**")
        fig_tech = px.bar(
            tech_counts,
            y='Teknologi',
            x='Jumlah',
            orientation='h',
            color='Teknologi',
            color_discrete_map={
                "MEDIUM CHARGING": "#4facfe",
                "ULTRA FAST CHARGING": "#ff007f",
                "STANDART CHARGING": "#e2e8f0",
                "FAST CHARGING": "#39ff14"
            }
        )
        fig_tech.update_layout(
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_tech, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Operator share row
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("🏢 Dominasi Operator Swasta vs BUMN dalam Penyediaan Charger")
    
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
        color_discrete_sequence=px.colors.sequential.Agsunset,
        hole=0.4
    )
    fig_op.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0',
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1)
    )
    op_col1, op_col2 = st.columns([1, 2])
    with op_col1:
        st.plotly_chart(fig_op, use_container_width=True)
    with op_col2:
        st.markdown("""
        **Analisis Ekosistem Infrastruktur:**
        * **Peran Swasta Sangat Besar:** Operator swasta seperti **Voltron** menjadi penyedia infrastruktur pengisian daya terbesar (447 lokasi sampel), melampaui **PLN** (250 lokasi). Hal ini membuktikan iklim investasi SPKLU di Jakarta cukup menarik bagi swasta.
        * **Kesenjangan Wilayah:** Kepadatan SPKLU sangat timpang. **Jakarta Selatan (286 lokasi)** dan **Jakarta Pusat (169 lokasi)** memiliki titik pengisian daya terbanyak, sementara wilayah pemukiman padat dan penyangga di luar Jakarta masih minim akses.
        * **Pentingnya Fast Charging:** Mayoritas charger masih bertipe *Medium Charging* (551 titik). Untuk mendorong adopsi BEV jarak jauh, peningkatan ke *Fast* dan *Ultra Fast Charging* mutlak diperlukan guna memangkas waktu pengisian daya dari jam menjadi menit.
        """)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 3: PELUANG, TANTANGAN & KERJA HIJAU -----------------
with tab3:
    st.markdown("<h3 class='glow-text'>🌱 Peluang & Tantangan Transisi Energi</h3>", unsafe_allow_html=True)
    st.write("Analisis dampak transisi energi terhadap struktur perdagangan otomotif nasional dan peta jalan pembukaan lapangan kerja baru (*green jobs*).")
    
    # Trade trajectory data
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("🚗 Lintasan Perdagangan Otomotif Indonesia (CBU Exports vs Imports)")
    
    # Data from trade trajectory
    trade_years = ["2020", "2022", "2025"]
    cbu_exports = [232175, 473802, 518212]
    cbu_imports = [35173, 83298, 97010]
    
    fig_trade = go.Figure()
    fig_trade.add_trace(go.Bar(
        x=trade_years, y=cbu_exports,
        name="Ekspor CBU (Unit)",
        marker_color="#39ff14"
    ))
    fig_trade.add_trace(go.Bar(
        x=trade_years, y=cbu_imports,
        name="Impor CBU (Unit)",
        marker_color="#ff007f"
    ))
    fig_trade.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e2e8f0',
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Tahun"),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title="Jumlah Kendaraan (Unit)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    trade_col1, trade_col2 = st.columns([3, 2])
    with trade_col1:
        st.plotly_chart(fig_trade, use_container_width=True)
    with trade_col2:
        st.markdown("""
        **Hilirisasi & Penguatan Manufaktur Lokal:**
        * **Rasio Ekspor-Impor 5:1:** Indonesia berhasil mengekspor kendaraan utuh (CBU) lima kali lipat lebih banyak daripada impor CBU pada tahun 2025 (**518.212 ekspor** vs **97.010 impor**). 
        * **Akselerasi CKD Lokal:** Melalui kebijakan Tingkat Komponen Dalam Negeri (TKDN), produsen EV asing didorong mendirikan pabrik perakitan (CKD) di Indonesia (seperti BYD, Wuling, Chery, Hyundai).
        * **Pentingnya Rantai Pasok Baterai:** Transformasi dari negara pengekspor nikel mentah menjadi produsen sel baterai terintegrasi (smelter HPAL) akan mengunci posisi tawar Indonesia di kancah otomotif hijau global.
        """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Paradox & Green Jobs
    col_para, col_jobs = st.columns(2)
    with col_para:
        st.markdown("<div class='premium-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h4 class='glow-text'>⚖️ Paradoks Listrik Bersih & Nikel</h4>", unsafe_allow_html=True)
        st.markdown("""
        * **Ketergantungan Batubara:** Lebih dari **60%** listrik pengisi daya EV di Indonesia masih dipasok dari pembangkit listrik berbahan bakar batubara (PLTU). Mengendarai EV memindahkan emisi dari knalpot kendaraan ke cerobong pembangkit listrik. Transisi ke Energi Baru Terbarukan (EBT) pada grid nasional harus berjalan pararel.
        * **Ekstraksi Nikel:** Tambang nikel skala besar di Morowali, Weda Bay, dan Pulau Obi memicu deforestasi dan pencemaran pesisir. Pemerintah dan industri harus menerapkan standar penambangan bertanggung jawab (*responsible mining*) agar transisi energi tidak mengorbankan ekosistem lokal.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_jobs:
        st.markdown("<div class='premium-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h4 class='glow-green'>💼 Lapangan Kerja Hijau (Green Jobs)</h4>", unsafe_allow_html=True)
        st.markdown("""
        * **Potensi Lapangan Kerja:** Proyeksi penciptaan **500.000 pekerjaan hijau baru pada 2030** dan berpotensi mencapai 1.7 juta pada 2045 di sektor manufaktur baterai, pemeliharaan EV, stasiun pengisian daya, dan daur ulang baterai.
        * **Tantangan Gap Keterampilan:** Indonesia terancam kekurangan tenaga ahli terlatih. Dibutuhkan program pelatihan ulang (*reskilling*) bagi jutaan mekanik bengkel konvensional agar terbiasa menangani sistem kelistrikan bertegangan tinggi (*high-voltage systems*), serta kurikulum ramah lingkungan (*green curriculum*) sejak bangku sekolah kejuruan.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TAB 4: POSTER INFOGRAFIS (FORMAT POSTER) -----------------
with tab4:
    # Print trigger button
    st.button("Print / Simpan Sebagai PDF", on_click=None, help="Gunakan menu print browser (Ctrl+P / Cmd+P) untuk menyimpan poster sebagai PDF.")
    
    # Render the poster layout as a single-page structured dashboard
    st.markdown("""
    <div id="print-section" style="background-color: #0b0c15; color: #e2e8f0; padding: 40px; border-radius: 12px; border: 2px solid #00f2fe; width: 100%; max-width: 900px; margin: 0 auto; box-shadow: 0 10px 40px rgba(0,0,0,0.5);">
        
        <!-- Poster Header -->
        <div style="text-align: center; border-bottom: 2px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 25px;">
            <div style="color: #39ff14; font-weight: 800; font-size: 1.1rem; letter-spacing: 2px; text-transform: uppercase;">
                Statistics Infographic Competition (SIC) SATRIA DATA 2026
            </div>
            <h1 style="color: #ffffff; font-size: 2.2rem; font-weight: 800; margin: 10px 0; line-height: 1.2;">
                TRANSISI EMERGENSI EKOSISTEM EV DI INDONESIA
            </h1>
            <p style="color: #94a3b8; font-size: 1rem; margin: 5px 0 0 0; font-style: italic;">
                Menakar Kesiapan Pasar, Infrastruktur SPKLU, serta Tantangan Kerja Hijau Nasional
            </p>
        </div>
        
        <!-- Section 1: The Transition Gap -->
        <div style="margin-bottom: 30px;">
            <h3 style="color: #00f2fe; border-bottom: 1px solid rgba(0,242,254,0.3); padding-bottom: 5px; font-weight: 700; margin-bottom: 15px;">
                1. Jurang Transisi: Skala Raksasa yang Harus Dielektrifikasi
            </h3>
            <div style="display: flex; gap: 20px; margin-bottom: 10px;">
                <div style="flex: 1; background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; border-left: 4px solid #64748b;">
                    <div style="font-size: 0.8rem; color: #94a3b8;">Populasi Kendaraan Konvensional (BBM)</div>
                    <div style="font-size: 1.6rem; font-weight: 700; color: #ffffff;">172.938.093 Unit</div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 5px;">Minyak bumi impor menekan APBN</div>
                </div>
                <div style="flex: 1; background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; border-left: 4px solid #39ff14;">
                    <div style="font-size: 0.8rem; color: #94a3b8;">Realisasi Populasi KBLBB (Listrik Murni)</div>
                    <div style="font-size: 1.6rem; font-weight: 700; color: #39ff14;">147.119 Unit</div>
                    <div style="font-size: 0.75rem; color: #39ff14; margin-top: 5px;">Hanya ~0,08% dari total armada nasional</div>
                </div>
            </div>
            <p style="font-size: 0.9rem; line-height: 1.5; color: #cbd5e1; margin-top: 10px;">
                Tantangan transisi energi di Indonesia bukan sekadar mendatangkan mobil listrik, melainkan bagaimana mengganti atau mengkonversi <b>172,9 juta kendaraan pembakaran internal (ICE)</b> yang saat ini mendominasi jalanan tanah air.
            </p>
        </div>
        
        <!-- Section 2: Market Dynamics -->
        <div style="margin-bottom: 30px;">
            <h3 style="color: #00f2fe; border-bottom: 1px solid rgba(0,242,254,0.3); padding-bottom: 5px; font-weight: 700; margin-bottom: 15px;">
                2. Lonjakan Pasar xEV (2024-2025)
            </h3>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px; font-size: 0.9rem; text-align: left;">
                <thead>
                    <tr style="border-bottom: 2px solid rgba(255,255,255,0.1); color: #94a3b8;">
                        <th style="padding: 10px 5px;">Kategori</th>
                        <th style="padding: 10px 5px;">Penjualan 2024</th>
                        <th style="padding: 10px 5px;">Penjualan 2025</th>
                        <th style="padding: 10px 5px; color: #39ff14;">Pertumbuhan</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <td style="padding: 10px 5px; font-weight: 600;">BEV (Listrik Murni)</td>
                        <td style="padding: 10px 5px;">43.188 unit</td>
                        <td style="padding: 10px 5px; font-weight: 700; color: #39ff14;">103.931 unit</td>
                        <td style="padding: 10px 5px; color: #39ff14; font-weight: bold;">+141%</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <td style="padding: 10px 5px; font-weight: 600;">HEV (Hybrid)</td>
                        <td style="padding: 10px 5px;">59.903 unit</td>
                        <td style="padding: 10px 5px;">65.943 unit</td>
                        <td style="padding: 10px 5px;">+10%</td>
                    </tr>
                    <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <td style="padding: 10px 5px; font-weight: 600;">PHEV (Plug-in Hybrid)</td>
                        <td style="padding: 10px 5px;">136 unit</td>
                        <td style="padding: 10px 5px;">5.270 unit</td>
                        <td style="padding: 10px 5px; color: #39ff14; font-weight: bold;">+3.775%</td>
                    </tr>
                </tbody>
            </table>
            <p style="font-size: 0.9rem; line-height: 1.5; color: #cbd5e1;">
                Tahun 2025 menjadi saksi peningkatan adopsi BEV secara drastis, berhasil melampaui pangsa pasar mobil Hybrid. Model terlaris didominasi oleh <b>BYD Atto 1</b> dan <b>Wuling BinguoEV</b> untuk segmen murni, sementara <b>Toyota Kijang Innova Zenix</b> memimpin segmen Hybrid dengan 61% pangsa pasar.
            </p>
        </div>
        
        <!-- Section 3: Infrastructure Bottleneck -->
        <div style="margin-bottom: 30px;">
            <h3 style="color: #00f2fe; border-bottom: 1px solid rgba(0,242,254,0.3); padding-bottom: 5px; font-weight: 700; margin-bottom: 15px;">
                3. Bottleneck Infrastruktur: Sentralisasi Jakarta
            </h3>
            <div style="display: flex; gap: 20px;">
                <div style="flex: 3; font-size: 0.9rem; line-height: 1.5; color: #cbd5e1;">
                    Berdasarkan sampling data spasial, ekosistem pengisian daya (SPKLU) masih <b>terkonsentrasi sangat padat di DKI Jakarta</b>, khususnya Jakarta Selatan dan Pusat. 
                    <br><br>
                    Hal ini memicu kekhawatiran jarak tempuh (*range anxiety*) bagi masyarakat di luar ibu kota. Penyediaan SPKLU didominasi oleh investasi swasta <b>Voltron (447 unit)</b> diikuti oleh BUMN <b>PLN (250 unit)</b>. Komposisi charger didominasi oleh tipe <i>Medium Charging</i> (38%), membutuhkan akselerasi ke tipe <i>Fast</i> & <i>Ultra Fast</i>.
                </div>
                <div style="flex: 2; background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; text-align: center; border: 1px solid rgba(255,255,255,0.05);">
                    <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 10px;">Teknologi Pengisian DKI Jakarta (Sample)</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #4facfe;">Medium: 551 unit</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #ff007f; margin: 5px 0;">Ultra Fast: 153 unit</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #39ff14;">Fast: 89 unit</div>
                </div>
            </div>
        </div>
        
        <!-- Section 4: The Paradox & Green Jobs -->
        <div style="margin-bottom: 30px;">
            <h3 style="color: #00f2fe; border-bottom: 1px solid rgba(0,242,254,0.3); padding-bottom: 5px; font-weight: 700; margin-bottom: 15px;">
                4. Kerja Hijau (Green Jobs) & Paradoks Energi
            </h3>
            <div style="display: flex; gap: 20px;">
                <div style="flex: 1; background: rgba(57, 255, 20, 0.02); padding: 15px; border-radius: 8px; border: 1px solid rgba(57, 255, 20, 0.1);">
                    <div style="font-weight: 700; color: #39ff14; font-size: 0.95rem; margin-bottom: 5px;">Peluang Kerja Hijau</div>
                    <ul style="margin: 0; padding-left: 15px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.4;">
                        <li>Target 500.000 lapangan kerja hijau baru pada 2030.</li>
                        <li>Kebutuhan insinyur baterai, teknisi tegangan tinggi, dan instalatur SPKLU.</li>
                        <li>Peralihan ekspor dari nikel mentah ke perakitan CKD lokal bernilai tinggi.</li>
                    </ul>
                </div>
                <div style="flex: 1; background: rgba(255, 0, 127, 0.02); padding: 15px; border-radius: 8px; border: 1px solid rgba(255, 0, 127, 0.1);">
                    <div style="font-weight: 700; color: #ff007f; font-size: 0.95rem; margin-bottom: 5px;">Paradoks & Tantangan</div>
                    <ul style="margin: 0; padding-left: 15px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.4;">
                        <li>Grid nasional masih disuplai >60% listrik berbasis batubara (PLTU).</li>
                        <li>Dampak lingkungan penambangan nikel terhadap ekosistem darat/laut lokal.</li>
                        <li>Skill gap: Jutaan mekanik otomotif konvensional terancam kehilangan kerja.</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <!-- Section 5: Recommendations -->
        <div style="background: rgba(0, 242, 254, 0.04); padding: 15px; border-radius: 8px; border: 1px solid rgba(0, 242, 254, 0.1); margin-bottom: 25px;">
            <h4 style="color: #00f2fe; margin: 0 0 8px 0; font-weight: 700; font-size: 0.95rem;">💡 Solusi & Rekomendasi Aplikatif:</h4>
            <ol style="margin: 0; padding-left: 18px; font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
                <li><b>Akselerasi Dekarbonisasi Grid:</b> Meningkatkan porsi EBT pada sistem kelistrikan nasional agar pengisian daya EV tidak memindahkan emisi ke batubara.</li>
                <li><b>Pemerataan SPKLU Koridor Antar-Kota:</b> Fokus pada pembangunan fast charger di jalur Trans-Jawa, Trans-Sumatera, dan pusat transportasi luar Jakarta.</li>
                <li><b>Program Reskilling Nasional:</b> Meluncurkan program sertifikasi teknisi EV nasional untuk mekanik konvensional guna mewujudkan transisi yang adil.</li>
            </ol>
        </div>
        
        <!-- Poster Footer -->
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px; font-size: 0.75rem; color: #64748b;">
            <div>
                Data diolah dari: ESDM, Gaikindo, BPS, Google Trends (Akses Juni 2026)
            </div>
            <div style="text-align: right;">
                Dibuat oleh: <b>Zaky Muhammad Fauzi & Brama Hartoyo</b><br>
                DS-48-03 S1 Sains Data, School of Computing, Telkom University
            </div>
        </div>
        
    </div>
    """, unsafe_allow_html=True)
