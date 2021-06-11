import logging
import multiprocessing
import urllib.parse
import webbrowser

import click

from xdrone import generate_commands_with_config
from xdrone.command_converters.dji_tello_edu_drone_executor import DJITelloEduExecutor
from xdrone.command_converters.simulation_converter import SimulationConverter


@click.command()
@click.option('--validate', 'function', flag_value='validate', help='Validate your code.', default=True)
@click.option('--simulate', 'function', flag_value='simulate', help='Simulate the drone flight.')
@click.option('--fly', 'function', flag_value='fly', help='Fly the drone.')
@click.option('--code', type=click.Path(), help='The file contains your code.')
@click.option('--config', type=click.Path(), help='The configuration json of your drone and flight environment.')
@click.option('--timeout', default=10, type=click.INT, help='Timeout of compilation.')
@click.option('--port', default=8080, type=click.INT, help='Port on localhost where the simulator server is running.')
@click.option('--no-check', is_flag=True, help='No safety check will be performed.')
@click.option('--save-check-log', is_flag=True, help='Save the log of the collision check.')
def xdrone(function, code, config, timeout, port, no_check, save_check_log):
    if code is None:
        code = click.prompt("Please enter path to your code", type=click.Path())
    if config is None:
        config = click.prompt("Please enter path to your configuration", type=click.Path())

    with open(code, mode='r') as file:
        program = file.read()
    with open(config, mode='r') as file:
        config = file.read()

    if no_check:
        if not click.confirm("Safety checks will be skipped, are you sure?"):
            print("Aborted.")
            return

    has_checks = not no_check
    queue = multiprocessing.Queue()
    _run_with_timeout(_validate, (program, config, has_checks, save_check_log, queue), timeout,
                      "Timed out. Please check whether your code contains an infinite loop. " +
                      "Your can change the timeout time by adding the '--timeout' tag.")
    if queue.empty():
        return
    drone_commands, drone_config_map = queue.get()
    if function == "simulate":
        _simulate(drone_commands, drone_config_map, port)
    if function == "fly":
        _fly(drone_commands, drone_config_map)


def _run_with_timeout(target, args, timeout, timeout_msg="Timeout"):
    p = multiprocessing.Process(target=target, args=args)
    p.start()
    p.join(timeout)
    if p.is_alive():
        print(timeout_msg)
        p.terminate()
        p.join()


def _validate(program, config, has_checks, save_check_log, queue):
    print("Validating your program...")
    if not has_checks:
        print("Skipping safety checks... only syntax will be checked")
    if save_check_log:
        print("Logs will be saved at directory ./logs/")
    try:
        drone_commands, drone_config_map, _ = generate_commands_with_config(program, config, has_checks, save_check_log)
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


def _fly(drone_commands, drone_config_map):
    # {"DRONE1": "0TQDG19EDB26V6", "DRONE2": "0TQDG19EDBNC96"}
    name_id_map = {}
    for name in drone_config_map.keys():
        id = click.prompt("Enter your Tello EDU drone id for \"{}\"".format(name), type=click.STRING)
        name_id_map[name] = id

    print("Start to fly your drone...")
    DJITelloEduExecutor(name_id_map).execute_drone_commands(drone_commands)


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        xdrone(standalone_mode=False)
    except Exception as e:
        print("Aborted. Error: {}".format(str(e)))
        return


if __name__ == '__main__':
    main()
