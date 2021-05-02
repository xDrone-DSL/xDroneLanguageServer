import logging
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
@click.option('--timeout', default=5, type=click.INT, help='Timeout of compilation.')
@click.option('--port', default=8080, type=click.INT, help='Port on localhost where the simulator server is running.')
def xdrone(function, code, config, timeout, port):
    with open(code, mode='r') as file:
        program = file.read()
    with open(config, mode='r') as file:
        config = file.read()

    queue = multiprocessing.Queue()
    _run_with_timeout(_validate, (program, config, queue), timeout,
                      "Timed out. Please check whether your code contains an infinite loop. " +
                      "Your can change the timeout time by adding the '--timeout' tag.")
    if queue.empty():
        return
    drone_commands, drone_config_map = queue.get()
    if function == "simulate":
        _simulate(drone_commands, drone_config_map, port)
    if function == "fly":
        _fly(drone_commands)


def _run_with_timeout(target, args, timeout, timeout_msg="Timeout"):
    p = multiprocessing.Process(target=target, args=args)
    p.start()
    p.join(timeout)
    if p.is_alive():
        print(timeout_msg)
        p.terminate()
        p.join()


def _validate(program, config, queue):
    print("Validating your program...")
    try:
        drone_commands, drone_config_map, _ = generate_commands_with_config(program, config)
        print("Your program is valid.")
        queue.put((drone_commands, drone_config_map))
    except Exception as e:
        print("Failed to validate your program, error: " + str(e))


def _simulate(drone_commands, drone_config_map, port):
    print("Start simulation...")
    if not _is_port_in_use(port):
        print("Aborted. Please make sure xDrone Simulator is running on localhost port {}. ".format(port) +
              "Your can change the port by adding the '--port' tag.")
        return
    simulation_json = SimulationConverter().convert(drone_commands, drone_config_map)
    url = "http://localhost:{}/?data={}".format(port, urllib.parse.quote(simulation_json))
    print(url)
    webbrowser.open(url)


def _is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def _fly(drone_commands):
    print("Start to fly your drone...")
    # TODO the following is for one drone only
    DJITelloExecutor().execute_commands(drone_commands)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    xdrone(standalone_mode=False)
