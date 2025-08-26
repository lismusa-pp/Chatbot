import datetime
import random
import re
from math_solver import solve_math
from transformer_chatbot import get_bot_response

def rule_based_response(user_input: str):
    user_input_lower = user_input.lower()

    if "hello" in user_input_lower or "hi" in user_input_lower:
        return "Hello! How can I help you today?"

    elif "how are you" in user_input_lower:
        return "I'm just a bot, but I'm doing great! How about you?"

    elif "your name" in user_input_lower:
        return "I'm a chatbot assistant created by Lis Musa 🙂"

    elif "time" in user_input_lower:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {now}"

    elif "date" in user_input_lower:
        today = datetime.date.today().strftime("%B %d, %Y")
        return f"Today is {today}"

    elif "joke" in user_input_lower:
        jokes = [
            "Why don’t skeletons fight each other? They don’t have the guts!",
            "Why did the computer go to the doctor? Because it caught a virus.",
            "Why do cows wear bells? Because their horns don’t work!"
        ]
        return random.choice(jokes)

    elif "bye" in user_input_lower:
        return "Goodbye!"

    return None  # No match found


def get_response(user_input: str):
    # 1. Try math solver
    math_answer = solve_math(user_input)
    if math_answer:
        return math_answer

    # 2. Try rule-based responses
    rule_answer = rule_based_response(user_input)
    if rule_answer:
        return rule_answer

    # 3. Fallback: Transformer AI
    return get_bot_response(user_input)
