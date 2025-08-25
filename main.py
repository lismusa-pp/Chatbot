from enhanced_chatbot import run_enhanced
from mlp_chatbot import run_mlp
from transformer_chatbot import run_transformer

def main():
    print("Choose a chatbot to run:")
    print("1 - Enhanced Rule-Based")
    print("2 - NLTK Pattern Chatbot")
    print("3 - Transformer Chatbot")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        run_enhanced()
    elif choice == "2":
        run_mlp()
    elif choice == "3":
        run_transformer()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
