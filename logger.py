import csv
import os
from datetime import datetime


class ExperimentLogger:
    def __init__(self, strategy_name, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file_path = os.path.join(
            log_dir,
            f"{strategy_name}_{timestamp}.csv"
        )

        self.headers = [
            "time",
            "strategy",
            "state",
            "action",
            "label",
            "confidence",
            "filtered_confidence",
            "bbox_x1",
            "bbox_y1",
            "bbox_x2",
            "bbox_y2",
            "center_x",
            "center_y",
            "width",
            "height",
        ]

        with open(self.file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)

    def log(self, strategy, state, action, detection, filtered_confidence):
        now = datetime.now().isoformat()

        if detection is None:
            row = [
                now, strategy, state, action,
                "", "", filtered_confidence,
                "", "", "", "", "", "", "", ""
            ]
        else:
            x1, y1, x2, y2 = detection["bbox"]
            cx, cy = detection["center"]

            row = [
                now,
                strategy,
                state,
                action,
                detection["label"],
                detection["confidence"],
                filtered_confidence,
                x1,
                y1,
                x2,
                y2,
                cx,
                cy,
                detection["width"],
                detection["height"],
            ]

        with open(self.file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)