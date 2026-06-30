import argparse
import cv2
import time

from config import CAMERA_INDEX
from detector import ObjectDetector
from logger import ExperimentLogger
from strategies.fixed_path import FixedPathStrategy
from strategies.confidence_aware import ConfidenceAwareStrategy


def draw_detections(frame, detections):
    for d in detections:
        x1, y1, x2, y2 = d["bbox"]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(
            frame,
            f"{d['label']} {d['confidence']:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )


def run_experiment(strategy):
    detector = ObjectDetector()
    logger = ExperimentLogger(strategy.name)

    cap = cv2.VideoCapture(CAMERA_INDEX)

    print(f"Running {strategy.name.upper()} experiment.")
    print("Press q to quit.")

    start_time = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("No camera frame.")
            break

        detections = detector.detect(frame)

        action, best_detection, filtered_conf, state = strategy.decide(detections)

        logger.log(
            strategy=strategy.name,
            state=state,
            action=action,
            detection=best_detection,
            filtered_confidence=filtered_conf
        )

        draw_detections(frame, detections)

        cv2.putText(
            frame,
            f"Strategy: {strategy.name} | State: {state} | Action: {action}",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Filtered Confidence: {filtered_conf:.2f}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.imshow("Confidence-Aware UAV Experiment", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    duration = time.time() - start_time

    print(f"Experiment finished in {duration:.2f} seconds.")
    print(f"Log saved to: {logger.file_path}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--strategy",
        choices=["baseline", "adaptive"],
        required=True,
        help="Choose baseline fixed-path or adaptive confidence-aware strategy."
    )

    args = parser.parse_args()

    if args.strategy == "baseline":
        strategy = FixedPathStrategy()
    else:
        strategy = ConfidenceAwareStrategy()

    run_experiment(strategy)


if __name__ == "__main__":
    main()