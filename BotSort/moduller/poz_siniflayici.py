import numpy as np

class PozisyonSiniflayici:
    def __init__(self):
        # COCO format indexleri
        self.omuz_sol = 5
        self.omuz_sag = 6
        self.kalca_sol = 11
        self.kalca_sag = 12
        self.diz_sol = 13
        self.diz_sag = 14
        self.ayak_sol = 15
        self.ayak_sag = 16

    def siniflandir(self, pose):
        try:
            if pose is None or len(pose) != 17:
                return "belirsiz"

            # Noktaları çek
            omuz_sag_y = pose[self.omuz_sag][1]
            omuz_sol_y = pose[self.omuz_sol][1]
            kalca_sag_y = pose[self.kalca_sag][1]
            kalca_sol_y = pose[self.kalca_sol][1]

            diz_sag_y = pose[self.diz_sag][1]
            diz_sol_y = pose[self.diz_sol][1]

            ayak_sag_x = pose[self.ayak_sag][0]
            ayak_sol_x = pose[self.ayak_sol][0]

            # Kurallar:
            # 🟠 Yere yatma → omuz-kalça arası dikey mesafe çok küçük
            omuz_ort = (omuz_sag_y + omuz_sol_y) / 2
            kalca_ort = (kalca_sag_y + kalca_sol_y) / 2
            if abs(omuz_ort - kalca_ort) < 20:
                return "yere yatma"

            # 🟠 Çömelme → kalça-diz arası çok yakınsa
            diz_ort = (diz_sag_y + diz_sol_y) / 2
            if abs(kalca_ort - diz_ort) < 40:
                return "comelme"

            # 🟠 Koşma → ayaklar arası yatay mesafe genişse
            ayak_mesafe = abs(ayak_sag_x - ayak_sol_x)
            if ayak_mesafe > 100:
                return "kosma"

            return "belirsiz"

        except Exception as e:
            print(f"Pozisyon sınıflandırma hatası: {e}")
            return "belirsiz"
