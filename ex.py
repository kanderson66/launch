import unittest
from ex_test import Car

class CarTest(unittest.TestCase):
    def test_car_exists(self):
        car = Car()
        self.assertTrue(car is not None)

    def test_wheels(self):
        car = Car()
        self.assertEqual(4, car.wheels)

    def test_name_is_none(self):
        car = Car()
        self.assertIsNone(car.name)

    def test_instance_of_car(self):
        car = Car()
        self.assertIsInstance(car, Car)
        # This test is more useful when dealing with inheritance.
        # This example is a bit contrived.

    def test_includes_car(self):
        car = Car()
        arr = [1, 2, 3]
        arr.append(car)
        self.assertIn(car, arr)

    @unittest.skip
    def test_bad_wheels(self):
        car = Car()
        self.assertEqual(3, car.wheels)

if __name__ == '__main__':
    unittest.main()
Output