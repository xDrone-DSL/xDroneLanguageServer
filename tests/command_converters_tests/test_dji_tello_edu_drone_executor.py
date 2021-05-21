import unittest
from unittest.mock import Mock, call, patch

from xdrone.command_converters.dji_tello_edu_drone_executor import DJITelloEduExecutor
from xdrone.shared.command import SingleDroneCommand, Command, ParallelDroneCommands


class TestDJITelloEduExecutor(unittest.TestCase):
    def setUp(self):
        self.fly = Mock()
        self.fly.attach_mock(Mock(), "wait_sync")
        self.fly.attach_mock(Mock(), "takeoff")
        self.fly.attach_mock(Mock(), "land")
        self.fly.attach_mock(Mock(), "up")
        self.fly.attach_mock(Mock(), "down")
        self.fly.attach_mock(Mock(), "left")
        self.fly.attach_mock(Mock(), "right")
        self.fly.attach_mock(Mock(), "forward")
        self.fly.attach_mock(Mock(), "back")
        self.fly.attach_mock(Mock(), "rotate_ccw")
        self.fly.attach_mock(Mock(), "rotate_cw")
        self.fly.attach_mock(Mock(), "pause")

        self.fly_tello = Mock()
        self.fly_tello.__enter__ = Mock(return_value=self.fly)
        self.fly_tello.__exit__ = Mock()

        self.name_id_map = {"name1": "id1", "name2": "id2"}

    def test_execute_single_drone_command(self):
        single_commands = [SingleDroneCommand("name1", Command.takeoff()),
                           SingleDroneCommand("name1", Command.land()),
                           SingleDroneCommand("name2", Command.up(1.1)),
                           SingleDroneCommand("name2", Command.down(1.2)),
                           SingleDroneCommand("name2", Command.left(1.3)),
                           SingleDroneCommand("name2", Command.right(1.4)),
                           SingleDroneCommand("name2", Command.forward(1.5)),
                           SingleDroneCommand("name2", Command.backward(1.6)),
                           SingleDroneCommand("name2", Command.rotate_left(91)),
                           SingleDroneCommand("name2", Command.rotate_right(92)),
                           SingleDroneCommand("name2", Command.wait(1))]
        with patch('xdrone.command_converters.dji_tello_edu_drone_executor.FlyTello', return_value=self.fly_tello):
            executor = DJITelloEduExecutor(self.name_id_map)
            executor.execute_drone_commands(single_commands)
            calls = [call.wait_sync(),
                     call.takeoff(tello=1),
                     call.wait_sync(),
                     call.land(tello=1),
                     call.wait_sync(),
                     call.up(110, tello=2),
                     call.wait_sync(),
                     call.down(120, tello=2),
                     call.wait_sync(),
                     call.left(130, tello=2),
                     call.wait_sync(),
                     call.right(140, tello=2),
                     call.wait_sync(),
                     call.forward(150, tello=2),
                     call.wait_sync(),
                     call.back(160, tello=2),
                     call.wait_sync(),
                     call.rotate_ccw(91, tello=2),
                     call.wait_sync(),
                     call.rotate_cw(92, tello=2),
                     call.wait_sync(),
                     call.pause(1)]
            self.fly.assert_has_calls(calls)

    def test_execute_parallel_drone_commands(self):
        parallel_commands = [
            ParallelDroneCommands([
                [SingleDroneCommand("name1", Command.takeoff()), SingleDroneCommand("name1", Command.land())],
                [SingleDroneCommand("name2", Command.takeoff()), SingleDroneCommand("name2", Command.land())]
            ])
        ]
        with patch('xdrone.command_converters.dji_tello_edu_drone_executor.FlyTello', return_value=self.fly_tello):
            executor = DJITelloEduExecutor(self.name_id_map)
            executor.execute_drone_commands(parallel_commands)
            calls = [call.wait_sync(),
                     call.takeoff(tello=1),
                     call.land(tello=1),
                     call.takeoff(tello=2),
                     call.land(tello=2)]
            self.fly.assert_has_calls(calls)

    def test_execute_nested_parallel_drone_commands(self):
        nested_parallel_commands = [
            ParallelDroneCommands([
                [ParallelDroneCommands([
                    [SingleDroneCommand("name1", Command.takeoff()), SingleDroneCommand("name1", Command.land())]
                ])],
                [SingleDroneCommand("name2", Command.takeoff()), SingleDroneCommand("name2", Command.land())]
            ])
        ]
        with patch('xdrone.command_converters.dji_tello_edu_drone_executor.FlyTello', return_value=self.fly_tello):
            executor = DJITelloEduExecutor(self.name_id_map)
            executor.execute_drone_commands(nested_parallel_commands)
            calls = [call.wait_sync(),
                     call.takeoff(tello=1),
                     call.land(tello=1),
                     call.takeoff(tello=2),
                     call.land(tello=2)]
            self.fly.assert_has_calls(calls)

    def test_execute_mixed_drone_commands(self):
        mixed_commands = [
            SingleDroneCommand("name1", Command.takeoff()),
            ParallelDroneCommands([
                [SingleDroneCommand("name1", Command.land())],
                [SingleDroneCommand("name2", Command.takeoff())]
            ]),
            SingleDroneCommand("name2", Command.land())
        ]
        with patch('xdrone.command_converters.dji_tello_edu_drone_executor.FlyTello', return_value=self.fly_tello):
            executor = DJITelloEduExecutor(self.name_id_map)
            executor.execute_drone_commands(mixed_commands)
            calls = [call.wait_sync(),
                     call.takeoff(tello=1),
                     call.wait_sync(),
                     call.land(tello=1),
                     call.takeoff(tello=2),
                     call.wait_sync(),
                     call.land(tello=2)]
            self.fly.assert_has_calls(calls)
