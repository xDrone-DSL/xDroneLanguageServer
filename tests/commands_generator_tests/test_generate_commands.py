import unittest
from unittest.mock import patch, Mock

from xdrone import generate_commands, generate_commands_with_config
from xdrone.safety_checker.boundary_checker import BoundaryChecker
from xdrone.shared.boundary_config import BoundaryConfig
from xdrone.shared.command import Command, SingleDroneCommand
from xdrone.shared.compile_error import CompileError, XDroneSyntaxError
from xdrone.shared.drone_config import DroneConfig
from xdrone.shared.safety_check_error import SafetyCheckError


class GenerateCommandsTest(unittest.TestCase):
    def test_basic_program(self):
        commands = "main() {takeoff(); land();}"
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()), SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, generate_commands(commands))

    def test_syntax_error_should_be_reported(self):
        commands = "main() {takeoff() land();}"
        with self.assertRaises(XDroneSyntaxError) as context:
            generate_commands(commands)
        self.assertTrue("missing ';' at 'land'" in str(context.exception))

    def test_all_syntax_errors_should_be_reported(self):
        commands = "main() {takeoff() land()}"
        with self.assertRaises(XDroneSyntaxError) as context:
            generate_commands(commands)
        self.assertTrue("missing ';' at 'land'" in str(context.exception))
        self.assertTrue("missing ';' at '}'" in str(context.exception))

    def test_compile_error_should_be_reported(self):
        commands = "main() {takeoff(); up(\"abc\"); land();}"
        with self.assertRaises(CompileError) as context:
            generate_commands(commands)
        self.assertTrue("should have type int or decimal, but is string" in str(context.exception))

    def test_if_not_given_state_updater_should_use_default_to_update_state(self):
        commands = "main() {takeoff(); land();}"
        generate_commands(commands, boundary_checker=BoundaryChecker(BoundaryConfig(max_seconds=10, max_z_meters=1)))

    def test_if_given_state_updater_should_use_it_to_update_state(self):
        commands = "main() {takeoff(); land();}"
        with self.assertRaises(SafetyCheckError) as context:
            generate_commands(commands, drone_config_map={"DEFAULT": DroneConfig(init_position=(0, 0, 0),
                                                                                 speed_mps=1, rotate_speed_dps=90,
                                                                                 takeoff_height_meters=10)},
                              boundary_checker=BoundaryChecker(BoundaryConfig(max_seconds=10, max_z_meters=1)))
        self.assertTrue("Drone 'DEFAULT': the z coordinate 10 will go beyond its upper limit 1"
                        in str(context.exception))

    def test_if_not_given_boundary_checker_should_use_default_to_check_safety(self):
        commands = "main() {takeoff(); wait(1000); up(1000); land();}"
        generate_commands(commands)

    def test_if_given_boundary_checker_should_use_it_to_check_safety(self):
        commands = "main() {takeoff(); up(1000); land();}"
        with self.assertRaises(SafetyCheckError) as context:
            generate_commands(commands,
                              boundary_checker=BoundaryChecker(BoundaryConfig(max_seconds=10000, max_z_meters=1)))
        self.assertTrue("Drone 'DEFAULT': the z coordinate 1001 will go beyond its upper limit 1"
                        in str(context.exception))


class GenerateCommandsWithConfig(unittest.TestCase):

    def test_generate_commands_with_config(self):
        program, config_json, has_checks = Mock(), Mock(), Mock()
        drone_config_map, boundary_config, collision_config = Mock(), Mock(), Mock()
        boundary_checker = Mock()
        collision_checker = Mock()
        generated_commands = Mock()
        with patch('xdrone.ConfigParser.parse', return_value=(drone_config_map, boundary_config, collision_config)):
            with patch('xdrone.generate_commands', return_value=generated_commands) as generate_commands:
                with patch('xdrone.BoundaryChecker', return_value=boundary_checker):
                    with patch('xdrone.CollisionChecker', return_value=collision_checker):
                        self.assertEqual((generated_commands, drone_config_map, boundary_config),
                                         generate_commands_with_config(program, config_json, has_checks))
                        generate_commands.assert_called_with(program, drone_config_map, boundary_checker,
                                                             collision_checker, has_checks)
