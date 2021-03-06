import unittest

from xdrone.shared.drone_config import DroneConfig, DefaultDroneConfig


class DroneConfigTest(unittest.TestCase):
    def test_init_with_wrong_parameter_should_give_error(self):
        for invalid_value in [-10, -1, 0]:
            with self.assertRaises(ValueError) as context:
                DroneConfig(init_position=(0, 0, 0), speed_mps=invalid_value,
                            rotate_speed_dps=45, takeoff_height_meters=1)
            self.assertTrue("speed_mps should > 0" in str(context.exception))

            with self.assertRaises(ValueError) as context:
                DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                            rotate_speed_dps=invalid_value, takeoff_height_meters=1)
            self.assertTrue("rotate_speed_dps should > 0" in str(context.exception))

            with self.assertRaises(ValueError) as context:
                DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                            rotate_speed_dps=45, takeoff_height_meters=invalid_value)
            self.assertTrue("takeoff_height_meters should > 0" in str(context.exception))

        for invalid_value in [-10, -1]:
            with self.assertRaises(ValueError) as context:
                DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                            rotate_speed_dps=45, takeoff_height_meters=1, var_per_meter=invalid_value)
            self.assertTrue("var_per_meter should >= 0" in str(context.exception))

            with self.assertRaises(ValueError) as context:
                DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                            rotate_speed_dps=45, takeoff_height_meters=1, var_per_degree=invalid_value)
            self.assertTrue("var_per_degree should >= 0" in str(context.exception))

    def test_property(self):
        drone_config = DroneConfig(init_position=(0, 0, 0), speed_mps=0.5, rotate_speed_dps=45, takeoff_height_meters=1,
                                   var_per_degree=1.0, var_per_meter=0.1)
        self.assertEqual((0, 0, 0), drone_config.init_position)
        self.assertEqual(0.5, drone_config.speed_mps)
        self.assertEqual(45, drone_config.rotate_speed_dps)
        self.assertEqual(1, drone_config.takeoff_height_meters)
        self.assertEqual(1.0, drone_config.var_per_degree)
        self.assertEqual(0.1, drone_config.var_per_meter)

    def test_str(self):
        drone_config = DroneConfig(init_position=(0, 0, 0), speed_mps=0.5, rotate_speed_dps=45,
                                   takeoff_height_meters=1, var_per_meter=1.0, var_per_degree=0.1)
        self.assertEqual("DroneConfig: { init_position: (0, 0, 0), speed_mps: 0.5, " +
                         "rotate_speed_dps: 45, takeoff_height_meters: 1, " +
                         "var_per_meter: 1.0, var_per_degree: 0.1 }",
                         str(drone_config))

    def test_eq(self):
        self.assertEqual(DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                     rotate_speed_dps=45, takeoff_height_meters=1),
                         DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                     rotate_speed_dps=45, takeoff_height_meters=1))
        self.assertNotEqual(DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=1),
                            DroneConfig(init_position=(1, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=1))
        self.assertNotEqual(DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=1),
                            DroneConfig(init_position=(0, 0, 0), speed_mps=1,
                                        rotate_speed_dps=45, takeoff_height_meters=1))
        self.assertNotEqual(DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=1),
                            DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=90, takeoff_height_meters=1))
        self.assertNotEqual(DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=1),
                            DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=2))
        self.assertNotEqual(DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=1, var_per_meter=1.0),
                            DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=1, var_per_meter=2.0))
        self.assertNotEqual(DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=1, var_per_degree=1.0),
                            DroneConfig(init_position=(0, 0, 0), speed_mps=0.5,
                                        rotate_speed_dps=45, takeoff_height_meters=1, var_per_degree=2.0))
        self.assertNotEqual(None,
                            DroneConfig(init_position=(0, 0, 0), speed_mps=0.5, rotate_speed_dps=45,
                                        takeoff_height_meters=2))


class DefaultDroneConfigTest(unittest.TestCase):
    def test_default_values(self):
        drone_config = DefaultDroneConfig()
        self.assertEqual(1, drone_config.speed_mps)
        self.assertEqual(90, drone_config.rotate_speed_dps)
        self.assertEqual(1, drone_config.takeoff_height_meters)
        self.assertEqual(0.0, drone_config.var_per_meter)
        self.assertEqual(0.0, drone_config.var_per_degree)
