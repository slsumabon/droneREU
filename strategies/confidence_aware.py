from confidence import ConfidenceFilter
from state_machine import ConfidenceStateMachine, FlightState
from planner import RefinementPlanner


class ConfidenceAwareStrategy:
    name = "adaptive"

    def __init__(self):
        self.conf_filter = ConfidenceFilter()
        self.state_machine = ConfidenceStateMachine()
        self.planner = RefinementPlanner()

    def decide(self, detections):
        if not detections:
            self.conf_filter.reset()
            self.planner.reset()
            state = self.state_machine.update(0.0, False)
            return "continue_search", None, 0.0, state.value

        best = max(detections, key=lambda d: d["confidence"])
        self.conf_filter.update(best["confidence"])

        filtered_conf = self.conf_filter.median()
        state = self.state_machine.update(filtered_conf, True)

        if state == FlightState.ACCEPT:
            action = "accept_detection_continue"
            self.planner.reset()

        elif state == FlightState.CANDIDATE:
            action = "hover_collect_more_frames"

        elif state == FlightState.REFINE:
            action = self.planner.next_action()

        elif state == FlightState.ABORT:
            action = "abort_target_continue"
            self.planner.reset()

        else:
            action = "continue_search"

        return action, best, filtered_conf, state.value