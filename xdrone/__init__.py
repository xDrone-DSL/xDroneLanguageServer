from typing import Dict

import antlr4

from antlr.xDroneLexer import xDroneLexer, CommonTokenStream
from antlr.xDroneParser import xDroneParser
from xdrone.compiler.compiler import Compiler
from xdrone.compiler.compiler_utils.drones import Drone
from xdrone.compiler.compiler_utils.error_listener import ParserErrorListener
from xdrone.compiler.compiler_utils.expressions import Expression
from xdrone.compiler.compiler_utils.functions import FunctionTable
from xdrone.compiler.compiler_utils.symbol_table import SymbolTable
from xdrone.config_parsers.config_parser import ConfigParser
from xdrone.safety_checker.boundary_checker import BoundaryChecker
from xdrone.safety_checker.collision_checker import CollisionChecker
from xdrone.shared.boundary_config import BoundaryConfig
from xdrone.shared.collision_config import DefaultCollisionConfig
from xdrone.shared.compile_error import XDroneSyntaxError
from xdrone.shared.drone_config import DefaultDroneConfig, DroneConfig
from xdrone.shared.safety_check_error import SafetyCheckError
from xdrone.state_updaters.state_updater import StateUpdater


def generate_commands(program, drone_config_map: Dict[str, DroneConfig] = None,
                      boundary_checker: BoundaryChecker = None, collision_checker: CollisionChecker = None,
                      has_checks: bool = True, symbol_table: SymbolTable = None, function_table: FunctionTable = None):
    if drone_config_map is None:
        drone_config_map = {"DEFAULT": DefaultDroneConfig()}
    if boundary_checker is None:
        boundary_checker = BoundaryChecker(BoundaryConfig.no_limit())
    if collision_checker is None:
        collision_checker = CollisionChecker(drone_config_map, DefaultCollisionConfig())
    if symbol_table is None:
        symbol_table = SymbolTable()
    if function_table is None:
        function_table = FunctionTable()
    state_updater_map = {name: StateUpdater(config) for name, config in drone_config_map.items()}

    tree = _parse_program(program)

    drone_commands = Compiler(drone_config_map, symbol_table, function_table).visit(tree)

    if has_checks:
        boundary_checker.check(drone_commands, state_updater_map)
        collision_checker.check(drone_commands, state_updater_map)

    return drone_commands


def _parse_program(program):
    input_stream = antlr4.InputStream(program)
    # lexing
    lexer = xDroneLexer(input_stream)
    stream = CommonTokenStream(lexer)
    # parsing
    parser = xDroneParser(stream)
    parser.removeErrorListeners()
    error_listener = ParserErrorListener()
    parser.addErrorListener(error_listener)
    tree = parser.prog()
    if error_listener.syntax_errors:
        raise XDroneSyntaxError(error_listener.get_error_string())
    return tree


def generate_commands_with_config(program, config_json, has_checks):
    drone_config_map, boundary_config, collision_config = ConfigParser.parse(config_json)
    boundary_checker = BoundaryChecker(boundary_config)
    collision_checker = CollisionChecker(drone_config_map, collision_config)
    return (generate_commands(program, drone_config_map, boundary_checker, collision_checker, has_checks),
            drone_config_map, boundary_config)
