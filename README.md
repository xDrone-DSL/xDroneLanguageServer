
This project is available on [Github](https://github.com/xDrone-DSL/xDroneLanguageServer) and [Pypi](https://pypi.org/project/xdrone/).

### To Use
Run `pip install xdrone` for to install the xdrone package.

Then run 
```
xdrone [--validate | --simulate | --fly] --code <code_path> --config <config_path>
```
to validate the code, simulate in the simulator, or fly real drones.

Note that to run the simulation, [xDroneWebSimulator](https://github.com/xDrone-DSL/xDroneWebSimulator) must be running on the localhost.

Run
```
xdrone --help
```
for more information.

### To Develop
Clone the Github repo for the source code.

The terminal commands are similar as before, but with `xdrone` replace by `python cmdline.py`, e.g.
```
python cmdline.py --help
```

### Language Spec
Please read [xDrone Spec](https://github.com/xDrone-DSL/xDroneLanguageServer/blob/master/docs/xDrone-spec.pdf).
