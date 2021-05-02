import json
import zlib
from base64 import b64encode
from typing import List, Dict

from xdrone.shared.command import AbstractDroneCommand, SingleDroneCommand, ParallelDroneCommands
from xdrone.shared.drone_config import DroneConfig


class SimulationConverter:

    def convert(self, drone_commands: List[AbstractDroneCommand], drone_config_map: Dict[str, DroneConfig]):
        commands = self._convert_commands(drone_commands)
        config = self._convert_config(drone_config_map)
        json_obj = {"config": config, "commands": commands}
        return self._compress_json_obj(json_obj)

    def _convert_config(self, drone_config_map: Dict[str, DroneConfig]):
        configs = []
        for name, config in drone_config_map.items():
            configs.append({"name": name,
                            "init_pos": config.init_position,
                            "speed": config.speed_mps,
                            "rotate_speed": config.rotate_speed_dps,
                            "takeoff_height": config.takeoff_height_meters})
        return configs

    def _convert_commands(self, drone_commands: List[AbstractDroneCommand]):
        sequential = []
        for drone_command in drone_commands:
            if isinstance(drone_command, SingleDroneCommand):
                sequential.append({"type": "single",
                                   "name": drone_command.drone_name,
                                   "action": drone_command.command.opcode,
                                   "values": drone_command.command.operands})
            elif isinstance(drone_command, ParallelDroneCommands):
                sequential.append({"type": "parallel",
                                   "branches": [self._convert_commands(branch) for branch in drone_command.branches]})
        return sequential

    def _compress_json_obj(self, json_obj):
        json_str = json.dumps(json_obj)
        json_bytes = json_str.encode('ascii')
        compressed = zlib.compress(json_bytes)
        compressed_b64 = b64encode(compressed)
        compressed_ascii = compressed_b64.decode('ascii')
        return compressed_ascii
