import json
from logging import warning

from xdrone.shared.drone_config import DroneConfig, DefaultDroneConfig
from xdrone.shared.safety_config import SafetyConfig


class ConfigParser:
    @staticmethod
    def parse(json_str: str) -> (DroneConfig, SafetyConfig):
        data = json.loads(json_str)
        drone_config = ConfigParser._parse_drone_config(data)
        safety_config = ConfigParser._parse_safety_config(data)
        return drone_config, safety_config

    @staticmethod
    def _parse_drone_config(data: dict) -> DroneConfig:
        if "drone_config" in data:
            if "speed_mps" in data["drone_config"]:
                speed_mps = data["drone_config"]["speed_mps"]
            else:
                warning("'speed_mps' missing when parsing 'drone_config', using default value 1. " +
                        "Position estimation may be inaccurate.")
                speed_mps = 1
            if "rotate_speed_dps" in data["drone_config"]:
                rotate_speed_dps = data["drone_config"]["rotate_speed_dps"]
            else:
                warning("'rotate_speed_dps' missing when parsing 'drone_config', using default value 90. " +
                        "Position estimation may be inaccurate.")
                rotate_speed_dps = 90
            if "takeoff_height_meters" in data["drone_config"]:
                takeoff_height_meters = data["drone_config"]["takeoff_height_meters"]
            else:
                warning("'takeoff_height_meters' missing when parsing 'drone_config', " +
                        "using default value 1. " +
                        "Position estimation may be inaccurate.")
                takeoff_height_meters = 1
            drone_config = DroneConfig(speed_mps, rotate_speed_dps, takeoff_height_meters)
        else:
            warning("'drone_config' missing when parsing configs, using default drone_config. " +
                    "Position estimation may be inaccurate.")
            drone_config = DefaultDroneConfig()
        return drone_config

    @staticmethod
    def _parse_safety_config(data: dict) -> SafetyConfig:
        if "safety_config" in data:
            if "max_seconds" in data["safety_config"]:
                max_seconds = data["safety_config"]["max_seconds"]
            else:
                warning("'max_seconds' missing when parsing 'safety_config', using default value inf. " +
                        "There will be no limit on 'max_seconds'.")
                max_seconds = float('inf')
            if "max_x_meters" in data["safety_config"]:
                max_x_meters = data["safety_config"]["max_x_meters"]
            else:
                warning("'max_x_meters' missing when parsing 'safety_config', using default value inf. " +
                        "There will be no limit on 'max_x_meters'.")
                max_x_meters = float('inf')
            if "max_y_meters" in data["safety_config"]:
                max_y_meters = data["safety_config"]["max_y_meters"]
            else:
                warning("'max_y_meters' missing when parsing 'safety_config', using default value inf. " +
                        "There will be no limit on 'max_y_meters'.")
                max_y_meters = float('inf')
            if "max_z_meters" in data["safety_config"]:
                max_z_meters = data["safety_config"]["max_z_meters"]
            else:
                warning("'max_z_meters' missing when parsing 'safety_config', using default value inf. " +
                        "There will be no limit on 'max_z_meters'.")
                max_z_meters = float('inf')
            if "min_x_meters" in data["safety_config"]:
                min_x_meters = data["safety_config"]["min_x_meters"]
            else:
                warning("'min_x_meters' missing when parsing 'safety_config', using default value -inf. " +
                        "There will be no limit on 'min_x_meters'.")
                min_x_meters = float('-inf')
            if "min_y_meters" in data["safety_config"]:
                min_y_meters = data["safety_config"]["min_y_meters"]
            else:
                warning("'min_y_meters' missing when parsing 'safety_config', using default value -inf. " +
                        "There will be no limit on 'min_y_meters'.")
                min_y_meters = float('-inf')
            if "min_z_meters" in data["safety_config"]:
                min_z_meters = data["safety_config"]["min_z_meters"]
            else:
                warning("'min_z_meters' missing when parsing 'safety_config', using default value -inf. " +
                        "There will be no limit on 'min_z_meters'.")
                min_z_meters = float('-inf')
            safety_config = SafetyConfig(max_seconds, max_x_meters, max_y_meters, max_z_meters,
                                         min_x_meters, min_y_meters, min_z_meters, )
        else:
            warning("'safety_config' missing when parsing configs, using unlimited safety_config. " +
                    "Time and position will be unlimited.")
            safety_config = SafetyConfig.no_limit()
        return safety_config
