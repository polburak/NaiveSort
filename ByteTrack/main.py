import cv2
from moduller.tespitci import Tespitci
from moduller.poz_siniflayici import PozSiniflayici
from moduller.takipci import TakipYonetici
from moduller.yardimcilar import bilgi_ciz, rapor_yaz_id_bazli

# Girdi / Çıktı yolları
video_yolu = "girdi/media4.mp4"
cikti_video_yolu = "cikti/islenmis_video.mp4"
cikti_rapor_yolu = "cikti/rapor.txt"

# Sistem bileşenleri
tespitci = Tespitci(model_yolu="yolov8n-pose.pt", cihaz="cpu")
siniflayici = PozSiniflayici()
video = cv2.VideoCapture(video_yolu)

fps = int(video.get(cv2.CAP_PROP_FPS))
genislik = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
yukseklik = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
cikti = cv2.VideoWriter(cikti_video_yolu, cv2.VideoWriter_fourcc(*"mp4v"), fps, (genislik, yukseklik))

takip_yonetici = TakipYonetici(fps=fps)

while True:
    basarili, kare = video.read()
    if not basarili:
        break

    insanlar = tespitci.insanlari_tespit_et(kare)

    for insan in insanlar:
        hareket = takip_yonetici.hareket_miktari(insan["id"])
        insan["hareketli"] = hareket > 5  # 30 px eşiğini test ederek ayarlayabilirsin
        insan["pozisyon"] = siniflayici.pozisyon_belirle(insan)

    takip_yonetici.guncelle(insanlar)

    for insan in insanlar:
        bilgi_ciz(kare, insan, fps)

    cikti.write(kare)
    cv2.imshow("izleme", kare)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Rapor çıktısı
rapor_yaz_id_bazli(takip_yonetici, cikti_rapor_yolu)

# Kapat
video.release()
cikti.release()
cv2.destroyAllWindows()
