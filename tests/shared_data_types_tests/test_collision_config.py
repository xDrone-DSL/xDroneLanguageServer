import unittest

from xdrone.shared.collision_config import CollisionConfig, DefaultCollisionConfig


class CollisionConfigTest(unittest.TestCase):
    def test_init_with_wrong_parameter_should_give_error(self):
        for invalid_value in [-10, -1]:
            with self.assertRaises(ValueError) as context:
                CollisionConfig(collision_meters=invalid_value)
            self.assertTrue("collision_meters should >= 0" in str(context.exception))
        for invalid_value in [-10, -1, 0]:
            with self.assertRaises(ValueError) as context:
                CollisionConfig(time_interval_seconds=invalid_value)
            self.assertTrue("time_interval_seconds should > 0" in str(context.exception))

    def test_property(self):
        drone_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5)
        self.assertEqual(0.3, drone_config.collision_meters)
        self.assertEqual(0.5, drone_config.time_interval_seconds)

    def test_str(self):
        drone_config = CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5)
        self.assertEqual("CollisionConfig: { collision_meters: 0.3, time_interval_seconds: 0.5 }", str(drone_config))

    def test_eq(self):
        self.assertEqual(CollisionConfig(),
                         CollisionConfig())
        self.assertEqual(CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5),
                         CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5))
        self.assertNotEqual(CollisionConfig(collision_meters=0.1, time_interval_seconds=0.5),
                            CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5))
        self.assertNotEqual(CollisionConfig(collision_meters=0.3, time_interval_seconds=0.1),
                            CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5))
        self.assertNotEqual(None,
                            CollisionConfig(collision_meters=0.3, time_interval_seconds=0.5))


class DefaultCollisionConfigTest(unittest.TestCase):
    def test_default_values(self):
        collision_config = DefaultCollisionConfig()
        self.assertEqual(0, collision_config.collision_meters)
        self.assertEqual(0.1, collision_config.time_interval_seconds)
