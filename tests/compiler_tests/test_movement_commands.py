import unittest

from xdrone import generate_commands
from xdrone.compiler.compiler_utils.expressions import Expression
from xdrone.compiler.compiler_utils.type import Type
from xdrone.shared.command import Command, SingleDroneCommand
from xdrone.shared.compile_error import CompileError


class MovementCommandsTest(unittest.TestCase):
    def test_takeoff_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.land())]
        self.assertEqual(expected, actual)

    def test_land_should_return_correct_command(self):
        actual = generate_commands("""
            main() { takeoff(); land(); }
        """)
        expected = [SingleDroneCommand("DEFAULT", Command.takeoff()),
                    SingleDroneCommand("DEFAULT", Command.land())]
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
