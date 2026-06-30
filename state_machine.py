from enum import Enum
from config import LOW_CONFIDENCE, HIGH_CONFIDENCE, MAX_REFINEMENTS


class FlightState(Enum):
    SEARCH = "search"
    CANDIDATE = "candidate_detection"
    ACCEPT = "accept_detection"
    REFINE = "viewpoint_refinement"
    ABORT = "abort_target"


class ConfidenceStateMachine:
    def __init__(self):
        self.state = FlightState.SEARCH
        self.refinement_count = 0

    def update(self, confidence, detection_found):
        if not detection_found:
            self.state = FlightState.SEARCH
            self.refinement_count = 0
            return self.state

        if confidence >= HIGH_CONFIDENCE:
            self.state = FlightState.ACCEPT
            self.refinement_count = 0
            return self.state

        if confidence >= LOW_CONFIDENCE:
            self.state = FlightState.CANDIDATE
            return self.state

        if self.refinement_count < MAX_REFINEMENTS:
            self.refinement_count += 1
            self.state = FlightState.REFINE
            return self.state

        self.state = FlightState.ABORT
        self.refinement_count = 0
        return self.state