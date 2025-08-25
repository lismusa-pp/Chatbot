def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"

    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"

    elif "bye" in user_input:
        return "Goodbye! Have a great day!"

    elif "your name" in user_input:
        return "I'm a simple chatbot created by Lis Musa 🙂"

    else:
        return "I'm not sure how to respond to that yet. Can you rephrase?"

# Run chatbot loop
print("Chatbot 🤖: Hi! Type 'bye' to exit.")
while True:
    user = input("You: ")
    if user.lower() == "bye":
        print("Chatbot 🤖: Goodbye!")
        break
    print("Chatbot 🤖:", chatbot_response(user))
