import numpy as np

class PozisyonSiniflayici:
    def __init__(self):
        self.bas_idx = 0
        self.omuz_sol = 5
        self.omuz_sag = 6
        self.kalca_sol = 11
        self.kalca_sag = 12
        self.diz_sol = 13
        self.diz_sag = 14
        self.ayak_sol = 15
        self.ayak_sag = 16

    def siniflandir(self, pose, hiz, id):
        try:
            if pose is None or len(pose) != 17:
                return "diger"

            # Anahtar noktaları al
            omuz_sol = pose[self.omuz_sol]
            omuz_sag = pose[self.omuz_sag]
            kalca_sol = pose[self.kalca_sol]
            kalca_sag = pose[self.kalca_sag]
            diz_sol = pose[self.diz_sol]
            diz_sag = pose[self.diz_sag]
            ayak_sol = pose[self.ayak_sol]
            ayak_sag = pose[self.ayak_sag]

            # Ölçümler
            kutu_genislik = abs(omuz_sag[0] - omuz_sol[0])
            kutu_yukseklik = abs(omuz_sol[1] - kalca_sol[1]) + 1e-5
            oran = kutu_genislik / kutu_yukseklik

            y_noktalari = [
                pose[self.bas_idx][1], omuz_sol[1], omuz_sag[1],
                kalca_sol[1], kalca_sag[1], diz_sol[1], diz_sag[1],
                ayak_sol[1], ayak_sag[1]
            ]
            yukseklik_farki = max(y_noktalari) - min(y_noktalari)

            egim = abs(omuz_sol[1] - kalca_sol[1])

            # 🔥 İyileştirilmiş yere yatma algısı 🔥
            if oran > 1.5 or yukseklik_farki < 100 or egim < 40:
                sonuc = "yere yatma"
            elif (0.8 < oran < 1.2 and 90 < yukseklik_farki < 130 and egim < 55):
                sonuc = "yere yatma"
            elif abs(kalca_sol[1] - diz_sol[1]) < 30:
                sonuc = "comelme"
            elif hiz > 10:
                sonuc = "kosma"
            else:
                sonuc = "diger"

            return sonuc

        except Exception as e:
            print(f"Pozisyon sınıflandırma hatası: {e}")
            return "diger"

