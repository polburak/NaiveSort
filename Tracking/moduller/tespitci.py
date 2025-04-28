from ultralytics import YOLO
import numpy as np

class Tespitci:
    def __init__(self, model_yolu="yolov8n-pose.pt", cihaz="cpu"):
        self.model = YOLO(model_yolu)
        self.cihaz = cihaz

    def insanlari_tespit_et(self, kare):
        sonuc = self.model.track(source=kare, device=self.cihaz, persist=True, verbose=False)[0]

        insanlar = []
        if sonuc.boxes.id is None:
            return insanlar

        for box, keypoints, id_tensor in zip(sonuc.boxes.xyxy, sonuc.keypoints.xy, sonuc.boxes.id):
            x1, y1, x2, y2 = map(int, box.tolist())
            anahtarlar = keypoints.cpu().numpy()
            anahtarlar = np.hstack([anahtarlar, np.ones((17, 1))])  # dummy confidence
            kisi_id = int(id_tensor.item())

            insan = {
                "id": kisi_id,
                "kutu": (x1, y1, x2, y2),
                "anahtar_noktalar": anahtarlar.tolist()
            }
            insanlar.append(insan)

        return insanlar
