from ultralytics import YOLO
import numpy as np

class Tespitci:
    def __init__(self, model_yolu="yolov8n-pose.pt", cihaz="cpu"):
        self.model = YOLO(model_yolu)
        self.model.to(cihaz)
        self.cihaz = cihaz

    def insanlari_tespit_et(self, kare):
        sonuclar = self.model.track(
            source=kare,
            persist=True,
            conf=0.4,
            iou=0.3,
            stream=True,
            tracker="bytetrack.yaml"  # <-- işte bu eklendi
        )

        insanlar = []

        for sonuc in sonuclar:
            if sonuc.boxes.id is None or sonuc.keypoints is None:
                continue

            kutular = sonuc.boxes.xyxy.cpu().numpy().astype(int)
            idler = sonuc.boxes.id.int().cpu().numpy()

            xy = sonuc.keypoints.xy.cpu().numpy()      # (N, 17, 2)
            conf = sonuc.keypoints.conf.cpu().numpy()  # (N, 17)
            xyc = [np.hstack((x, c[:, None])) for x, c in zip(xy, conf)]  # (17, 3)

            for kutu, takip_id, kps in zip(kutular, idler, xyc):
                x1, y1, x2, y2 = kutu
                insan = {
                    "id": int(takip_id),
                    "kutu": (int(x1), int(y1), int(x2), int(y2)),
                    "anahtar_noktalar": kps.tolist()  # x, y, confidence
                }
                insanlar.append(insan)

        return insanlar
