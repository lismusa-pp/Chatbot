import datetime
import random

def rule_based_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"

    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"

    elif "your name" in user_input:
        return "I'm a chatbot assistant created by Lis Musa 🙂"

    elif "time" in user_input:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {now}"

    elif "date" in user_input:
        today = datetime.date.today().strftime("%B %d, %Y")
        return f"Today is {today}"

    elif "joke" in user_input:
        jokes = [
            "Why don’t skeletons fight each other? They don’t have the guts!",
            "Why did the computer go to the doctor? Because it caught a virus.",
            "Why do cows wear bells? Because their horns don’t work!"
        ]
        return random.choice(jokes)

    elif "calculate" in user_input:
        try:
            expression = user_input.replace("calculate", "").strip()
            result = eval(expression)  # ⚠️ only safe for practice projects
            return f"The result is {result}"
        except:
            return "Sorry, I couldn't calculate that. Try something like 'calculate 5+3'."

    elif "bye" in user_input:
        return "Goodbye!"

    else:
        return "I'm not sure how to respond to that yet. Try asking about time, date, jokes, or math."
