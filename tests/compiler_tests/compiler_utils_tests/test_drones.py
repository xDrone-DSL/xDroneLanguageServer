import unittest

from xdrone.compiler.compiler_utils.drones import Drone, NullDrone
from xdrone.shared.drone_config import DefaultDroneConfig, DroneConfig


class TestDrone(unittest.TestCase):
    def test_property(self):
        self.assertEqual("a", Drone("a", DefaultDroneConfig()).name)
        self.assertEqual(DefaultDroneConfig(), Drone("a", DefaultDroneConfig()).config)

    def test_str(self):
        self.assertEqual("Drone: {{ name: a, config: {} }}".format(DefaultDroneConfig())
                         , str(Drone("a", DefaultDroneConfig())))

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
