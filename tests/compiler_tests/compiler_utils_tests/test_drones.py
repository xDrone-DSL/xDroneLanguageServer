import unittest

from xdrone import DefaultDroneConfig, DroneConfig
from xdrone.compiler.compiler_utils.drones import Drone, NullDrone


class TestDrone(unittest.TestCase):
    def test_property(self):
        self.assertEqual("a", Drone("a", DefaultDroneConfig()).name)
        self.assertEqual(DefaultDroneConfig(), Drone("a", DefaultDroneConfig()).config)

    def test_str(self):
        self.assertEqual("Drone: { name: a, config: DroneConfig: { init_position: (0, 0, 0), speed_mps: 1, " +
                         "rotate_speed_dps: 90, takeoff_height_meters: 1 } }", str(Drone("a", DefaultDroneConfig())))

    def test_eq(self):
        self.assertEqual(Drone("a", DefaultDroneConfig()), Drone("a", DefaultDroneConfig()))
        self.assertNotEqual(Drone("b", DefaultDroneConfig()), Drone("a", DefaultDroneConfig()))
        self.assertNotEqual(Drone("a", DroneConfig((1, 2, 3), 1, 90, 2)), Drone("a", DefaultDroneConfig()))
        self.assertNotEqual(None, Drone("a", DefaultDroneConfig()))


class TestNullDrone(unittest.TestCase):
    def test_property(self):
        self.assertEqual("null", NullDrone().name)
        self.assertEqual(DefaultDroneConfig(), NullDrone().config)

    def test_str(self):
        self.assertEqual("NullDrone: { }", str(NullDrone()))

    def test_eq(self):
        self.assertEqual(NullDrone(), NullDrone())
        self.assertNotEqual(Drone("a", DefaultDroneConfig()), NullDrone())
        self.assertNotEqual(Drone("null", DefaultDroneConfig()), NullDrone())
        self.assertNotEqual(None, NullDrone())
