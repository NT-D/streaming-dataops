import unittest
from app import add

class AppTest(unittest.TestCase):
    def test_add(self):
        """add returns added value"""
        self.assertEqual(add(1,2), 3)

if __name__ == "__main__":
    unittest.main()