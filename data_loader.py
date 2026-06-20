import pandas as pd
import numpy as np
import re
import os

DATA_DIR = "data"

def get_google_trends():
    path = os.path.join(DATA_DIR, "time_series_ID_20110620-0000_20260620-2213.csv")
    df = pd.read_csv(path)
    df['Time'] = pd.to_datetime(df['Time'])
    # Convert numeric columns
    for col in ["ev", "SPKLU", "kendaraan listrik", "Infrastruktur kendaraan listrik"]:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

def get_bps_provinsi_2025():
    path = os.path.join(DATA_DIR, "Jumlah Kendaraan Bermotor Menurut Provinsi dan Jenis Kendaraan (unit), 2025.csv")
    df = pd.read_csv(path)
    # Filter out footer rows/empty rows
    df = df.dropna(subset=['Provinsi'])
    df = df[df['Provinsi'].str.strip() != '']
    # Clean the numeric columns (remove ' (*)' and spaces)
    cols_to_clean = [
        "Jumlah Kendaraan Bermotor - Mobil Penumpang",
        "Jumlah Kendaraan Bermotor - Bus",
        "Jumlah Kendaraan Bermotor - Truk",
        "Jumlah Kendaraan Bermotor - Sepeda Motor",
        "Jumlah Kendaraan Bermotor - Jumlah"
    ]
    for col in cols_to_clean:
        df[col] = df[col].astype(str).str.replace(r'\(\*\)', '', regex=True)
        df[col] = df[col].str.replace(',', '', regex=True)
        df[col] = df[col].str.replace(' ', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Separate Indonesia total and provinces
    df_provinces = df[df['Provinsi'].str.strip() != 'Indonesia'].copy()
    df_total = df[df['Provinsi'].str.strip() == 'Indonesia'].copy()
    return df_provinces, df_total

def get_bps_nasional_2024():
    path = os.path.join(DATA_DIR, "Perkembangan Jumlah Kendaraan Bermotor Menurut Jenis, 2024.csv")
    # This file has a slightly weird format:
    # Row 1: Jenis Kendaraan Bermotor,
    # Row 2: ,Perkembangan Jumlah Kendaraan Bermotor Menurut Jenis (Unit)
    # Row 3: ,2024
    # Row 4: Mobil Penumpang,20444507
    # ...
    # We can load it manually
    df = pd.read_csv(path, header=None, skiprows=3)
    df.columns = ["Jenis", "Jumlah"]
    df = df.dropna()
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors='coerce').fillna(0).astype(int)
    return df

def get_spklu_targets():
    path = os.path.join(DATA_DIR, "Filedata Persentase Pembangunan Stasiun Pengisian Kendaraan Listrik.csv")
    df = pd.read_csv(path)
    return df

def get_spklu_list():
    path = os.path.join(DATA_DIR, "Filedata Data Stasiun Pengisian Kendaraan Listrik Umum SPKLU.csv")
    df = pd.read_csv(path)
    
    # Standardize Operator names
    def clean_operator(op):
        if not isinstance(op, str):
            return "LAINNYA"
        op = op.upper().strip()
        if "VOLTRON" in op or "STARVO" in op or "WULING" in op or "DAYAGREEN" in op or "TERRA CHARGE" in op or "BLUECHARGE" in op or "HVT" in op:
            # Note: Voltron is a major private operator, many brands use Voltron system
            if "VOLTRON" in op: return "VOLTRON"
            if "STARVO" in op: return "STARVO"
            if "TERRA" in op: return "TERRA CHARGE"
            if "BLUECHARGE" in op: return "BLUECHARGE"
            return op
        if "PLN" in op:
            return "PLN"
        if "TOYOTA" in op or "LEXUS" in op:
            return "TOYOTA-LEXUS"
        if "HYUNDAI" in op:
            return "HYUNDAI"
        if "INDOMOBIL" in op or "NISSAN" in op or "KIA" in op or "CITROEN" in op:
            return "INDOMOBIL GROUP"
        if "CHUNLAN" in op or "UCI" in op:
            return "CHUNLAN (UCI)"
        if "DIVINA" in op or "EVCITY" in op:
            return "EVCITY (ANUGERAH DIVINA)"
        if "HIGH VOLT" in op:
            return "HIGH VOLT TECHNOLOGY"
        return op
        
    df['clean_operator'] = df['owner_operator'].apply(clean_operator)
    
    # Extract Jakarta region and assign coordinates
    regions_coords = {
        "Jakarta Selatan": (-6.2615, 106.8106),
        "Jakarta Pusat": (-6.1865, 106.8270),
        "Jakarta Timur": (-6.2250, 106.9004),
        "Jakarta Barat": (-6.1683, 106.7588),
        "Jakarta Utara": (-6.1384, 106.8664),
        "Tangerang / Banten": (-6.1783, 106.6319),
        "Bekasi / Jawa Barat": (-6.2383, 106.9756),
        "Depok / Jawa Barat": (-6.4025, 106.7942),
        "Bogor / Jawa Barat": (-6.5971, 106.8060),
        "DKI Jakarta (Lainnya)": (-6.2000, 106.8200)
    }
    
    def extract_region(lokasi):
        if not isinstance(lokasi, str):
            return "DKI Jakarta (Lainnya)"
        lokasi = lokasi.upper()
        if "JAKARTA PUSAT" in lokasi or "JKT PUSAT" in lokasi:
            return "Jakarta Pusat"
        elif "JAKARTA UTARA" in lokasi or "JKT UTARA" in lokasi:
            return "Jakarta Utara"
        elif "JAKARTA BARAT" in lokasi or "JKT BARAT" in lokasi:
            return "Jakarta Barat"
        elif "JAKARTA SELATAN" in lokasi or "JKT SELATAN" in lokasi:
            return "Jakarta Selatan"
        elif "JAKARTA TIMUR" in lokasi or "JKT TIMUR" in lokasi:
            return "Jakarta Timur"
        elif "TANGERANG" in lokasi:
            return "Tangerang / Banten"
        elif "BEKASI" in lokasi:
            return "Bekasi / Jawa Barat"
        elif "DEPOK" in lokasi:
            return "Depok / Jawa Barat"
        elif "BOGOR" in lokasi:
            return "Bogor / Jawa Barat"
        else:
            return "DKI Jakarta (Lainnya)"
            
    df['region'] = df['lokasi'].apply(extract_region)
    
    # Assign coordinates with a small random jitter to make points spread out on the map
    lats = []
    lons = []
    np.random.seed(42)  # For reproducible jitter
    
    for reg in df['region']:
        base_lat, base_lon = regions_coords.get(reg, (-6.2000, 106.8200))
        # Add random jitter: ~2-3 km dispersion (approx 0.015 degrees)
        lat_jitter = base_lat + np.random.uniform(-0.025, 0.025)
        lon_jitter = base_lon + np.random.uniform(-0.025, 0.025)
        lats.append(lat_jitter)
        lons.append(lon_jitter)
        
    df['latitude'] = lats
    df['longitude'] = lons
    
    return df

