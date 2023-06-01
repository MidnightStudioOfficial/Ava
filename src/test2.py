from core.chatbot.chatbot import ChatbotProfile

p = ChatbotProfile()
p.load_profile()
p.update_profile()
p.save_profile()
print(p.profile_data)
