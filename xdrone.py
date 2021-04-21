import multiprocessing
import urllib.parse
import webbrowser

import click

from xdrone import generate_commands_with_config
from xdrone.command_converters.dji_tello_drone_executor import DJITelloExecutor
from xdrone.command_converters.simulation_converter import SimulationConverter


@click.command()
@click.option('--validate', 'function', flag_value='validate', help='Validate your code.', default=True)
@click.option('--simulate', 'function', flag_value='simulate', help='Simulate the drone flight.')
@click.option('--fly', 'function', flag_value='fly', help='Fly the drone.')
@click.option('--code', type=click.Path(), help='The file contains your code.')
@click.option('--config', type=click.Path(), help='The configuration json of your drone and flight environment.')
@click.option('--timeout', type=click.INT, help='Timeout.')
def xdrone(function, code, config, timeout):
    with open(code, mode='r') as file:
        program = file.read()
    with open(config, mode='r') as file:
        config = file.read()

    if function == "validate":
        timeout = 5 if timeout is None else timeout
        _run_with_timeout(_validate, (program, config), timeout)
    if function == "simulate":
        timeout = 5 if timeout is None else timeout
        _run_with_timeout(_simulate, (program, config), timeout)
    if function == "fly":
        timeout = 30 if timeout is None else timeout
        _run_with_timeout(_fly, (program, config), timeout)


def _run_with_timeout(target, args, timeout):
    p = multiprocessing.Process(target=target, args=args)
    p.start()
    p.join(timeout)
    if p.is_alive():
        print("Timeout")
        p.terminate()
        p.join()


def _validate(program, config):
    try:
        generate_commands_with_config(program, config)
        print("Your program is valid.")
    except Exception as e:
        print("Failed to validate your program, error: " + str(e))


def _simulate(program, config):
    try:
        commands = generate_commands_with_config(program, config)
        print("Your program is valid.")
    except Exception as e:
        print("Failed to validate your program, error: " + str(e))
        return
    print("Start simulation...")
    if not _is_port_in_use(8080):
        print("Aborted. Please make sure xDrone Simulator is running at localhost port 8080")
        return
    simulation_json = SimulationConverter().convert_commands(commands)
    url = "http://localhost:8080/?commands=" + urllib.parse.quote(simulation_json)
    print(url)
    webbrowser.open(url)


def _is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def _fly(program, config):
    try:
        commands = generate_commands_with_config(program, config)
        print("Your program is valid.")
    except Exception as e:
        print("Failed to validate your program, error: " + str(e))
        return
    print("Start to fly your drone...")
    DJITelloExecutor().execute_commands(commands)


if __name__ == '__main__':
    xdrone()
