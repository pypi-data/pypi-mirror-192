import unittest
from calculator_2023_02_15 import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.calculator.add(5)
        self.assertEqual(self.calculator.value, 5)

    def test_subtract(self):
        self.calculator.subtract(5)
        self.assertEqual(self.calculator.value, -5)

    def test_multiply_by(self):
        self.calculator.multiply_by(5)
        self.assertEqual(self.calculator.value, 0)

    def test_divide_by(self):
        self.calculator.divide_by(5)
        self.assertEqual(self.calculator.value, 0)

    def test_take_root(self):
        self.calculator.set_value(25)
        self.calculator.take_root(2)
        self.assertEqual(self.calculator.value, 5)

    def test_set_value(self):
        self.calculator.set_value(10)
        self.assertEqual(self.calculator.value, 10)
        self.calculator.set_value()
        self.assertEqual(self.calculator.value, 0)

if __name__ == '__main__':
    unittest.main()