import numpy as np

def iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = area1 + area2 - inter_area
    return inter_area / union_area if union_area > 0 else 0


class NaiveSortTracker:
    def __init__(self, iou_threshold=0.3, max_age=15):
        self.tracks = []
        self.next_id = 0
        self.iou_threshold = iou_threshold
        self.max_age = max_age

    def update(self, detections):
        updated_tracks = []
        used_detections = set()

        for track in self.tracks:
            best_iou = 0
            best_det_idx = -1
            for det_idx, det in enumerate(detections):
                if det_idx in used_detections:
                    continue
                iou_score = iou(track['bbox'], det)
                if iou_score > best_iou:
                    best_iou = iou_score
                    best_det_idx = det_idx

            if best_iou > self.iou_threshold:
                det = detections[best_det_idx]
                yeni_merkez = [(det[0]+det[2])/2, (det[1]+det[3])/2]
                eski_merkez = track.get('onceki_merkez')
                if eski_merkez:
                    dx = yeni_merkez[0] - eski_merkez[0]
                    dy = yeni_merkez[1] - eski_merkez[1]
                    hiz = (dx**2 + dy**2)**0.5
                else:
                    hiz = 0

                track['bbox'] = det
                track['onceki_merkez'] = yeni_merkez
                track['hiz'] = hiz
                track['age'] = 0
                used_detections.add(best_det_idx)
                updated_tracks.append(track)
            else:
                track['age'] += 1
                updated_tracks.append(track)

        for idx, det in enumerate(detections):
            if idx not in used_detections:
                merkez = [(det[0]+det[2])/2, (det[1]+det[3])/2]
                new_track = {
                    "id": self.next_id,
                    "bbox": det,
                    "age": 0,
                    "onceki_merkez": merkez,
                    "hiz": 0
                }
                self.next_id += 1
                updated_tracks.append(new_track)

        self.tracks = [t for t in updated_tracks if t['age'] <= self.max_age]
        return self.tracks
