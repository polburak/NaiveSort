import cv2
import numpy as np
from moduller.bot_sort.tracker.bot_sort import BoTSORT
from moduller.bot_sort.deep.reid import ReIDExtractor


class BotTakipYonetici:
    def __init__(self, config):
        reid_model_yolu = config["reid_model_path"]
        self.reid_extractor = ReIDExtractor(reid_model_yolu)

        self.tracker = BoTSORT(
            max_iou_distance=0.7,
            max_age=30,
            embedding_threshold=0.5
        )

    def takip_et(self, kutular, skorlar, frame):
        crops = []

        for bbox in kutular:
            x1, y1, x2, y2 = map(int, bbox)
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0 or crop.shape[0] < 10 or crop.shape[1] < 10:
                crop = np.zeros((128, 64, 3), dtype=np.uint8)
            crops.append(crop)

        embeddings = []
        for crop in crops:
            try:
                embedding = self.reid_extractor.extract(crop)
            except Exception as e:
                print(f"Embedding hatası: {e}")
                embedding = np.zeros((128,), dtype=np.float32)
            embeddings.append(embedding)

        embeddings = np.array(embeddings)
        takip_sonuclari = self.tracker.update(kutular, skorlar, frame, embeddings)
        return takip_sonuclari
