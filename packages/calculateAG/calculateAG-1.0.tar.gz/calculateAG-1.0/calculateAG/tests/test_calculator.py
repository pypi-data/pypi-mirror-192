import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        result = self.calculator.add(10)
        self.assertEqual(result, 10)

        result = self.calculator.add(20)
        self.assertEqual(result, 30)
        

    def test_subtract(self):
        result = self.calculator.subtract(10)
        
        

        result = self.calculator.subtract(20)
        self.assertEqual(result, -30)
        

    def test_multiply(self):
        result = self.calculator.multiply(10)
        self.assertEqual(result, 0)
        

        self.calculator.add(10)
        result = self.calculator.multiply(20)
        self.assertEqual(result, 200)
        

    def test_divide(self):
        result = self.calculator.divide(10)
        self.assertEqual(result, 0)
        

        self.calculator.add(200)
        result = self.calculator.divide(20)
        self.assertEqual(result, 10)
        

    def test_root(self):
        result = self.calculator.root(2)
        self.assertEqual(result, 0)
        

        self.calculator.add(16)
        result = self.calculator.root(2)
        self.assertEqual(result, 4)
        

    def test_reset(self):
        self.calculator.add(10)
        self.calculator.reset()
        self.assertEqual(self.calculator.memory, 0)

if __name__ == '__main__':
    unittest.main()