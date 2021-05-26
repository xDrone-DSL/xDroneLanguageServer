import json
from logging import warning
from typing import Dict

from xdrone.shared.boundary_config import BoundaryConfig
from xdrone.shared.collision_config import CollisionConfig, DefaultCollisionConfig
from xdrone.shared.drone_config import DroneConfig, DefaultDroneConfig


class ConfigParser:
    @staticmethod
    def parse(json_str: str) -> (Dict[str, DroneConfig], BoundaryConfig, CollisionConfig):
        data = json.loads(json_str)
        drone_config_map = ConfigParser._parse_drone_config(data)
        boundary_config = ConfigParser._parse_boundary_config(data)
        collision_config = ConfigParser._parse_collision_config(data)
        return drone_config_map, boundary_config, collision_config

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
    def _parse_boundary_config(data: dict) -> BoundaryConfig:
        if "boundary_config" in data:
            if "max_seconds" in data["boundary_config"]:
                max_seconds = data["boundary_config"]["max_seconds"]
            else:
                warning("'max_seconds' missing when parsing 'boundary_config', using default value inf. " +
                        "There will be no limit on 'max_seconds'.")
                max_seconds = float('inf')
            if "max_x_meters" in data["boundary_config"]:
                max_x_meters = data["boundary_config"]["max_x_meters"]
            else:
                warning("'max_x_meters' missing when parsing 'boundary_config', using default value inf. " +
                        "There will be no limit on 'max_x_meters'.")
                max_x_meters = float('inf')
            if "max_y_meters" in data["boundary_config"]:
                max_y_meters = data["boundary_config"]["max_y_meters"]
            else:
                warning("'max_y_meters' missing when parsing 'boundary_config', using default value inf. " +
                        "There will be no limit on 'max_y_meters'.")
                max_y_meters = float('inf')
            if "max_z_meters" in data["boundary_config"]:
                max_z_meters = data["boundary_config"]["max_z_meters"]
            else:
                warning("'max_z_meters' missing when parsing 'boundary_config', using default value inf. " +
                        "There will be no limit on 'max_z_meters'.")
                max_z_meters = float('inf')
            if "min_x_meters" in data["boundary_config"]:
                min_x_meters = data["boundary_config"]["min_x_meters"]
            else:
                warning("'min_x_meters' missing when parsing 'boundary_config', using default value -inf. " +
                        "There will be no limit on 'min_x_meters'.")
                min_x_meters = float('-inf')
            if "min_y_meters" in data["boundary_config"]:
                min_y_meters = data["boundary_config"]["min_y_meters"]
            else:
                warning("'min_y_meters' missing when parsing 'boundary_config', using default value -inf. " +
                        "There will be no limit on 'min_y_meters'.")
                min_y_meters = float('-inf')
            if "min_z_meters" in data["boundary_config"]:
                min_z_meters = data["boundary_config"]["min_z_meters"]
            else:
                warning("'min_z_meters' missing when parsing 'boundary_config', using default value -inf. " +
                        "There will be no limit on 'min_z_meters'.")
                min_z_meters = float('-inf')
            boundary_config = BoundaryConfig(max_seconds, max_x_meters, max_y_meters, max_z_meters,
                                             min_x_meters, min_y_meters, min_z_meters)
        else:
            warning("'boundary_config' missing when parsing configs, using unlimited boundary_config. " +
                    "Time and position will be unlimited.")
            boundary_config = BoundaryConfig.no_limit()
        return boundary_config

    @staticmethod
    def _parse_collision_config(data: dict) -> CollisionConfig:
        if "collision_config" in data:
            if "collision_meters" in data["collision_config"]:
                collision_meters = data["collision_config"]["collision_meters"]
            else:
                warning("'collision_meters' missing when parsing 'collision_config', using default value 0. " +
                        "There will be no limit on 'collision_meters'.")
                collision_meters = 0.0
            if "time_interval_seconds" in data["collision_config"]:
                collision_time_interval_seconds = data["collision_config"]["time_interval_seconds"]
            else:
                warning("'time_interval_seconds' missing when parsing 'collision_config', " +
                        "using default value 0.1.")
                collision_time_interval_seconds = 0.1
            collision_config = CollisionConfig(collision_meters, collision_time_interval_seconds)
        else:
            warning("'collision_config' missing when parsing configs, using default collision_config.")
            collision_config = DefaultCollisionConfig()
        return collision_config
