import numpy as np

class PozSiniflayici:
    def guvenli_ortalama(self, noktalar):
        noktalar = [n for n in noktalar if len(n) > 2 and n[2] > 0.5]
        return np.mean([n[1] for n in noktalar]) if noktalar else 0

    def pozisyon_belirle(self, insan):
        kps = np.array(insan["anahtar_noktalar"])  # (17, 3)

        # Ortalama Y koordinatları
        omuz_y = self.guvenli_ortalama([kps[5], kps[6]])       # sol/sag omuz
        kalca_y = self.guvenli_ortalama([kps[11], kps[12]])    # sol/sag kalça
        diz_y = self.guvenli_ortalama([kps[13], kps[14]])      # sol/sag diz
        ayak_y = self.guvenli_ortalama([kps[15], kps[16]])     # sol/sag ayak
        burun_y = kps[0][1] if len(kps[0]) > 2 and kps[0][2] > 0.5 else 0

        # Dikey farklar
        omuz_kalca = kalca_y - omuz_y
        kalca_diz = diz_y - kalca_y
        diz_ayak = ayak_y - diz_y

        # POZİSYON KARARLARI

        # 1. Yere yatma
        if omuz_kalca < 30 and burun_y > diz_y - 10:
            return "yere_yatma"

        # 2. Çömelme
        elif kalca_diz < 30 and kalca_y > omuz_y and kalca_y < diz_y:
            return "comelme"

        # 3. Koşma (Hareketli ve yüksek duruşluysa)
        elif omuz_kalca > 40 and insan.get("hareketli", False):
            return "kosma"


        # 4. Diğer
        else:
            return "diger"

