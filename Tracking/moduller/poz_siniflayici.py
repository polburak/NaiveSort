import numpy as np

class PozSiniflayici:
    def __init__(self):
        pass

    def pozisyon_belirle(self, insan):
        noktalar = np.array(insan["anahtar_noktalar"])  # (17, 3)

        try:
            burun = noktalar[0]
            sol_omuz = noktalar[5]
            sag_omuz = noktalar[6]
            sol_kalca = noktalar[11]
            sag_kalca = noktalar[12]
            sol_diz = noktalar[13]
            sag_diz = noktalar[14]
            sol_ayak = noktalar[15]
            sag_ayak = noktalar[16]
        except IndexError:
            return "diger"

        kritik_noktalar = [burun, sol_omuz, sag_omuz, sol_kalca, sag_kalca, sol_diz, sag_diz, sol_ayak, sag_ayak]
        if any(n[2] < 0.5 for n in kritik_noktalar):
            return "diger"

        # Koordinatlar [x, y]
        burun = burun[:2]
        sol_omuz = sol_omuz[:2]
        sag_omuz = sag_omuz[:2]
        sol_kalca = sol_kalca[:2]
        sag_kalca = sag_kalca[:2]
        sol_diz = sol_diz[:2]
        sag_diz = sag_diz[:2]
        sol_ayak = sol_ayak[:2]
        sag_ayak = sag_ayak[:2]

        omuz_y = np.mean([sol_omuz[1], sag_omuz[1]])
        kalca_y = np.mean([sol_kalca[1], sag_kalca[1]])
        diz_y = np.mean([sol_diz[1], sag_diz[1]])
        ayak_y = np.mean([sol_ayak[1], sag_ayak[1]])

        vucut_uzunlugu = ayak_y - burun[1]
        if vucut_uzunlugu < 50:
            return "diger"

        x1, y1, x2, y2 = insan["kutu"]
        kutu_yukseklik = y2 - y1
        kutu_genislik = x2 - x1

        # --- YERE YATMA ---
        yere_yatma_puani = 0

        if abs(burun[1] - ayak_y) < vucut_uzunlugu * 0.3:
            yere_yatma_puani += 1
        if kalca_y - omuz_y < vucut_uzunlugu * 0.3:
            yere_yatma_puani += 1
        if ayak_y - kalca_y < vucut_uzunlugu * 0.25:
            yere_yatma_puani += 1
        if kutu_yukseklik < kutu_genislik * 0.6:
            yere_yatma_puani += 1

        if yere_yatma_puani >= 2:
            return "yere_yatma"

        # --- ÇÖMELME (eski sade sürüm) ---
        if (ayak_y - kalca_y) < vucut_uzunlugu * 0.25:
            return "comelme"

        # --- KOŞMA (yürüme dahil) ---
        kosma_puani = 0

        if abs(sol_ayak[1] - sag_ayak[1]) > vucut_uzunlugu * 0.1:
            kosma_puani += 1
        if abs(sol_diz[1] - sag_diz[1]) > vucut_uzunlugu * 0.1:
            kosma_puani += 1
        if abs(sol_ayak[0] - sag_ayak[0]) > vucut_uzunlugu * 0.2:
            kosma_puani += 1

        kalca_x = np.mean([sol_kalca[0], sag_kalca[0]])
        if abs(burun[0] - kalca_x) > vucut_uzunlugu * 0.1:
            kosma_puani += 1

        if kosma_puani >= 1:
            return "kosma"

        return "diger"
