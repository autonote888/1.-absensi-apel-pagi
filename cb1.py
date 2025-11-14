def garis():
    print("-" * 50)

def main():
    garis()
    print("   SISTEM LAPORAN APEL PAGI (INPUT MANUAL)")
    garis()

    total_personel = int(input("Jumlah Personel       : "))
    hadir = int(input("Jumlah Hadir          : "))
    sakit = int(input("Jumlah Sakit          : "))
    izin = int(input("Jumlah Izin           : "))
    tanpa_ket = int(input("Tanpa Keterangan (TK) : "))

    # Kalkulasi otomatis
    total_tidak_hadir = sakit + izin + tanpa_ket
    selisih = total_personel - hadir

    garis()
    print("                 LAPORAN APEL PAGI")
    garis()
    print(f"Total Personel : {total_personel}")
    print(f"Hadir          : {hadir}")
    print(f"Tidak Hadir    : {total_tidak_hadir}")
    print(f"  - Sakit      : {sakit}")
    print(f"  - Izin       : {izin}")
    print(f"  - TK         : {tanpa_ket}")
    print(f"Selisih        : {selisih}")
    garis()

    # Catatan otomatis
    if selisih == total_tidak_hadir:
        print("STATUS: Valid ✔ Semua ketidakhadiran tercatat.")
    else:
        print("STATUS: ⚠ Data tidak sinkron. Periksa kembali input.")

    garis()


if __name__ == "__main__":
    main()
