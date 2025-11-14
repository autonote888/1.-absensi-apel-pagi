import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Absensi Apel Pagi", layout="centered")

st.title("📋 SISTEM LAPORAN APEL PAGI (Dropdown Version)")
st.write("---")

# --- DAFTAR PERSONEL UNTUK DROPDOWN ---
daftar_personel = [
    "Aipda Joko", "Briptu Bagas", "Bripda Andi", "Ipda Satria",
    "Bripka Rudi", "Aiptu Wawan", "Briptu Bayu", "Bripda Seno",
    "Bripka Feri", "Aiptu Tama"
]

# --- INPUT ANGKA ---
jumlah_personel = st.number_input("Jumlah Personel", min_value=0, step=1)

hadir = st.number_input("Jumlah Hadir", min_value=0, max_value=jumlah_personel, step=1)
sakit = st.number_input("Jumlah Sakit", min_value=0, max_value=jumlah_personel, step=1)
izin = st.number_input("Jumlah Izin", min_value=0, max_value=jumlah_personel, step=1)
dinas = st.number_input("Jumlah Dinas / Tugas Luar", min_value=0, max_value=jumlah_personel, step=1)

tanpa_kehadiran = jumlah_personel - (hadir + sakit + izin + dinas)
st.info(f"Tanpa Kehadiran (Alpha): **{tanpa_kehadiran}**")

st.write("---")
st.write("### ✏️ Pilih Nama Personel (Dropdown)")

# --- DROPDOWN MULTISELECT ---
list_sakit = st.multiselect("Personel Sakit", daftar_personel)
list_izin = st.multiselect("Personel Izin", daftar_personel)
list_dinas = st.multiselect("Personel Dinas / Tugas Luar", daftar_personel)

tanggal = st.date_input("Tanggal Apel", datetime.now().date())

st.write("---")

# --- PROSES LAPORAN ---
if st.button("📄 Generate Laporan"):
    if len(list_sakit) != sakit:
        st.error("Jumlah nama Sakit tidak sesuai angka Sakit.")
    elif len(list_izin) != izin:
        st.error("Jumlah nama Izin tidak sesuai angka Izin.")
    elif len(list_dinas) != dinas:
        st.error("Jumlah nama Dinas tidak sesuai angka Dinas.")
    else:
        st.success("Laporan Absensi Berhasil Dibuat!")

        laporan = {
            "Tanggal": [tanggal.strftime("%d-%m-%Y")],
            "Jumlah Personel": [jumlah_personel],
            "Hadir": [hadir],
            "Sakit": [sakit],
            "Izin": [izin],
            "Dinas": [dinas],
            "Tanpa Kehadiran": [tanpa_kehadiran],
        }

        df = pd.DataFrame(laporan)
        st.table(df)

        st.subheader("📌 Daftar Nama Personel")

        st.write("### 🤒 Sakit")
        st.write(", ".join(list_sakit) if list_sakit else "-")

        st.write("### 📝 Izin")
        st.write(", ".join(list_izin) if list_izin else "-")

        st.write("### 🛫 Dinas / Tugas Luar")
        st.write(", ".join(list_dinas) if list_dinas else "-")

