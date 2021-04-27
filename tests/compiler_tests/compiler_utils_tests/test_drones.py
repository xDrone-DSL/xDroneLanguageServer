import unittest

from xdrone.compiler.compiler_utils.drones import DroneIdentifier


class TestDroneIdentifier(unittest.TestCase):
    def test_property(self):
        self.assertEqual("a", DroneIdentifier("a").ident)

    def test_str(self):
        self.assertEqual("DroneIdentifier: { ident: a }", str(DroneIdentifier("a")))

    def test_eq(self):
        self.assertEqual(DroneIdentifier("a"), DroneIdentifier("a"))
        self.assertNotEqual(DroneIdentifier("a"), DroneIdentifier("abc"))
        self.assertNotEqual(DroneIdentifier("a"), None)
