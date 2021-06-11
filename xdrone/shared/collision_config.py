from __future__ import annotations

import copy


class CollisionConfig:
    def __init__(self, collision_meters: float = 0, time_interval_seconds: float = 0.1,
                 confidence_threshold: float = 1.0):
        if collision_meters < 0:
            raise ValueError("collision_meters should >= 0")
        if time_interval_seconds <= 0:
            raise ValueError("time_interval_seconds should > 0")
        if confidence_threshold < 0 or confidence_threshold > 1:
            raise ValueError("confidence_threshold should between 0 and 1")
        self._collision_meters = collision_meters
        self._time_interval_seconds = time_interval_seconds
        self._confidence_threshold = confidence_threshold

    @property
    def collision_meters(self) -> float:
        return copy.deepcopy(self._collision_meters)

    @property
    def time_interval_seconds(self) -> float:
        return copy.deepcopy(self._time_interval_seconds)

    @property
    def confidence_threshold(self) -> float:
        return copy.deepcopy(self._confidence_threshold)

    def __str__(self):
        return "CollisionConfig: {{ collision_meters: {}, time_interval_seconds: {}, confidence_threshold: {} }}" \
            .format(self._collision_meters, self._time_interval_seconds, self._confidence_threshold)

    def __eq__(self, other):
        if isinstance(other, CollisionConfig):
            return other._collision_meters == self._collision_meters \
                   and other._time_interval_seconds == self._time_interval_seconds \
                   and other._confidence_threshold == self._confidence_threshold


class DefaultCollisionConfig(CollisionConfig):
    def __init__(self):
        super().__init__()
