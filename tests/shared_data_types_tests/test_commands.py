import unittest

from xdrone.shared.command import Command, SingleDroneCommand, ParallelDroneCommands, AbstractDroneCommand, \
    RepeatDroneNameException


class TestCommands(unittest.TestCase):

    def test_takeoff(self):
        self.assertEqual(Command.takeoff(), Command.takeoff())
        self.assertEqual("takeoff", Command.takeoff().opcode)
        self.assertEqual([], Command.takeoff().operands)
        self.assertEqual("Command: { opcode: takeoff, operands: [] }", str(Command.takeoff()))

    def test_land(self):
        self.assertEqual(Command.land(), Command.land())
        self.assertEqual("land", Command.land().opcode)
        self.assertEqual([], Command.land().operands)
        self.assertEqual("Command: { opcode: land, operands: [] }", str(Command.land()))

    def test_up(self):
        self.assertEqual(Command.up(1), Command.up(1))
        self.assertEqual("up", Command.up(1).opcode)
        self.assertEqual([1], Command.up(1).operands)
        self.assertEqual("Command: { opcode: up, operands: [1] }", str(Command.up(1)))

    def test_down(self):
        self.assertEqual(Command.down(1), Command.down(1))
        self.assertEqual("down", Command.down(1).opcode)
        self.assertEqual([1], Command.down(1).operands)
        self.assertEqual("Command: { opcode: down, operands: [1] }", str(Command.down(1)))

    def test_left(self):
        self.assertEqual(Command.left(1), Command.left(1))
        self.assertEqual("left", Command.left(1).opcode)
        self.assertEqual([1], Command.left(1).operands)
        self.assertEqual("Command: { opcode: left, operands: [1] }", str(Command.left(1)))

    def test_right(self):
        self.assertEqual(Command.right(1), Command.right(1))
        self.assertEqual("right", Command.right(1).opcode)
        self.assertEqual([1], Command.right(1).operands)
        self.assertEqual("Command: { opcode: right, operands: [1] }", str(Command.right(1)))

    def test_forward(self):
        self.assertEqual(Command.forward(1), Command.forward(1))
        self.assertEqual("forward", Command.forward(1).opcode)
        self.assertEqual([1], Command.forward(1).operands)
        self.assertEqual("Command: { opcode: forward, operands: [1] }", str(Command.forward(1)))

    def test_backward(self):
        self.assertEqual(Command.backward(1), Command.backward(1))
        self.assertEqual("backward", Command.backward(1).opcode)
        self.assertEqual([1], Command.backward(1).operands)
        self.assertEqual("Command: { opcode: backward, operands: [1] }", str(Command.backward(1)))

    def test_rotate_left(self):
        self.assertEqual(Command.rotate_left(1), Command.rotate_left(1))
        self.assertEqual("rotate_left", Command.rotate_left(1).opcode)
        self.assertEqual([1], Command.rotate_left(1).operands)
        self.assertEqual("Command: { opcode: rotate_left, operands: [1] }", str(Command.rotate_left(1)))

    def test_rotate_right(self):
        self.assertEqual(Command.rotate_right(1), Command.rotate_right(1))
        self.assertEqual("rotate_right", Command.rotate_right(1).opcode)
        self.assertEqual([1], Command.rotate_right(1).operands)
        self.assertEqual("Command: { opcode: rotate_right, operands: [1] }", str(Command.rotate_right(1)))

    def test_wait(self):
        self.assertEqual(Command.wait(1), Command.wait(1))
        self.assertEqual("wait", Command.wait(1).opcode)
        self.assertEqual([1], Command.wait(1).operands)
        self.assertEqual("Command: { opcode: wait, operands: [1] }", str(Command.wait(1)))

    def test_eq(self):
        commands1 = [None, Command.takeoff(), Command.land(),
                     Command.up(1), Command.down(1), Command.left(1), Command.right(1), Command.forward(1),
                     Command.backward(1), Command.rotate_left(1), Command.rotate_right(1), Command.wait(1),
                     Command.up(2), Command.down(2), Command.left(2), Command.right(2), Command.forward(2),
                     Command.backward(2), Command.rotate_left(2), Command.rotate_right(2), Command.wait(2)]
        commands2 = [None, Command.takeoff(), Command.land(),
                     Command.up(1), Command.down(1), Command.left(1), Command.right(1), Command.forward(1),
                     Command.backward(1), Command.rotate_left(1), Command.rotate_right(1), Command.wait(1),
                     Command.up(2), Command.down(2), Command.left(2), Command.right(2), Command.forward(2),
                     Command.backward(2), Command.rotate_left(2), Command.rotate_right(2), Command.wait(2)]
        for i in range(len(commands1)):
            for j in range(len(commands2)):
                if i == j:
                    self.assertEqual(commands1[i], commands2[j])
                else:
                    self.assertNotEqual(commands1[i], commands2[j])

    def test_corrupted_command_should_not_affect_correct_type(self):
        command = Command.forward(1)
        corrupted_command = Command.forward(1)
        corrupted_command._opcode = "corrupted"
        self.assertNotEqual(command, corrupted_command)
        self.assertEqual("forward", Command.forward(1).opcode)
        self.assertEqual([1], Command.forward(1).operands)
        self.assertEqual("corrupted", corrupted_command.opcode)
        self.assertEqual([1], corrupted_command.operands)


