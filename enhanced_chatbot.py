from logic import rule_based_response

def run_enhanced():
    print("Enhanced Chatbot 🤖: Hi! Type 'bye' to exit.")
    while True:
        user = input("You: ")
        if user.lower() == "bye":
            print("Enhanced Chatbot 🤖: Goodbye!")
            break
        print("Enhanced Chatbot 🤖:", rule_based_response(user))