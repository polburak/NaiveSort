import cv2

def rapor_yaz_id_bazli(takip_yonetici, dosya_yolu):
    kisiler = takip_yonetici.rapor_al()
    with open(dosya_yolu, "w", encoding="utf-8") as dosya:
        for kisi_id, poz_sureleri in kisiler.items():
            dosya.write(f"Kişi {kisi_id}\n")
            for pozisyon, sure in poz_sureleri.items():
                dosya.write(f"- {pozisyon}: {sure:.2f} saniye\n")
            dosya.write("\n")

def bilgi_ciz(kare, insan, fps):
    x1, y1, x2, y2 = insan["kutu"]
    kisi_id = insan["id"]
    pozisyon = insan["pozisyon"]

    # Renkler pozisyona göre
    renkler = {
        "yere_yatma": (0, 0, 255),      # Kırmızı
        "comelme": (0, 255, 255),       # Sarı
        "kosma": (0, 255, 0),           # Yeşil
        "diger": (255, 255, 255)        # Beyaz
    }
    renk = renkler.get(pozisyon, (200, 200, 200))

    etiket = f"ID:{kisi_id} | {pozisyon}"
    cv2.rectangle(kare, (x1, y1), (x2, y2), renk, 2)
    cv2.putText(kare, etiket, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, renk, 2)
