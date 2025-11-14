import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Absensi Apel Pagi", layout="centered")

st.title("📋 SISTEM LAPORAN APEL PAGI")
st.write("---")

# ===== INPUT ANGKA =====
jumlah_personel = st.number_input("Jumlah Personel", min_value=0, step=1)

hadir = st.number_input("Jumlah Hadir", min_value=0, max_value=jumlah_personel, step=1)
sakit = st.number_input("Jumlah Sakit", min_value=0, max_value=jumlah_personel, step=1)
izin = st.number_input("Jumlah Izin", min_value=0, max_value=jumlah_personel, step=1)
dinas = st.number_input("Jumlah Dinas / Tugas Luar", min_value=0, max_value=jumlah_personel, step=1)

# Hitung Alpha
tanpa_kehadiran = jumlah_personel - (hadir + sakit + izin + dinas)

if tanpa_kehadiran < 0:
    st.error("❗ Total angka melebihi jumlah personel.")
else:
    st.info(f"Personel Tanpa Kehadiran (Alpha): **{tanpa_kehadiran}**")

st.write("### ✏️ Masukkan Nama Personel (hanya yang ada keterangannya)")
st.caption("Isi satu nama per baris.")

# ===== INPUT NAMA-NAMA =====
nama_sakit = st.text_area("Nama Personel Sakit", placeholder="Isi satu nama per baris")
nama_izin = st.text_area("Nama Personel Izin", placeholder="Isi satu nama per baris")
nama_dinas = st.text_area("Nama Personel Dinas / Tugas Luar", placeholder="Isi satu nama per baris")

# Konversi ke list
list_sakit = [n.strip() for n in nama_sakit.split("\n") if n.strip()]
list_izin = [n.strip() for n in nama_izin.split("\n") if n.strip()]
list_dinas = [n.strip() for n in nama_dinas.split("\n") if n.strip()]

tanggal = st.date_input("Tanggal Apel", datetime.now().date())

st.write("---")

# ===== TOMBOL PROSES =====
if st.button("📄 Generate Laporan"):
    # Validasi jumlah nama
    if len(list_sakit) != sakit:
        st.error("Jumlah nama Sakit tidak sesuai angka Sakit.")
    elif len(list_izin) != izin:
        st.error("Jumlah nama Izin tidak sesuai angka Izin.")
    elif len(list_dinas) != dinas:
        st.error("Jumlah nama Dinas tidak sesuai angka Dinas.")
    else:
        st.success("Laporan Absensi Berhasil Dibuat!")

        # Ringkasan Tabel
        laporan = {
            "Tanggal": [tanggal.strftime("%d-%m-%Y")],
            "Jumlah Personel": [jumlah_personel],
            "Hadir": [hadir],
            "Sakit": [sakit],
            "Izin": [izin],
            "Dinas": [dinas],
            "Tanpa Kehadiran": [tanpa_kehadiran]
        }

        df = pd.DataFrame(laporan)

        st.subheader("📊 Ringkasan Laporan Apel Pagi")
        st.table(df)

        # ===== Tampilkan Daftar Nama =====
        st.subheader("📌 Daftar Nama Personel")

        st.write("### 🤒 Sakit")
        st.write("\n".join(list_sakit) if list_sakit else "-")

        st.write("### 📝 Izin")
        st.write("\n".join(list_izin) if list_izin else "-")

        st.write("### 🛫 Dinas / Tugas Luar")
        st.write("\n".join(list_dinas) if list_dinas else "-")

        # Simpan CSV
        df_nama = pd.DataFrame({
            "Sakit": list_sakit,
            "Izin": list_izin,
            "Dinas": list_dinas
        })

        csv = df_nama.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Daftar Nama (CSV)",
            data=csv,
            file_name=f"daftar_keterangan_{tanggal}.csv",
            mime="text/csv"
        )

st.write("---")
st.caption("Sistem Absensi Apel Pagi — Streamlit Version")
