import customtkinter as ctk
from datetime import datetime
from smart_engine import smart_reply

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ----- Chat logic -----
def chatbot_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm doing great! How about you?"
    elif "bye" in user_input:
        return "Goodbye! 👋"
    else:
        return "I didn't understand that. Try asking about time, date, or jokes."

# ----- GUI -----
root = ctk.CTk()
root.title("Lis Chatbot")
root.geometry("500x600")

# Header
header = ctk.CTkLabel(root, text="🤖 Lis' Chatbot", font=("Arial", 20, "bold"))
header.pack(pady=10)

# Chat window using CTkTextbox for scrollable messages
chat_window = ctk.CTkTextbox(root, width=480, height=450, corner_radius=10)
chat_window.pack(padx=10, pady=5, fill="both", expand=True)
chat_window.configure(state="disabled")  # Read-only

# Input frame
input_frame = ctk.CTkFrame(root)
input_frame.pack(fill="x", padx=10, pady=10)

user_entry = ctk.CTkEntry(input_frame, placeholder_text="Type your message...", width=380)
user_entry.pack(side="left", padx=(10,5), pady=5, fill="x", expand=True)

def add_message(sender, message):
    timestamp = datetime.now().strftime("%H:%M")
    chat_window.configure(state="normal")
    if sender == "user":
        chat_window.insert("end", f"You [{timestamp}]: {message}\n", "user")
    else:
        chat_window.insert("end", f"Bot 🤖 [{timestamp}]: {message}\n", "bot")
    chat_window.tag_config("user", foreground="#1ABC9C")
    chat_window.tag_config("bot", foreground="#F39C12")
    chat_window.see("end")  # <-- auto-scroll to bottom
    chat_window.configure(state="disabled")

def send_message():
    user_msg = user_entry.get().strip()
    if user_msg == "":
        return
    add_message("user", user_msg)
    user_entry.delete(0, "end")
    bot_msg = chatbot_response(user_msg)
    bot_msg = smart_reply(user_msg)
    add_message("bot", bot_msg)

send_button = ctk.CTkButton(input_frame, text="Send", width=80, command=send_message)
send_button.pack(side="right", padx=(5,10), pady=5)

# Bind Enter key
user_entry.bind("<Return>", lambda event: send_message())

root.mainloop()
