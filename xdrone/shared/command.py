from __future__ import annotations

import copy
from typing import Union, List, Set


class Command:
    def __init__(self, opcode: str, operands: list):
        self._opcode = opcode
        self._operands = operands

    @property
    def opcode(self) -> str:
        return copy.deepcopy(self._opcode)

    @property
    def operands(self) -> list:
        return copy.deepcopy(self._operands)

    @staticmethod
    def takeoff() -> Command:
        return Command("takeoff", [])

    @staticmethod
    def land() -> Command:
        return Command("land", [])

    @staticmethod
    def up(distance_meters: Union[int, float]) -> Command:
        return Command("up", [distance_meters])

    @staticmethod
    def down(distance_meters: Union[int, float]) -> Command:
        return Command("down", [distance_meters])

    @staticmethod
    def left(distance_meters: Union[int, float]) -> Command:
        return Command("left", [distance_meters])

    @staticmethod
    def right(distance_meters: Union[int, float]) -> Command:
        return Command("right", [distance_meters])

    @staticmethod
    def forward(distance_meters: Union[int, float]) -> Command:
        return Command("forward", [distance_meters])

    @staticmethod
    def backward(distance_meters: Union[int, float]) -> Command:
        return Command("backward", [distance_meters])

    @staticmethod
    def rotate_left(angle_degrees: Union[int, float]) -> Command:
        return Command("rotate_left", [angle_degrees])

    @staticmethod
    def rotate_right(angle_degrees: Union[int, float]) -> Command:
        return Command("rotate_right", [angle_degrees])

    @staticmethod
    def wait(time_seconds: Union[int, float]) -> Command:
        return Command("wait", [time_seconds])

    def __str__(self):
        return "Command: {{ opcode: {}, operands: {} }}".format(self._opcode, self._operands)

    def __eq__(self, other):
        if isinstance(other, Command):
            return other._opcode == self._opcode and other._operands == self._operands
        return False


class AbstractDroneCommand:
    def get_drones_involved(self) -> Set[str]:
        raise NotImplementedError("get_drones_involved not supported in AbstractDroneCommand")


class SingleDroneCommand(AbstractDroneCommand):
    def __init__(self, drone_name: str, command: Command):
        self._drone_name = drone_name
        self._command = command

    @property
    def drone_name(self) -> str:
        return copy.deepcopy(self._drone_name)

    @property
    def command(self) -> Command:
        return copy.deepcopy(self._command)

    def get_drones_involved(self) -> Set[str]:
        return {self.drone_name}

    def __str__(self):
        return "SingleDroneCommand: {{ drone_name: {}, command: {} }}".format(self._drone_name, self._command)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, SingleDroneCommand):
            return other._drone_name == self._drone_name and other._command == self._command
        return False


class RepeatDroneNameException(Exception):
    def __init__(self, repeated_names: Set[str]):
        self._repeated_names = repeated_names

    @property
    def repeated_names(self) -> Set[str]:
        return copy.deepcopy(self._repeated_names)


class ParallelDroneCommands(AbstractDroneCommand):
    def __init__(self, branches: List[List[AbstractDroneCommand]] = None):
        self._branches = []
        self._drones_involved = set()
        if branches is not None:
            for branch in branches:
                self.add(branch)

    @property
    def branches(self) -> List[List[AbstractDroneCommand]]:
        return copy.deepcopy(self._branches)

    def get_drones_involved(self) -> Set[str]:
        return copy.deepcopy(self._drones_involved)

    def add(self, drone_commands: List[AbstractDroneCommand]):
        drones_to_be_involved = set.union(set(),
                                          *[drone_command.get_drones_involved() for drone_command in drone_commands])
        repeated_names = self._drones_involved.intersection(drones_to_be_involved)
        if len(repeated_names) > 0:
            raise RepeatDroneNameException(repeated_names)
        self._branches.append(drone_commands)
        self._drones_involved = self._drones_involved.union(drones_to_be_involved)

    def __str__(self):
        result = "ParallelDroneCommands: { "
        result += ", ".join([str(commands) for commands in self._branches])
        result += " }"
        return result

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, ParallelDroneCommands):
            return other._branches == self._branches
        return False
