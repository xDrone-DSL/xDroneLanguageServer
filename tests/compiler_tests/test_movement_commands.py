import unittest

from xdrone import generate_commands
from xdrone.compiler.compiler_utils.expressions import Expression
from xdrone.compiler.compiler_utils.type import Type
from xdrone.shared.command import Command, SingleDroneCommand
from xdrone.shared.compile_error import CompileError
from xdrone.shared.drone_config import DefaultDroneConfig


class MovementCommandsTest(unittest.TestCase):
    def test_takeoff_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_takeoff_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_land_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_land_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_up_with_int_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); up(1); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.up(1)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_up_with_decimal_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); up(1.0); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.up(1.0)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_up_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.up(1); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.up(1)),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_up_with_incorrect_parameter_should_give_error(self):
        types = [Type.boolean(), Type.string(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{
                      {} a;
                      takeoff();
                      up(a);
                      land(); 
                    }}
                """.format(type.type_name))

            self.assertTrue("Expression {} should have type int or decimal, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))

    def test_down_with_int_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); down(1); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.down(1)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_down_with_decimal_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); down(1.0); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.down(1.0)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_down_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.down(1); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.down(1)),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_down_with_incorrect_parameter_should_give_error(self):
        types = [Type.boolean(), Type.string(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{
                      {} a;
                      takeoff();
                      down(a);
                      land(); 
                    }}
                """.format(type.type_name))

            self.assertTrue("Expression {} should have type int or decimal, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))

    def test_left_with_int_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); left(1); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.left(1)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_left_with_decimal_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); left(1.0); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.left(1.0)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_left_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.left(1); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.left(1)),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_left_with_incorrect_parameter_should_give_error(self):
        types = [Type.boolean(), Type.string(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{
                      {} a;
                      takeoff();
                      left(a);
                      land(); 
                    }}
                """.format(type.type_name))

            self.assertTrue("Expression {} should have type int or decimal, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))

    def test_right_with_int_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); right(1); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.right(1)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_right_with_decimal_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); right(1.0); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.right(1.0)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_right_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.right(1); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.right(1)),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_right_with_incorrect_parameter_should_give_error(self):
        types = [Type.boolean(), Type.string(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{
                      {} a;
                      takeoff();
                      right(a);
                      land(); 
                    }}
                """.format(type.type_name))

            self.assertTrue("Expression {} should have type int or decimal, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))

    def test_forward_with_int_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); forward(1); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.forward(1)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_forward_with_decimal_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); forward(1.0); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.forward(1.0)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_forward_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.forward(1); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.forward(1)),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_forward_with_incorrect_parameter_should_give_error(self):
        types = [Type.boolean(), Type.string(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{
                      {} a;
                      takeoff();
                      forward(a);
                      land(); 
                    }}
                """.format(type.type_name))

            self.assertTrue("Expression {} should have type int or decimal, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))

    def test_backward_with_int_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); backward(1); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.backward(1)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_backward_with_decimal_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); backward(1.0); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.backward(1.0)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_backward_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.backward(1); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.backward(1)),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_backward_with_incorrect_parameter_should_give_error(self):
        types = [Type.boolean(), Type.string(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{
                      {} a;
                      takeoff();
                      backward(a);
                      land(); 
                    }}
                """.format(type.type_name))

            self.assertTrue("Expression {} should have type int or decimal, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))

    def test_rotate_left_with_int_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); rotate_left(1); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.rotate_left(1)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_rotate_left_with_decimal_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); rotate_left(1.0); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.rotate_left(1.0)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_rotate_left_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.rotate_left(1); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.rotate_left(1)),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_rotate_left_with_incorrect_parameter_should_give_error(self):
        types = [Type.boolean(), Type.string(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{
                      {} a;
                      takeoff();
                      rotate_left(a);
                      land(); 
                    }}
                """.format(type.type_name))

            self.assertTrue("Expression {} should have type int or decimal, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))

    def test_rotate_right_with_int_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); rotate_right(1); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.rotate_right(1)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_rotate_right_with_decimal_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); rotate_right(1.0); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.rotate_right(1)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_rotate_right_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.takeoff(); DRONE1.rotate_right(1); DRONE1.land(); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.rotate_right(1)),
                    SingleDroneCommand("DRONE1", Command.land())]
        self.assertEqual(expected, actual)

    def test_rotate_right_with_incorrect_parameter_should_give_error(self):
        types = [Type.boolean(), Type.string(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{
                      {} a;
                      takeoff();
                      rotate_right(a);
                      land(); 
                    }}
                """.format(type.type_name))

            self.assertTrue("Expression {} should have type int or decimal, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))

    def test_wait_with_int_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { wait(1); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.wait(1))]
        self.assertEqual(expected, actual)

    def test_wait_with_decimal_parameter_should_return_correct_command(self):
        actual = generate_commands("""
            main() { wait(1.0); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.wait(1.0))]
        self.assertEqual(expected, actual)

    def test_wait_with_drone_name_should_return_correct_command(self):
        actual = generate_commands("""
            main() { DRONE1.wait(1); }
        """, drone_config_map={"DRONE1": DefaultDroneConfig()})
        expected = [SingleDroneCommand("DRONE1", Command.wait(1))]
        self.assertEqual(expected, actual)

    def test_wait_with_incorrect_parameter_should_give_error(self):
        types = [Type.boolean(), Type.string(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main() {{
                      {} a;
                      wait(a); 
                    }}
                """.format(type.type_name))

            self.assertTrue("Expression {} should have type int or decimal, but is {}"
                            .format(Expression(type, type.default_value, ident="a"), type.type_name)
                            in str(context.exception))

    def test_multiple_commands_should_return_correct_command(self):
        actual = generate_commands("""
            main() {
             takeoff();
             up(1);
             down(2);
             left(3);
             right(4);
             forward(5);
             backward(6);
             rotate_left(7);
             rotate_right(8);
             wait(9);
             land(); 
            }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.up(1)),
                    SingleDroneCommand("DEFAULT", Command.down(2)),
                    SingleDroneCommand("DEFAULT", Command.left(3)),
                    SingleDroneCommand("DEFAULT", Command.right(4)),
                    SingleDroneCommand("DEFAULT", Command.forward(5)),
                    SingleDroneCommand("DEFAULT", Command.backward(6)),
                    SingleDroneCommand("DEFAULT", Command.rotate_left(7)),
                    SingleDroneCommand("DEFAULT", Command.rotate_right(8)),
                    SingleDroneCommand("DEFAULT", Command.wait(9)),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)


class MovementGetDroneNameTest(unittest.TestCase):
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
