import time
from collections import defaultdict

class TakipYonetici:
    def __init__(self, fps=30):
        self.fps = fps
        self.gecmis = {}
        self.toplam_sure = defaultdict(lambda: defaultdict(float))
        self.konum_gecmisi = defaultdict(list)

    def guncelle(self, insanlar):
        simdi = time.time()
        for insan in insanlar:
            kisi_id = insan["id"]
            pozisyon = insan["pozisyon"]
            kutu = insan["kutu"]

            # Hareket takibi için kutuları kaydet
            self.konum_gecmisi[kisi_id].append(kutu)
            if len(self.konum_gecmisi[kisi_id]) > 5:
                self.konum_gecmisi[kisi_id].pop(0)

            # Süre takibi
            if kisi_id not in self.gecmis:
                self.gecmis[kisi_id] = {"pozisyon": pozisyon, "baslangic": simdi}
                continue

            onceki = self.gecmis[kisi_id]["pozisyon"]
            baslangic = self.gecmis[kisi_id]["baslangic"]

            if pozisyon != onceki:
                gecen_sure = simdi - baslangic
                self.toplam_sure[kisi_id][onceki] += gecen_sure
                self.gecmis[kisi_id] = {"pozisyon": pozisyon, "baslangic": simdi}

    def hareket_miktari(self, kisi_id):
        kutular = self.konum_gecmisi.get(kisi_id, [])
        if len(kutular) < 2:
            return 0

        (x1a, y1a, x2a, y2a), (x1b, y1b, x2b, y2b) = kutular[-2], kutular[-1]
        dx = ((x1b + x2b) / 2) - ((x1a + x2a) / 2)
        dy = ((y1b + y2b) / 2) - ((y1a + y2a) / 2)
        return (dx**2 + dy**2) ** 0.5

    def rapor_al(self):
        simdi = time.time()
        for kisi_id, veri in self.gecmis.items():
            pozisyon = veri["pozisyon"]
            baslangic = veri["baslangic"]
            self.toplam_sure[kisi_id][pozisyon] += simdi - baslangic
            self.gecmis[kisi_id]["baslangic"] = simdi
        return self.toplam_sure
