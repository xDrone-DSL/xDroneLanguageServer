import unittest

from xdrone import generate_commands
from xdrone.compiler.compiler_utils.expressions import Expression
from xdrone.compiler.compiler_utils.type import Type
from xdrone.shared.command import Command, SingleDroneCommand, ParallelDroneCommands
from xdrone.shared.compile_error import CompileError
from xdrone.shared.drone_config import DefaultDroneConfig


class MultipleDroneMovementTest(unittest.TestCase):
    def test_movement_with_no_name_specified_if_only_one_drone_should_use_that_drone(self):
        drone_config_map = {"the_one": DefaultDroneConfig()}
        actual = generate_commands("""
            main() { takeoff(); land(); }
        """, drone_config_map=drone_config_map)
        expected = [SingleDroneCommand("the_one", Command.takeoff()),
                    SingleDroneCommand("the_one", Command.land())]
        self.assertEqual(expected, actual)

    def test_movement_with_no_name_specified_if_multiple_drones_should_give_error(self):
        drone_config_map = {"drone1": DefaultDroneConfig(), "drone2": DefaultDroneConfig()}
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main() { takeoff(); land(); }
            """, drone_config_map=drone_config_map)
        print(context.exception)
        self.assertTrue("Drone should be specified if there are multiple drones in config"
                        in str(context.exception))

    def test_movement_with_undefined_name_specified_should_give_error(self):
        drone_config_map = {"drone1": DefaultDroneConfig()}
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main() { drone2.takeoff(); drone2.land(); }
            """, drone_config_map=drone_config_map)
        print(context.exception)
        self.assertTrue("Identifier drone2 has not been declared"
                        in str(context.exception))


class ParallelCommand(object):
    pass


class ParallelTest(unittest.TestCase):
    def test_parallel_with_different_drones_should_give_correct_commands(self):
        drone_config_map = {"drone1": DefaultDroneConfig(),
                            "drone2": DefaultDroneConfig(),
                            "drone3": DefaultDroneConfig()}
        actual = generate_commands("""
            main() { 
              {drone1.takeoff();} || {drone2.takeoff();} || {drone3.takeoff();}; 
              {
                drone1.land();
              } || {
                {drone2.land();} || {drone3.land();};
              };
            }
        """, drone_config_map=drone_config_map)
        expected = [ParallelDroneCommands([[SingleDroneCommand("drone1", Command.takeoff())],
                                           [SingleDroneCommand("drone2", Command.takeoff())],
                                           [SingleDroneCommand("drone3", Command.takeoff())]]),
                    ParallelDroneCommands([[SingleDroneCommand("drone1", Command.land())],
                                           [ParallelDroneCommands([
                                               [SingleDroneCommand("drone2", Command.land())],
                                               [SingleDroneCommand("drone3", Command.land())]
                                           ])]])]
        self.assertEqual(expected, actual)

    def test_parallel_with_repeated_drones_in_branches_should_give_error(self):
        drone_config_map = {"drone1": DefaultDroneConfig(),
                            "drone2": DefaultDroneConfig(),
                            "drone3": DefaultDroneConfig()}
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                procedure foo() {
                  drone1.takeoff();
                  drone2.takeoff();
                  drone1.land();
                  drone2.land();
                }
                procedure bar() {
                  drone2.takeoff();
                  drone3.takeoff();
                  drone2.land();
                  drone3.land();
                }
                main() { 
                  {foo();} || {bar();} || {drone3.takeoff(); drone3.land();}; 
                }
            """, drone_config_map=drone_config_map)
        self.assertTrue("Parallel branches should have exclusive drone names, " +
                        "but {'drone2'} appeared in more than one branches"
                        in str(context.exception))

    def test_parallel_return_in_branch_should_return_early(self):
        drone_config_map = {"drone1": DefaultDroneConfig(),
                            "drone2": DefaultDroneConfig(),
                            "drone3": DefaultDroneConfig()}
        actual = generate_commands("""
            main() { 
              {return; drone1.takeoff();} || {drone2.takeoff(); drone2.land();}; 
            }
        """, drone_config_map=drone_config_map)
        expected = [ParallelDroneCommands([[],
                                           [SingleDroneCommand("drone2", Command.takeoff()),
                                            SingleDroneCommand("drone2", Command.land())]])]
        self.assertEqual(expected, actual)

    def test_parallel_return_with_value_in_branch_should_give_error(self):
        drone_config_map = {"drone1": DefaultDroneConfig(),
                            "drone2": DefaultDroneConfig(),
                            "drone3": DefaultDroneConfig()}
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main() { 
                  {return 1; drone1.takeoff();} || {drone2.takeoff(); drone2.land();}; 
                }
            """, drone_config_map=drone_config_map)
        self.assertTrue("Parallel branch should not return anything, but {} is returned"
                        .format(Expression(Type.int(), 1))
                        in str(context.exception))
