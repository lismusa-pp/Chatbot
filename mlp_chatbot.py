import nltk
from nltk.chat.util import Chat, reflections

# Download resources once
nltk.download('punkt')

# Pairs of patterns and responses
pairs = [
    (r"hi|hello|hey", ["Hello!", "Hi there!", "Hey!"]),
    (r"how are you ?", ["I'm doing great, thanks!", "I'm fine, how about you?"]),
    (r"what is your name ?", ["I'm Lis' chatbot.", "You can call me ChatBuddy."]),
    (r"quit", ["Goodbye!", "See you later!"]),
]

# reflections adds "I -> you", "my -> your" etc.
chatbot = Chat(pairs, reflections)

print("Chatbot 🤖: Hi, I'm ready to chat. Type 'quit' to exit.")
chatbot.converse()

