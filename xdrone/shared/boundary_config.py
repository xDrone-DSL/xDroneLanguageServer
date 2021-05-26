from __future__ import annotations

from xdrone.shared.safety_check_error import SafetyCheckError
from xdrone.shared.state import State


class BoundaryConfig:
    def __init__(self, max_seconds: float = float('inf'),
                 max_x_meters: float = float('inf'), max_y_meters: float = float('inf'),
                 max_z_meters: float = float('inf'), min_x_meters: float = float('-inf'),
                 min_y_meters: float = float('-inf'), min_z_meters: float = float('-inf')):
        if max_seconds < 0:
            raise ValueError("max_seconds should >= 0")
        if max_x_meters < min_x_meters:
            raise ValueError("max_x_meters should >= min_x_meters")
        if max_y_meters < min_y_meters:
            raise ValueError("max_y_meters should >= min_y_meters")
        if max_z_meters < min_z_meters:
            raise ValueError("max_z_meters should >= min_z_meters")
        self._max_seconds = max_seconds
        self._max_x_meters = max_x_meters
        self._max_y_meters = max_y_meters
        self._max_z_meters = max_z_meters
        self._min_x_meters = min_x_meters
        self._min_y_meters = min_y_meters
        self._min_z_meters = min_z_meters

    @staticmethod
    def no_limit() -> BoundaryConfig:
        return BoundaryConfig()

    def __str__(self):
        return ("BoundaryConfig: {{ max_seconds: {}, x_range_meters: {}, y_range_meters: {}, z_range_meters: {} }}"
                .format(self._max_seconds, (self._min_x_meters, self._max_x_meters),
                        (self._min_y_meters, self._max_y_meters), (self._min_z_meters, self._max_z_meters)))

    def __eq__(self, other):
        if isinstance(other, BoundaryConfig):
            return other._max_seconds == self._max_seconds and other._max_x_meters == self._max_x_meters \
                   and other._max_y_meters == self._max_y_meters and other._max_z_meters == self._max_z_meters \
                   and other._min_x_meters == self._min_x_meters and other._min_y_meters == self._min_y_meters \
                   and other._min_z_meters == self._min_z_meters
        return False

    def check_state(self, drone_name: str, state: State) -> None:
        if state.x_meters > self._max_x_meters:
            raise SafetyCheckError("Drone '{}': the x coordinate {} will go beyond its upper limit {}"
                                   .format(drone_name, state.x_meters, self._max_x_meters))
        if state.y_meters > self._max_y_meters:
            raise SafetyCheckError("Drone '{}': the y coordinate {} will go beyond its upper limit {}"
                                   .format(drone_name, state.y_meters, self._max_y_meters))
        if state.z_meters > self._max_z_meters:
            raise SafetyCheckError("Drone '{}': the z coordinate {} will go beyond its upper limit {}"
                                   .format(drone_name, state.z_meters, self._max_z_meters))
        if state.x_meters < self._min_x_meters:
            raise SafetyCheckError("Drone '{}': the x coordinate {} will go beyond its lower limit {}"
                                   .format(drone_name, state.x_meters, self._min_x_meters))
        if state.y_meters < self._min_y_meters:
            raise SafetyCheckError("Drone '{}': the y coordinate {} will go beyond its lower limit {}"
                                   .format(drone_name, state.y_meters, self._min_y_meters))
        if state.z_meters < self._min_z_meters:
            raise SafetyCheckError("Drone '{}': the z coordinate {} will go beyond its lower limit {}"
                                   .format(drone_name, state.z_meters, self._min_z_meters))
        if state.time_used_seconds > self._max_seconds:
            raise SafetyCheckError("Drone '{}': the time used {} seconds will go beyond the time limit {} seconds"
                                   .format(drone_name, state.time_used_seconds, self._max_seconds))
