import nltk
from nltk.chat.util import Chat, reflections

nltk.download('punkt', quiet=True)

pairs = [
    (r"hi|hello|hey", ["Hello!", "Hi there!", "Hey!"]),
    (r"how are you ?", ["I'm doing great, thanks!", "I'm fine, how about you?"]),
    (r"what is your name ?", ["I'm Lis' chatbot.", "You can call me ChatBuddy."]),
    (r"quit", ["Goodbye!", "See you later!"]),
]

chatbot = Chat(pairs, reflections)

def run_mlp():
    print("MLP Chatbot 🤖: Hi, I'm ready to chat. Type 'quit' to exit.")
    chatbot.converse()
