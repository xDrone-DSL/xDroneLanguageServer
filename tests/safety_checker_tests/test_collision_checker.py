import unittest
from unittest.mock import patch, mock_open, Mock

from xdrone.safety_checker.collision_checker import CollisionChecker
from xdrone.shared.collision_config import CollisionConfig
from xdrone.shared.command import Command, SingleDroneCommand, ParallelDroneCommands
from xdrone.shared.drone_config import DroneConfig
from xdrone.shared.safety_check_error import SafetyCheckError
from xdrone.state_updaters.state_updater import StateUpdater


class CollisionCheckerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.1)
        self.drone_config_map = {"DRONE1": DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                       rotate_speed_dps=90, takeoff_height_meters=1),
                                 "DRONE2": DroneConfig(init_position=(1, 0, 0), speed_mps=2,
                                                       rotate_speed_dps=180, takeoff_height_meters=1)}
        self.state_updater_map = {"DRONE1": StateUpdater(DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                                     rotate_speed_dps=90, takeoff_height_meters=1)),
                                  "DRONE2": StateUpdater(DroneConfig(init_position=(1, 0, 0), speed_mps=2,
                                                                     rotate_speed_dps=180, takeoff_height_meters=1))}

        self.collision_checker = CollisionChecker(self.drone_config_map, self.collision_config)

    def test_check_no_collision_should_not_give_error(self):
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.land())]
        self.collision_checker.check(drone_commands, self.state_updater_map)

    def test_check_bad_collision_config_should_not_give_error(self):
        collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.001)
        collision_checker = CollisionChecker(self.drone_config_map, collision_config)
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.land())]
        with self.assertRaises(SafetyCheckError) as context:
            collision_checker.check(drone_commands, self.state_updater_map)
        self.assertTrue("Error occurred during collision check, please retry with a better collision_config."
                        in str(context.exception))

    def test_check_with_large_variance_should_perform_not_like_determined(self):
        collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.1, confidence_threshold=0.95)
        drone_config_map = {"DRONE1": DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                  rotate_speed_dps=90, takeoff_height_meters=1,
                                                  var_per_meter=100),
                            "DRONE2": DroneConfig(init_position=(1, 0, 0), speed_mps=2,
                                                  rotate_speed_dps=180, takeoff_height_meters=1,
                                                  var_per_meter=100)}
        collision_checker = CollisionChecker(drone_config_map, collision_config)

        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE2", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.right(1)),
                          SingleDroneCommand("DRONE1", Command.left(1)),
                          SingleDroneCommand("DRONE1", Command.land()),
                          SingleDroneCommand("DRONE2", Command.land())]

        collision_checker.check(drone_commands, self.state_updater_map)

    def test_check_with_small_variance_should_perform_similar_to_determined(self):
        collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.1, confidence_threshold=0.99)
        drone_config_map = {"DRONE1": DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                  rotate_speed_dps=90, takeoff_height_meters=1,
                                                  var_per_meter=0.001),
                            "DRONE2": DroneConfig(init_position=(1, 0, 0), speed_mps=2,
                                                  rotate_speed_dps=180, takeoff_height_meters=1,
                                                  var_per_meter=0.001)}
        collision_checker = CollisionChecker(drone_config_map, collision_config)

        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE2", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.right(1)),
                          SingleDroneCommand("DRONE1", Command.left(1)),
                          SingleDroneCommand("DRONE1", Command.land()),
                          SingleDroneCommand("DRONE2", Command.land())]

        with self.assertRaises(SafetyCheckError) as context:
            collision_checker.check(drone_commands, self.state_updater_map)
        self.assertTrue("Collision might happen between DRONE1 and DRONE2, at time 2.4s, " +
                        "near position (x=0.95m, y=0.0m, z=1.0m), distance=0.1m, confidence=99.968%"
                        in str(context.exception))
        self.assertTrue("Collision might happen between DRONE1 and DRONE2, at time 2.6s, " +
                        "near position (x=0.95m, y=0.0m, z=1.0m), distance=0.1m, confidence=99.949%"
                        in str(context.exception))

    def test_check_with_zero_variance_should_perform_as_determined(self):
        collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.1, confidence_threshold=1.0)
        drone_config_map = {"DRONE1": DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                  rotate_speed_dps=90, takeoff_height_meters=1,
                                                  var_per_meter=0),
                            "DRONE2": DroneConfig(init_position=(1, 0, 0), speed_mps=2,
                                                  rotate_speed_dps=180, takeoff_height_meters=1,
                                                  var_per_meter=0)}
        collision_checker = CollisionChecker(drone_config_map, collision_config)

        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE2", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.right(1)),
                          SingleDroneCommand("DRONE1", Command.left(1)),
                          SingleDroneCommand("DRONE1", Command.land()),
                          SingleDroneCommand("DRONE2", Command.land())]

        with self.assertRaises(SafetyCheckError) as context:
            collision_checker.check(drone_commands, self.state_updater_map)
        self.assertTrue("Collision might happen between DRONE1 and DRONE2, at time 2.2s, " +
                        "near position (x=0.85m, y=0.0m, z=1.0m), distance=0.3m, confidence=100.000%"
                        in str(context.exception))
        self.assertTrue("Collision might happen between DRONE1 and DRONE2, at time 2.8s, " +
                        "near position (x=0.85m, y=0.0m, z=1.0m), distance=0.3m, confidence=100.000%"
                        in str(context.exception))

    def test_check_single_drone_command_should_detect_collision_and_give_error(self):
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE2", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.right(1)),
                          SingleDroneCommand("DRONE2", Command.wait(1)),
                          SingleDroneCommand("DRONE2", Command.rotate_left(90)),
                          SingleDroneCommand("DRONE2", Command.forward(1)),
                          SingleDroneCommand("DRONE1", Command.land()),
                          SingleDroneCommand("DRONE2", Command.land())]

        with self.assertRaises(SafetyCheckError) as context:
            self.collision_checker.check(drone_commands, self.state_updater_map)
        self.assertTrue("Collisions might happen!\nCollision might happen between DRONE1 and DRONE2"
                        in str(context.exception))

    def test_check_parallel_drone_command_should_detect_collision_and_give_error(self):
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE2", Command.takeoff()),
                          ParallelDroneCommands([
                              [SingleDroneCommand("DRONE1", Command.right(1))],
                              [SingleDroneCommand("DRONE2", Command.left(1))]
                          ]),
                          SingleDroneCommand("DRONE1", Command.land()),
                          SingleDroneCommand("DRONE2", Command.land())]

        with self.assertRaises(SafetyCheckError) as context:
            self.collision_checker.check(drone_commands, self.state_updater_map)
        self.assertTrue("Collisions might happen!\nCollision might happen between DRONE1 and DRONE2"
                        in str(context.exception))

    @patch('xdrone.safety_checker.collision_checker.CollisionLogSaver.save_check_log')
    def test_check_with_save_log_flag_should_call_log_saver(self, mock_save_check_log):
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.land())]
        self.collision_checker.check(drone_commands, self.state_updater_map, save_check_log=True)
        mock_save_check_log.assert_called()


