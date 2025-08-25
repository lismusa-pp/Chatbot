import customtkinter as ctk
from datetime import datetime

# ----- Logic -----
def chatbot_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "your name" in user_input:
        return "I'm Lis' chatbot 🤖"
    elif "time" in user_input:
        now = datetime.now().strftime("%H:%M")
        return f"The current time is {now}"
    elif "date" in user_input:
        today = datetime.now().strftime("%B %d, %Y")
        return f"Today is {today}"
    elif "joke" in user_input:
        jokes = [
            "Why don’t skeletons fight each other? They don’t have the guts!",
            "Why did the computer go to the doctor? Because it caught a virus.",
            "Why do cows wear bells? Because their horns don’t work!"
        ]
        import random
        return random.choice(jokes)
    elif "calculate" in user_input:
        try:
            expression = user_input.replace("calculate", "").strip()
            result = eval(expression)
            return f"The result is {result}"
        except:
            return "Sorry, I couldn't calculate that. Try something like 'calculate 5+3'."
    elif "bye" in user_input:
        return "Goodbye! 👋"
    else:
        return "I'm not sure how to respond to that yet. Try asking about time, date, jokes, or math."

# ----- GUI -----
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Main window
root = ctk.CTk()
root.title("Lis Chatbot")
root.geometry("500x600")

# Header
header = ctk.CTkLabel(root, text="🤖 Lis' Chatbot", font=("Arial", 20, "bold"))
header.pack(pady=10)

# Chat frame
chat_frame = ctk.CTkScrollableFrame(root, width=480, height=450)
chat_frame.pack(padx=10, pady=5, fill="both", expand=True)

# Entry frame
input_frame = ctk.CTkFrame(root)
input_frame.pack(fill="x", padx=10, pady=10)

user_entry = ctk.CTkEntry(input_frame, placeholder_text="Type your message...", width=380)
user_entry.pack(side="left", padx=(10,5), pady=5, fill="x", expand=True)

def add_message(sender, message):
    timestamp = datetime.now().strftime("%H:%M")
    if sender == "user":
        msg_label = ctk.CTkLabel(chat_frame, text=f"You [{timestamp}]: {message}", fg_color="#1ABC9C", text_color="white", corner_radius=10, anchor="e", justify="right", wraplength=400)
        msg_label.pack(anchor="e", padx=10, pady=5)
    else:
        msg_label = ctk.CTkLabel(chat_frame, text=f"Bot 🤖 [{timestamp}]: {message}", fg_color="#F39C12", text_color="white", corner_radius=10, anchor="w", justify="left", wraplength=400)
        msg_label.pack(anchor="w", padx=10, pady=5)
    chat_frame.update_idletasks()
    chat_frame.yview_moveto(1.0)

def send_message():
    user_msg = user_entry.get().strip()
    if user_msg == "":
        return
    add_message("user", user_msg)
    user_entry.delete(0, "end")
    
    bot_msg = chatbot_response(user_msg)
    add_message("bot", bot_msg)

send_button = ctk.CTkButton(input_frame, text="Send", width=80, command=send_message)
send_button.pack(side="right", padx=(5,10), pady=5)

# Bind Enter key
def enter_pressed(event):
    send_message()

user_entry.bind("<Return>", enter_pressed)

root.mainloop()