def get_gaikindo_sales():
    """
    Returns Gaikindo electrified vehicle sales data compiled from 2024, 2025, and early 2026 reports.
    """
    # 1. Annual sales comparison
    annual_data = {
        "Tahun": ["2024", "2024", "2024", "2025", "2025", "2025"],
        "Kategori": ["BEV", "HEV", "PHEV", "BEV", "HEV", "PHEV"],
        "Penjualan": [43188, 59903, 136, 103931, 65943, 5270]
    }
    df_annual = pd.DataFrame(annual_data)
    
    # 2. Monthly sales 2026 (Jan-Apr)
    monthly_2026 = {
        "Bulan": ["Januari", "Februari", "Maret", "April"],
        "BEV": [10259, 12313, 10394, 14815],
        "HEV": [4522, 6078, 7322, 8414],
        "PHEV": [390, 663, 443, 593] # Combined from February report (663/651) and others
    }
    df_monthly_2026 = pd.DataFrame(monthly_2026)
    
    # 3. Brand data for 2026 (BEV, HEV, PHEV leaders)
    bev_brands = {
        "Brand": ["BYD", "Jaecoo", "Wuling", "Geely", "Lainnya"],
        "Penjualan": [17098, 11006, 8500, 4800, 6377] # Extrapolated from Jan-Apr 2026 report
    }
    df_bev_brands = pd.DataFrame(bev_brands)
    
    hev_brands = {
        "Brand": ["Toyota", "Suzuki", "Chery", "Hyundai", "Lainnya"],
        "Penjualan": [16181, 4527, 1261, 841, 3527]
    }
    df_hev_brands = pd.DataFrame(hev_brands)
    
    phev_brands = {
        "Brand": ["Chery", "Wuling", "Jaecoo", "Lainnya"],
        "Penjualan": [1179, 407, 266, 237]
    }
    df_phev_brands = pd.DataFrame(phev_brands)
    
    return df_annual, df_monthly_2026, df_bev_brands, df_hev_brands, df_phev_brands

if __name__ == '__main__':
    # Test loading
    trends = get_google_trends()
    provinces, total = get_bps_provinsi_2025()
    nasional_2024 = get_bps_nasional_2024()
    spklu_target = get_spklu_targets()
    spklu_list = get_spklu_list()
    df_ann, df_mon, df_bev, df_hev, df_phev = get_gaikindo_sales()
    
    print("Google trends shape:", trends.shape)
    print("BPS provinces shape:", provinces.shape)
    print("BPS nasional 2024 row count:", len(nasional_2024))
    print("SPKLU list shape:", spklu_list.shape)
    print("SPKLU targets row count:", len(spklu_target))
    print("Gaikindo annual shape:", df_ann.shape)
    print("Data Loader works fine!")
