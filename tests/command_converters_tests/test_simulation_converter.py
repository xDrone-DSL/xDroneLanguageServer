import json
import unittest
import zlib
from base64 import b64decode

from xdrone.command_converters.simulation_converter import SimulationConverter
from xdrone.shared.command import Command, SingleDroneCommand, ParallelDroneCommands
from xdrone.shared.drone_config import DroneConfig


class TestSimulationConverter(unittest.TestCase):
    def test_convert_command(self):
        commands = [SingleDroneCommand("DRONE1", Command.takeoff()),
                    SingleDroneCommand("DRONE1", Command.up(1)),
                    SingleDroneCommand("DRONE1", Command.down(1)),
                    SingleDroneCommand("DRONE1", Command.left(1)),
                    SingleDroneCommand("DRONE1", Command.right(1)),
                    SingleDroneCommand("DRONE1", Command.forward(1)),
                    SingleDroneCommand("DRONE1", Command.backward(1)),
                    SingleDroneCommand("DRONE1", Command.rotate_left(1)),
                    SingleDroneCommand("DRONE1", Command.rotate_right(1)),
                    ParallelDroneCommands([
                        [ParallelDroneCommands([
                            [],
                            [SingleDroneCommand("DRONE1", Command.up(1))]
                        ])],
                        [SingleDroneCommand("DRONE2", Command.takeoff()), SingleDroneCommand("DRONE2", Command.land())]

                    ]),
                    SingleDroneCommand("DRONE1", Command.land()),
                    SingleDroneCommand("DRONE1", Command.wait(1))]
        drone_config_map = {"DRONE1": DroneConfig((1, 2, 3), 1, 90, 2), "DRONE2": DroneConfig((0, 0, 0), 1, 90, 1)}
        expected = {"config": [{"name": "DRONE1", "init_pos": [1, 2, 3],
                                "speed": 1, "rotate_speed": 90, "takeoff_height": 2},
                               {"name": "DRONE2", "init_pos": [0, 0, 0],
                                "speed": 1, "rotate_speed": 90, "takeoff_height": 1}],
                    "commands": [{"type": "single", "name": "DRONE1", "action": "takeoff", "values": []},
                                 {"type": "single", "name": "DRONE1", "action": "up", "values": [1]},
                                 {"type": "single", "name": "DRONE1", "action": "down", "values": [1]},
                                 {"type": "single", "name": "DRONE1", "action": "left", "values": [1]},
                                 {"type": "single", "name": "DRONE1", "action": "right", "values": [1]},
                                 {"type": "single", "name": "DRONE1", "action": "forward", "values": [1]},
                                 {"type": "single", "name": "DRONE1", "action": "backward", "values": [1]},
                                 {"type": "single", "name": "DRONE1", "action": "rotate_left", "values": [1]},
                                 {"type": "single", "name": "DRONE1", "action": "rotate_right", "values": [1]},
                                 {"type": "parallel", "branches": [
                                     [{"type": "parallel", "branches": [
                                         [],
                                         [{"type": "single", "name": "DRONE1", "action": "up", "values": [1]}]]}],
                                     [{"type": "single", "name": "DRONE2", "action": "takeoff", "values": []},
                                      {"type": "single", "name": "DRONE2", "action": "land", "values": []}]
                                 ]},
                                 {"type": "single", "name": "DRONE1", "action": "land", "values": []},
                                 {"type": "single", "name": "DRONE1", "action": "wait", "values": [1]}
                                 ]}
        actual = SimulationConverter().convert(commands, drone_config_map)

        self.assertEqual(expected, json.loads(zlib.decompress(b64decode(actual))))
