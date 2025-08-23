def penjelasan_fiqh_waris(entitas):
    if not entitas:
        return 

    entitas = {k: v for k, v in entitas.items() if v != 0}

    jenis_pewaris = ""  # fallback default
    if 'suami' not in entitas:
        jenis_pewaris = "seorang suami"

    if 'istri' not in entitas:
        jenis_pewaris = "seorang istri"

    # --- Ambil AHLI WARIS dari entitas
    ahli_waris = []
    daftar_bagian = []
    penjelasan = []

    if 'istri' in entitas and 'anak' in entitas:
        ahli_waris.append(f"{entitas['istri']} istri")
        daftar_bagian.append("istri mendapat 1/8 dari harta")
        penjelasan.append("jika pewaris memiliki anak, maka istri mendapat 1/8 bagian harta")

    if 'istri' in entitas and 'anak' not in entitas:
        ahli_waris.append(f"{entitas['istri']} istri")
        daftar_bagian.append("istri mendapat 1/4 dari harta")
        penjelasan.append("jika pewaris tidak memiliki anak, maka istri mendapat 1/4 bagian harta")
    
    if 'suami' in entitas and 'anak' in entitas:
        ahli_waris.append("seorang suami")
        daftar_bagian.append("suami mendapat 1/4 dari harta")
        penjelasan.append("jika pewaris memiliki anak, maka suami mendapat 1/4 bagian harta")

    if 'suami' in entitas and 'anak' not in entitas:
        ahli_waris.append("seorang suami")
        daftar_bagian.append("suami mendapat 1/2 dari harta")
        penjelasan.append("jika pewaris tidak memiliki anak, maka suami mendapat 1/2 bagian harta")

    if 'ayah' in entitas and 'anak_laki-laki' in entitas and 'anak_perempuan' in entitas:
        ahli_waris.append("seorang ayah")
        daftar_bagian.append("ayah mendapat 1/6 dari harta")
        penjelasan.append("Ayah dari pewaris mendapat 1/6 bagian harta karena pewaris memiliki anak laki-laki")

    if 'ayah' in entitas and 'anak_laki-laki' in entitas and 'anak_perempuan' not in entitas:
        ahli_waris.append("seorang ayah")
        daftar_bagian.append("ayah mendapat 1/6 dari harta")
        penjelasan.append("Ayah dari pewaris mendapat 1/6 bagian harta karena pewaris memiliki anak laki-laki")
    
    if 'ayah' in entitas and 'anak_perempuan' in entitas and 'anak_laki-laki' not in entitas:
        ahli_waris.append("seorang ayah")
        daftar_bagian.append("ayah mendapat 1/6 dan sisa (ashabah) dari harta")
        penjelasan.append("Ayah dari pewaris mendapat 1/6 bagian harta dan ashabah karena pewaris memiliki anak perempuan")
    
    if 'kakek' in entitas and 'anak_laki-laki' in entitas:
        ahli_waris.append("seorang kakek")
        daftar_bagian.append("kakek mendapat 1/6 dari harta")
        penjelasan.append("Kakek dari pewaris mendapat 1/6 bagian harta karena pewaris memiliki anak laki-laki")

    if 'kakek' in entitas and 'anak_perempuan' in entitas:
        ahli_waris.append("seorang kakek")
        daftar_bagian.append("kakek mendapat 1/6 dan sisa (ashabah) dari harta")
        penjelasan.append("Kakek dari pewaris jalur ayah mendapat 1/6 bagian harta dan ashabah karena pewaris memiliki anak perempuan")

    if 'kakek' in entitas and "anak_perempuan" not in entitas and "anak_laki-laki" not in entitas:
        ahli_waris.append("seorang kakek")
        daftar_bagian.append("kakek mendapat ashabah (sisa) dari harta")
        penjelasan.append("Kakek dari pewaris jalur ayah mendapat bagian ashabah (sisa) karena tidak adanya ahli waris lainnya")

    # if 'ibu' in entitas and 'anak_perempuan' in entitas:
    #     ahli_waris.append("seorang ibu")
    #     daftar_bagian.append("ibu mendapat 1/6 dari harta")
    #     penjelasan.append("Ibu dari pewaris mendapat 1/6 bagian harta karena pewaris memiliki anak")

    if 'ibu' in entitas and 'anak_perempuan' in entitas and 'anak_laki-laki' in entitas:
        ahli_waris.append("seorang ibu")
        daftar_bagian.append("ibu mendapat 1/6 dari harta")
        penjelasan.append("Ibu dari pewaris mendapat 1/6 bagian harta karena pewaris memiliki anak")

    if 'nenek' in entitas and 'ayah' not in entitas and 'ibu' not in entitas:
        ahli_waris.append("seorang nenek")
        daftar_bagian.append('nenek mendapat 1/6 dari harta')
        penjelasan.append('Nenek dari pewaris mendapat 1/6 bagian harta karena sudah tidak ayah atau ibu dari pewaris')
    
    if 'anak_laki-laki' in entitas and "anak_perempuan" in entitas:
        jumlah_anak_laki = entitas['anak_laki-laki']
        jumlah_anak_perempuan = entitas['anak_perempuan']

        ahli_waris.append(f"{jumlah_anak_laki} anak laki-laki")
        ahli_waris.append(f"{jumlah_anak_perempuan} anak perempuan")

        daftar_bagian.append("anak laki-laki dan perempuan mendapat sisa harta sebagai Ashabah bil Ghair")
        penjelasan.append("Anak perempuan menjadi Ashabah bil Ghair dikarenakan kehadiran anak laki-laki")

    if 'anak_laki-laki' in entitas and 'anak_perempuan' not in entitas:
        jumlah_anak_laki = entitas['anak_laki-laki']

        ahli_waris.append(f"{jumlah_anak_laki} anak laki-laki")

        daftar_bagian.append("anak laki-laki mendapat sisa harta sebagai Ashabah Binafsi")
        penjelasan.append("Anak laki-laki mendapat semua sisa harta karena merupakan Ashabah Binafsi, yakni mendapat bagian waris dengan sendirinya")

    if 'anak_perempuan' in entitas and 'anak_laki-laki' not in entitas:
        jumlah = int(entitas['anak_perempuan'])

        if jumlah == 1:
            ahli_waris.append(f"{jumlah} anak perempuan")
            daftar_bagian.append("anak perempuan mendapat bagian 1/2")
            penjelasan.append("Anak perempuan mendapat bagian 1/2 karena sendiri")
        elif jumlah > 1:
            ahli_waris.append(f"{jumlah} anak perempuan")
            daftar_bagian.append("anak perempuan mendapat bagian 2/3")
            penjelasan.append("Anak perempuan mendapat bagian 2/3 karena lebih dari satu orang")
        

    if not ahli_waris:
        return "Tidak ditemukan ahli waris yang dapat dijelaskan. Mohon lengkapi informasi."

    # --- Format harta
    harta = entitas.get('harta', 0)
    hutang = entitas.get('hutang', 0)

    # Hitung sisa harta setelah dikurangi hutang
    sisa_harta = harta - hutang

    if sisa_harta:
        if sisa_harta >= 1_000_000_000:
            harta_float = sisa_harta / 1_000_000_000
            harta_str = f"{harta_float:.2f}".rstrip('0').rstrip('.').replace('.', ',') + " miliar"
        else:
            harta_float = sisa_harta / 1_000_000
            harta_str = f"{harta_float:.2f}".rstrip('0').rstrip('.').replace('.', ',') + " juta"

        if harta and hutang:
            harta_teks = f" dari total harta yang sudah dikurangi hutang sebesar {harta_str}"
        elif harta:
            harta_teks = f" dari total harta sebesar {harta_str}"
    else:
        harta_teks = ""

    # --- Gabungkan jawaban
    ahli_waris_str = ", ".join(ahli_waris)
    bagian_str = "; ".join(daftar_bagian)
    penjelasan_str = ". ".join(penjelasan)

    return (
        f"Berdasarkan hukum waris Islam, apabila {jenis_pewaris} meninggal dunia dan meninggalkan {ahli_waris_str}, "
        f"maka {bagian_str}{harta_teks}. Hal ini sesuai dengan ketentuan di dalam Al-Quran dan Hadits, {penjelasan_str}. Berikut ini ialah hasil pembagian warisnya \n"
    )