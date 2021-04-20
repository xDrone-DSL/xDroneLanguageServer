from typing import List

from xdrone.shared.command import Command


class SimulationConverter:
    @staticmethod
    def convert_commands(commands: List[Command]) -> List:
        return [{"action": command.opcode, "value": command.operands} for command in commands]
