import logging
import unittest

from xdrone.config_parsers.config_parser import ConfigParser
from xdrone.shared.boundary_config import BoundaryConfig
from xdrone.shared.collision_config import CollisionConfig, DefaultCollisionConfig
from xdrone.shared.drone_config import DroneConfig, DefaultDroneConfig


class ConfigParserTest(unittest.TestCase):
    def test_parse_if_provided_configs_should_parse_all_configs(self):
        config = """
            {
              "drones": [{
                "name": "DRONE1",
                "init_position": {"x": 1, "y": 2, "z": 3},
                "speed_mps": 2,
                "rotate_speed_dps": 180,
                "takeoff_height_meters": 2
              },{
                "name": "DRONE2",
                "init_position": {"x": 4, "y": 5, "z": 6},
                "speed_mps": 1,
                "rotate_speed_dps": 90,
                "takeoff_height_meters": 1
              }],
              "boundary_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              },
              "collision_config": {
                "collision_meters": 0.3,
                "time_interval_seconds": 0.5
              }
            }
            """
        actual_drone_config, actual_boundary_config, acutal_collision_config = ConfigParser.parse(config)
        expected_drone_configs = {"DRONE1": DroneConfig(init_position=(1, 2, 3), speed_mps=2,
                                                        rotate_speed_dps=180, takeoff_height_meters=2),
                                  "DRONE2": DroneConfig(init_position=(4, 5, 6), speed_mps=1,
                                                        rotate_speed_dps=90, takeoff_height_meters=1)}
        expected_boundary_config = BoundaryConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                                  min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        expected_collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5)
        self.assertEqual(expected_drone_configs, actual_drone_config)
        self.assertEqual(expected_boundary_config, actual_boundary_config)
        self.assertEqual(expected_collision_config, acutal_collision_config)

    def test_parse_if_not_provided_configs_should_use_default_configs(self):
        config = "{}"
        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_boundary_config, acutal_collision_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'drones' missing when parsing configs, using default drone_config. " +
                        "Position estimation may be inaccurate.",
                        "WARNING:root:'boundary_config' missing when parsing configs, using unlimited boundary_config. " +
                        "Time and position will be unlimited.",
                        "WARNING:root:'collision_config' missing when parsing configs, using default collision_config."]
        self.assertEqual(expected_log, log.output)
        self.assertEqual({"DEFAULT": DefaultDroneConfig()}, actual_drone_configs)
        self.assertEqual(BoundaryConfig.no_limit(), actual_boundary_config)
        self.assertEqual(DefaultCollisionConfig(), acutal_collision_config)

    def test_parse_if_configs_missing_fields_should_use_default_value(self):
        config = """
            {
              "drones": [],
              "boundary_config": {
              },
              "collision_config": {
              }
            }
            """
        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_boundary_config, actual_collision_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'drones' is empty when parsing configs, using default drone_config. " +
                        "Position estimation may be inaccurate.",
                        "WARNING:root:'max_seconds' missing when parsing 'boundary_config', " +
                        "using default value inf. There will be no limit on 'max_seconds'.",
                        "WARNING:root:'max_x_meters' missing when parsing 'boundary_config', " +
                        "using default value inf. There will be no limit on 'max_x_meters'.",
                        "WARNING:root:'max_y_meters' missing when parsing 'boundary_config', " +
                        "using default value inf. There will be no limit on 'max_y_meters'.",
                        "WARNING:root:'max_z_meters' missing when parsing 'boundary_config', " +
                        "using default value inf. There will be no limit on 'max_z_meters'.",
                        "WARNING:root:'min_x_meters' missing when parsing 'boundary_config', " +
                        "using default value -inf. There will be no limit on 'min_x_meters'.",
                        "WARNING:root:'min_y_meters' missing when parsing 'boundary_config', " +
                        "using default value -inf. There will be no limit on 'min_y_meters'.",
                        "WARNING:root:'min_z_meters' missing when parsing 'boundary_config', " +
                        "using default value -inf. There will be no limit on 'min_z_meters'.",
                        "WARNING:root:'collision_meters' missing when parsing 'collision_config', " +
                        "using default value 0. There will be no limit on 'collision_meters'.",
                        "WARNING:root:'time_interval_seconds' missing when parsing 'collision_config', " +
                        "using default value 0.1."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"DEFAULT": DefaultDroneConfig()}
        expected_boundary_config = BoundaryConfig(max_seconds=float("inf"), max_x_meters=float("inf"),
                                                  max_y_meters=float("inf"), max_z_meters=float("inf"),
                                                  min_x_meters=float("-inf"), min_y_meters=float("-inf"),
                                                  min_z_meters=float("-inf"))
        expected_collision_config = DefaultCollisionConfig()
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_boundary_config, actual_boundary_config)
        self.assertEqual(expected_collision_config, actual_collision_config)

    def test_parse_if_drone_object_missing_fields_should_use_default_value(self):
        config = """
            {
              "drones": [{}],
              "boundary_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              },
              "collision_config": {
                "collision_meters": 0.3,
                "time_interval_seconds": 0.5
              }
            }
            """
        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_boundary_config, actual_collision_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'name' missing when parsing object in 'drones', using default value 'DEFAULT'.",
                        "WARNING:root:'init_position' missing when parsing drone 'DEFAULT', " +
                        "using default value (0, 0, 0). Position estimation may be inaccurate.",
                        "WARNING:root:'speed_mps' missing when parsing drone 'DEFAULT', " +
                        "using default value 1. Position estimation may be inaccurate.",
                        "WARNING:root:'rotate_speed_dps' missing when parsing drone 'DEFAULT', " +
                        "using default value 90. Position estimation may be inaccurate.",
                        "WARNING:root:'takeoff_height_meters' missing when parsing drone 'DEFAULT', " +
                        "using default value 1. Position estimation may be inaccurate."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"DEFAULT": DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                         rotate_speed_dps=90, takeoff_height_meters=1)}
        expected_boundary_config = BoundaryConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                                  min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        expected_collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5)
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_boundary_config, actual_boundary_config)
        self.assertEqual(expected_collision_config, actual_collision_config)

    def test_parse_if_init_position_missing_fields_should_use_default_value(self):
        config = """
            {
              "drones": [{
                "name": "DRONE1",
                "init_position": {},
                "speed_mps": 2,
                "rotate_speed_dps": 180,
                "takeoff_height_meters": 2
              }],
              "boundary_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              },
              "collision_config": {
                "collision_meters": 0.3,
                "time_interval_seconds": 0.5
              }
            }
            """

        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_boundary_config, actual_collision_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'x' missing when parsing drone 'DRONE1', using default value 0. " +
                        "Position estimation may be inaccurate.",
                        "WARNING:root:'y' missing when parsing drone 'DRONE1', using default value 0. " +
                        "Position estimation may be inaccurate.",
                        "WARNING:root:'z' missing when parsing drone 'DRONE1', using default value 0. " +
                        "Position estimation may be inaccurate."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"DRONE1": DroneConfig(init_position=(0, 0, 0), speed_mps=2,
                                                        rotate_speed_dps=180, takeoff_height_meters=2)}
        expected_boundary_config = BoundaryConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                                  min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        expected_collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5)
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_boundary_config, actual_boundary_config)
        self.assertEqual(expected_collision_config, actual_collision_config)

    def test_parse_if_name_is_empty_string_should_use_default_value(self):
        config = """
            {
              "drones": [{
                "name": "",
                "init_position": {"x": 1, "y": 2, "z": 3},
                "speed_mps": 2,
                "rotate_speed_dps": 180,
                "takeoff_height_meters": 2
              }],
              "boundary_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              },
              "collision_config": {
                "collision_meters": 0.3,
                "time_interval_seconds": 0.5
              }
            }
            """

        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_boundary_config, actual_collision_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'name' cannot be an empty string, using default value 'DEFAULT' instead."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"DEFAULT": DroneConfig(init_position=(1, 2, 3), speed_mps=2,
                                                         rotate_speed_dps=180, takeoff_height_meters=2)}
        expected_boundary_config = BoundaryConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                                  min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        expected_collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5)
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_boundary_config, actual_boundary_config)
        self.assertEqual(expected_collision_config, actual_collision_config)

    def test_parse_if_name_repeated_should_ignore_second_appearance(self):
        config = """
            {
              "drones": [{
                "name": "DRONE1",
                "init_position": {"x": 1, "y": 2, "z": 3},
                "speed_mps": 2,
                "rotate_speed_dps": 180,
                "takeoff_height_meters": 2
              },{
                "name": "DRONE1",
                "init_position": {"x": 4, "y": 5, "z": 6},
                "speed_mps": 1,
                "rotate_speed_dps": 90,
                "takeoff_height_meters": 1
              }],
              "boundary_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              },
              "collision_config": {
                "collision_meters": 0.3,
                "time_interval_seconds": 0.5
              }
            }
            """

        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_boundary_config, actual_collision_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:Drone name 'DRONE1' appeared more than ones in 'drones', ignored."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"DRONE1": DroneConfig(init_position=(1, 2, 3), speed_mps=2,
                                                        rotate_speed_dps=180, takeoff_height_meters=2)}
        expected_boundary_config = BoundaryConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                                  min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        expected_collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5)
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_boundary_config, actual_boundary_config)
        self.assertEqual(expected_collision_config, actual_collision_config)
