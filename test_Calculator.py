
import unittest
from Calculator import SimpleCalculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = SimpleCalculator()

    def test_addition(self):
        result = self.calc.calculate("add", 5, 3)
        self.assertEqual(result, 8)
        result = self.calc.calculate("add", 5)
        self.assertEqual(result, 13) # 8 + 5 from last result
        print("Addition test passed.")

    def test_subtraction(self):
        result = self.calc.calculate("subtract", 10, 4)
        self.assertEqual(result, 6)
        result = self.calc.calculate("subtract", 2)
        self.assertEqual(result, 4)
        result = self.calc.calculate("subtract", 0, 5)
        self.assertEqual(result, -5)
        result = self.calc.calculate("subtract", -5)
        self.assertEqual(result, 0)  # 5 - 5 from last result

    def test_multiplication(self):
        result = self.calc.calculate("multiply", 3, 4)
        self.assertEqual(result, 12)
        result = self.calc.calculate("multiply", 2)
        self.assertEqual(result, 24)

    def test_division(self):
        result = self.calc.calculate("divide", 8, 2)
        self.assertEqual(result, 4)
        result = self.calc.calculate("divide", 4)
        self.assertEqual(result, 1)
        result = self.calc.calculate("divide", 0, 5)
        self.assertEqual(result, 0)
        result = self.calc.calculate("divide", 5)
        self.assertEqual(result, 0)  # 5 / 5 from last result

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("divide", 5, 0)

    def test_power(self):
        result = self.calc.calculate("power", 2, 3)
        self.assertEqual(result, 8)
        result = self.calc.calculate("power", 2)
        self.assertEqual(result, 64)

    def test_root(self):
        result = self.calc.calculate("root", 16, 2)
        self.assertEqual(result, 4)
        result = self.calc.calculate("root", 2)
        self.assertEqual(result, 2)

    def test_invalid_action_name(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("invalid_action", 5, 3)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("divide", 5, 0)

    def test_progress(self):
        # Test the progress of calculations
        self.calc.calculate("add", 10, 5)
        self.calc.calculate("subtract", 3)
        last_result = self.calc.get_last_result()
        self.assertEqual(last_result, 12)
        self.calc.calculate("multiply", 2, 3)
        last_result = self.calc.get_last_result()
        self.assertEqual(last_result, 6)
        self.calc.calculate("divide",  2)
        self.calc.calculate("power",  3)
        self.calc.calculate("root", 3)
        # Check the last result after a series of operations
        last_result = self.calc.get_last_result()
        self.assertEqual(last_result, 3)
