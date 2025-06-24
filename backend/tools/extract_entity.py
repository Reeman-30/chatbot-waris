import re

# Ekstraksi entitas dari teks
def is_ibu_sebagai_istri(text):
    # Tangkap frasa seperti: "ibu saya sebagai istri", "ibu saya adalah istri", dst
    return bool(re.search(r'ibu\s+saya\s+(sebagai|adalah)?\s*(seorang\s+)?istri(\s+sah)?', text))

def is_kakek_pihak_ayah(text):
    return bool(re.search(r'kakek\s+dari\s+(pihak\s+)?ayah', text))

def extract_entitas(pertanyaan):
    text = pertanyaan.lower()
    entitas = {}

    # Step 1: Daftar entitas dan yang sudah meninggal
    entitas_list = [
        "istri", "anak laki-laki", "anak perempuan",
        "ibu", "ayah", "suami", "nenek", "kakek", "anak angkat"
    ]

    BILANGAN_MAP = {
        "satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5,
        "enam": 6, "tujuh": 7, "delapan": 8, "sembilan": 9, "sepuluh": 10
    }

    subjek_meninggal = set()
    for ent in entitas_list:
        ent_key = ent.replace(" ", "[- ]?")
        pattern = rf'\b{ent_key}\b(?:\s+saya)?\s+(?:yang\s+)?(meninggal|wafat|meninggal dunia|telah wafat)\b'
        if re.search(pattern, text):
            subjek_meninggal.add(ent)

    # Step 2: Deteksi harta dan hutang lebih longgar
    harta_patterns = [
      r'(?:harta|warisan|uang tunai|uang|tabungan|harta warisan)[^\d]{0,10}(\d{3,})',
      r'(?:meninggalkan|peninggalan|yang ditinggalkan)[^\d]{0,10}(?:harta|warisan|uang|tabungan|harta warisan)[^\d]{0,10}(\d{3,})'
    ]

    for pat in harta_patterns:
      match = re.search(pat, text)
      if match:
          entitas['harta'] = int(match.group(1))
          break
    
    # Step 3: Deteksi entitas manusia
    for ent in entitas_list:
        ent_key = ent.replace(" ", "_")
        if ent in subjek_meninggal:
            continue

        ent_pattern = ent.replace(" ", "[- ]?")
        found = False

        # Ambil jumlah harta dari kalimat
        harta_match = re.search(r'harta(?: waris| warisan)?(?: sebesar| sejumlah)? ([\d\.]+) ?(juta|miliar)?', pertanyaan, re.IGNORECASE)
        if harta_match:
            raw_angka = harta_match.group(1).replace('.', '').replace(',', '.')  # tangani format 1.500.000 dan 1,5
            try:
                jumlah = float(raw_angka)
                satuan = harta_match.group(2)

                if satuan:
                    satuan = satuan.lower()
                    if satuan == 'juta':
                        jumlah *= 1_000_000
                    elif satuan == 'miliar':
                        jumlah *= 1_000_000_000

                entitas['harta'] = int(jumlah)
            except ValueError:
                pass  # jika parsing gagal, bisa dilewatkan atau log error

        # Format: 2 anak perempuan
        match_digit = re.search(rf'(\d+)\s+{ent_pattern}', text)
        if match_digit:
            entitas[ent_key] = int(match_digit.group(1))
            continue

        # Format: tiga anak perempuan
        for kata, angka in BILANGAN_MAP.items():
            if re.search(rf'\b{kata}\s+{ent_pattern}\b', text):
                entitas[ent_key] = angka
                found = True
                break
        if found:
            continue

        # Format: "punya istri", "seorang ibu", "dan anak perempuan"
        if re.search(rf'(punya|memiliki|dan|dengan|seorang)?\s*\b{ent_pattern}\b', text):
            if ent_key not in entitas:
              # Tambahkan validasi khusus untuk kakek
              if ent_key == "kakek" and not is_kakek_pihak_ayah(text):
                  continue  # abaikan kakek dari selain pihak ayah

              entitas[ent_key] = 1  # fallback default 1

              if 'ibu' in entitas and is_ibu_sebagai_istri(text):
                del entitas['ibu']

        # Tambahkan penanda umum "anak" jika ada anak laki-laki atau perempuan
        if "anak_laki-laki" in entitas or "anak_perempuan" in entitas:
          entitas["anak"] = True

        # ====== DETEKSI HUTANG ======

        # 1. Tidak ada hutang
        if re.search(r'(tidak\s+ada|tanpa)\s+hutang', text):
            entitas['hutang'] = 0

        # 2. Ada hutang
        match = re.search(r'hutang(?: sebesar| sejumlah)?\s*([\d\.]+)\s*(juta|miliar)?', text)
        if match:
            jumlah = float(match.group(1).replace(',', '.'))
            satuan = match.group(2)

            if satuan:
                if satuan.lower() == 'juta':
                    jumlah *= 1_000_000
                elif satuan.lower() == 'miliar':
                    jumlah *= 1_000_000_000
            entitas['hutang'] = int(jumlah)

    return entitas