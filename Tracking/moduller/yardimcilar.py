class TakipYonetici:
    def __init__(self):
        # id -> pozisyon -> süre (saniye)
        self.kisiler = {}

    def sure_ekle(self, kisi_id, pozisyon, saniye):
        if kisi_id not in self.kisiler:
            self.kisiler[kisi_id] = {
                "yere_yatma": 0.0,
                "comelme": 0.0,
                "kosma": 0.0,
                "diger": 0.0
            }

        if pozisyon in self.kisiler[kisi_id]:
            self.kisiler[kisi_id][pozisyon] += saniye
        else:
            self.kisiler[kisi_id]["diger"] += saniye

    def rapor_al(self):
        return self.kisiler


def rapor_yaz_id_bazli(takip_yonetici, dosya_yolu):
    kisiler = takip_yonetici.rapor_al()
    with open(dosya_yolu, "w", encoding="utf-8") as dosya:
        for kisi_id, poz_sureleri in kisiler.items():
            dosya.write(f"Kişi {kisi_id}\n")
            for pozisyon, sure in poz_sureleri.items():
                dosya.write(f"- {pozisyon}: {sure:.2f} saniye\n")
            dosya.write("\n")
