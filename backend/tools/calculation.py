def hitung_pembagian_khusus(entitas):
    harta = entitas.get("harta", 0)
    hutang = entitas.get("hutang", 0)
    sisa_harta = harta - hutang

    hasil = {}

    suami = entitas.get("suami", 0)
    istri = entitas.get("istri", 0)
    anak_laki = entitas.get("anak_laki-laki", 0)
    anak_perempuan = entitas.get("anak_perempuan", 0)
    ayah = entitas.get("ayah", 0)
    ibu = entitas.get("ibu", 0)
    kakek = entitas.get("kakek", 0)
    nenek = entitas.get("nenek", 0)

    # Kondisi istri wafat meninggalkan suami
    if suami == 1:
        # Kondisi adanya suami, anak laki-laki dan perempuan, serta kedua orang tua pewaris (istri)
        if anak_laki >= 1 and anak_perempuan >= 1 and ayah == 1 and ibu == 1:
            # 1/4 + 1/6 + 1/6 = 3/12 + 2/12 + 2/12 = 7/12
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 12 * total_bagian # 12/12 - 7/12 = 5/12 = 12 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 5
            total_bagian_anak_perempuan = 1 * 5

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_suami = round((3 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)
            bagian_waris_ayah = round((2 * total_bagian) * bagian_waris)
            bagian_waris_ibu = round((2 * total_bagian) * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Suami"] = bagian_waris_suami
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan
            hasil["Ayah"] = bagian_waris_ayah
            hasil["Ibu"] = bagian_waris_ibu

            return hasil
        
        # Kondisi adanya suami, anak laki-laki dan perempuan, serta ibu dari pewaris (istri)
        if anak_laki >= 1 and anak_perempuan >= 1 and ibu == 1:
            # 1/4 + 1/6  = 3/12 +  2/12 = 5/12
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 12 * total_bagian # 12/12 - 5/12 = 7/12 = 12 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 7 # 7 diambil dari pembilang pecahan dan 2 diambil berdasarkan jumlah bagian waris anak
            total_bagian_anak_perempuan = 1 * 7

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_suami = round((3 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)
            bagian_waris_ibu = round((2 * total_bagian) * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Suami"] = bagian_waris_suami
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan
            hasil["Ibu"] = bagian_waris_ibu

            return hasil
        
        # Kondisi adanya suami, anak laki-laki dan perempuan, serta nenek dari pewaris (istri)
        if anak_laki >= 1 and anak_perempuan >= 1 and nenek == 1:
            # 1/4 + 1/6  = 3/12 +  2/12 = 5/12
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 12 * total_bagian # 12/12 - 5/12 = 7/12 = 12 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 7 # 7 diambil dari pembilang pecahan dan 2 diambil berdasarkan jumlah bagian waris anak
            total_bagian_anak_perempuan = 1 * 7

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_suami = round((3 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)
            bagian_waris_nenek = round((2 * total_bagian) * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Suami"] = bagian_waris_suami
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan
            hasil["Nenek"] = bagian_waris_nenek

            return hasil
        
        # Kondisi adanya suami, memiliki anak laki-laki dan perempuan, serta kakek dari jalur ayah pewaris (istri)
        if anak_laki >= 1 and anak_perempuan >= 1 and kakek == 1:
            # 1/4 + 1/6 = 3/12 + 2/12 = 5/12
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 12 * total_bagian # 12/12 - 5/12 = 7/12 = 12 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 7
            total_bagian_anak_perempuan = 1 * 7

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_suami = round((3 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)
            bagian_waris_ayah = round((2 * total_bagian) * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["suami"] = bagian_waris_suami
            hasil["ayah"] = bagian_waris_ayah
            hasil["anak_laki-laki"] = bagian_waris_anak_laki
            hasil["anak_perempuan"] = bagian_waris_anak_perempuan

            return hasil
        
        # Kondisi adanya suami, memiliki anak laki-laki dan perempuan, serta ayah pewaris (istri)
        if anak_laki >= 1 and anak_perempuan >= 1 and ayah == 1:
            # 1/4 + 1/6 = 3/12 + 2/12 = 5/12
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 12 * total_bagian # 12/12 - 5/12 = 7/12 = 12 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 7
            total_bagian_anak_perempuan = 1 * 7

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_suami = round((3 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)
            bagian_waris_ayah = round((2 * total_bagian) * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Suami"] = bagian_waris_suami
            hasil["Ayah"] = bagian_waris_ayah
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan

            return hasil
        
        # Kondisi adanya suami, serta memiliki anak laki-laki dan perempuan
        if anak_laki >= 1 and anak_perempuan >= 1:
            # 4/4 - 1/4 = 3/4
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 4 * total_bagian # 4/4 - 1/4 = 3/4 = 4 asal masalah

            total_bagian_anak_laki = 2 * 3
            total_bagian_anak_perempuan = 1 * 3

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_suami = round((1 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Suami"] = bagian_waris_suami
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan

            return hasil
        
        # Kondisi adanya suami, serta hanya memiliki seorang anak perempuan
        if anak_perempuan == 1:
            if ayah == 1:
                # 1/4 + 1/2 + 1/6  = 3/12 + 6/12 + 2/12 = 11/12
                ashabah = 12 - 11

                asal_masalah = 12
                bagian_waris = round(sisa_harta / asal_masalah)

                bagian_waris_suami = round(3 * bagian_waris)
                bagian_waris_anak_perempuan = round(6 * bagian_waris)
                bagian_waris_ayah = round((ashabah + 2) * bagian_waris)

                hasil["Suami"] = bagian_waris_suami
                hasil["harta_bagian_waris"] = bagian_waris
                hasil["Anak Perempuan"] = bagian_waris_anak_perempuan
                hasil["Ayah"] = bagian_waris_ayah

                return hasil

            # 1/4 - 1/2 = 1/4 + 2/4 = 3/4
            harta_sisa = 4 - 3
            jumlah_bagian_anak_perempuan = 2 + harta_sisa

            asal_masalah = 4
            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_suami = round(1 * bagian_waris)
            bagian_waris_anak_perempuan = round(jumlah_bagian_anak_perempuan * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Suami"] = bagian_waris_suami
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan

            return hasil
        
        # Kondisi adanya suami, serta memiliki lebih dari satu orang anak perempuan
        if anak_perempuan > 1:
            # 1/4 - 2/3 = 3/12 + 8/12 = 11/12
            harta_sisa = 12 - 11
            jumlah_bagian_anak_perempuan = 8 + harta_sisa

            asal_masalah = 12
            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_suami = round(3 * bagian_waris)
            bagian_waris_anak_perempuan_total = round(jumlah_bagian_anak_perempuan * bagian_waris)
            bagian_waris_anak_perempuan = round(jumlah_bagian_anak_perempuan * bagian_waris) / anak_perempuan

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Suami"] = bagian_waris_suami
            hasil["total_bagian_anak_perempuan"] = bagian_waris_anak_perempuan_total
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan

            return hasil
        
        if anak_laki >= 1:
          # 4/4 - 1/4 = 3/4
          bagian_anak_laki = 2 * anak_laki

          total_bagian = bagian_anak_laki
          asal_masalah = 4 * total_bagian # Berdasarkan 4/4 - 1/4 = 3/4 = 4 (diambil penyebutnya)

          total_bagian_anak_laki = 2 * 3

          bagian_waris = round(sisa_harta / asal_masalah)

          bagian_waris_suami = round((1 * total_bagian) * bagian_waris)
          bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)

          hasil["total_harta"] = harta
          hasil["harta_bagian_waris"] = bagian_waris
          hasil["Suami"] = bagian_waris_suami
          hasil["Anak Laki-Laki"] = bagian_waris_anak_laki

          return hasil

    # Kondisi suami wafat meninggalkan istri
    if istri >= 1 and istri <= 4:
        # Kondisi ahli waris hanya istri, anak, dan orang tua pewaris
        if anak_laki >= 1 and anak_perempuan >= 1 and ayah == 1 and ibu == 1:
            # 1/8 + 1/6 + 1/6 = 3/24 + 4/24 + 4/24 = 11/24
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 24 * total_bagian # 24/24 - 11/24 = 13/24 = 24 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 13 # 13 diambil dari pembilang sebelumnya
            total_bagian_anak_perempuan = 1 * 13

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_istri = round((3 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)
            bagian_waris_ayah = round((4 * total_bagian) * bagian_waris)
            bagian_waris_ibu = round((4 * total_bagian) * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Istri"] = bagian_waris_istri
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan
            hasil["Ayah"] = bagian_waris_ayah
            hasil["Ibu"] = bagian_waris_ibu

            return hasil
        
        # Kondisi ahli waris hanya istri, anak, dan ayah pewaris
        if anak_laki >= 1 and anak_perempuan >= 1 and ayah == 1:
            # 1/8 + 1/6 = 3/24 + 4/24 = 7/24
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 24 * total_bagian # 24/24 - 7/24 = 17/24 = 24 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 17 # 17 diambil dari pembilang sebelumnya
            total_bagian_anak_perempuan = 1 * 17

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_istri = round((3 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)
            bagian_waris_ayah = round((4 * total_bagian) * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Istri"] = bagian_waris_istri
            hasil["Ayah"] = bagian_waris_ayah
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan

            return hasil
        
        if anak_laki >= 1 and anak_perempuan >= 1 and ibu == 1:
            # 1/8 + 1/6 = 3/24 + 4/24 = 7/24
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 24 * total_bagian # 24/24 - 7/24 = 17/24 = 24 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 17 # 17 diambil dari pembilang sebelumnya
            total_bagian_anak_perempuan = 1 * 17

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_istri = round((3 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)
            bagian_waris_ibu = round((4 * total_bagian) * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Istri"] = bagian_waris_istri
            hasil["Ibu"] = bagian_waris_ibu
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan

            return hasil
        
        # Kondisi jika adanya istri,  anak laki-laki dan perempuan, serta kakek dari jalur ayah pewaris (suami)
        if anak_laki >= 1 and anak_perempuan >= 1 and kakek == 1:
            # 1/8 + 1/6 = 3/24 + 4/24 = 7/24
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 24 * total_bagian # 24/24 - 7/24 = 17/24 = 24 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 17
            total_bagian_anak_perempuan = 1 * 17

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_istri = round((3 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)
            bagian_waris_kakek = round((4 * total_bagian) * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Istri"] = bagian_waris_suami
            hasil["Kakek"] = bagian_waris_ayah
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan

            return hasil
        
        if anak_laki >= 1 and anak_perempuan >= 1:
            # 8/8 - 1/8 = 7/8
            bagian_anak_laki = 2 * anak_laki
            bagian_anak_perempuan = 1 * anak_perempuan

            total_bagian = bagian_anak_laki + bagian_anak_perempuan
            asal_masalah = 8 * total_bagian # 12 diambil dari penyebutnya

            total_bagian_anak_laki = 2 * 7 # 7 diambil dari pembilang
            total_bagian_anak_perempuan = 1 * 7

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_istri = round((1 * total_bagian) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
            bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Istri"] = bagian_waris_istri
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan

            return hasil

        if anak_laki >= 1:
            # 8/8 - 1/8 = 7/8
            bagian_anak_laki = 2 * anak_laki # 2 bagian anak laki x jumlah anak laki

            total_bagian = bagian_anak_laki
            asal_masalah = 8 * total_bagian # 8/8 - 1/8 = 7/8 = 8 (diambil penyebutnya)

            total_bagian_anak_laki = 2 * 7

            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_istri = round((total_bagian * 1) * bagian_waris)
            bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)

            hasil["total_harta"] = harta
            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Istri"] = bagian_waris_istri
            hasil["Anak Laki-Laki"] = bagian_waris_anak_laki

            return hasil
        
    if anak_perempuan > 1:
        if ayah == 1:
            # 2/3 + 1/6  = 8/12 + 2/12 = 10/12
            ashabah = 12 - 10

            asal_masalah = 12
            bagian_waris = round(sisa_harta / asal_masalah)

            bagian_waris_anak_perempuan = round(8 * bagian_waris)
            bagian_waris_ayah = round((ashabah + 2) * bagian_waris)

            hasil["harta_bagian_waris"] = bagian_waris
            hasil["Anak Perempuan"] = bagian_waris_anak_perempuan
            hasil["Ayah"] = bagian_waris_ayah

            return hasil

    if anak_laki >= 1 and anak_perempuan >= 1:
        # 1 : 6 = 1/6
        bagian_anak_laki = 2 * anak_laki
        bagian_anak_perempuan = 1 * anak_perempuan

        total_bagian = bagian_anak_laki + bagian_anak_perempuan
        asal_masalah = 1 * total_bagian # 6 diambil dari total bagian anak

        total_bagian_anak_laki = 2 * 1 # 1 diambil dari pembilang
        total_bagian_anak_perempuan = 1 * 1

        bagian_waris = round(sisa_harta / asal_masalah)

        bagian_waris_anak_laki = round(total_bagian_anak_laki * bagian_waris)
        bagian_waris_anak_perempuan = round(total_bagian_anak_perempuan * bagian_waris)

        hasil["total_harta"] = harta
        hasil["harta_bagian_waris"] = bagian_waris
        hasil["Anak Laki-Laki"] = bagian_waris_anak_laki
        hasil["Anak Perempuan"] = bagian_waris_anak_perempuan

        return hasil
        