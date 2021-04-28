import logging
import unittest

from xdrone.config_parsers.config_parser import ConfigParser
from xdrone.shared.drone_config import DroneConfig, DefaultDroneConfig
from xdrone.shared.safety_config import SafetyConfig


class ConfigParserTest(unittest.TestCase):
    def test_parse_if_provided_configs_should_parse_all_configs(self):
        config = """
            {
              "drones": [{
                "name": "drone1",
                "init_position": {"x": 1, "y": 2, "z": 3},
                "speed_mps": 2,
                "rotate_speed_dps": 180,
                "takeoff_height_meters": 2
              },{
                "name": "drone2",
                "init_position": {"x": 4, "y": 5, "z": 6},
                "speed_mps": 1,
                "rotate_speed_dps": 90,
                "takeoff_height_meters": 1
              }],
              "safety_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              }
            }
            """
        actual_drone_config, actual_safety_config = ConfigParser.parse(config)
        expected_drone_configs = {"drone1": DroneConfig(init_position=(1, 2, 3), speed_mps=2,
                                                        rotate_speed_dps=180, takeoff_height_meters=2),
                                  "drone2": DroneConfig(init_position=(4, 5, 6), speed_mps=1,
                                                        rotate_speed_dps=90, takeoff_height_meters=1)}
        expected_safety_config = SafetyConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                              min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        self.assertEqual(expected_drone_configs, actual_drone_config)
        self.assertEqual(expected_safety_config, actual_safety_config)

    def test_parse_if_not_provided_configs_should_use_default_configs(self):
        config = "{}"
        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_safety_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'drones' missing when parsing configs, using default drone_config. " +
                        "Position estimation may be inaccurate.",
                        "WARNING:root:'safety_config' missing when parsing configs, using unlimited safety_config. " +
                        "Time and position will be unlimited."]
        self.assertEqual(expected_log, log.output)
        self.assertEqual({"default": DefaultDroneConfig()}, actual_drone_configs)
        self.assertEqual(SafetyConfig.no_limit(), actual_safety_config)

    def test_parse_if_configs_missing_fields_should_use_default_value(self):
        config = """
            {
              "drones": [],
              "safety_config": {
              }
            }
            """
        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_safety_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'drones' is empty when parsing configs, using default drone_config. " +
                        "Position estimation may be inaccurate.",
                        "WARNING:root:'max_seconds' missing when parsing 'safety_config', " +
                        "using default value inf. There will be no limit on 'max_seconds'.",
                        "WARNING:root:'max_x_meters' missing when parsing 'safety_config', " +
                        "using default value inf. There will be no limit on 'max_x_meters'.",
                        "WARNING:root:'max_y_meters' missing when parsing 'safety_config', " +
                        "using default value inf. There will be no limit on 'max_y_meters'.",
                        "WARNING:root:'max_z_meters' missing when parsing 'safety_config', " +
                        "using default value inf. There will be no limit on 'max_z_meters'.",
                        "WARNING:root:'min_x_meters' missing when parsing 'safety_config', " +
                        "using default value -inf. There will be no limit on 'min_x_meters'.",
                        "WARNING:root:'min_y_meters' missing when parsing 'safety_config', " +
                        "using default value -inf. There will be no limit on 'min_y_meters'.",
                        "WARNING:root:'min_z_meters' missing when parsing 'safety_config', " +
                        "using default value -inf. There will be no limit on 'min_z_meters'."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"default": DefaultDroneConfig()}
        expected_safety_config = SafetyConfig(max_seconds=float("inf"), max_x_meters=float("inf"),
                                              max_y_meters=float("inf"), max_z_meters=float("inf"),
                                              min_x_meters=float("-inf"), min_y_meters=float("-inf"),
                                              min_z_meters=float("-inf"))
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_safety_config, actual_safety_config)

    def test_parse_if_drone_object_missing_fields_should_use_default_value(self):
        config = """
            {
              "drones": [{}],
              "safety_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              }
            }
            """
        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_safety_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'name' missing when parsing object in 'drones', using default value 'default'.",
                        "WARNING:root:'init_position' missing when parsing drone 'default', " +
                        "using default value (0, 0, 0). Position estimation may be inaccurate.",
                        "WARNING:root:'speed_mps' missing when parsing drone 'default', " +
                        "using default value 1. Position estimation may be inaccurate.",
                        "WARNING:root:'rotate_speed_dps' missing when parsing drone 'default', " +
                        "using default value 90. Position estimation may be inaccurate.",
                        "WARNING:root:'takeoff_height_meters' missing when parsing drone 'default', " +
                        "using default value 1. Position estimation may be inaccurate."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"default": DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                         rotate_speed_dps=90, takeoff_height_meters=1)}
        expected_safety_config = SafetyConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                              min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_safety_config, actual_safety_config)

    def test_parse_if_init_position_missing_fields_should_use_default_value(self):
        config = """
            {
              "drones": [{
                "name": "drone1",
                "init_position": {},
                "speed_mps": 2,
                "rotate_speed_dps": 180,
                "takeoff_height_meters": 2
              }],
              "safety_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              }
            }
            """

        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_safety_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'x' missing when parsing drone 'drone1', using default value 0. " +
                        "Position estimation may be inaccurate.",
                        "WARNING:root:'y' missing when parsing drone 'drone1', using default value 0. " +
                        "Position estimation may be inaccurate.",
                        "WARNING:root:'z' missing when parsing drone 'drone1', using default value 0. " +
                        "Position estimation may be inaccurate."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"drone1": DroneConfig(init_position=(0, 0, 0), speed_mps=2,
                                                        rotate_speed_dps=180, takeoff_height_meters=2)}
        expected_safety_config = SafetyConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                              min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_safety_config, actual_safety_config)

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
              "safety_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              }
            }
            """

        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_safety_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:'name' cannot be an empty string, using default value 'default' instead."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"default": DroneConfig(init_position=(1, 2, 3), speed_mps=2,
                                                         rotate_speed_dps=180, takeoff_height_meters=2)}
        expected_safety_config = SafetyConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                              min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_safety_config, actual_safety_config)

    def test_parse_if_name_repeated_should_ignore_second_appearance(self):
        config = """
            {
              "drones": [{
                "name": "drone1",
                "init_position": {"x": 1, "y": 2, "z": 3},
                "speed_mps": 2,
                "rotate_speed_dps": 180,
                "takeoff_height_meters": 2
              },{
                "name": "drone1",
                "init_position": {"x": 4, "y": 5, "z": 6},
                "speed_mps": 1,
                "rotate_speed_dps": 90,
                "takeoff_height_meters": 1
              }],
              "safety_config": {
                "max_seconds": 100,
                "max_x_meters": 10,
                "max_y_meters": 20,
                "max_z_meters": 30,
                "min_x_meters": -10,
                "min_y_meters": -20,
                "min_z_meters": -30
              }
            }
            """

        with self.assertLogs(logging.getLogger()) as log:
            actual_drone_configs, actual_safety_config = ConfigParser.parse(config)
        expected_log = ["WARNING:root:Drone name 'drone1' appeared more than ones in 'drones', ignored."]
        self.assertEqual(expected_log, log.output)
        expected_drone_configs = {"drone1": DroneConfig(init_position=(1, 2, 3), speed_mps=2,
                                                        rotate_speed_dps=180, takeoff_height_meters=2)}
        expected_safety_config = SafetyConfig(max_seconds=100, max_x_meters=10, max_y_meters=20, max_z_meters=30,
                                              min_x_meters=-10, min_y_meters=-20, min_z_meters=-30)
        self.assertEqual(expected_drone_configs, actual_drone_configs)
        self.assertEqual(expected_safety_config, actual_safety_config)