class TestAbstractDroneCommands(unittest.TestCase):

    def test_get_drones_involved(self):
        with self.assertRaises(NotImplementedError) as context:
            AbstractDroneCommand().get_drones_involved()

    def test_to_command_str(self):
        with self.assertRaises(NotImplementedError) as context:
            AbstractDroneCommand().to_command_str()


class TestSingleDroneCommand(unittest.TestCase):

    def test_properties(self):
        drone_command = SingleDroneCommand("abc", Command.takeoff())
        self.assertEqual("abc", drone_command.drone_name)
        self.assertEqual(Command.takeoff(), drone_command.command)

    def test_get_drones_involved(self):
        drone_command = SingleDroneCommand("abc", Command.takeoff())
        self.assertEqual({"abc"}, drone_command.get_drones_involved())

    def test_to_command_str(self):
        drone_command = SingleDroneCommand("abc", Command.takeoff())
        self.assertEqual("abc.takeoff();", drone_command.to_command_str())
        drone_command = SingleDroneCommand("abc", Command.up(1))
        self.assertEqual("abc.up(1);", drone_command.to_command_str())

    def test_str(self):
        drone_command = SingleDroneCommand("abc", Command.takeoff())
        self.assertEqual("SingleDroneCommand: { drone_name: abc, command: Command: { opcode: takeoff, operands: [] } }",
                         str(drone_command))

    def test_repr(self):
        drone_command = SingleDroneCommand("abc", Command.takeoff())
        self.assertEqual("SingleDroneCommand: { drone_name: abc, command: Command: { opcode: takeoff, operands: [] } }",
                         repr(drone_command))

    def test_eq(self):
        self.assertEqual(SingleDroneCommand("abc", Command.takeoff()), SingleDroneCommand("abc", Command.takeoff()))
        self.assertNotEqual(SingleDroneCommand("", Command.takeoff()), SingleDroneCommand("abc", Command.takeoff()))
        self.assertNotEqual(SingleDroneCommand("abc", Command.takeoff()), SingleDroneCommand("abc", Command.land()))
        self.assertNotEqual(None, SingleDroneCommand("abc", Command.takeoff()))

    def test_immutable(self):
        drone_command = SingleDroneCommand("abc", Command.takeoff())
        drone_name = drone_command.drone_name
        command = drone_command.command
        drone_name += "corrupted"
        command._opcode = "corrupted"
        self.assertEqual("abc", drone_command.drone_name)
        self.assertEqual(Command.takeoff(), drone_command.command)


class TestRepeatDroneNameException(unittest.TestCase):

    def test_properties(self):
        exception = RepeatDroneNameException({"abc"})
        self.assertEqual({"abc"}, exception.repeated_names)

    def test_immutable(self):
        exception = RepeatDroneNameException({"abc"})
        exception.repeated_names.add("corrupted")
        self.assertEqual({"abc"}, exception.repeated_names)


