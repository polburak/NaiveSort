from moduller.bot_tracker import BotTakipYonetici


class Tespitci:
    def __init__(self, yolo_model, config):
        self.model = yolo_model
        self.takip_yonetici = BotTakipYonetici(config)

    def insanlari_tespit_et(self, kare):
        sonuc = self.model.predict(kare, conf=0.4, iou=0.5)[0]

        kutular = []
        skorlar = []
        pozlar = []

        # Kutu ve skor bilgilerini al
        for box in sonuc.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            skor = float(box.conf[0])
            kutular.append([x1.item(), y1.item(), x2.item(), y2.item()])
            skorlar.append(skor)

        # Pose keypoints (her kişi için)
        for pose in sonuc.keypoints:
            pozlar.append(pose.xy[0].cpu().numpy())

        # Takip sistemi ile ID eşleştirmeli sonuçlar
        takip_sonuclari = self.takip_yonetici.takip_et(kutular, skorlar, kare)

        # Takip sonuçları ile poz verilerini eşleştir
        insanlar = []
        for i, takip in enumerate(takip_sonuclari):
            insan = {
                "id": takip["id"],
                "bbox": takip["bbox"],
                "score": takip["score"],
                "pose": pozlar[i] if i < len(pozlar) else None
            }
            insanlar.append(insan)

        return insanlar
