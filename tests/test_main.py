# tests/test_main.py
import unittest
from src.utils.helper import greet

class TestModule(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Alice"), "Hello, Alice!")

if __name__ == '__main__':
    unittest.main()

