# BPMP Provinsi Lampung - Quality Intelligence Dashboard (v4 Operasional)

Aplikasi Web Dashboard Interaktif untuk mempermudah pegawai BPMP Provinsi Lampung dalam mencari, memantau, dan menganalisis data mutu sekolah serta Capaian 8 Standar Nasional Pendidikan (SPMI) di seluruh Provinsi Lampung.

---

## 📁 Struktur Folder & File Proyek

```text
bpmp-lampung-dashboard/
│
├── BPMP_Lampung_Quality_Intelligence_Dashboard_v4_Operasional.xlsx   <-- File Excel Data Anda
├── app.py                                                           <-- Kode Aplikasi Utama Streamlit
├── requirements.txt                                                 <-- Daftar Library Python
└── README.md                                                        <-- Panduan ini
```

---

## 🚀 Panduan Step-by-Step Menjalankan di Localhost (VS Code)

### Langkah 1: Buka Terminal di VS Code

1. Buka folder proyek ini di **Visual Studio Code**.
2. Buka terminal baru dengan menekan shortcut `Ctrl + ~` (atau menu **Terminal** > **New Terminal**).

### Langkah 2: Buat Lingkungan Virtual (Opsional tapi Direkomendasikan)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Langkah 3: Install Library yang Dibutuhkan

Ketik perintah berikut lalu tekan Enter:

```bash

pip install -r requirements.txt
```

*Library yang terinstall: `streamlit`, `pandas`, `plotly`, `openpyxl`, `numpy`.*

### Langkah 4: Pastikan File Excel Sudah Berada di Satu Folder

Pastikan file bernama:
`BPMP_Lampung_Quality_Intelligence_Dashboard_v4_Operasional.xlsx`
sudah diletakkan di dalam folder yang sama dengan `app.py`.

### Langkah 5: Jalankan Aplikasi Streamlit

Jalankan perintah ini:

```bash
streamlit run app.py
```

Browser default Anda akan otomatis membuka alamat localhost:
👉 `http://localhost:8501`

---

## 📊 Struktur Sheet Excel yang Digunakan

1. **`DISTRICT`**: Agregasi data per kabupaten/kota (Jumlah Sekolah, Rata-rata SNP, Risk Tinggi/Sedang/Rendah, dll).
2. **`HEATMAP_STANDAR`**: Nilai rata-rata 8 Standar Nasional Pendidikan per Kabupaten/Kota.
3. **`SCHOOL_PROFILE`**: Profil detail sekolah (NPSN, Nama, Jenjang, Akreditasi, Nilai 8 Standar, Risk Level, dll).
4. **`SEKOLAH_PRIORITAS`**: Daftar sekolah yang memerlukan intervensi mutu dan pendampingan khusus BPMP Lampung.

---

## 🌟 Fitur Utama Dashboard

- **Ringkasan Provinsi**: KPI total sekolah & rata-rata SNP provinsi, Bar Chart peringkat Kab/Kota dengan garis batas rerata provinsi, dan Heatmap matriks 8 standar.
- **Pencarian Profil Sekolah**: Autocomplete pencarian berdasarkan NPSN atau nama sekolah, kartu profil komprehensif, KPI skor risiko, dan Grafik Radar (Spider Chart) 8 Standar vs Rerata Provinsi.
- **Sekolah Prioritas**: Tabel interaktif dengan filter wilayah kabupaten/kota, jenjang, dan tingkat risiko, disertai tombol ekspor CSV.
