import json
from logging import warning
from typing import Dict

from xdrone.shared.drone_config import DroneConfig, DefaultDroneConfig
from xdrone.shared.safety_config import SafetyConfig


class ConfigParser:
    @staticmethod
    def parse(json_str: str) -> (Dict[str, DroneConfig], SafetyConfig):
        data = json.loads(json_str)
        drone_config_map = ConfigParser._parse_drone_config(data)
        safety_config = ConfigParser._parse_safety_config(data)
        return drone_config_map, safety_config

    @staticmethod
    def _parse_drone_config(data: dict) -> Dict[str, DroneConfig]:
        drone_config_map = {}
        if "drones" in data:
            if len(data["drones"]) == 0:
                warning("'drones' is empty when parsing configs, using default drone_config. " +
                        "Position estimation may be inaccurate.")
                return {"DEFAULT": DefaultDroneConfig()}
            for drone in data["drones"]:
                if "name" in drone:
                    name = drone["name"]
                    if name == "":
                        warning("'name' cannot be an empty string, using default value 'DEFAULT' instead.")
                        name = "DEFAULT"
                else:
                    warning("'name' missing when parsing object in 'drones', using default value 'DEFAULT'.")
                    name = "DEFAULT"

                if name in drone_config_map:
                    warning("Drone name '{}' appeared more than ones in 'drones', ignored.".format(name))
                    continue

                if "init_position" in drone:
                    position = drone["init_position"]
                    init_position = []
                    for dim in ["x", "y", "z"]:
                        if dim in position:
                            init_position.append(position[dim])
                        else:
                            warning("'{}' missing when parsing drone '{}', using default value 0. ".format(dim, name) +
                                    "Position estimation may be inaccurate.")
                            init_position.append(0)
                    init_position = tuple(init_position)
                else:
                    warning("'init_position' missing when parsing drone '{}', ".format(name) +
                            "using default value (0, 0, 0). " +
                            "Position estimation may be inaccurate.")
                    init_position = (0, 0, 0)
                if "speed_mps" in drone:
                    speed_mps = drone["speed_mps"]
                else:
                    warning("'speed_mps' missing when parsing drone '{}', ".format(name) +
                            "using default value 1. " +
                            "Position estimation may be inaccurate.")
                    speed_mps = 1
                if "rotate_speed_dps" in drone:
                    rotate_speed_dps = drone["rotate_speed_dps"]
                else:
                    warning("'rotate_speed_dps' missing when parsing drone '{}', ".format(name) +
                            "using default value 90. " +
                            "Position estimation may be inaccurate.")
                    rotate_speed_dps = 90
                if "takeoff_height_meters" in drone:
                    takeoff_height_meters = drone["takeoff_height_meters"]
                else:
                    warning("'takeoff_height_meters' missing when parsing drone '{}', ".format(name) +
                            "using default value 1. " +
                            "Position estimation may be inaccurate.")
                    takeoff_height_meters = 1

                drone_config = DroneConfig(init_position, speed_mps, rotate_speed_dps, takeoff_height_meters)
                drone_config_map[name] = drone_config
        else:
            warning("'drones' missing when parsing configs, using default drone_config. " +
                    "Position estimation may be inaccurate.")
            return {"DEFAULT": DefaultDroneConfig()}
        return drone_config_map

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
