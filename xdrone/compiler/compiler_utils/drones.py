import copy

from xdrone.shared.drone_config import DroneConfig, DefaultDroneConfig


class Drone:
    def __init__(self, name: str, config: DroneConfig):
        self._name = name
        self._config = config

    @property
    def name(self) -> str:
        return copy.deepcopy(self._name)

    @property
    def config(self) -> DroneConfig:
        return copy.deepcopy(self._config)

    def __str__(self):
        return "Drone: {{ name: {}, config: {} }}".format(self._name, self._config)

    def __eq__(self, other):
        if isinstance(other, Drone):
            return other._name == self._name and other._config == self._config
        return False


class NullDrone(Drone):
    def __init__(self):
        super().__init__("null", DefaultDroneConfig())

    def __str__(self):
        return "NullDrone: { }"

    def __eq__(self, other):
        return isinstance(other, NullDrone)
