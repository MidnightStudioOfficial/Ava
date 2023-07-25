import unittest
from core.brain.brain import Brain


class TestBrain(unittest.TestCase):
    def setUp(self):
        self.brain = Brain()

    def test_attributes_and_methods(self):
        # Check if MyClass has the expected attributes and methods
        self.assertTrue(hasattr(self.brain, "__init__"))
        self.assertTrue(hasattr(self.brain, "update_mood"))

    def update_mood_test(self):
        self.brain.update_mood("I love you so much")

if __name__ == '__main__':
    unittest.main()
