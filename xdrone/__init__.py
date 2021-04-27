from typing import Dict

import antlr4

from antlr.xDroneLexer import xDroneLexer, CommonTokenStream
from antlr.xDroneParser import xDroneParser
from xdrone.compiler.compiler import Compiler
from xdrone.compiler.compiler_utils.error_listener import ParserErrorListener
from xdrone.compiler.compiler_utils.functions import FunctionTable
from xdrone.compiler.compiler_utils.symbol_table import SymbolTable
from xdrone.config_parsers.config_parser import ConfigParser
from xdrone.safety_checker.safety_checker import SafetyChecker
from xdrone.shared.compile_error import XDroneSyntaxError
from xdrone.shared.drone_config import DefaultDroneConfig
from xdrone.shared.safety_config import SafetyConfig
from xdrone.state_updaters.state_updater import StateUpdater


def generate_commands(program, state_updaters: Dict[str, StateUpdater] = None, safety_checker: SafetyChecker = None,
                      symbol_table: SymbolTable = None, function_table: FunctionTable = None):
    if state_updaters is None:
        state_updaters = {"default": StateUpdater(DefaultDroneConfig())}
    if safety_checker is None:
        safety_checker = SafetyChecker(SafetyConfig.no_limit())
    if symbol_table is None:
        symbol_table = SymbolTable()
    if function_table is None:
        function_table = FunctionTable()
    drones = set(state_updaters.keys())

    tree = _parse_program(program)

    drone_commands = Compiler(drones, symbol_table, function_table).visit(tree)

    # safety_checker.check(drone_commands, state_updaters)

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


def generate_commands_with_config(program, config_json):
    drone_config, safety_config = ConfigParser.parse(config_json)  # TODO: change drone config and its parser
    state_updaters = StateUpdater(drone_config)  # TODO: should be a dict now
    safety_checker = SafetyChecker(safety_config)
    return generate_commands(program, state_updaters, safety_checker)


if __name__ == '__main__':
    cs = generate_commands("""
    main() {
    int i <- 1;
    hello.takeoff();
    {i <- i + 1 ; hello.up(i);} || {hello2.takeoff();hello2.up(i);hello2.land();};
    hello.up(i);
    hello.land();
    }
    """, state_updaters={"hello": StateUpdater(DefaultDroneConfig()), "hello2": StateUpdater(DefaultDroneConfig())})
    for c in cs:
        print(c)
