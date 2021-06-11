import unittest

from xdrone.command_generators import generate_commands
from xdrone.compiler.compiler_utils.expressions import Expression
from xdrone.compiler.compiler_utils.type import Type
from xdrone.shared.command import Command, SingleDroneCommand, ParallelDroneCommands
from xdrone.shared.compile_error import CompileError
from xdrone.shared.drone_config import DefaultDroneConfig


class ParallelTest(unittest.TestCase):
    def test_parallel_with_different_drones_should_give_correct_commands(self):
        drone_config_map = {"DRONE1": DefaultDroneConfig(),
                            "DRONE2": DefaultDroneConfig(),
                            "DRONE3": DefaultDroneConfig()}
        actual = generate_commands("""
            main() { 
              {DRONE1.takeoff();} || {DRONE2.takeoff();} || {DRONE3.takeoff();}; 
              {
                DRONE1.land();
              } || {
                {DRONE2.land();} || {DRONE3.land();};
              };
            }
        """, drone_config_map=drone_config_map)
        expected = [ParallelDroneCommands([[SingleDroneCommand("DRONE1", Command.takeoff())],
                                           [SingleDroneCommand("DRONE2", Command.takeoff())],
                                           [SingleDroneCommand("DRONE3", Command.takeoff())]]),
                    ParallelDroneCommands([[SingleDroneCommand("DRONE1", Command.land())],
                                           [ParallelDroneCommands([
                                               [SingleDroneCommand("DRONE2", Command.land())],
                                               [SingleDroneCommand("DRONE3", Command.land())]
                                           ])]])]
        self.assertEqual(expected, actual)

    def test_parallel_with_repeated_drones_in_branches_should_give_error(self):
        drone_config_map = {"DRONE1": DefaultDroneConfig(),
                            "DRONE2": DefaultDroneConfig(),
                            "DRONE3": DefaultDroneConfig()}
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                procedure foo() {
                  DRONE1.takeoff();
                  DRONE2.takeoff();
                  DRONE1.land();
                  DRONE2.land();
                }
                procedure bar() {
                  DRONE2.takeoff();
                  DRONE3.takeoff();
                  DRONE2.land();
                  DRONE3.land();
                }
                main() { 
                  {foo();} || {bar();} || {DRONE3.takeoff(); DRONE3.land();}; 
                }
            """, drone_config_map=drone_config_map)
        self.assertTrue("Parallel branches should have exclusive drone names, " +
                        "but {'DRONE2'} appeared in more than one branches"
                        in str(context.exception))

    def test_parallel_return_in_branch_should_return_early(self):
        drone_config_map = {"DRONE1": DefaultDroneConfig(),
                            "DRONE2": DefaultDroneConfig(),
                            "DRONE3": DefaultDroneConfig()}
        actual = generate_commands("""
            main() { 
              {return; DRONE1.takeoff();} || {DRONE2.takeoff(); DRONE2.land();}; 
            }
        """, drone_config_map=drone_config_map)
        expected = [ParallelDroneCommands([[],
                                           [SingleDroneCommand("DRONE2", Command.takeoff()),
                                            SingleDroneCommand("DRONE2", Command.land())]])]
        self.assertEqual(expected, actual)

    def test_parallel_return_with_value_in_branch_should_give_error(self):
        drone_config_map = {"DRONE1": DefaultDroneConfig(),
                            "DRONE2": DefaultDroneConfig(),
                            "DRONE3": DefaultDroneConfig()}
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main() { 
                  {return 1; DRONE1.takeoff();} || {DRONE2.takeoff(); DRONE2.land();}; 
                }
            """, drone_config_map=drone_config_map)
        self.assertTrue("Parallel branch should not return anything, but {} is returned"
                        .format(Expression(Type.int(), 1))
                        in str(context.exception))
