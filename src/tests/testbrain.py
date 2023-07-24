import unittest
from core.brain.brain import Brain

class TestChatbot(unittest.TestCase):
    def setUp(self):
        self.brain = Brain()

    def update_mood_test(self):
        self.brain.update_mood("I love you so much")

if __name__ == '__main__':
    unittest.main()
