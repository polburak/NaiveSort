class Tespitci:
    def __init__(self, yolo_model):
        self.model = yolo_model

    def insan_kutularini_tespit_et(self, kare):
        sonuc = self.model.predict(kare, conf=0.4, iou=0.5)[0]
        kutular = [box.xyxy[0].tolist() for box in sonuc.boxes]
        return kutular

