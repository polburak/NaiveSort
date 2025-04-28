import numpy as np

class IDDuzenleyici:
    def __init__(self, mesafe_esigi=50):
        self.stabil_id_sayaci = 0
        self.stabil_konumlar = {}  # stabil_id -> son merkez pozisyon
        self.mesafe_esigi = mesafe_esigi

    def merkez_noktasi(self, insan):
        try:
            # Kalçaların ortalaması → daha stabil
            sol_kalca = np.array(insan["anahtar_noktalar"][11][:2])
            sag_kalca = np.array(insan["anahtar_noktalar"][12][:2])
            merkez = (sol_kalca + sag_kalca) / 2
        except:
            # Fallback: kutu merkezi
            x1, y1, x2, y2 = insan["kutu"]
            merkez = np.array([(x1 + x2) / 2, (y1 + y2) / 2])
        return merkez

    def guncelle(self, insanlar):
        yeni_idler = {}

        for insan in insanlar:
            yeni_merkez = self.merkez_noktasi(insan)

            # En yakın stabil ID'yi bul
            eslesen_id = None
            for stabil_id, eski_merkez in self.stabil_konumlar.items():
                mesafe = np.linalg.norm(yeni_merkez - eski_merkez)
                if mesafe < self.mesafe_esigi:
                    eslesen_id = stabil_id
                    break

            if eslesen_id is None:
                eslesen_id = self.stabil_id_sayaci
                self.stabil_id_sayaci += 1

            yeni_idler[insan["id"]] = eslesen_id
            self.stabil_konumlar[eslesen_id] = yeni_merkez

        # ID'leri güncelle
        for insan in insanlar:
            gecici_id = insan["id"]
            insan["id"] = yeni_idler[gecici_id]

        return insanlar
