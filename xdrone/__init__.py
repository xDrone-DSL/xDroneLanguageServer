import antlr4

from antlr.xDroneLexer import xDroneLexer, CommonTokenStream
from antlr.xDroneParser import xDroneParser
from xdrone.config_parsers.config_parser import ConfigParser
from xdrone.visitors.compiler_utils.command import Command
from xdrone.visitors.compiler_utils.compile_error import XDroneSyntaxError
from xdrone.visitors.compiler_utils.error_listener import ParserErrorListener
from xdrone.visitors.compiler_utils.functions import FunctionTable
from xdrone.visitors.compiler_utils.symbol_table import SymbolTable
from xdrone.visitors.compiler_utils.type_hints import NestedCommands
from xdrone.visitors.fly import Fly
from xdrone.visitors.interpreter import Interpreter
from xdrone.visitors.state_safety_checker.drone_config import DroneConfig, DefaultDroneConfig
from xdrone.visitors.state_safety_checker.safety_checker import SafetyChecker
from xdrone.visitors.state_safety_checker.safety_config import SafetyConfig
from xdrone.visitors.state_safety_checker.state_updater import StateUpdater
from xdrone.visitors.validate import Validate


def fly(program, rs, addr="d0:3a:86:9d:e6:5a"):
    # TODO
    pass
    # parse_tree = xdrone_parser.parse(program)
    # requirements = generate_requirements(rs)
    # Fly(addr, requirements).visit(parse_tree)
    #
    # return all(r.is_completed() for r in requirements)


def validate(program, bounds):
    # TODO
    pass
    # parse_tree = xdrone_parser.parse(program)
    # validator = Validate()
    # validator.visit(parse_tree)
    #
    # if validator.max_z > bounds["height"]:
    #     return {"success": False, "message": "The drone flies too high"}
    # if (
    #     abs(validator.max_x) > bounds["width"] / 2 or
    #     abs(validator.min_x) > bounds["width"] / 2 or
    #     abs(validator.max_y) > bounds["depth"] / 2 or
    #     abs(validator.min_y) > bounds["depth"] / 2
    # ):
    #     return {"success": False, "message": "The drone flies out of bounds"}
    #
    # return {"success": True}


def generate_simulation_json(program, state_updater=None, safety_checker=None):
    commands = generate_commands(program, state_updater, safety_checker)
    return [command.to_simulation_json() for command in commands]


def generate_commands(program, state_updater: StateUpdater = None, safety_checker: SafetyChecker = None,
                      symbol_table: SymbolTable = None, function_table: FunctionTable = None):
    if state_updater is None:
        state_updater = StateUpdater(DefaultDroneConfig())
    if safety_checker is None:
        safety_checker = SafetyChecker(SafetyConfig.no_limit())
    if symbol_table is None:
        symbol_table = SymbolTable()
    if function_table is None:
        function_table = FunctionTable()

    tree = _parse_program(program)

    commands, states = Interpreter(state_updater, symbol_table, function_table).visit(tree)

    safety_checker.check(commands, states)

    return commands


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


def generate_commands_with_config(program, config_json):
    drone_config, safety_config = ConfigParser.parse(config_json)
    state_updater = StateUpdater(drone_config)
    safety_checker = SafetyChecker(safety_config)
    return generate_commands(program, state_updater, safety_checker)
