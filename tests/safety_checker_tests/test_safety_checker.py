import unittest
from unittest.mock import Mock, call

from xdrone.safety_checker.safety_checker import SafetyChecker
from xdrone.shared.command import Command, SingleDroneCommand, ParallelDroneCommands
from xdrone.shared.drone_config import DroneConfig
from xdrone.shared.safety_check_error import SafetyCheckError
from xdrone.shared.safety_config import SafetyConfig
from xdrone.shared.state import State
from xdrone.state_updaters.state_updater import StateUpdater


class SafetyCheckerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.safety_config = SafetyConfig(max_seconds=10, max_x_meters=5, max_y_meters=5, max_z_meters=5,
                                          min_x_meters=-5, min_y_meters=-5, min_z_meters=-5)
        self.state_updaters = {"drone1": StateUpdater(DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                                                  rotate_speed_dps=90, takeoff_height_meters=1)),
                               "drone2": StateUpdater(DroneConfig(init_position=(1, 0, 0), speed_mps=2,
                                                                  rotate_speed_dps=180, takeoff_height_meters=2))}

    def test_check_should_call_update_states_and_check_drone_commands_with_correct_parameters(self):
        safety_checker = SafetyChecker(self.safety_config)
        safety_checker._update_states_and_check_drone_commands = Mock()
        drone_state_map = {"drone1": State(), "drone2": State(x_meters=1)}
        drones_involved = {"drone1", "drone2"}
        safety_checker.check([], self.state_updaters)
        safety_checker._update_states_and_check_drone_commands.assert_called_once_with([], self.state_updaters,
                                                                                       drone_state_map, drones_involved)

    def test_check_in_the_end_not_land_should_give_error(self):
        with self.assertRaises(SafetyCheckError) as context:
            drone_commands = [SingleDroneCommand("drone1", Command.takeoff())]
            SafetyChecker(self.safety_config).check(drone_commands, self.state_updaters)
        self.assertTrue("Drone 'drone1' did not land in the end" in str(context.exception))

    def test_check_takeoff_land_takeoff_land_should_not_give_error(self):
        drone_commands = [SingleDroneCommand("drone1", Command.takeoff()),
                          SingleDroneCommand("drone1", Command.land()),
                          SingleDroneCommand("drone1", Command.takeoff()),
                          SingleDroneCommand("drone1", Command.land()), ]
        SafetyChecker(self.safety_config).check(drone_commands, self.state_updaters)

    def test_check_single_drone_command_wait_when_taken_off_should_not_give_error(self):
        drone_commands = [SingleDroneCommand("drone1", Command.takeoff()),
                          SingleDroneCommand("drone1", Command.wait(1)),
                          SingleDroneCommand("drone1", Command.land())]
        SafetyChecker(self.safety_config).check(drone_commands, self.state_updaters)

    def test_check_single_drone_command_wait_when_not_taken_off_should_not_give_error(self):
        drone_commands = [SingleDroneCommand("drone1", Command.wait(1))]
        SafetyChecker(self.safety_config).check(drone_commands, self.state_updaters)

    def test_check_single_drone_command_takeoff_when_taken_off_should_give_error(self):
        with self.assertRaises(SafetyCheckError) as context:
            drone_commands = [SingleDroneCommand("drone1", Command.takeoff()),
                              SingleDroneCommand("drone1", Command.takeoff())]
            SafetyChecker(self.safety_config).check(drone_commands, self.state_updaters)
        self.assertTrue("'takeoff' command used when drone 'drone1' has already been taken off"
                        in str(context.exception))

    def test_check_single_drone_command_other_command_when_not_taken_off_should_give_error(self):
        commands = [Command.land(), Command.up(1), Command.down(1), Command.left(1), Command.right(1),
                    Command.forward(1), Command.backward(1), Command.rotate_left(90), Command.rotate_right(90)]
        for command in commands:
            with self.assertRaises(SafetyCheckError) as context:
                drone_commands = [SingleDroneCommand("drone1", command)]
                SafetyChecker(self.safety_config).check(drone_commands, self.state_updaters)
            self.assertTrue("'{}' command used when drone 'drone1' has not been taken off"
                            .format(command.opcode)
                            in str(context.exception))

    def test_check_single_drone_command_should_update_state_correctly(self):
        drone_commands = [SingleDroneCommand("drone1", Command.takeoff())]
        drone_state_map = {"drone1": State(), "drone2": State(x_meters=1)}
        drones_involved = {"drone1", "drone2"}
        SafetyChecker(self.safety_config)._update_states_and_check_drone_commands(drone_commands,
                                                                                  self.state_updaters,
                                                                                  drone_state_map,
                                                                                  drones_involved)
        expected = {"drone1": State(has_taken_off=True, time_used_seconds=1, z_meters=1),
                    "drone2": State(time_used_seconds=1, x_meters=1)}
        self.assertEqual(expected, drone_state_map)

    def test_check_single_drone_command_should_check_state(self):
        safety_checker = SafetyChecker(self.safety_config)
        safety_checker.safety_config.check_state = Mock()
        drone_commands = [SingleDroneCommand("drone1", Command.takeoff()),
                          SingleDroneCommand("drone1", Command.land())]
        SafetyChecker(self.safety_config).check(drone_commands, self.state_updaters)
        calls = [call("drone1", State(has_taken_off=True, time_used_seconds=1, z_meters=1)),
                 call("drone2", State(time_used_seconds=1, x_meters=1)),
                 call("drone1", State(time_used_seconds=2)),
                 call("drone2", State(time_used_seconds=2, x_meters=1))]
        safety_checker.safety_config.check_state.assert_has_calls(calls)

    def test_check_parallel_drone_commands_should_wait_for_slower_branch(self):
        drone_commands = [ParallelDroneCommands([
            [SingleDroneCommand("drone1", Command.takeoff())],
            [SingleDroneCommand("drone2", Command.wait(5))]
        ])]
        drone_state_map = {"drone1": State(), "drone2": State(x_meters=1)}
        drones_involved = {"drone1", "drone2"}
        SafetyChecker(self.safety_config)._update_states_and_check_drone_commands(drone_commands,
                                                                                  self.state_updaters,
                                                                                  drone_state_map,
                                                                                  drones_involved)
        expected = {"drone1": State(has_taken_off=True, time_used_seconds=5, z_meters=1),
                    "drone2": State(time_used_seconds=5, x_meters=1)}
        self.assertEqual(expected, drone_state_map)

    def test_check_parallel_drone_commands_should_let_drone_not_involved_wait(self):
        drone_commands = [ParallelDroneCommands([
            [],
            [SingleDroneCommand("drone2", Command.wait(5))]
        ])]
        drone_state_map = {"drone1": State(), "drone2": State(x_meters=1)}
        drones_involved = {"drone1", "drone2"}
        SafetyChecker(self.safety_config)._update_states_and_check_drone_commands(drone_commands,
                                                                                  self.state_updaters,
                                                                                  drone_state_map,
                                                                                  drones_involved)
        expected = {"drone1": State(time_used_seconds=5),
                    "drone2": State(time_used_seconds=5, x_meters=1)}
        self.assertEqual(expected, drone_state_map)

    def test_check_parallel_drone_commands_nested_should_update_states_correctly(self):
        drone_commands = \
            [
                ParallelDroneCommands([
                    [SingleDroneCommand("drone1", Command.wait(5))],
                    [SingleDroneCommand("drone2", Command.wait(3)),
                     ParallelDroneCommands([
                         [SingleDroneCommand("drone3", Command.wait(4))],
                         [SingleDroneCommand("drone4", Command.wait(1))]
                     ])]
                ]),
                SingleDroneCommand("drone1", Command.wait(1))
            ]
        drones_involved = {"drone1", "drone2", "drone3", "drone4", "drone5"}
        state_updaters = {name: StateUpdater(DroneConfig((1, 0, 0), 2, 180, 2)) for name in drones_involved}
        drone_state_map = {name: State() for name in drones_involved}
        SafetyChecker(self.safety_config)._update_states_and_check_drone_commands(drone_commands,
                                                                                  state_updaters,
                                                                                  drone_state_map,
                                                                                  drones_involved)
        expected = {name: State(time_used_seconds=8) for name in drones_involved}
        self.assertEqual(expected, drone_state_map)

    def test_check_parallel_drone_commands_should_check_state(self):
        safety_checker = SafetyChecker(self.safety_config)
        safety_checker.safety_config.check_state = Mock()
        drone_commands = [ParallelDroneCommands([
            [SingleDroneCommand("drone1", Command.takeoff()), SingleDroneCommand("drone1", Command.land())],
            [SingleDroneCommand("drone2", Command.takeoff()), SingleDroneCommand("drone2", Command.land())]
        ])]
        SafetyChecker(self.safety_config).check(drone_commands, self.state_updaters)
        last_two_calls = [call("drone1", State(time_used_seconds=2)),
                          call("drone2", State(time_used_seconds=2, x_meters=1))]
        safety_checker.safety_config.check_state.assert_has_calls(last_two_calls)
