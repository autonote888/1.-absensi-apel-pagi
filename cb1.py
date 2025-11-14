import streamlit as st
import pandas as pd
from datetime import datetime

# --- SET PAGE CONFIG ---
st.set_page_config(
    page_title="Rekap Absensi Apel Pagi untuk danton",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.streamlit.io/help',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "# aplikasi danton apel pagi."
    }
)

# --- CUSTOM CSS FOR MODERN LOOK ---
st.markdown("""
    <style>
    .main-header {
        font-size: 3.5em;
        font-weight: bold;
        color: #4CAF50; /* Green */
        text-align: center;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1.2em;
        border: none;
        transition: all 0.3s ease-in-out;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 3px 3px 8px rgba(0,0,0,0.3);
    }
    /* Mengubah tampilan input field */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px;
        box-shadow: inset 1px 1px 3px rgba(0,0,0,0.1);
    }
    /* Pastikan kolom Detail Nama di DataFrame terlihat luas */
    .dataframe th:nth-child(3), .dataframe td:nth-child(3) {
        width: 60%;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("<h1 class='main-header'>Absensi Apel Pagi</h1>", unsafe_allow_html=True)
st.markdown("---")

st.subheader("Input Data Kehadiran")

# ===== INPUT ANGKA =====
jumlah_personel_input = st.number_input("Total Jumlah Personel", min_value=0, step=1, value=None, help="Masukkan total personel yang seharusnya hadir.")
jumlah_personel = jumlah_personel_input if jumlah_personel_input is not None else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    hadir_input = st.number_input("Hadir", min_value=0, max_value=jumlah_personel, step=1, value=None)
with col2:
    sakit_input = st.number_input("Sakit", min_value=0, max_value=jumlah_personel, step=1, value=None)
with col3:
    izin_input = st.number_input("Izin", min_value=0, max_value=jumlah_personel, step=1, value=None)
with col4:
    dinas_input = st.number_input("Dinas / Tugas Luar", min_value=0, max_value=jumlah_personel, step=1, value=None)

hadir = hadir_input if hadir_input is not None else 0
sakit = sakit_input if sakit_input is not None else 0
izin = izin_input if izin_input is not None else 0
dinas = dinas_input if dinas_input is not None else 0

# Hitung Tanpa Kehadiran (Alpha)
tanpa_kehadiran = jumlah_personel - (hadir + sakit + izin + dinas)

if tanpa_kehadiran < 0:
    st.error("❗ Total jumlah kehadiran melebihi jumlah personel yang terdaftar.")
elif tanpa_kehadiran == 0 and jumlah_personel > 0:
    st.success("Semua personel terisi!")
else:
    st.info(f"Personel Tanpa Keterangan (Alpha): **{tanpa_kehadiran}**")

st.markdown("---")

st.subheader("👥 Detail Personel dengan Keterangan")
st.caption("Mohon masukkan nama-nama personel dalam satu baris, **dipisahkan dengan tanda koma** (contoh: Budi, Siti, Agus).")

# ===== INPUT NAMA-NAMA (Menggunakan Koma sebagai Pemisah) =====
nama_sakit = st.text_area("Nama Personel Sakit", placeholder="Contoh: Budi, Siti, Agus", height=100)
nama_izin = st.text_area("Nama Personel Izin", placeholder="Contoh: Joko, Rina, Toni", height=100)
nama_dinas = st.text_area("Nama Personel Dinas / Tugas Luar", placeholder="Contoh: Fajar, Clara, Dedi", height=100)

# Konversi ke list (MENGGUNAKAN PEMISAH KOMA)
list_sakit = [n.strip() for n in nama_sakit.split(",") if n.strip()]
list_izin = [n.strip() for n in nama_izin.split(",") if n.strip()]
list_dinas = [n.strip() for n in nama_dinas.split(",") if n.strip()]

tanggal = st.date_input("Tanggal Apel", datetime.now().date(), help="Pilih tanggal apel pagi ini.")

st.markdown("---")

# ===== TOMBOL PROSES =====
if st.button("Generate Laporan Absensi"):
    # 1. Validasi angka kehadiran
    if (hadir + sakit + izin + dinas) > jumlah_personel:
         st.error("❗ Total angka kehadiran melebihi jumlah personel. Harap periksa kembali.")
    # 2. Validasi jumlah nama vs angka
    elif len(list_sakit) != sakit:
        st.error(f"⚠️ Jumlah nama Sakit ({len(list_sakit)}) tidak sesuai dengan angka Sakit yang diinput ({sakit}).")
    elif len(list_izin) != izin:
        st.error(f"⚠️ Jumlah nama Izin ({len(list_izin)}) tidak sesuai dengan angka Izin yang diinput ({izin}).")
    elif len(list_dinas) != dinas:
        st.error(f"⚠️ Jumlah nama Dinas ({len(list_dinas)}) tidak sesuai dengan angka Dinas yang diinput ({dinas}).")
    else:
        st.success("✅ Laporan Absensi Berhasil Dibuat!")

        # ----------------------------------------------------
        # PERUBAHAN UTAMA: Membuat kolom Detail Nama untuk tabel ringkasan
        # ----------------------------------------------------
        nama_hadir_str = "-"
        nama_total_str = "-"
        nama_alpha_str = "-"
        nama_sakit_str = ", ".join(list_sakit) if list_sakit else "-"
        nama_izin_str = ", ".join(list_izin) if list_izin else "-"
        nama_dinas_str = ", ".join(list_dinas) if list_dinas else "-"
        
        # Ringkasan Tabel dengan kolom Detail Nama
        laporan_data = {
            "Kategori": ["Total Personel", "Hadir", "Sakit", "Izin", "Dinas", "Tanpa Keterangan (Alpha)"],
            "Jumlah": [jumlah_personel, hadir, sakit, izin, dinas, tanpa_kehadiran],
            "Detail Nama": [nama_total_str, nama_hadir_str, nama_sakit_str, nama_izin_str, nama_dinas_str, nama_alpha_str] 
        }
        df_laporan = pd.DataFrame(laporan_data)

        st.subheader(f"Ringkasan Kehadiran Apel Tanggal {tanggal.strftime('%d %B %Y')}")
        # Menampilkan DataFrame baru
        st.dataframe(df_laporan.set_index("Kategori")) 

        st.markdown("---")

        # ----------------------------------------------------
        # MENGHAPUS BAGIAN DAFTAR NAMA TERPISAH (KARENA SUDAH DI TABEL)
        # ----------------------------------------------------
        
        # Simpan CSV (tetap dibuat detail agar mudah diolah)
        all_names = []
        for name in list_sakit:
            all_names.append({"Kategori": "Sakit", "Nama": name})
        for name in list_izin:
            all_names.append({"Kategori": "Izin", "Nama": name})
        for name in list_dinas:
            all_names.append({"Kategori": "Dinas", "Nama": name})

        df_nama_detail = pd.DataFrame(all_names)
        
        if not df_nama_detail.empty:
            csv = df_nama_detail.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Detail Daftar Nama (CSV)",
                data=csv,
                file_name=f"detail_absensi_{tanggal.strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Tidak ada data nama yang perlu diunduh.")

st.markdown("---")
st.caption("Ditenagai oleh Streamlit | Absensi Apel Pagi v1.4")
