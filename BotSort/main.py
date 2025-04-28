import cv2
import os
from ultralytics import YOLO
from moduller.tespitci import Tespitci
from moduller.poz_siniflayici import PozisyonSiniflayici
from datetime import datetime

# 🔧 Ayarlar
video_yolu = "girdi/media4.mp4"
model_yolu = "modeller/yolov8n-pose.pt"
reid_model_yolu = "modeller/osnet.onnx"
cikti_klasoru = "cikti"
os.makedirs(cikti_klasoru, exist_ok=True)

# 📦 Modelleri başlat
yolo_model = YOLO(model_yolu)
config = {"reid_model_path": reid_model_yolu}
tespitci = Tespitci(yolo_model, config)
siniflayici = PozisyonSiniflayici()

# 🎥 Video giriş ve çıkış
video = cv2.VideoCapture(video_yolu)
fps = video.get(cv2.CAP_PROP_FPS)
genislik = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
yukseklik = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
cikti_video_yolu = os.path.join(cikti_klasoru, "sonuc.mp4")
video_yazici = cv2.VideoWriter(cikti_video_yolu, fourcc, fps, (genislik, yukseklik))

# 🧠 Kişi başı pozisyon süreleri
poz_sureleri = {}

# 📋 Log dosyası
rapor_yolu = os.path.join(cikti_klasoru, "rapor.txt")
rapor = open(rapor_yolu, "w", encoding="utf-8")

# 🔄 Kareleri işle
while True:
    ret, kare = video.read()
    if not ret:
        break

    insanlar = tespitci.insanlari_tespit_et(kare)

    for kisi in insanlar:
        bbox = kisi["bbox"]
        id = kisi["id"]
        pose = kisi["pose"]

        sinif = siniflayici.siniflandir(pose)
        poz_sureleri.setdefault(id, {}).setdefault(sinif, 0)
        poz_sureleri[id][sinif] += 1 / fps

        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(kare, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(kare, f"ID:{id} {sinif}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    video_yazici.write(kare)
    cv2.imshow("İzleme", kare)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 🧾 Rapor yaz
for id, siniflar in poz_sureleri.items():
    rapor.write(f"Kişi ID: {id}\n")
    for sinif, sure in siniflar.items():
        rapor.write(f"  - {sinif}: {sure:.2f} saniye\n")
    rapor.write("\n")

# 🔚 Temizlik
video.release()
video_yazici.release()
rapor.close()
cv2.destroyAllWindows()
