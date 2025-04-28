import numpy as np

class TakipYonetici:
    def __init__(self, fps=30):
        self.fps = fps
        self.kisi_gecmisi = {}        # ID bazlı toplam süre (saniye)
        self.kare_sayaci = {}         # ID bazlı pozisyon sayacı (kare)
        self.onceki_konumlar = {}     # ID bazlı hareket bilgisi

    def guncelle(self, insanlar):
        for insan in insanlar:
            kid = insan["id"]
            pozisyon = insan["pozisyon"]
            x1, y1, x2, y2 = insan["kutu"]
            merkez = ((x1 + x2) / 2, (y1 + y2) / 2)

            if kid not in self.kisi_gecmisi:
                self.kisi_gecmisi[kid] = {"yere_yatma": 0, "comelme": 0, "kosma": 0, "diger": 0}
                self.kare_sayaci[kid] = {"yere_yatma": 0, "comelme": 0, "kosma": 0, "diger": 0}
                self.onceki_konumlar[kid] = []

            self.kare_sayaci[kid][pozisyon] += 1
            self.onceki_konumlar[kid].append(merkez)

            # Hareket geçmişi kısa tut
            if len(self.onceki_konumlar[kid]) > 10:
                self.onceki_konumlar[kid] = self.onceki_konumlar[kid][-10:]

        # FPS'e göre saniyeye çevir
        for kid in self.kare_sayaci:
            for poz, kare_sayisi in self.kare_sayaci[kid].items():
                self.kisi_gecmisi[kid][poz] = kare_sayisi / self.fps

    def rapor_al(self):
        return self.kisi_gecmisi

    def hareket_miktari(self, kid):
        if kid not in self.onceki_konumlar:
            return 0
        konumlar = self.onceki_konumlar[kid]
        if len(konumlar) < 2:
            return 0
        toplam = 0
        for i in range(1, len(konumlar)):
            x1, y1 = konumlar[i - 1]
            x2, y2 = konumlar[i]
            toplam += np.linalg.norm(np.array([x2 - x1, y2 - y1]))
        return toplam
