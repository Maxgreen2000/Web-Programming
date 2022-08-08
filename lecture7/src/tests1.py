# Import the unittest library and our function
import unittest
from prime import is_prime

# A class containing all of out tests
class Tests(unittest.TestCase):

    def test_1(self):
        self.assertFalse(is_prime(1))

    def test_2(self):
        self.assertTrue(is_prime(2))

    def test_3(self):
        self.assertFalse(is_prime(8))

    def test_4(self):
        self.assertTrue(is_prime(11))

    def test_5(self):
        self.assertFalse(is_prime(25))

    def test_6(self):
        self.assertFalse(is_prime(28))

# Run each of the testing functions
if __name__ == "__main__":
    unittest.main()