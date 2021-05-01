from typing import List, Dict, Set

from xdrone.shared.command import AbstractDroneCommand, SingleDroneCommand, ParallelDroneCommands
from xdrone.shared.safety_check_error import SafetyCheckError
from xdrone.shared.safety_config import SafetyConfig
from xdrone.shared.state import State
from xdrone.state_updaters.state_updater import StateUpdater


class SafetyChecker:
    def __init__(self, safety_config: SafetyConfig):
        self.safety_config = safety_config

    def check(self, drone_commands: List[AbstractDroneCommand], state_updater_map: Dict[str, StateUpdater]):
        drone_state_map = {name: state_updater.get_init_state() for name, state_updater in state_updater_map.items()}
        drones_involved = set(state_updater_map.keys())
        self._update_states_and_check_drone_commands(drone_commands, state_updater_map, drone_state_map,
                                                     drones_involved)
        for name, state in drone_state_map.items():
            if state.has_taken_off:
                raise SafetyCheckError("Drone '{}' did not land in the end".format(name))

    def _update_states_and_check_drone_commands(self, drone_commands: List[AbstractDroneCommand],
                                                state_updaters: Dict[str, StateUpdater],
                                                drone_state_map: Dict[str, State],
                                                drones_involved: Set[str]) -> float:
        total_time_used = 0
        for drone_command in drone_commands:
            if isinstance(drone_command, SingleDroneCommand):
                total_time_used += self._update_states_and_check_single_drone_command(drone_command,
                                                                                      state_updaters,
                                                                                      drone_state_map,
                                                                                      drones_involved)
            elif isinstance(drone_command, ParallelDroneCommands):
                total_time_used += self._update_states_and_check_parallel_drone_commands(drone_command,
                                                                                         state_updaters,
                                                                                         drone_state_map,
                                                                                         drones_involved)
        return total_time_used

    def _update_states_and_check_single_drone_command(self, single_drone_command: SingleDroneCommand,
                                                      state_updaters: Dict[str, StateUpdater],
                                                      drone_state_map: Dict[str, State],
                                                      drones_involved: Set[str]) -> float:
        self._check_takeoff_state(single_drone_command, drone_state_map)
        time_used = self._update_states(single_drone_command, state_updaters, drone_state_map, drones_involved)
        for name, state in drone_state_map.items():
            self.safety_config.check_state(name, state)
        return time_used

    def _check_takeoff_state(self, single_drone_command: SingleDroneCommand, drone_state_map: Dict[str, State]):
        drone_name = single_drone_command.drone_name
        command = single_drone_command.command
        if command.opcode == 'wait':
            # `wait` can be called in both cases
            pass
        elif command.opcode == "takeoff":
            # `takeoff` can only be called when has not taken off
            if drone_state_map[drone_name].has_taken_off:
                raise SafetyCheckError("'{}' command used when drone '{}' has already been taken off"
                                       .format(command.opcode, drone_name))
        else:
            # other commands can only be called when has taken off
            if not drone_state_map[drone_name].has_taken_off:
                raise SafetyCheckError("'{}' command used when drone '{}' has not been taken off"
                                       .format(command.opcode, drone_name))

    def _update_states(self, single_drone_command: SingleDroneCommand,
                       state_updaters: Dict[str, StateUpdater],
                       drone_state_map: Dict[str, State],
                       drones_involved: Set[str]) -> float:
        drone_name = single_drone_command.drone_name
        command = single_drone_command.command
        old_state = drone_state_map[drone_name]
        new_state = state_updaters[drone_name].update(command, old_state)
        drone_state_map[drone_name] = new_state
        # update other drones
        time_used = new_state.time_used_seconds - old_state.time_used_seconds
        for name in drones_involved.difference({drone_name}):
            state = drone_state_map[name]
            drone_state_map[name] = state.copy_and_set_time_used_seconds(state.time_used_seconds + time_used)
        return time_used

    def _update_states_and_check_parallel_drone_commands(self, parallel_drone_commands: ParallelDroneCommands,
                                                         state_updaters: Dict[str, StateUpdater],
                                                         drone_state_map: Dict[str, State],
                                                         drones_involved: Set[str]) -> float:
        assert len(parallel_drone_commands.branches) > 0
        time_used_in_branches = self._update_states_and_check_for_each_branch(parallel_drone_commands,
                                                                              state_updaters,
                                                                              drone_state_map)
        longest_time_used = self._update_states_to_wait_for_slowest_branch(parallel_drone_commands,
                                                                           drone_state_map,
                                                                           time_used_in_branches,
                                                                           drones_involved)

        for name, state in drone_state_map.items():
            self.safety_config.check_state(name, state)
        return longest_time_used

    def _update_states_and_check_for_each_branch(self, parallel_drone_commands: ParallelDroneCommands,
                                                 state_updaters: Dict[str, StateUpdater],
                                                 drone_state_map: Dict[str, State]) -> List[float]:
        time_used_in_branches = []
        for i, branch in enumerate(parallel_drone_commands.branches):
            drones_involved = parallel_drone_commands.drones_involved_each_branch[i]
            time_used = self._update_states_and_check_drone_commands(branch, state_updaters,
                                                                     drone_state_map, drones_involved)
            time_used_in_branches.append(time_used)
        return time_used_in_branches

    def _update_states_to_wait_for_slowest_branch(self, parallel_drone_commands: ParallelDroneCommands,
                                                  drone_state_map: Dict[str, State],
                                                  time_used_in_branches: List[float],
                                                  drones_involved: Set[str]) -> float:
        longest_time_used = max(time_used_in_branches)
        # for each branch, let drones involved in the branch wait until longest_time_used
        for i, time_used in enumerate(time_used_in_branches):
            for name in parallel_drone_commands.drones_involved_each_branch[i]:
                old_state = drone_state_map[name]
                drone_state_map[name] = old_state.copy_and_set_time_used_seconds(
                    old_state.time_used_seconds + longest_time_used - time_used)
        # let drones not involved in any branch wait for longest_time_used
        for name in drones_involved.difference(parallel_drone_commands.get_drones_involved()):
            old_state = drone_state_map[name]
            drone_state_map[name] = old_state.copy_and_set_time_used_seconds(
                old_state.time_used_seconds + longest_time_used)
        return longest_time_used
