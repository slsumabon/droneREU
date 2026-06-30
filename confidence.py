from collections import deque
import statistics
from config import CONFIDENCE_WINDOW


class ConfidenceFilter:
    def __init__(self, window_size=CONFIDENCE_WINDOW):
        self.values = deque(maxlen=window_size)

    def update(self, confidence):
        self.values.append(confidence)

    def median(self):
        if not self.values:
            return 0.0
        return statistics.median(self.values)

    def reset(self):
        self.values.clear()