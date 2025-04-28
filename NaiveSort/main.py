import cv2
import os
import numpy as np
from collections import defaultdict, deque
from ultralytics import YOLO
from moduller.tespitci import Tespitci
from moduller.naive_tracker import NaiveSortTracker
from moduller.poz_siniflayici import PozisyonSiniflayici

video_yolu = "girdi/media4.mp4"
model_yolu = "modeller/yolov8n-pose.pt"
cikti_klasoru = "cikti"
os.makedirs(cikti_klasoru, exist_ok=True)

video = cv2.VideoCapture(video_yolu)
fps = video.get(cv2.CAP_PROP_FPS)
genislik = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
yukseklik = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_yazici = cv2.VideoWriter(os.path.join(cikti_klasoru, "sonuc.mp4"), fourcc, fps, (genislik, yukseklik))

model = YOLO(model_yolu)
tespitci = Tespitci(model)
tracker = NaiveSortTracker()
siniflayici = PozisyonSiniflayici()

# Süre takibi
pozisyon_sure = defaultdict(lambda: defaultdict(int))

# Her ID için pozisyon geçmişi
pozisyon_gecmisi = defaultdict(lambda: deque(maxlen=5))  # Son 5 pozisyonu tutacak

# Her ID için kararli pozisyonları tut
kararli_pozisyonlar = dict()

# Rapor dosyası
rapor = open(os.path.join(cikti_klasoru, "rapor.txt"), "w", encoding="utf-8")
rapor.write(f"{'ID':<6}{'Pozisyon':<15}{'Süre (sn)':<10}\n")


renkler = {
    "yere yatma": (0, 0, 255),
    "comelme": (0, 165, 255),
    "kosma": (0, 255, 0),
    "diger": (200, 200, 200)
}


while True:
    ret, kare = video.read()
    if not ret:
        break

    sonuc = model.predict(kare, conf=0.4, iou=0.5)[0]

    kutular = [box.xyxy[0].tolist() for box in sonuc.boxes]
    pozlar = [kp.xy[0].cpu().numpy() for kp in sonuc.keypoints]

    takip_sonuclari = tracker.update(kutular)

    for i, kisi in enumerate(takip_sonuclari):
        id = kisi["id"]
        x1, y1, x2, y2 = map(int, kisi["bbox"])
        pose = pozlar[i] if i < len(pozlar) else None
        hiz = kisi.get("hiz", 0)

        # Anlık pozisyonu bul
        anlik_pozisyon = siniflayici.siniflandir(pose, hiz, id)

        # Eğer ID için daha önce kararli pozisyon kosma ise
        onceki_kararli = kararli_pozisyonlar.get(id, None)

        if onceki_kararli == "kosma":
            if anlik_pozisyon in ["comelme", "yere yatma", "diger"]:
                # Küçük sapmaları dikkate alma, koşmaya devam et
                stabil_pozisyon = "kosma"
            else:
                # Koşmadan farklı büyük bir pozisyon olursa değiştir
                stabil_pozisyon = anlik_pozisyon
                kararli_pozisyonlar[id] = stabil_pozisyon
        else:
            # Eğer daha önce kosma değilse, anlık pozisyonu kararli pozisyon olarak güncelle
            stabil_pozisyon = anlik_pozisyon
            kararli_pozisyonlar[id] = stabil_pozisyon

        # Süreyi arttır
        pozisyon_sure[id][stabil_pozisyon] += 1

        renk = renkler.get(stabil_pozisyon, (0, 255, 255))

        # Kutu çiz
        cv2.rectangle(kare, (x1, y1), (x2, y2), renk, 2)
        cv2.putText(kare, f"ID:{id} {stabil_pozisyon}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, renk, 2)

    video_yazici.write(kare)
    cv2.imshow("Takip", kare)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Raporu yaz
for id in sorted(pozisyon_sure.keys()):
    for poz in pozisyon_sure[id]:
        sure_saniye = round(pozisyon_sure[id][poz] / fps, 1)
        if sure_saniye >= 1.0:
            rapor.write(f"{id:<6}{poz:<15}{sure_saniye:<10}\n")

rapor.close()
video.release()
video_yazici.release()
cv2.destroyAllWindows()
