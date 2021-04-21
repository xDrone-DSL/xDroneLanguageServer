import json
import zlib
from base64 import b64encode
from typing import List

from xdrone.shared.command import Command


class SimulationConverter:

    def convert_commands(self, commands: List[Command]):
        json_str = json.dumps([{"action": command.opcode, "value": command.operands} for command in commands])
        json_bytes = json_str.encode('ascii')
        compressed = zlib.compress(json_bytes)
        compressed_b64 = b64encode(compressed)
        compressed_ascii = compressed_b64.decode('ascii')
        return compressed_ascii
