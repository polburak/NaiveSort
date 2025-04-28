import numpy as np
import cv2
import onnxruntime as ort


class ReIDExtractor:
    def __init__(self, model_path):
        self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name

    def preprocess(self, image):
        image = cv2.resize(image, (64, 128))
        image = image[:, :, ::-1].astype(np.float32)  # BGR → RGB
        image /= 255.0
        image = np.transpose(image, (2, 0, 1))  # (HWC → CHW)
        image = np.expand_dims(image, axis=0)   # (1, 3, 128, 64)
        return image

    def extract(self, image):
        img_input = self.preprocess(image)

        try:
            embedding = self.session.run(None, {self.input_name: img_input})[0]
        except Exception as e:
            print(f"[ReID] ONNX çalıştırma hatası: {e}")
            return np.zeros((128,), dtype=np.float32)

        # NAN kontrolü
        if np.isnan(embedding).any():
            print("[ReID] NAN tespit edildi! Boş veya hatalı embedding.")
            return np.zeros((128,), dtype=np.float32)

        return embedding[0]
        print("[DEBUG] Embedding shape:", embedding.shape)
        print("[DEBUG] Embedding değerleri (ilk 5):", embedding[0][:5])

