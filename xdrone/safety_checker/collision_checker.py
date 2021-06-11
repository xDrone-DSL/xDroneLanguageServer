from __future__ import annotations

import copy
import itertools
import math
from scipy.stats import ncx2
from itertools import combinations
from typing import List, Dict, Set

from xdrone.shared.collision_config import CollisionConfig
from xdrone.shared.command import AbstractDroneCommand, SingleDroneCommand, ParallelDroneCommands, Command
from xdrone.shared.drone_config import DroneConfig
from xdrone.shared.safety_check_error import SafetyCheckError
from xdrone.shared.state import State
from xdrone.state_updaters.state_updater import StateUpdater


class StateVariance:
    def __init__(self, state: State, variance: float = 0.0):
        self._state = state
        self._variance = variance

    @property
    def variance(self) -> float:
        return copy.deepcopy(self._variance)

    @property
    def state(self) -> State:
        return copy.deepcopy(self._state)


class CollisionChecker:
    def __init__(self, drone_config_map: Dict[str, DroneConfig], collision_config: CollisionConfig):
        self.drone_config_map = drone_config_map
        self.collision_config = collision_config

    def check(self, drone_commands: List[AbstractDroneCommand], state_updater_map: Dict[str, StateUpdater]):
        if len(self.drone_config_map) == 1:
            # no need to check if there is only 1 drone
            return
        drone_trajectory_map = {name: [StateVariance(state_updater.get_init_state())] for name, state_updater in
                                state_updater_map.items()}
        drones_involved = set(state_updater_map.keys())
        try:
            self._update_states_for_abstract_drone_command(drone_commands, state_updater_map, drone_trajectory_map,
                                                           drones_involved)
        except Exception as e:
            raise SafetyCheckError("Error occurred during collision check, "
                                   "please retry with a better collision_config. Error: " + str(e))
        self._check_distance(drone_trajectory_map)

    def _check_distance(self, drone_trajectory_map):
        time = 0
        collisions = []
        drone_trajectories = dict(drone_trajectory_map)
        while any(drone_trajectories.values()):
            time += self.collision_config.time_interval_seconds
            state_group = []
            for name, drone_trajectory in drone_trajectories.items():
                possible_states = []
                while drone_trajectory and drone_trajectory[0].state.time_used_seconds < time:
                    state_variance = drone_trajectory.pop(0)
                    possible_states.append((name, state_variance))
                if possible_states:
                    state_group.append(possible_states)
            # Commented out: check all possible states combinations if one drone has multiple states in time interval
            # possible_combinations = list(itertools.product(*state_group))
            # Only check combinations of last states if one drone has multiple states in time interval
            state_group = [possible_states[-1] for possible_states in state_group]
            possible_combinations = list(itertools.combinations(state_group, r=2))
            for possible_combination in possible_combinations:
                for (name1, state_variance1), (name2, state_variance2) in combinations(possible_combination, r=2):
                    state1, variance1 = state_variance1.state, state_variance1.variance
                    state2, variance2 = state_variance2.state, state_variance2.variance
                    variance = variance1 + variance2

                    x = state1.x_meters - state2.x_meters
                    y = state1.y_meters - state2.y_meters
                    z = state1.z_meters - state2.z_meters
                    mean_distance = math.sqrt(x ** 2 + y ** 2 + z ** 2)
                    collision_meters = self.collision_config.collision_meters

                    if math.isclose(variance, 0):
                        # when variance is 0, perform as determined, confidence is either 1 or 0
                        if collision_meters == 0:
                            confidence = 0.0
                        elif mean_distance > collision_meters + 1e-5:
                            confidence = 0.0
                        else:
                            confidence = 1.0
                    else:
                        # use non central chi-squared distribution to calculated confidence
                        nc = x ** 2 / variance + y ** 2 / variance + z ** 2 / variance
                        confidence = ncx2.cdf(collision_meters ** 2 / variance, df=3, nc=nc)

                    if confidence >= self.collision_config.confidence_threshold - 1e-5:
                        collisions.append((name1, name2, state1, state2, mean_distance, confidence))

                    # print("{}-{}, time {:.2f}s, distance={:.2f}m, confidence={:.3f}%"
                    #       .format(name1, name2, time, mean_distance, confidence * 100))

        if collisions:
            error_msg = "Collisions might happen!\n"
            for name1, name2, state1, state2, mean_distance, confidence in collisions:
                time = round((state1.time_used_seconds + state2.time_used_seconds) / 2, 2)
                x = round((state1.x_meters + state2.x_meters) / 2, 2)
                y = round((state1.y_meters + state2.y_meters) / 2, 2)
                z = round((state1.z_meters + state2.z_meters) / 2, 2)
                mean_distance = round(mean_distance, 5)
                confidence = round(confidence, 5) * 100
                error_msg += ("Collision might happen between {} and {}, at time {}s, ".format(name1, name2, time) +
                              "near position (x={}m, y={}m, z={}m), distance={}m, confidence={}%\n"
                              .format(x, y, z, mean_distance, confidence))
            raise SafetyCheckError(error_msg)

    def _update_states_for_abstract_drone_command(self, drone_commands: List[AbstractDroneCommand],
                                                  state_updaters: Dict[str, StateUpdater],
                                                  drone_trajectory_map: Dict[str, List[StateVariance]],
                                                  drones_involved: Set[str]) -> float:
        total_time_used = 0
        for drone_command in drone_commands:
            if isinstance(drone_command, SingleDroneCommand):
                total_time_used += self._update_states_for_single_drone_command(drone_command,
                                                                                state_updaters,
                                                                                drone_trajectory_map,
                                                                                drones_involved)
            elif isinstance(drone_command, ParallelDroneCommands):
                total_time_used += self._update_states_for_parallel_drone_commands(drone_command,
                                                                                   state_updaters,
                                                                                   drone_trajectory_map,
                                                                                   drones_involved)
        return total_time_used

    def _update_states_for_single_drone_command(self, single_drone_command: SingleDroneCommand,
                                                state_updaters: Dict[str, StateUpdater],
                                                drone_trajectory_map: Dict[str, List[StateVariance]],
                                                drones_involved: Set[str]) -> float:
        time_used = self._update_states(single_drone_command, state_updaters, drone_trajectory_map, drones_involved)
        return time_used

    def _get_last_state_and_variance(self, drone_trajectory_map: Dict[str, List[StateVariance]],
                                     drone_name: str) -> (State, float):
        old_state_variance = drone_trajectory_map[drone_name][-1]
        old_state = old_state_variance.state
        old_variance = old_state_variance.variance
        return old_state, old_variance

    def _update_states(self, single_drone_command: SingleDroneCommand,
                       state_updaters: Dict[str, StateUpdater],
                       drone_trajectory_map: Dict[str, List[StateVariance]],
                       drones_involved: Set[str]) -> float:
        time_interval = self.collision_config.time_interval_seconds
        drone_name = single_drone_command.drone_name
        command = single_drone_command.command
        if command.opcode == "takeoff":
            takeoff_distance = self.drone_config_map[drone_name].takeoff_height_meters
            new_drone_command = SingleDroneCommand(drone_name, Command.up(takeoff_distance))
            return self._update_states(new_drone_command, state_updaters, drone_trajectory_map, drones_involved)
        if command.opcode == "land":
            old_state, old_variance = self._get_last_state_and_variance(drone_trajectory_map, drone_name)
            land_distance = old_state.z_meters
            new_drone_command = SingleDroneCommand(drone_name, Command.down(land_distance))
            return self._update_states(new_drone_command, state_updaters, drone_trajectory_map, drones_involved)
        if command.opcode == "wait":
            seconds, = command.operands
            old_state, old_variance = self._get_last_state_and_variance(drone_trajectory_map, drone_name)
            if seconds <= time_interval:
                new_state = state_updaters[drone_name].update(Command.wait(seconds), old_state)
                new_state_variance = StateVariance(new_state, old_variance)
                drone_trajectory_map[drone_name].append(new_state_variance)
                for name in drones_involved.difference({drone_name}):
                    state, variance = self._get_last_state_and_variance(drone_trajectory_map, name)
                    state = state.copy_and_set_time_used_seconds(state.time_used_seconds + seconds)
                    drone_trajectory_map[name].append(StateVariance(state, variance))
                return seconds
            else:
                new_state = state_updaters[drone_name].update(Command.wait(time_interval), old_state)
                new_state_variance = StateVariance(new_state, old_variance)
                drone_trajectory_map[drone_name].append(new_state_variance)
                for name in drones_involved.difference({drone_name}):
                    state, variance = self._get_last_state_and_variance(drone_trajectory_map, name)
                    state = state.copy_and_set_time_used_seconds(state.time_used_seconds + time_interval)
                    drone_trajectory_map[name].append(StateVariance(state, variance))
                new_drone_command = SingleDroneCommand(drone_name, Command.wait(seconds - time_interval))
                return time_interval + self._update_states(new_drone_command, state_updaters, drone_trajectory_map,
                                                           drones_involved)
        if command.opcode in ["rotate_left", "rotate_right"]:
            degrees, = command.operands
            old_state, old_variance = self._get_last_state_and_variance(drone_trajectory_map, drone_name)
            rotate_speed = self.drone_config_map[drone_name].rotate_speed_dps
            seconds = degrees / rotate_speed
            if seconds <= time_interval:
                new_state = state_updaters[drone_name].update(Command(command.opcode, [rotate_speed * seconds]),
                                                              old_state)
                new_variance = old_variance + self.drone_config_map[drone_name].var_per_degree * seconds * rotate_speed
                new_state_variance = StateVariance(new_state, new_variance)
                drone_trajectory_map[drone_name].append(new_state_variance)
                for name in drones_involved.difference({drone_name}):
                    state, variance = self._get_last_state_and_variance(drone_trajectory_map, name)
                    state = state.copy_and_set_time_used_seconds(state.time_used_seconds + seconds)
                    drone_trajectory_map[name].append(StateVariance(state, variance))
                return seconds
            else:
                new_state = state_updaters[drone_name].update(Command(command.opcode, [rotate_speed * time_interval]),
                                                              old_state)
                new_variance = old_variance + \
                               self.drone_config_map[drone_name].var_per_degree * time_interval * rotate_speed
                new_state_variance = StateVariance(new_state, new_variance)
                drone_trajectory_map[drone_name].append(new_state_variance)
                for name in drones_involved.difference({drone_name}):
                    state, variance = self._get_last_state_and_variance(drone_trajectory_map, name)
                    state = state.copy_and_set_time_used_seconds(state.time_used_seconds + time_interval)
                    drone_trajectory_map[name].append(StateVariance(state, variance))
                new_drone_command = SingleDroneCommand(drone_name,
                                                       Command(command.opcode,
                                                               [degrees - rotate_speed * time_interval]))
                return time_interval + self._update_states(new_drone_command, state_updaters, drone_trajectory_map,
                                                           drones_involved)
        if command.opcode in ["up", "down", "left", "right", "forward", "backward"]:
            meters, = command.operands
            old_state_variance = drone_trajectory_map[drone_name][-1]
            old_state = old_state_variance.state
            old_variance = old_state_variance.variance
            speed = self.drone_config_map[drone_name].speed_mps
            seconds = meters / speed
            if seconds <= time_interval:
                new_state = state_updaters[drone_name].update(Command(command.opcode, [speed * seconds]),
                                                              old_state)
                new_variance = old_variance + self.drone_config_map[drone_name].var_per_meter * seconds * speed
                new_state_variance = StateVariance(new_state, new_variance)
                drone_trajectory_map[drone_name].append(new_state_variance)
                for name in drones_involved.difference({drone_name}):
                    state_variance = drone_trajectory_map[name][-1]
                    state = state_variance.state
                    variance = state_variance.variance
                    state = state.copy_and_set_time_used_seconds(state.time_used_seconds + seconds)
                    drone_trajectory_map[name].append(StateVariance(state, variance))
                return seconds
            else:
                new_state = state_updaters[drone_name].update(Command(command.opcode, [speed * time_interval]),
                                                              old_state)
                new_variance = old_variance + self.drone_config_map[drone_name].var_per_meter * time_interval * speed
                new_state_variance = StateVariance(new_state, new_variance)
                drone_trajectory_map[drone_name].append(new_state_variance)
                for name in drones_involved.difference({drone_name}):
                    state_variance = drone_trajectory_map[name][-1]
                    state = state_variance.state
                    variance = state_variance.variance
                    state = state.copy_and_set_time_used_seconds(state.time_used_seconds + time_interval)
                    drone_trajectory_map[name].append(StateVariance(state, variance))
                new_drone_command = SingleDroneCommand(drone_name,
                                                       Command(command.opcode, [meters - speed * time_interval]))
                return time_interval + self._update_states(new_drone_command, state_updaters, drone_trajectory_map,
                                                           drones_involved)

    def _update_states_for_parallel_drone_commands(self, parallel_drone_commands: ParallelDroneCommands,
                                                   state_updaters: Dict[str, StateUpdater],
                                                   drone_trajectory_map: Dict[str, List[StateVariance]],
                                                   drones_involved: Set[str]) -> float:
        assert len(parallel_drone_commands.branches) > 0
        time_used_in_branches = self._update_states_and_check_for_each_branch(parallel_drone_commands,
                                                                              state_updaters,
                                                                              drone_trajectory_map)
        longest_time_used = self._update_states_to_wait_for_slowest_branch(parallel_drone_commands,
                                                                           state_updaters,
                                                                           drone_trajectory_map,
                                                                           time_used_in_branches,
                                                                           drones_involved)
        return longest_time_used

    def _update_states_and_check_for_each_branch(self, parallel_drone_commands: ParallelDroneCommands,
                                                 state_updaters: Dict[str, StateUpdater],
                                                 drone_trajectory_map: Dict[str, List[StateVariance]]) -> List[float]:
        time_used_in_branches = []
        for i, branch in enumerate(parallel_drone_commands.branches):
            drones_involved = parallel_drone_commands.drones_involved_each_branch[i]
            time_used = self._update_states_for_abstract_drone_command(branch, state_updaters,
                                                                       drone_trajectory_map, drones_involved)
            time_used_in_branches.append(time_used)
        return time_used_in_branches

    def _update_states_to_wait_for_slowest_branch(self, parallel_drone_commands: ParallelDroneCommands,
                                                  state_updaters: Dict[str, StateUpdater],
                                                  drone_trajectory_map: Dict[str, List[StateVariance]],
                                                  time_used_in_branches: List[float],
                                                  drones_involved: Set[str]) -> float:
        longest_time_used = max(time_used_in_branches)
        # for each branch, let drones involved in the branch wait until longest_time_used
        for i, time_used in enumerate(time_used_in_branches):
            for name in parallel_drone_commands.drones_involved_each_branch[i]:
                wait_command = Command.wait(longest_time_used - time_used)
                self._update_states_for_single_drone_command(SingleDroneCommand(name, wait_command),
                                                             state_updaters,
                                                             drone_trajectory_map,
                                                             drones_involved={name})
        # let drones not involved in any branch wait for longest_time_used
        for name in drones_involved.difference(parallel_drone_commands.get_drones_involved()):
            wait_command = Command.wait(longest_time_used)
            self._update_states_for_single_drone_command(SingleDroneCommand(name, wait_command),
                                                         state_updaters,
                                                         drone_trajectory_map,
                                                         drones_involved={name})
        return longest_time_used
