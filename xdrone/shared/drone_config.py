import copy


class DroneConfig:
    def __init__(self, init_position: tuple, speed_mps: float, rotate_speed_dps: float, takeoff_height_meters: float,
                 var_per_meter: float = 0.0, var_per_degree: float = 0.0):
        if speed_mps <= 0:
            raise ValueError("speed_mps should > 0")
        if rotate_speed_dps <= 0:
            raise ValueError("rotate_speed_dps should > 0")
        if takeoff_height_meters <= 0:
            raise ValueError("takeoff_height_meters should > 0")
        if var_per_meter < 0:
            raise ValueError("var_per_meter should >= 0")
        if var_per_degree < 0:
            raise ValueError("var_per_degree should >= 0")
        self._init_position = init_position
        self._speed_mps = speed_mps
        self._rotate_speed_dps = rotate_speed_dps
        self._takeoff_height_meters = takeoff_height_meters
        self._var_per_meter = var_per_meter
        self._var_per_degree = var_per_degree

    @property
    def init_position(self) -> tuple:
        return copy.deepcopy(self._init_position)

    @property
    def speed_mps(self) -> float:
        return copy.deepcopy(self._speed_mps)

    @property
    def rotate_speed_dps(self) -> float:
        return copy.deepcopy(self._rotate_speed_dps)

    @property
    def takeoff_height_meters(self) -> float:
        return copy.deepcopy(self._takeoff_height_meters)

    @property
    def var_per_meter(self) -> float:
        return copy.deepcopy(self._var_per_meter)

    @property
    def var_per_degree(self) -> float:
        return copy.deepcopy(self._var_per_degree)

    def __str__(self):
        return ("DroneConfig: {{ init_position: {}, speed_mps: {}, rotate_speed_dps: {}, takeoff_height_meters: {}, "
                .format(self._init_position, self._speed_mps, self._rotate_speed_dps, self._takeoff_height_meters) +
                "var_per_meter: {}, var_per_degree: {} }}".format(self._var_per_meter, self._var_per_degree))

    def __eq__(self, other):
        if isinstance(other, DroneConfig):
            return other._init_position == self._init_position and other._speed_mps == self._speed_mps \
                   and other._rotate_speed_dps == self._rotate_speed_dps \
                   and other._takeoff_height_meters == self._takeoff_height_meters \
                   and other._var_per_meter == self.var_per_meter and other._var_per_degree == self._var_per_degree
        return False


class DefaultDroneConfig(DroneConfig):
    def __init__(self):
        super().__init__(init_position=(0, 0, 0), speed_mps=1, rotate_speed_dps=90, takeoff_height_meters=1)
