from core.chatbot.chatbot import Chatbot

c = Chatbot()

user = input("ENTER:")
print(c.get_response(user))
print(c.get_response("play music"))
print(c.get_response("play some music"))