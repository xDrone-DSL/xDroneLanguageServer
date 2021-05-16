import unittest

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
        self.assertTrue("Error occurred during collision check, please retry with better the collision_config."
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
