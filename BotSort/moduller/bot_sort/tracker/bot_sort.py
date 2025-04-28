import numpy as np
from scipy.spatial.distance import cdist


class SimpleTrack:
    def __init__(self, track_id, bbox, embedding):
        self.track_id = track_id
        self.bbox = bbox
        self.embedding = embedding
        self.age = 0  # Kaç karedir görülmedi

    def update(self, bbox, embedding):
        self.bbox = bbox
        self.embedding = embedding
        self.age = 0


class BoTSORT:
    def __init__(self, max_iou_distance=0.7, max_age=30, embedding_threshold=0.8):
        self.tracks = []
        self.next_id = 0
        self.max_age = max_age
        self.embedding_threshold = embedding_threshold


    def _cosine_distance(self, a, b):
        a = np.asarray(a)
        b = np.asarray(b)
        return cdist(a, b, metric='cosine')

    def update(self, kutular, skorlar, frame, embeddings):
        aktif_ids = []
        yeni_trackler = []

        if len(kutular) == 0:
            for track in self.tracks:
                track.age += 1
            return []

        if len(self.tracks) > 0:
            track_embeddings = np.array([t.embedding for t in self.tracks])
            dists = self._cosine_distance(track_embeddings, embeddings)
        else:
            dists = np.full((0, len(kutular)), fill_value=1.0)

        kullanilan_track_idx = set()
        kullanilan_det_idx = set()
        eslesmeler = []

        for det_idx in range(len(kutular)):
            en_iyi_idx = -1
            en_iyi_dist = self.embedding_threshold

            for track_idx, track in enumerate(self.tracks):
                if track_idx in kullanilan_track_idx:
                    continue
                dist = dists[track_idx][det_idx]
                print(f"[Karşılaştırma] Track {track_idx} ↔ Det {det_idx} mesafe: {dist:.3f}")

                if dist < en_iyi_dist:
                    en_iyi_dist = dist
                    en_iyi_idx = track_idx

            if en_iyi_idx != -1:
                track = self.tracks[en_iyi_idx]
                track.update(kutular[det_idx], embeddings[det_idx])
                aktif_ids.append({
                    "id": track.track_id,
                    "bbox": kutular[det_idx],
                    "score": skorlar[det_idx],
                    "embedding": embeddings[det_idx]
                })
                kullanilan_track_idx.add(en_iyi_idx)
                kullanilan_det_idx.add(det_idx)

        for i in range(len(kutular)):
            if i not in kullanilan_det_idx:
                yeni_id = self.next_id
                self.next_id += 1
                yeni_track = SimpleTrack(yeni_id, kutular[i], embeddings[i])
                self.tracks.append(yeni_track)
                aktif_ids.append({
                    "id": yeni_id,
                    "bbox": kutular[i],
                    "score": skorlar[i],
                    "embedding": embeddings[i]
                })

        # Eski track'lerin yaşını artır
        for track in self.tracks:
            track.age += 1

        # Çok yaşlananları sil
        self.tracks = [t for t in self.tracks if t.age <= self.max_age]

        return aktif_ids
