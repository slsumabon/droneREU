from ultralytics import YOLO
from config import MODEL_PATH, TARGET_LABELS, DETECTION_CONFIDENCE


class ObjectDetector:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]
        detections = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]
            confidence = float(box.conf[0])

            if confidence < DETECTION_CONFIDENCE:
                continue

            if TARGET_LABELS and label not in TARGET_LABELS:
                continue

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            detections.append({
                "label": label,
                "confidence": confidence,
                "bbox": (int(x1), int(y1), int(x2), int(y2)),
                "center": (int((x1 + x2) / 2), int((y1 + y2) / 2)),
                "width": int(x2 - x1),
                "height": int(y2 - y1),
            })

        return detections