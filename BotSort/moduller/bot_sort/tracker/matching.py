import numpy as np
from scipy.optimize import linear_sum_assignment


def iou(bbox, candidates):
    bbox_tl = bbox[:2]
    bbox_br = bbox[:2] + bbox[2:]
    candidates_tl = candidates[:, :2]
    candidates_br = candidates[:, :2] + candidates[:, 2:]

    tl = np.maximum(bbox_tl, candidates_tl)
    br = np.minimum(bbox_br, candidates_br)
    wh = np.maximum(0., br - tl)

    area_intersection = wh[:, 0] * wh[:, 1]
    area_bbox = bbox[2] * bbox[3]
    area_candidates = candidates[:, 2] * candidates[:, 3]

    return area_intersection / (area_bbox + area_candidates - area_intersection)


def cosine_distance(a, b):
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=1, keepdims=True)
    return 1.0 - np.dot(a_norm, b_norm.T)


def iou_distance(a, b):
    if len(a) == 0 or len(b) == 0:
        return np.empty((len(a), len(b)))
    return 1. - np.array([[iou(bb, b) for b in b] for bb in a])


def matching_cascade(distance_metric, max_distance, tracks, detections, track_indices=None, detection_indices=None):
    if track_indices is None:
        track_indices = list(range(len(tracks)))
    if detection_indices is None:
        detection_indices = list(range(len(detections)))

    unmatched_tracks = []
    matches = []
    unmatched_detections = list(detection_indices)

    if len(track_indices) == 0 or len(detection_indices) == 0:
        return matches, track_indices, unmatched_detections

    cost_matrix = distance_metric(tracks, detections)
    cost_matrix = cost_matrix[track_indices][:, detection_indices]

    row_indices, col_indices = linear_sum_assignment(cost_matrix)

    for row, col in zip(row_indices, col_indices):
        if cost_matrix[row, col] > max_distance:
            unmatched_tracks.append(track_indices[row])
        else:
            matches.append((track_indices[row], detection_indices[col]))
            unmatched_detections.remove(detection_indices[col])

    unmatched_tracks += [i for i in track_indices if i not in [m[0] for m in matches]]
    return matches, unmatched_tracks, unmatched_detections
