import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Absensi Apel Pagi", layout="centered")

st.title("📋 SISTEM LAPORAN APEL PAGI (INPUT MANUAL)")
st.write("---")

# ===== INPUT DATA =====
jumlah_personel = st.number_input("Jumlah Personel", min_value=0, step=1)
hadir = st.number_input("Jumlah Hadir", min_value=0, max_value=jumlah_personel, step=1)
sakit = st.number_input("Jumlah Sakit", min_value=0, max_value=jumlah_personel, step=1)
izin = st.number_input("Jumlah Izin", min_value=0, max_value=jumlah_personel, step=1)

# dihitung otomatis
tanpa_kehadiran = jumlah_personel - (hadir + sakit + izin)

if tanpa_kehadiran < 0:
    st.error("❗ Total Hadir + Sakit + Izin melebihi jumlah personel.")
else:
    st.info(f"Personel Tanpa Kehadiran: **{tanpa_kehadiran}**")

st.write("---")
tanggal = st.date_input("Tanggal Apel", datetime.now().date())

# ===== TOMBOL PROSES =====
if st.button("📄 Generate Laporan"):
    if jumlah_personel == 0:
        st.warning("Jumlah personel tidak boleh nol.")
    else:
        st.success("Laporan Absensi Berhasil Dibuat!")

        laporan = {
            "Tanggal": [tanggal.strftime("%d-%m-%Y")],
            "Jumlah Personel": [jumlah_personel],
            "Hadir": [hadir],
            "Sakit": [sakit],
            "Izin": [izin],
            "Tanpa Kehadiran": [tanpa_kehadiran]
        }

        df = pd.DataFrame(laporan)

        st.subheader("📊 Hasil Laporan Apel Pagi")
        st.table(df)

        # Simpan sebagai CSV untuk diunduh
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Laporan CSV",
            data=csv,
            file_name=f"laporan_apel_{tanggal}.csv",
            mime="text/csv"
        )

st.write("---")
st.caption("Sistem Absensi Apel Pagi — Streamlit Version")
