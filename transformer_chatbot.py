from transformers import pipeline

chatbot = pipeline("text-generation", model="gpt2")

print("Chatbot 🤖: Hello! Type 'bye' to exit.")
while True:
    user = input("You: ")
    if user.lower() == "bye":
        print("Chatbot 🤖: Goodbye!")
        break

    response = chatbot(user, max_length=50, num_return_sequences=1)[0]['generated_text']
    print("Chatbot 🤖:", response)
