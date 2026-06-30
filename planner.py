from config import HOVER_TIME, ROTATE_ANGLE, FORWARD_DISTANCE, RIGHT_DISTANCE


class RefinementPlanner:
    def __init__(self):
        self.steps = [
            "hover_collect_frames",
            "rotate_left",
            "move_forward",
            "move_right",
            "abort_target"
        ]
        self.index = 0

    def next_action(self):
        if self.index >= len(self.steps):
            return "abort_target"

        action = self.steps[self.index]
        self.index += 1
        return action

    def reset(self):
        self.index = 0

    def action_details(self, action):
        return {
            "hover_collect_frames": {"seconds": HOVER_TIME},
            "rotate_left": {"degrees": ROTATE_ANGLE},
            "move_forward": {"meters": FORWARD_DISTANCE},
            "move_right": {"meters": RIGHT_DISTANCE},
            "abort_target": {}
        }.get(action, {})