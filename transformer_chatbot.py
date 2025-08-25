from transformers import pipeline

chatbot = pipeline("text-generation", model="gpt2")

def run_transformer():
    print("Transformer Chatbot 🤖: Hello! Type 'bye' to exit.")
    while True:
        user = input("You: ")
        if user.lower() == "bye":
            print("Transformer Chatbot 🤖: Goodbye!")
            break
        response = chatbot(user, max_length=50, num_return_sequences=1)[0]['generated_text']
        print("Transformer Chatbot 🤖:", response)