class CollisionLogSaverTest(unittest.TestCase):
    def setUp(self) -> None:
        self.collision_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.1)
        self.drone_config_map = {"DRONE1": DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                       rotate_speed_dps=90, takeoff_height_meters=1),
                                 "DRONE2": DroneConfig(init_position=(1, 0, 0), speed_mps=2,
                                                       rotate_speed_dps=180, takeoff_height_meters=1)}
        self.state_updater_map = {"DRONE1": StateUpdater(DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                                     rotate_speed_dps=90, takeoff_height_meters=1)),
                                  "DRONE2": StateUpdater(DroneConfig(init_position=(1, 0, 0), speed_mps=2,
                                                                     rotate_speed_dps=180, takeoff_height_meters=1))}

        self.collision_checker = CollisionChecker(self.drone_config_map, self.collision_config)

    @patch('os.path.isdir')
    @patch('os.path.join')
    @patch('os.mkdir')
    @patch('builtins.open', new_callable=mock_open())
    @patch('matplotlib.pyplot.subplots')
    def test_save_check_log_should_save_log(self, mock_subplots, mock_open_file, mock_mkdir, mock_join, mock_isdir):
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.land())]
        mock_isdir.return_value = False
        mock_join.return_value = "joined_path"
        mock_subplots.return_value = (Mock(), Mock())

        self.collision_checker.check(drone_commands, self.state_updater_map, save_check_log=True)

        mock_mkdir.assert_called_with("logs")
        mock_open_file.assert_called_with("joined_path", "w")
