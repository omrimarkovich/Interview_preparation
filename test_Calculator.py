import unittest
from Calculator import SimpleCalculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = SimpleCalculator()

    def test_addition(self):
        result = self.calc.calculate("add", "5", "3")
        self.assertEqual(result, 8)
        result = self.calc.calculate("add", "5")
        self.assertEqual(result, 13)  # 8 + 5 from last result
        print("Addition test passed.")

    def test_subtraction(self):
        result = self.calc.calculate("subtract", "10", "4")
        self.assertEqual(result, 6)
        result = self.calc.calculate("subtract", "2")
        self.assertEqual(result, 4)
        result = self.calc.calculate("subtract", "0", "5")
        self.assertEqual(result, -5)
        result = self.calc.calculate("subtract", "-5")
        self.assertEqual(result, 0)  # 5 - 5 from last result

    def test_multiplication(self):
        result = self.calc.calculate("multiply", "3", "4")
        self.assertEqual(result, 12)
        result = self.calc.calculate("multiply", "2")
        self.assertEqual(result, 24)

    def test_division(self):
        result = self.calc.calculate("divide", "8", "2")
        self.assertEqual(result, 4)
        result = self.calc.calculate("divide", "4")
        self.assertEqual(result, 1)
        result = self.calc.calculate("divide", "0", "5")
        self.assertEqual(result, 0)
        result = self.calc.calculate("divide", "5")
        self.assertEqual(result, 0)  # 5 / 5 from last result

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.calculate("divide", "5", "0")

    def test_power(self):
        result = self.calc.calculate("power", "2", "3")
        self.assertEqual(result, 8)
        result = self.calc.calculate("power", "2")
        self.assertEqual(result, 64)
        with self.assertRaises(ValueError):
            self.calc.calculate("power", "-8", "0.5")


    def test_root(self):
        result = self.calc.calculate("root", "16", "2")
        self.assertEqual(result, 4)
        result = self.calc.calculate("root", "2")
        self.assertEqual(result, 2)

    def test_negative_root(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("root", "-4", "2")

    def test_invalid_action_name(self):
        with self.assertRaises(ValueError):
            self.calc.calculate("invalid_action", "5", "3")

    def test_case_sensitivity(self):
        # Test that action names are case-insensitive
        result = self.calc.calculate("ADD", "5", "3")
        self.assertEqual(result, 8)
        result = self.calc.calculate("Subtract", "10", "4")
        self.assertEqual(result, 6)
        result = self.calc.calculate("MULTIPLY", "2", "3")
        self.assertEqual(result, 6)

    def test_no_calculation_performed(self):
        # Test that get_last_result raises ValueError when no calculation has been performed
        calc = SimpleCalculator()  # Create a new calculator instance
        result = calc.get_last_result()
        self.assertIsNone(result)  # Should return None when no calculations have been performed

    # def test_calculate_with_none_values(self):
    #     # Test calculate with a=None when last_result is None
    #     calc = SimpleCalculator()  # Create a new calculator instance
    #     with self.assertRaises(TypeError):
    #         calc.calculate(
    #             "add", None, "5"
    #         )  # This should fail because last_result is None

    # def test_incorrect_number_of_arguments(self):
    #     # Test that an error is raised when the number of arguments is incorrect
    #     with self.assertRaises(ValueError):
    #         self.calc.calculate("add", "5")
    #
    #
    # def test_invalid_arguments(self):
    #     # Test that an error is raised when invalid arguments are passed
    #     # with self.assertRaises(TypeError):
    #     #     self.calc.calculate("add", "five", "3")

    def test_progress_binary(self):
        # Test the progress of calculations
        self.calc.calculate("add", "10", "5")
        self.calc.calculate("subtract", "3")
        last_result = self.calc.get_last_result()
        self.assertEqual(last_result, 12)
        self.calc.calculate("multiply", "2", "3")
        last_result = self.calc.get_last_result()
        self.assertEqual(last_result, 6)
        self.calc.calculate("divide", "2")
        self.calc.calculate("power", "3")
        self.calc.calculate("root", "3")
        # Check the last result after a series of operations
        last_result = self.calc.get_last_result()
        self.assertEqual(last_result, 3)

    def test_progres_more_then_two_arguments(self):
        # Test the progress of calculations with more than two arguments
        self.calc.calculate("add", "10", "5", "2")
        self.calc.calculate("subtract", "3")
        last_result = self.calc.get_last_result()
        self.assertEqual(last_result, 14)
        self.calc.calculate("multiply", "2", "3", "4")
        last_result = self.calc.get_last_result()
        self.assertEqual(last_result, 24)
        result = self.calc.calculate("add" , "None", "4", "2")
        self.assertEqual(self.calc.get_last_result() , 30)

    def test_sin(self):
        # Test the sine function
        result = self.calc.calculate("sin", "0")
        self.assertAlmostEqual(result, 0.0)
        result = self.calc.calculate("sin", "90")
        self.assertAlmostEqual(result, 1.0)
        # with self.assertRaises(TypeError):
        #     self.calc.calculate("sin", "ninety")

    def test_cos(self):
        result = self.calc.calculate("cos", "0")
        self.assertAlmostEqual(result , 1)
        # with self.assertRaises(TypeError):
        #     self.calc.calculate("cos", "one-ninety")


if __name__ == "__main__":
    unittest.main()
