import unittest

from xdrone import generate_commands
from xdrone.compiler.compiler_utils.expressions import Expression
from xdrone.compiler.compiler_utils.type import Type
from xdrone.shared.command import Command, SingleDroneCommand, ParallelDroneCommands
from xdrone.shared.compile_error import CompileError
from xdrone.shared.drone_config import DefaultDroneConfig


class MultipleDroneMovementTest(unittest.TestCase):
    def test_movement_with_no_name_specified_if_only_one_drone_should_use_that_drone(self):
        drone_config_map = {"THE_ONE": DefaultDroneConfig()}
        actual = generate_commands("""
            main() { takeoff(); land(); }
        """, drone_config_map=drone_config_map)
        expected = [SingleDroneCommand("THE_ONE", Command.takeoff()),
                    SingleDroneCommand("THE_ONE", Command.land())]
        self.assertEqual(expected, actual)

    def test_movement_with_no_name_specified_if_multiple_drones_should_give_error(self):
        drone_config_map = {"DRONE1": DefaultDroneConfig(), "DRONE2": DefaultDroneConfig()}
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main() { takeoff(); land(); }
            """, drone_config_map=drone_config_map)
        self.assertTrue("Drone should be specified if there are multiple drones in config"
                        in str(context.exception))

    def test_movement_with_undefined_name_specified_should_give_error(self):
        drone_config_map = {"DRONE1": DefaultDroneConfig()}
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main() { DRONE2.takeoff(); DRONE2.land(); }
            """, drone_config_map=drone_config_map)
        self.assertTrue("Identifier DRONE2 has not been declared"
                        in str(context.exception))

    def test_movement_with_null_drone_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main() { drone d; d.takeoff(); d.land(); }
            """, )
        self.assertTrue("Drone has not been assigned"
                        in str(context.exception))

    def test_movement_with_other_type_should_give_error(self):
        types = [Type.int(), Type.decimal(), Type.string(), Type.boolean(), Type.vector(),
                 Type.list_of(Type.int()), Type.list_of(Type.decimal()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{ {} a; a.takeoff(); a.land(); }}
                """.format(type))
            self.assertTrue("Expression {} should have type drone, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))


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