class TestParallelCommands(unittest.TestCase):

    def test_properties(self):
        parallel_commands = ParallelDroneCommands()
        self.assertEqual([], parallel_commands.branches)
        self.assertEqual([], parallel_commands.drones_involved_each_branch)
        parallel_commands = ParallelDroneCommands([[], []])
        self.assertEqual([[], []], parallel_commands.branches)
        self.assertEqual([set(), set()], parallel_commands.drones_involved_each_branch)

    def test_get_drones_involved(self):
        parallel_commands = ParallelDroneCommands()
        self.assertEqual(set(), parallel_commands.get_drones_involved())
        parallel_commands = ParallelDroneCommands([[SingleDroneCommand("DRONE1", Command.takeoff())],
                                                   [SingleDroneCommand("DRONE2", Command.takeoff())],
                                                   [ParallelDroneCommands([
                                                       [SingleDroneCommand("DRONE3", Command.takeoff())],
                                                       [SingleDroneCommand("DRONE4", Command.takeoff())]
                                                   ])]])
        self.assertEqual({"DRONE1", "DRONE2", "DRONE3", "DRONE4"}, parallel_commands.get_drones_involved())

    def test_add(self):
        parallel_commands = ParallelDroneCommands()
        parallel_commands.add([])
        self.assertEqual([[]], parallel_commands.branches)
        self.assertEqual([set()], parallel_commands.drones_involved_each_branch)
        parallel_commands.add([SingleDroneCommand("abc", Command.takeoff())])
        self.assertEqual([[], [SingleDroneCommand("abc", Command.takeoff())]], parallel_commands.branches)
        self.assertEqual([set(), {"abc"}], parallel_commands.drones_involved_each_branch)

    def test_add_already_involved_drones_should_give_error(self):
        parallel_commands = ParallelDroneCommands()
        parallel_commands.add([SingleDroneCommand("DRONE1", Command.takeoff())])
        with self.assertRaises(RepeatDroneNameException) as context:
            parallel_commands.add([SingleDroneCommand("DRONE1", Command.takeoff())])
        self.assertTrue({"DRONE1"}, context.exception.repeated_names)

    def test_init_with_repeated_drones_should_give_error(self):
        with self.assertRaises(RepeatDroneNameException) as context:
            ParallelDroneCommands([
                [SingleDroneCommand("DRONE1", Command.takeoff())],
                [SingleDroneCommand("DRONE1", Command.takeoff())]
            ])
        self.assertTrue({"DRONE1"}, context.exception.repeated_names)

    def test_to_command_str(self):
        parallel_commands = ParallelDroneCommands()
        parallel_commands.add([])
        parallel_commands.add([SingleDroneCommand("abc", Command.takeoff()),
                               SingleDroneCommand("abc", Command.up(1))])
        self.assertEqual("{ } || { abc.takeoff(); abc.up(1); };",
                         parallel_commands.to_command_str())
        outer_parallel_commands = ParallelDroneCommands()
        outer_parallel_commands.add([])
        outer_parallel_commands.add([parallel_commands])
        self.assertEqual("{ } || { { } || { abc.takeoff(); abc.up(1); }; };",
                         outer_parallel_commands.to_command_str())

    def test_str(self):
        parallel_commands = ParallelDroneCommands()
        parallel_commands.add([])
        parallel_commands.add([SingleDroneCommand("abc", Command.takeoff())])
        self.assertEqual("ParallelDroneCommands: { [], " +
                         "[SingleDroneCommand: { drone_name: abc, " +
                         "command: Command: { opcode: takeoff, operands: [] } }] }",
                         str(parallel_commands))

    def test_repr(self):
        parallel_commands = ParallelDroneCommands()
        parallel_commands.add([])
        parallel_commands.add([SingleDroneCommand("abc", Command.takeoff())])
        self.assertEqual("ParallelDroneCommands: { [], " +
                         "[SingleDroneCommand: { drone_name: abc, " +
                         "command: Command: { opcode: takeoff, operands: [] } }] }",
                         repr(parallel_commands))

    def test_eq(self):
        parallel_commands1 = ParallelDroneCommands()
        parallel_commands1.add([])
        parallel_commands1.add([SingleDroneCommand("abc", Command.takeoff())])
        parallel_commands2 = ParallelDroneCommands([[], [SingleDroneCommand("abc", Command.takeoff())]])
        parallel_commands3 = ParallelDroneCommands([[SingleDroneCommand("abc", Command.takeoff())], []])
        self.assertEqual(ParallelDroneCommands(), ParallelDroneCommands())
        self.assertEqual(parallel_commands1, parallel_commands2)
        self.assertNotEqual(parallel_commands1, parallel_commands3)
        self.assertNotEqual(None, parallel_commands1)
