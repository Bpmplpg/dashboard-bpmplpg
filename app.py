"""
========================================================================================
BPMP PROVINSI LAMPUNG - QUALITY INTELLIGENCE DASHBOARD (v4 Operasional)
Aplikasi Analisis & Pemantauan Mutu Pendidikan (8 Standar Nasional Pendidikan / SPMI)
========================================================================================
Framework: Streamlit, Pandas, Plotly
File Sumber: BPMP_Lampung_Quality_Intelligence_Dashboard_v4_Operasional.xlsx
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN STREAMLIT
# --------------------------------------------------------------------------------------
st.set_page_config(
    page_title="BPMP Lampung - Quality Intelligence Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan elegan, modern, dan profesional
st.markdown("""
<style>
    /* Styling Header dan Font */
    .main-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 0.95rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-val {
        font-size: 2rem;
        font-weight: 700;
        color: #0F172A;
    }
    .metric-lbl {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 500;
    }
    .badge-high {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-medium {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-low {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    /* Sembunyikan footer streamlit */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# 2. FUNGSI PEMUATAN DATA EXCEL
# --------------------------------------------------------------------------------------
FILE_NAME = "BPMP_Lampung_Quality_Intelligence_Dashboard_v4_Operasional.xlsx"

STANDAR_COLS = [
    "Standar Kompetensi Lulusan",
    "Standar Isi",
    "Standar Proses",
    "Standar Penilaian",
    "Standar Sarana Prasarana",
    "Standar Pembiayaan",
    "Standar PTK",
    "Standar Pengelolaan"
]

@st.cache_data(show_spinner=True)
def load_data(file_source):
    """
    Membaca 4 sheet wajib dari file Excel BPMP Lampung:
    1. DISTRICT
    2. HEATMAP_STANDAR
    3. SCHOOL_PROFILE
    4. SEKOLAH_PRIORITAS
    """
    try:
        excel_file = pd.ExcelFile(file_source)
        df_district = pd.read_excel(excel_file, sheet_name="DISTRICT")
        df_heatmap = pd.read_excel(excel_file, sheet_name="HEATMAP_STANDAR")
        df_school = pd.read_excel(excel_file, sheet_name="SCHOOL_PROFILE")
        df_priority = pd.read_excel(excel_file, sheet_name="SEKOLAH_PRIORITAS")
        return df_district, df_heatmap, df_school, df_priority, None
    except Exception as e:
        return None, None, None, None, str(e)


# --------------------------------------------------------------------------------------
# 3. SIDEBAR NAVIGASI & SUMBER FILE
# --------------------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/9c/Logo_of_Ministry_of_Education_and_Culture_of_Republic_of_Indonesia.svg", width=64)
    st.markdown("### **BPMP Provinsi Lampung**")
    st.caption("Balai Penjaminan Mutu Pendidikan\nKemendikdasmen Republik Indonesia")
    st.markdown("---")

    menu = st.radio(
        "Navigasi Modul",
        ["📊 Ringkasan Provinsi", "🔍 Profil Sekolah", "⚠️ Sekolah Prioritas"],
        index=0
    )

    st.markdown("---")
    st.markdown("#### **Status Data Sumber**")

    # Cek ketersediaan file lokal
    local_file_exists = os.path.exists(FILE_NAME)
    uploaded_file = None

    if local_file_exists:
        st.success(f"File lokal terdeteksi:\n`{FILE_NAME}`")
        file_to_load = FILE_NAME
    else:
        st.warning(f"File `{FILE_NAME}` tidak ditemukan di direktori saat ini.")
        uploaded_file = st.file_uploader("Unggah file Excel di sini:", type=["xlsx", "xls"])
        file_to_load = uploaded_file

    st.markdown("---")
    st.caption("v4.0 Operasional BPMP Lampung\n© 2025/2026 BPMP Lampung")

# --------------------------------------------------------------------------------------
# 4. KONDISI JIKA DATA BELUM TERSEDIA
# --------------------------------------------------------------------------------------
if file_to_load is None:
    st.info("👋 **Selamat Datang di Quality Intelligence Dashboard BPMP Lampung!**")
    st.write(f"""
    Silakan letakkan file **`{FILE_NAME}`** di dalam folder yang sama dengan file `app.py`, 
    atau gunakan tombol unggah file di bilah navigasi kiri (sidebar).
    
    **Pastikan sheet yang tersedia adalah:**
    1. `DISTRICT`
    2. `HEATMAP_STANDAR`
    3. `SCHOOL_PROFILE`
    4. `SEKOLAH_PRIORITAS`
    """)
    st.stop()

# Load Data
df_district, df_heatmap, df_school, df_priority, err = load_data(file_to_load)

if err:
    st.error(f"Gagal membaca data dari file Excel. Error: {err}")
    st.stop()

# --------------------------------------------------------------------------------------
# 5. HALAMAN 1: RINGKASAN PROVINSI
# --------------------------------------------------------------------------------------
if menu == "📊 Ringkasan Provinsi":
    st.markdown('<div class="main-title">🏛️ Ringkasan Mutu Pendidikan Provinsi Lampung</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Pemantauan Agregat Capaian Standar Nasional Pendidikan (SNP) dan Pemetaan Risiko per Kabupaten/Kota</div>', unsafe_allow_html=True)

    # 1. Metrik Utama
    total_sekolah = int(df_district["Jumlah Sekolah"].sum()) if "Jumlah Sekolah" in df_district.columns else len(df_school)
    
    # Rata-rata SNP terbobot atau rerata
    if "Rata-rata SNP" in df_district.columns and "Jumlah Sekolah" in df_district.columns:
        prov_snp_avg = (df_district["Rata-rata SNP"] * df_district["Jumlah Sekolah"]).sum() / total_sekolah
    else:
        prov_snp_avg = df_school["SNP"].mean() if "SNP" in df_school.columns else 0

    total_risk_tinggi = int(df_district["Risk Tinggi"].sum()) if "Risk Tinggi" in df_district.columns else 0
    total_risk_sedang = int(df_district["Risk Sedang"].sum()) if "Risk Sedang" in df_district.columns else 0
    total_risk_rendah = int(df_district["Risk Rendah"].sum()) if "Risk Rendah" in df_district.columns else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">TOTAL SEKOLAH</div>
            <div class="metric-val">{total_sekolah:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">RATA-RATA SNP PROVINSI</div>
            <div class="metric-val" style="color:#2563EB;">{prov_snp_avg:.2f} <span style="font-size:1rem;color:#64748B;">/ 100</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">RISIKO TINGGI (INTERVENSI)</div>
            <div class="metric-val" style="color:#DC2626;">{total_risk_tinggi:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">RISIKO SEDANG</div>
            <div class="metric-val" style="color:#D97706;">{total_risk_sedang:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-lbl">RISIKO RENDAH (MANDIRI)</div>
            <div class="metric-val" style="color:#16A34A;">{total_risk_rendah:,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # 2. Grafik Bar Rata-rata SNP per Kabupaten/Kota
    st.subheader("📈 Perbandingan Capaian Rata-Rata SNP per Kabupaten/Kota")
    df_sorted = df_district.sort_values(by="Rata-rata SNP", ascending=True)

    fig_bar = px.bar(
        df_sorted,
        x="Rata-rata SNP",
        y="Kabupaten/Kota",
        orientation="h",
        text="Rata-rata SNP",
        color="Rata-rata SNP",
        color_continuous_scale="Teal",
        title="Peringkat Rata-rata Nilai SNP per Kabupaten/Kota se-Provinsi Lampung"
    )
    fig_bar.add_vline(x=prov_snp_avg, line_dash="dash", line_color="red", 
                      annotation_text=f"Rerata Provinsi ({prov_snp_avg:.2f})", annotation_position="top right")
    fig_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_bar.update_layout(
        height=520,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Nilai Rata-rata SNP",
        yaxis_title="",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.write("")

    # 3. Heatmap 8 Standar Nasional Pendidikan
    st.subheader("🗺️ Heatmap Capaian 8 Standar Nasional Pendidikan per Kabupaten/Kota")
    st.caption("Visualisasi pemetaan kekuatan dan kelemahan tiap standar pendidikan di masing-masing wilayah kabupaten/kota.")

    # Filter kolom standar yang ada di df_heatmap
    available_standards = [col for col in STANDAR_COLS if col in df_heatmap.columns]

    if "Kabupaten/Kota" in df_heatmap.columns and available_standards:
        heatmap_matrix = df_heatmap.set_index("Kabupaten/Kota")[available_standards]

        fig_heatmap = px.imshow(
            heatmap_matrix,
            labels=dict(x="Standar Nasional Pendidikan", y="Kabupaten/Kota", color="Nilai"),
            x=available_standards,
            y=heatmap_matrix.index,
            color_continuous_scale="RdYlGn",
            text_auto=".1f",
            aspect="auto"
        )
        fig_heatmap.update_layout(
            height=600,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_tickangle=-30
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.warning("Struktur kolom pada sheet 'HEATMAP_STANDAR' tidak sesuai spesifikasi.")


# --------------------------------------------------------------------------------------
# 6. HALAMAN 2: PROFIL SEKOLAH & RADAR CHART
# --------------------------------------------------------------------------------------
elif menu == "🔍 Profil Sekolah":
    st.markdown('<div class="main-title">🔍 Pencarian & Analisis Profil Mutu Sekolah</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Eksplorasi mendalam capaian 8 Standar Nasional Pendidikan (SNP) per satuan pendidikan</div>', unsafe_allow_html=True)

    # 1. Pilihan / Pencarian Sekolah
    # Gabungkan NPSN dan Nama Sekolah untuk opsi dropdown / pencarian
    df_school["search_label"] = df_school["NPSN"].astype(str) + " - " + df_school["Nama Sekolah"].astype(str)
    
    col_search1, col_search2 = st.columns([3, 1])
    with col_search1:
        selected_label = st.selectbox(
            "Cari atau Pilih Sekolah (Ketik NPSN atau Nama Sekolah):",
            options=df_school["search_label"].tolist(),
            index=0
        )
    with col_search2:
        if "Kabupaten/Kota" in df_school.columns:
            list_kab = ["Semua"] + sorted(df_school["Kabupaten/Kota"].dropna().unique().tolist())
            filter_kab = st.selectbox("Filter Kab/Kota (Opsional):", list_kab, index=0)
            if filter_kab != "Semua":
                filtered_labels = df_school[df_school["Kabupaten/Kota"] == filter_kab]["search_label"].tolist()
                if filtered_labels and selected_label not in filtered_labels:
                    selected_label = filtered_labels[0]

    # Ambil baris data sekolah terpilih
    selected_school = df_school[df_school["search_label"] == selected_label].iloc[0]

    st.write("")
    
    # 2. Kartu Identitas & Metrik Utama Sekolah
    col_info, col_kpi = st.columns([1.8, 1.2])

    with col_info:
        st.markdown(f"""
        <div style="background-color: white; color: black; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
            <div style="font-size: 1.4rem; font-weight: 700; color: #1E3A8A;">{selected_school.get('Nama Sekolah', '-')}</div>
            <div style="font-size: 0.95rem; color: #64748B; margin-bottom: 12px;">NPSN: <b>{selected_school.get('NPSN', '-')}</b> | Bentuk: <b>{selected_school.get('Jenjang', '-')}</b> | Status: <b>{selected_school.get('Status', '-')}</b></div>
            <hr style="margin: 10px 0; border: none; border-top: 1px solid #F1F5F9;">
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; font-size: 0.9rem; color: black;">
                <div>📍 <b>Kabupaten/Kota:</b> {selected_school.get('Kabupaten/Kota', '-')}</div>
                <div>🏢 <b>Kecamatan:</b> {selected_school.get('Kecamatan', '-')}</div>
                <div>🎖️ <b>Akreditasi:</b> {selected_school.get('Akreditasi', '-')}</div>
                <div>👥 <b>Peserta Didik:</b> {selected_school.get('Peserta Didik', '-')} Siswa</div>
                <div>👨‍🏫 <b>Guru:</b> {selected_school.get('Guru', '-')} Orang</div>
                <div>🚪 <b>Ruang Kelas:</b> {selected_school.get('Ruang Kelas', '-')} Rombel: {selected_school.get('Rombel', '-')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_kpi:
        risk_lvl = str(selected_school.get("Risk Level", "Sedang")).upper()
        if "TINGGI" in risk_lvl:
            badge_html = '<span class="badge-high">⚠️ RISIKO TINGGI</span>'
        elif "RENDAH" in risk_lvl:
            badge_html = '<span class="badge-low">✅ RISIKO RENDAH</span>'
        else:
            badge_html = '<span class="badge-medium">⚡ RISIKO SEDANG</span>'

        st.markdown(f"""
        <div style="background-color: white; color: black; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
            <div style="font-size: 0.85rem; color: #64748B; font-weight:600;">CAPAIAN SNP & STATUS RISIKO</div>
            <div style="display: flex; align-items: baseline; gap: 12px; margin-top: 4px;">
                <div style="font-size: 2.3rem; font-weight: 800; color: #1E3A8A;">{selected_school.get('SNP', 0):.2f}</div>
                <div>{badge_html}</div>
            </div>
            <div style="margin-top: 12px; font-size: 0.9rem;">
                <div>🎯 <b>Standar Terendah:</b> <span style="color:#DC2626; font-weight:600;">{selected_school.get('Standar Terendah', '-')}</span></div>
                <div>⚠️ <b>Jumlah Standar &lt; 60:</b> <b>{selected_school.get('Jumlah Standar <60', 0)}</b> standar</div>
                <div>💡 <b>Fokus Awal:</b> {selected_school.get('Fokus Awal', '-')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 3. Visualisasi Spider / Radar Chart 8 Standar Nasional Pendidikan
    st.subheader("🕸️ Radar Capaian 8 Standar Nasional Pendidikan")
    st.caption("Visualisasi perbandingan antara nilai satuan pendidikan dengan nilai rata-rata provinsi Lampung.")

    available_radar = [col for col in STANDAR_COLS if col in selected_school.index]
    
    if available_radar:
        school_values = [float(selected_school[std]) for std in available_radar]
        # Benchmark provinsi
        benchmark_values = [float(df_heatmap[std].mean()) if std in df_heatmap.columns else 70.0 for std in available_radar]

        # Menutup loop radar chart
        radar_categories = available_radar + [available_radar[0]]
        school_values_closed = school_values + [school_values[0]]
        benchmark_values_closed = benchmark_values + [benchmark_values[0]]

        fig_radar = go.Figure()

        # Garis Rata-Rata Provinsi
        fig_radar.add_trace(go.Scatterpolar(
            r=benchmark_values_closed,
            theta=radar_categories,
            fill='toself',
            fillcolor='rgba(148, 163, 184, 0.15)',
            line=dict(color='#94A3B8', width=2, dash='dot'),
            name='Rata-rata Provinsi Lampung'
        ))

        # Garis Capaian Sekolah
        fig_radar.add_trace(go.Scatterpolar(
            r=school_values_closed,
            theta=radar_categories,
            fill='toself',
            fillcolor='rgba(37, 99, 235, 0.25)',
            line=dict(color='#2563EB', width=3),
            name=str(selected_school.get('Nama Sekolah', 'Sekolah'))
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10)
                )
            ),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            height=540,
            margin=dict(l=40, r=40, t=30, b=40)
        )

        col_radar, col_detail = st.columns([1.8, 1.2])
        with col_radar:
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_detail:
            st.markdown("#### Detail Nilai 8 Standar")
            df_std_breakdown = pd.DataFrame({
                "Standar Nasional Pendidikan": available_radar,
                "Nilai Sekolah": [f"{v:.1f}" for v in school_values],
                "Rerata Prov": [f"{b:.1f}" for b in benchmark_values]
            })
            st.dataframe(df_std_breakdown, use_container_width=True, hide_index=True)


# --------------------------------------------------------------------------------------
# 7. HALAMAN 3: SEKOLAH PRIORITAS (INTERVENSI)
# --------------------------------------------------------------------------------------
elif menu == "⚠️ Sekolah Prioritas":
    st.markdown('<div class="main-title">⚠️ Daftar Sekolah Prioritas Intervensi Mutu</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Identifikasi sekolah dengan skor risiko tinggi dan standar terendah yang membutuhkan pendampingan khusus BPMP Lampung</div>', unsafe_allow_html=True)

    # 1. Filter Interaktif
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        all_districts = ["Semua Kabupaten/Kota"] + sorted(df_priority["Kabupaten/Kota"].dropna().unique().tolist())
        selected_district = st.selectbox("Filter Kabupaten/Kota:", all_districts)

    with col_f2:
        if "Jenjang" in df_priority.columns:
            all_levels = ["Semua Jenjang"] + sorted(df_priority["Jenjang"].dropna().unique().tolist())
            selected_level = st.selectbox("Filter Jenjang:", all_levels)
        else:
            selected_level = "Semua Jenjang"

    with col_f3:
        if "Risk Level" in df_priority.columns:
            all_risks = ["Semua Tingkat Risiko"] + sorted(df_priority["Risk Level"].dropna().unique().tolist())
            selected_risk = st.selectbox("Filter Tingkat Risiko:", all_risks)
        else:
            selected_risk = "Semua Tingkat Risiko"

    # Aplikasi Filter
    df_filtered_priority = df_priority.copy()

    if selected_district != "Semua Kabupaten/Kota":
        df_filtered_priority = df_filtered_priority[df_filtered_priority["Kabupaten/Kota"] == selected_district]

    if selected_level != "Semua Jenjang" and "Jenjang" in df_filtered_priority.columns:
        df_filtered_priority = df_filtered_priority[df_filtered_priority["Jenjang"] == selected_level]

    if selected_risk != "Semua Tingkat Risiko" and "Risk Level" in df_filtered_priority.columns:
        df_filtered_priority = df_filtered_priority[df_filtered_priority["Risk Level"] == selected_risk]

    # Ringkasan Hasil Filter
    st.write(f"Menampilkan **{len(df_filtered_priority)}** sekolah prioritas dari total {len(df_priority)} sekolah.")

    # 2. Tabel Interaktif Dataframe
    display_cols = [
        "Prioritas", "NPSN", "Nama Sekolah", "Jenjang", "Kabupaten/Kota", 
        "Kecamatan", "SNP", "Risk Score", "Risk Level", 
        "Standar Terendah", "Nilai Terendah", "Jumlah Standar <60", "Rekomendasi"
    ]
    # Ambil kolom yang valid ada di dataframe
    valid_cols = [c for c in display_cols if c in df_filtered_priority.columns]

    st.dataframe(
        df_filtered_priority[valid_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Prioritas": st.column_config.NumberColumn("Prioritas #", format="%d"),
            "SNP": st.column_config.NumberColumn("Capaian SNP", format="%.2f"),
            "Risk Score": st.column_config.NumberColumn("Risk Score", format="%.1f"),
            "Nilai Terendah": st.column_config.NumberColumn("Nilai Terendah", format="%.1f"),
            "Jumlah Standar <60": st.column_config.NumberColumn("Standar <60", format="%d")
        }
    )

    # 3. Tombol Unduh Laporan
    st.write("")
    csv_data = df_filtered_priority.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Data Sekolah Prioritas (CSV)",
        data=csv_data,
        file_name="BPMP_Lampung_Sekolah_Prioritas_Intervensi.csv",
        mime="text/csv"
    )
