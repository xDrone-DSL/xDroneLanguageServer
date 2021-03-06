import unittest

from xdrone.command_generators import generate_commands
from xdrone.compiler.compiler_utils.drones import NullDrone, Drone
from xdrone.compiler.compiler_utils.expressions import Expression
from xdrone.compiler.compiler_utils.symbol_table import SymbolTable
from xdrone.compiler.compiler_utils.type import Type
from xdrone.shared.compile_error import CompileError
from xdrone.shared.drone_config import DefaultDroneConfig


class DeclareTest(unittest.TestCase):
    def test_declare_int_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { int a; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.int(), 0, ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_decimal_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { decimal a; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.decimal(), 0, ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_string_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { string a; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.string(), "", ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_boolean_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { boolean a; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.boolean(), False, ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_vector_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { vector a; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.vector(), [0, 0, 0], ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_drone_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { drone a; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.drone(), NullDrone(), ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_list_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { list[int] a; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.list_of(Type.int()), [], ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_nested_list_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { list[list[int]] a; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.list_of(Type.list_of(Type.int())), [], ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_with_different_variable_name_should_change_symbol_table(self):
        for name in ["a", "A", "_a", "_1", "_A", "abc", "Abc", "a12", "aA1", "_aA1"]:
            actual = SymbolTable()
            generate_commands("""
                main () {{ int {}; }}
                """.format(name), symbol_table=actual)
            expected = SymbolTable()
            expected.store(name, Expression(Type.int(), 0, ident=name))
            self.assertEqual(expected, actual)

    def test_repeated_declare_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 int a;
                 int a;
                }
                """)

        self.assertTrue("Identifier a already declared" in str(context.exception))

    def test_repeated_declare_different_type_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 int a;
                 decimal a;
                }
                """)

        self.assertTrue("Identifier a already declared" in str(context.exception))

    def test_repeated_declare_drone_constant_should_give_error(self):
        types = [Type.int(), Type.decimal(), Type.string(), Type.boolean(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main () {{
                     {} DRONE;
                    }}
                    """.format(type.type_name), drone_config_map={"DRONE": DefaultDroneConfig()})

            self.assertTrue("Identifier DRONE already declared" in str(context.exception))


class AssignIdentTest(unittest.TestCase):
    def test_assign_ident_int_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             int a;
             a <- -1;
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.int(), -1, ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_ident_decimal_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             decimal a;
             a <- -1.5e10;
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.decimal(), -1.5e10, ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_ident_string_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             string a;
             a <- "1";
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.string(), "1", ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_ident_boolean_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             boolean a;
             a <- true;
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.boolean(), True, ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_ident_vector_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             vector a;
             a <- (1.0, -1.0, +1.0);
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.vector(), [1, -1, 1], ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_ident_drone_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             drone a;
             a <- DRONE1;
            }
            """, drone_config_map={"DRONE1": DefaultDroneConfig()}, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.drone(), Drone("DRONE1", DefaultDroneConfig()), ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_ident_list_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             list[int] a;
             a <- [1, -1, +1];
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.list_of(Type.int()), [1, -1, 1], ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_ident_nested_list_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             list[list[int]] a;
             a <- [[1], [-1], [+1]];
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.list_of(Type.list_of(Type.int())), [[1], [-1], [1]], ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_ident_empty_list_should_update_symbol_table(self):
        types = [Type.int(), Type.decimal(), Type.string(), Type.boolean(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            actual = SymbolTable()
            generate_commands("""
                main () {{
                 list[{}] a;
                 a <- [];
                }}
                """.format(type.type_name), symbol_table=actual)
            expected = SymbolTable()
            expected.store("a", Expression(Type.list_of(type), [], ident="a"))
            self.assertEqual(expected, actual)

    def test_assign_not_declared_variable_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 a <- true;
                }
            """)

        self.assertTrue("Identifier a has not been declared" in str(context.exception))

    def test_assign_drone_constant_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 DRONE1 <- DRONE1;
                }
            """, drone_config_map={"DRONE1": DefaultDroneConfig()})

        self.assertTrue("Identifier DRONE1 is a drone constant, cannot be assigned" in str(context.exception))

    def test_declare_and_then_assign_with_different_type_should_give_error(self):
        types = ["int", "decimal", "string", "boolean", "vector", "drone", "list[int]", "list[decimal]",
                 "list[list[int]]"]
        for t1 in types:
            for t2 in types:
                if t1 == t2:
                    continue
                with self.assertRaises(CompileError) as context:
                    generate_commands("""
                        main () {{
                         {} a;
                         {} b;
                         a <- b;
                        }}
                    """.format(t1, t2))

                self.assertTrue("Identifier a has been declared as {}, but assigned as {}"
                                .format(t1, t2) in str(context.exception))

    def test_declare_and_then_assign_with_same_type_should_success(self):
        types = ["int", "decimal", "string", "boolean", "vector", "drone", "list[int]", "list[decimal]",
                 "list[list[int]]"]
        for type in types:
            generate_commands("""
                main () {{
                 {} a;
                 {} b;
                 a <- b;
                }}
            """.format(type, type))


class AssignVectorElemTest(unittest.TestCase):

    def test_assign_vector_elem_to_temp_vector_should_not_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             (0.0, 0.0, 0.0).x <- 1.0;
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        self.assertEqual(expected, actual)

    def test_assign_vector_elem_to_variable_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             vector a;
             vector b;
             a.x <- 1;
             a.y <- 2;
             a.z <- -2;
             b.x <- 1.0;
             b.y <- 2.0;
             b.z <- -2.0;
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.vector(), [1.0, 2.0, -2.0], ident="a"))
        expected.store("b", Expression(Type.vector(), [1.0, 2.0, -2.0], ident="b"))
        self.assertEqual(expected, actual)

    def test_assign_vector_elem_not_declared_variable_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
            main () {
             a.x <- 1.0;
            }
            """)

        self.assertTrue("Identifier a has not been declared" in str(context.exception))

    def test_declare_and_then_assign_vector_elem_with_different_type_should_give_error(self):
        for type in [Type.string(), Type.boolean(), Type.vector(), Type.drone(),
                     Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]:
            for index in ["x", "y", "z"]:
                with self.assertRaises(CompileError) as context:
                    generate_commands("""
                        main () {{
                         vector a;
                         {} b;
                         a.{} <- b;
                        }}
                    """.format(type.type_name, index))

                self.assertTrue("Assigned value {} should have type int or decimal, but is {}"
                                .format(Expression(type, type.default_value, ident="b"), type.type_name)
                                in str(context.exception))


class AssignListElemTest(unittest.TestCase):

    def test_assign_list_elem_to_temp_vector_should_not_change_symbol_table(self):
        for code in ["[0.0][0] <- 1.0", "[0][0] <- 1", "[[\"a\"]][0] <- [\"b\"]", "[0.0, 1.0][0] <- 1.0"]:
            actual = SymbolTable()
            generate_commands("""
                main () {{
                 {};
                }}
                """.format(code), symbol_table=actual)
            expected = SymbolTable()
            self.assertEqual(expected, actual)

    def test_assign_list_elem_to_variable_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             list[int] a <- [0, 1, 2];
             a[0] <- 1;
             a[2] <- a[0];
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.list_of(Type.int()), [1, 1, 1], ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_list_elem_to_variable_nested_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             list[list[int]] a <- [[0, 1], [2, 3]];
             a[0] <- [4, 5];
             a[1][0] <- 6;
             a[1][1] <- 7;
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.list_of(Type.list_of(Type.int())), [[4, 5], [6, 7]], ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_list_elem_with_vector_should_update_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             list[vector] a <- [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0)];
             a[0] <- (7.0, 8.0, 9.0);
             a[1].x <- 10.0;
             a[1].y <- 11.0;
             a[1].z <- 12.0;
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.list_of(Type.vector()), [[7, 8, 9], [10, 11, 12]], ident="a"))
        self.assertEqual(expected, actual)

    def test_assign_list_elem_to_variable_out_of_bound_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 list[int] a <- [];
                 a[0] <- 1;
                }
                """)

        self.assertTrue("List {} has length 0, but has been assessed with out-of-range index 0"
                        .format(Expression(Type.list_of(Type.int()), [], ident="a"))
                        in str(context.exception))

    def test_assess_list_elem_out_of_bound_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 list[int] a <- [1];
                 a[0] <- a[1];
                }
                """)

        self.assertTrue("List {} has length 1, but has been assessed with out-of-range index 1"
                        .format(Expression(Type.list_of(Type.int()), [1], ident="a"))
                        in str(context.exception))

    def test_assess_list_elem_nested_out_of_bound_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 list[list[list[int]]] a <- [[[1], [2]]];
                 a[0][2] <- [1];
                }
                """)
        self.assertTrue("List {} has length 2, but has been assessed with out-of-range index 2"
                        .format(Expression(Type.list_of(Type.list_of(Type.int())), [[1], [2]], ident="a[0]"))
                        in str(context.exception))

        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 list[list[list[int]]] a <- [[[1], [2]]];
                 a[0][1][1] <- 1;
                }
                """)
        self.assertTrue("List {} has length 1, but has been assessed with out-of-range index 1"
                        .format(Expression(Type.list_of(Type.int()), [2], ident="a[0][1]"))
                        in str(context.exception))

    def test_assign_list_elem_not_declared_variable_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
            main () {
             a[0] <- 1;
            }
            """)

        self.assertTrue("Identifier a has not been declared" in str(context.exception))

    def test_declare_and_assign_list_elem_with_different_type_should_give_error(self):
        types = [Type.int(), Type.decimal(), Type.string(), Type.boolean(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for t1 in types:
            for t2 in types:
                if t1 == t2:
                    continue
                with self.assertRaises(CompileError) as context:
                    generate_commands("""
                    main () {{
                     {} a;
                     list[{}] b <- [a];
                    }}
                    """.format(t1, t2))

                self.assertTrue("Identifier b has been declared as list[{}], but assigned as list[{}]"
                                .format(t2, t1) in str(context.exception))

    def test_assign_list_elem_with_different_type_should_give_error(self):
        types = [Type.int(), Type.decimal(), Type.string(), Type.boolean(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for t1 in types:
            for t2 in types:
                if t1 == t2:
                    continue
                with self.assertRaises(CompileError) as context:
                    generate_commands("""
                    main () {{
                     {} a;
                     {} b;
                     list[{}] c <- [a];
                     c[0] <- b;
                    }}
                    """.format(t1, t2, t1))

                self.assertTrue("Assigned value {} should have type {}, but is {}"
                                .format(Expression(t2, t2.default_value, ident="b"), t1.type_name, t2.type_name)
                                in str(context.exception))


class CombinedDeclareAssignTest(unittest.TestCase):

    def test_declare_and_assign_int_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { int a <- 1; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.int(), 1, ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_and_assign_decimal_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { decimal a <- 1.0; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.decimal(), 1.0, ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_and_assign_string_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { string a <- "\0a"; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.string(), "\0a", ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_and_assign_boolean_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { boolean a <- true; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.boolean(), True, ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_and_assign_vector_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { vector a <- (1.0, 2.0, -3.0); }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.vector(), [1, 2, -3], ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_and_assign_drone_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { drone a <- DRONE1; }
            """, drone_config_map={"DRONE1": DefaultDroneConfig()}, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.drone(), Drone("DRONE1", DefaultDroneConfig()), ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_and_assign_list_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { list[int] a <- [1, 2, -3]; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.list_of(Type.int()), [1, 2, -3], ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_and_assign_nested_list_should_change_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () { list[list[int]] a <- [[1], [2]]; }
            """, symbol_table=actual)
        expected = SymbolTable()
        expected.store("a", Expression(Type.list_of(Type.list_of(Type.int())), [[1], [2]], ident="a"))
        self.assertEqual(expected, actual)

    def test_declare_and_assign_ident_empty_list_should_update_symbol_table(self):
        types = [Type.int(), Type.decimal(), Type.string(), Type.boolean(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            actual = SymbolTable()
            generate_commands("""
                main () {{
                 list[{}] a <- [];
                }}
                """.format(type.type_name), symbol_table=actual)
            expected = SymbolTable()
            expected.store("a", Expression(Type.list_of(type), [], ident="a"))
            self.assertEqual(expected, actual)

    def test_repeated_declare_and_assign_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 int a;
                 int a <- 0;
                }
                """)

        self.assertTrue("Identifier a already declared" in str(context.exception))

    def test_repeated_declare_and_assign_drone_constant_should_give_error(self):
        types = [Type.int(), Type.decimal(), Type.string(), Type.boolean(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for type in types:
            with self.assertRaises(CompileError) as context:
                generate_commands("""
                    main () {{
                     {} a;
                     {} DRONE <- a;
                    }}
                    """.format(type.type_name, type.type_name), drone_config_map={"DRONE": DefaultDroneConfig()})

            self.assertTrue("Identifier DRONE already declared" in str(context.exception))

    def test_declare_and_assign_with_different_type_should_give_error(self):
        types = [Type.int(), Type.decimal(), Type.string(), Type.boolean(), Type.vector(), Type.drone(),
                 Type.list_of(Type.int()), Type.list_of(Type.list_of(Type.int()))]
        for t1 in types:
            for t2 in types:
                if t1 == t2:
                    continue
                with self.assertRaises(CompileError) as context:
                    generate_commands("""
                    main () {{
                     {} a;
                     {} b <- a;
                    }}
                    """.format(t1, t2))

                self.assertTrue("Identifier b has been declared as {}, but assigned as {}"
                                .format(t2.type_name, t1.type_name) in str(context.exception))


class DelTest(unittest.TestCase):
    def test_del_should_delete_symbol_table(self):
        actual = SymbolTable()
        generate_commands("""
            main () {
             int a;
             del a;
            }
            """, symbol_table=actual)
        expected = SymbolTable()
        self.assertEqual(expected, actual)

    def test_del_not_declared_variable_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
            main () {
             del a;
            }
            """)

        self.assertTrue("Identifier a has not been declared" in str(context.exception))

    def test_del_drone_constant_should_give_error(self):
        with self.assertRaises(CompileError) as context:
            generate_commands("""
                main () {
                 del DRONE1;
                }
            """, drone_config_map={"DRONE1": DefaultDroneConfig()})

        self.assertTrue("Identifier DRONE1 is a drone constant, cannot be deleted" in str(context.exception))
