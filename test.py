from chatbot.chatbot import ChatBot

bot = ChatBot(keys_file="api_keys.json")
bot.add_dynamic_function("""
def eh(self, x, y):
    return x + y
""", "eh")

result = bot.eh(bot, 1, 2)
print(result)