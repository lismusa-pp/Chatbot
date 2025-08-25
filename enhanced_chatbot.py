import datetime
import random

def chatbot_response(user_input):
    user_input = user_input.lower()

    # Greetings
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"

    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"

    elif "your name" in user_input:
        return "I'm a chatbot assistant created by Lis Musa 🙂"

    # Time and Date
    elif "time" in user_input:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {now}"

    elif "date" in user_input:
        today = datetime.date.today().strftime("%B %d, %Y")
        return f"Today is {today}"

    # Jokes
    elif "joke" in user_input:
        jokes = [
            "Why don’t skeletons fight each other? They don’t have the guts!",
            "Why did the computer go to the doctor? Because it caught a virus.",
            "Why do cows wear bells? Because their horns don’t work!"
        ]
        return random.choice(jokes)

    # Math (basic calculator)
    elif "calculate" in user_input:
        try:
            expression = user_input.replace("calculate", "").strip()
            result = eval(expression)  # ⚠️ be careful, only safe in small personal projects
            return f"The result is {result}"
        except:
            return "Sorry, I couldn't calculate that. Try something like 'calculate 5+3'."

    # Weather (placeholder)
    elif "weather" in user_input:
        return "I can’t fetch live weather yet, but I could if you connect me to an API!"

    # Exit
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"

    else:
        return "I'm not sure how to respond to that yet. Try asking about time, date, jokes, or math."

# Run chatbot loop
print("Chatbot 🤖: Hi! Type 'bye' to exit.")
while True:
    user = input("You: ")
    if user.lower() == "bye":
        print("Chatbot 🤖: Goodbye!")
        break
    print("Chatbot 🤖:", chatbot_response(user))


