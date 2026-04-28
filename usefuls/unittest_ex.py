import unittest

class Car:
    def __init__(self):
        self.wheels = 4

class TestCar(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        
    def test_wheels(self):
        self.assertEqual(4, self.car.wheels)
        
    def test_type(self):
        with self.assertRaises(TypeError):
            self.car.wheels += 'b'
    
    @unittest.skip
    def test_skip(self):
        self.assertNotEqual(2, self.car.wheels)
        
if __name__ == '__main__':
    unittest.main()
