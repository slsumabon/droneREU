class FixedPathStrategy:
    name = "baseline"

    def decide(self, detections):
        if detections:
            best = max(detections, key=lambda d: d["confidence"])
            return "continue_fixed_path", best, 0.0, "fixed_path"
        return "continue_fixed_path", None, 0.0, "fixed_path"