import unittest
from core.chatbot.chatbot import Chatbot

class TestChatbot(unittest.TestCase):
    def setUp(self):
        self.chatbot = Chatbot()

    def test_train_bot(self):
        self.chatbot.train_bot()
        self.assertTrue(self.chatbot.chatbot_exists)

    def test_get_skill(self):
        result = self.chatbot.get_skill("(NOT_FOUND)")
        self.assertFalse(result)
        
        result = self.chatbot.get_skill("Hello")
        self.assertTrue(result)

    def test_get_response(self):
        response = self.chatbot.get_response("Hello")
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()
