from typing import Dict, List

from libs.TelloEduSwarmSearch.fly_tello import FlyTello
from xdrone.shared.command import AbstractDroneCommand, SingleDroneCommand, ParallelDroneCommands


class DJITelloEduExecutor:

    def __init__(self, name_id_map: Dict[str, str]):
        self.names = list(name_id_map.keys())
        self.ids = [name_id_map[name] for name in self.names]
        self.in_parallel = False

    def execute_drone_commands(self, drone_commands: List[AbstractDroneCommand]):
        with FlyTello(self.ids) as fly:
            self._execute_drone_commands(fly, drone_commands)

    def _execute_drone_commands(self, fly: FlyTello, drone_commands: List[AbstractDroneCommand]):
        for drone_command in drone_commands:
            self._execute_drone_command(fly, drone_command)

    def _execute_drone_command(self, fly: FlyTello, drone_command: AbstractDroneCommand):
        if isinstance(drone_command, SingleDroneCommand):
            if self.in_parallel:
                self._execute_single_drone_command(fly, drone_command)
            else:
                fly.wait_sync()
                self._execute_single_drone_command(fly, drone_command)
        elif isinstance(drone_command, ParallelDroneCommands):
            if self.in_parallel:
                fly.wait_sync()
                for branch in drone_command.branches:
                    self._execute_drone_commands(fly, branch)
            else:
                self.in_parallel = True
                fly.wait_sync()
                for branch in drone_command.branches:
                    self._execute_drone_commands(fly, branch)
                self.in_parallel = False

    def _execute_single_drone_command(self, fly: FlyTello, drone_command: SingleDroneCommand):
        tello_num = self.names.index(drone_command.drone_name) + 1
        command = drone_command.command
        if command.opcode == "takeoff":
            fly.takeoff(tello=tello_num)
        if command.opcode == "land":
            fly.land(tello=tello_num)
        if command.opcode == "up":
            fly.up(int(command.operands[0] * 100), tello=tello_num)
        if command.opcode == "down":
            fly.down(int(command.operands[0] * 100), tello=tello_num)
        if command.opcode == "left":
            fly.left(int(command.operands[0] * 100), tello=tello_num)
        if command.opcode == "right":
            fly.right(int(command.operands[0] * 100), tello=tello_num)
        if command.opcode == "forward":
            fly.forward(int(command.operands[0] * 100), tello=tello_num)
        if command.opcode == "backward":
            fly.back(int(command.operands[0] * 100), tello=tello_num)
        if command.opcode == "rotate_left":
            fly.rotate_ccw(int(command.operands[0]), tello=tello_num)
        if command.opcode == "rotate_right":
            fly.rotate_cw(int(command.operands[0]), tello=tello_num)
        if command.opcode == "wait":
            fly.pause(command.operands[0])
