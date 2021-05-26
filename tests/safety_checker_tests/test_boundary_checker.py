import unittest
from unittest.mock import Mock, call

from xdrone.safety_checker.boundary_checker import BoundaryChecker
from xdrone.shared.boundary_config import BoundaryConfig
from xdrone.shared.command import Command, SingleDroneCommand, ParallelDroneCommands
from xdrone.shared.drone_config import DroneConfig
from xdrone.shared.safety_check_error import SafetyCheckError
from xdrone.shared.state import State
from xdrone.state_updaters.state_updater import StateUpdater


class BoundaryCheckerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.boundary_config = BoundaryConfig(max_seconds=10, max_x_meters=5, max_y_meters=5, max_z_meters=5,
                                              min_x_meters=-5, min_y_meters=-5, min_z_meters=-5)
        self.state_updater_map = {"DRONE1": StateUpdater(DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                                     rotate_speed_dps=90, takeoff_height_meters=1)),
                                  "DRONE2": StateUpdater(DroneConfig(init_position=(1, 0, 0), speed_mps=2,
                                                                     rotate_speed_dps=180, takeoff_height_meters=2))}

    def test_check_should_call_update_states_and_check_drone_commands_with_correct_parameters(self):
        boundary_checker = BoundaryChecker(self.boundary_config)
        boundary_checker._update_states_and_check_drone_commands = Mock()
        drone_state_map = {"DRONE1": State(), "DRONE2": State(x_meters=1)}
        drones_involved = {"DRONE1", "DRONE2"}
        boundary_checker.check([], self.state_updater_map)
        boundary_checker._update_states_and_check_drone_commands.assert_called_once_with([], self.state_updater_map,
                                                                                         drone_state_map,
                                                                                         drones_involved)

    def test_check_in_the_end_not_land_should_give_error(self):
        with self.assertRaises(SafetyCheckError) as context:
            drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff())]
            BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)
        self.assertTrue("Drone 'DRONE1' did not land in the end" in str(context.exception))

    def test_check_takeoff_land_takeoff_land_should_not_give_error(self):
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.land()),
                          SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.land()), ]
        BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)

    def test_check_single_drone_command_wait_when_taken_off_should_not_give_error(self):
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.wait(1)),
                          SingleDroneCommand("DRONE1", Command.land())]
        BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)

    def test_check_single_drone_command_wait_when_not_taken_off_should_not_give_error(self):
        drone_commands = [SingleDroneCommand("DRONE1", Command.wait(1))]
        BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)

    def test_check_single_drone_command_takeoff_when_taken_off_should_give_error(self):
        with self.assertRaises(SafetyCheckError) as context:
            drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                              SingleDroneCommand("DRONE1", Command.takeoff())]
            BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)
        self.assertTrue("'takeoff' command used when drone 'DRONE1' has already been taken off"
                        in str(context.exception))

    def test_check_single_drone_command_other_command_when_not_taken_off_should_give_error(self):
        commands = [Command.land(), Command.up(1), Command.down(1), Command.left(1), Command.right(1),
                    Command.forward(1), Command.backward(1), Command.rotate_left(90), Command.rotate_right(90)]
        for command in commands:
            with self.assertRaises(SafetyCheckError) as context:
                drone_commands = [SingleDroneCommand("DRONE1", command)]
                BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)
            self.assertTrue("'{}' command used when drone 'DRONE1' has not been taken off"
                            .format(command.opcode)
                            in str(context.exception))

    def test_check_single_drone_command_should_update_state_correctly(self):
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff())]
        drone_state_map = {"DRONE1": State(), "DRONE2": State(x_meters=1)}
        drones_involved = {"DRONE1", "DRONE2"}
        BoundaryChecker(self.boundary_config)._update_states_and_check_drone_commands(drone_commands,
                                                                                      self.state_updater_map,
                                                                                      drone_state_map,
                                                                                      drones_involved)
        expected = {"DRONE1": State(has_taken_off=True, time_used_seconds=1, z_meters=1),
                    "DRONE2": State(time_used_seconds=1, x_meters=1)}
        self.assertEqual(expected, drone_state_map)

    def test_check_single_drone_command_should_check_state(self):
        boundary_checker = BoundaryChecker(self.boundary_config)
        boundary_checker.boundary_config.check_state = Mock()
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.land())]
        BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)
        calls = [call("DRONE1", State(has_taken_off=True, time_used_seconds=1, z_meters=1)),
                 call("DRONE2", State(time_used_seconds=1, x_meters=1)),
                 call("DRONE1", State(time_used_seconds=2)),
                 call("DRONE2", State(time_used_seconds=2, x_meters=1))]
        boundary_checker.boundary_config.check_state.assert_has_calls(calls)

    def test_check_single_drone_command_should_check_state_and_catch_error(self):
        boundary_checker = BoundaryChecker(self.boundary_config)
        boundary_checker.boundary_config.check_state = Mock(side_effect=SafetyCheckError)
        drone_commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                          SingleDroneCommand("DRONE1", Command.land())]
        with self.assertRaises(SafetyCheckError) as context:
            BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)

    def test_check_parallel_drone_commands_should_wait_for_slower_branch(self):
        drone_commands = [ParallelDroneCommands([
            [SingleDroneCommand("DRONE1", Command.takeoff())],
            [SingleDroneCommand("DRONE2", Command.wait(5))]
        ])]
        drone_state_map = {"DRONE1": State(), "DRONE2": State(x_meters=1)}
        drones_involved = {"DRONE1", "DRONE2"}
        BoundaryChecker(self.boundary_config)._update_states_and_check_drone_commands(drone_commands,
                                                                                      self.state_updater_map,
                                                                                      drone_state_map,
                                                                                      drones_involved)
        expected = {"DRONE1": State(has_taken_off=True, time_used_seconds=5, z_meters=1),
                    "DRONE2": State(time_used_seconds=5, x_meters=1)}
        self.assertEqual(expected, drone_state_map)

    def test_check_parallel_drone_commands_should_let_drone_not_involved_wait(self):
        drone_commands = [ParallelDroneCommands([
            [],
            [SingleDroneCommand("DRONE2", Command.wait(5))]
        ])]
        drone_state_map = {"DRONE1": State(), "DRONE2": State(x_meters=1)}
        drones_involved = {"DRONE1", "DRONE2"}
        BoundaryChecker(self.boundary_config)._update_states_and_check_drone_commands(drone_commands,
                                                                                      self.state_updater_map,
                                                                                      drone_state_map,
                                                                                      drones_involved)
        expected = {"DRONE1": State(time_used_seconds=5),
                    "DRONE2": State(time_used_seconds=5, x_meters=1)}
        self.assertEqual(expected, drone_state_map)

    def test_check_parallel_drone_commands_nested_should_update_states_correctly(self):
        drone_commands = \
            [
                ParallelDroneCommands([
                    [SingleDroneCommand("DRONE1", Command.wait(5))],
                    [SingleDroneCommand("DRONE2", Command.wait(3)),
                     ParallelDroneCommands([
                         [SingleDroneCommand("DRONE3", Command.wait(4))],
                         [SingleDroneCommand("DRONE4", Command.wait(1))]
                     ])]
                ]),
                SingleDroneCommand("DRONE1", Command.wait(1))
            ]
        drones_involved = {"DRONE1", "DRONE2", "DRONE3", "DRONE4", "DRONE5"}
        state_updaters = {name: StateUpdater(DroneConfig((1, 0, 0), 2, 180, 2)) for name in drones_involved}
        drone_state_map = {name: State() for name in drones_involved}
        BoundaryChecker(self.boundary_config)._update_states_and_check_drone_commands(drone_commands,
                                                                                      state_updaters,
                                                                                      drone_state_map,
                                                                                      drones_involved)
        expected = {name: State(time_used_seconds=8) for name in drones_involved}
        self.assertEqual(expected, drone_state_map)

    def test_check_parallel_drone_commands_should_check_state(self):
        boundary_checker = BoundaryChecker(self.boundary_config)
        boundary_checker.boundary_config.check_state = Mock()
        drone_commands = [ParallelDroneCommands([
            [SingleDroneCommand("DRONE1", Command.takeoff()), SingleDroneCommand("DRONE1", Command.land())],
            [SingleDroneCommand("DRONE2", Command.takeoff()), SingleDroneCommand("DRONE2", Command.land())]
        ])]
        BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)
        last_two_calls = [call("DRONE1", State(time_used_seconds=2)),
                          call("DRONE2", State(time_used_seconds=2, x_meters=1))]
        boundary_checker.boundary_config.check_state.assert_has_calls(last_two_calls)

    def test_check_parallel_drone_commands_should_check_state_and_catch_error(self):
        boundary_checker = BoundaryChecker(self.boundary_config)
        boundary_checker.boundary_config.check_state = Mock(side_effect=SafetyCheckError)
        drone_commands = [ParallelDroneCommands([
            [],
            []
        ])]
        with self.assertRaises(SafetyCheckError) as context:
            BoundaryChecker(self.boundary_config).check(drone_commands, self.state_updater_map)
