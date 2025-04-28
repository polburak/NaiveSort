import cv2

def bilgi_ciz(kare, insan, fps):
    x1, y1, x2, y2 = map(int, insan["kutu"])
    kisi_id = insan["id"]
    pozisyon = insan.get("pozisyon", "bilinmiyor")

    renk = (0, 255, 0)  # varsayılan renk: yeşil

    if pozisyon == "yere_yatma":
        renk = (0, 0, 255)  # kırmızı
    elif pozisyon == "comelme":
        renk = (255, 255, 0)  # açık mavi
    elif pozisyon == "kosma":
        renk = (0, 165, 255)  # turuncu

    cv2.rectangle(kare, (x1, y1), (x2, y2), renk, 2)
    cv2.putText(kare, f"ID {kisi_id} - {pozisyon}", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, renk, 2)

def rapor_yaz_id_bazli(takip_yonetici, dosya_yolu):
    kisiler = takip_yonetici.rapor_al()
    with open(dosya_yolu, "w", encoding="utf-8") as dosya:
        for kisi_id, poz_sureleri in kisiler.items():
            dosya.write(f"Kişi {kisi_id}\n")
            for pozisyon, sure in poz_sureleri.items():
                dosya.write(f"- {pozisyon}: {sure:.2f} saniye\n")
            dosya.write("\n")
