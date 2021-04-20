import unittest

from xdrone.command_converters.simulation_converter import SimulationConverter
from xdrone.shared.command import Command


class TestSimulationConverter(unittest.TestCase):
    def test_convert_command(self):
        expected = [{"action": "takeoff", "value": []},
                    {"action": "land", "value": []},
                    {"action": "up", "value": [1]},
                    {"action": "down", "value": [1]},
                    {"action": "left", "value": [1]},
                    {"action": "right", "value": [1]},
                    {"action": "forward", "value": [1]},
                    {"action": "backward", "value": [1]},
                    {"action": "rotate_left", "value": [1]},
                    {"action": "rotate_right", "value": [1]},
                    {"action": "wait", "value": [1]}]
        actual = SimulationConverter.convert_commands([Command.takeoff(),
                                                       Command.land(),
                                                       Command.up(1),
                                                       Command.down(1),
                                                       Command.left(1),
                                                       Command.right(1),
                                                       Command.forward(1),
                                                       Command.backward(1),
                                                       Command.rotate_left(1),
                                                       Command.rotate_right(1),
                                                       Command.wait(1)])
        self.assertEqual(expected, actual)
