import tkinter as tk
from tkinter import scrolledtext
from enhanced_chatbot import rule_based_response  # Using rule-based first

def send_message():
    user_msg = user_entry.get()
    if user_msg.strip() == "":
        return
    chat_window.config(state='normal')
    chat_window.insert(tk.END, "You: " + user_msg + "\n")
    
    # Get bot response
    if user_msg.lower() == "bye":
        bot_msg = "Goodbye!"
    else:
        bot_msg = rule_based_response(user_msg)
    
    chat_window.insert(tk.END, "Bot 🤖: " + bot_msg + "\n\n")
    chat_window.config(state='disabled')
    user_entry.delete(0, tk.END)
    chat_window.yview(tk.END)

# GUI window
root = tk.Tk()
root.title("Lis' Chatbot")
root.geometry("500x500")

chat_window = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_entry = tk.Entry(root)
user_entry.pack(padx=10, pady=5, fill=tk.X)
user_entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=5)

root.mainloop()
