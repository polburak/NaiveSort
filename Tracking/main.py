import cv2
from moduller.tespitci import Tespitci
from moduller.poz_siniflayici import PozSiniflayici
from moduller.yardimcilar import TakipYonetici, rapor_yaz_id_bazli
from moduller.id_duzenleyici import IDDuzenleyici

# Dosya yolları
video_yolu = "girdi/media4.mp4"
cikti_video_yolu = "cikti/islenmis_video.mp4"
rapor_dosyasi_yolu = "cikti/rapor.txt"

# Bileşenleri oluştur
tespitci = Tespitci(model_yolu="yolov8n-pose.pt")
siniflayici = PozSiniflayici()
takip_yonetici = TakipYonetici()
id_duzenleyici = IDDuzenleyici(mesafe_esigi=50)

# Video giriş/çıkış ayarları
video = cv2.VideoCapture(video_yolu)
fps = video.get(cv2.CAP_PROP_FPS)
genislik = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
yukseklik = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
dortcc = cv2.VideoWriter_fourcc(*'mp4v')
video_yazici = cv2.VideoWriter(cikti_video_yolu, dortcc, fps, (genislik, yukseklik))

# Renk tanımları
renkler = {
    "yere_yatma": (255, 0, 0),
    "comelme": (0, 255, 255),
    "kosma": (0, 0, 255),
    "diger": (128, 128, 128)
}

while True:
    basarili, kare = video.read()
    if not basarili:
        break

    insanlar = tespitci.insanlari_tespit_et(kare)
    insanlar = id_duzenleyici.guncelle(insanlar)

    for insan in insanlar:
        kisi_id = insan["id"]
        pozisyon = siniflayici.pozisyon_belirle(insan)
        takip_yonetici.sure_ekle(kisi_id, pozisyon, 1 / fps)

        x1, y1, x2, y2 = insan["kutu"]
        renk = renkler.get(pozisyon, (0, 255, 0))
        cv2.rectangle(kare, (x1, y1), (x2, y2), renk, 2)
        cv2.putText(kare, f"ID {kisi_id} - {pozisyon}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, renk, 2)

    video_yazici.write(kare)
    cv2.imshow("Poz Takibi", kare)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Temizlik ve çıktı
video.release()
video_yazici.release()
cv2.destroyAllWindows()

# ID bazlı rapor yazımı
rapor_yaz_id_bazli(takip_yonetici, rapor_dosyasi_yolu)
print("✔️ Video işlendi ve ID bazlı rapor oluşturuldu.")
