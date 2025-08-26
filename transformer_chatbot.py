from transformers import pipeline, Conversation

# Load conversational AI (BlenderBot)
chatbot = pipeline("conversational", model="facebook/blenderbot_small-90M")

# Keep track of conversation history
conversation = Conversation()

def get_bot_response(user_input: str) -> str:
    global conversation
    try:
        # Add new message to the conversation
        conversation.add_user_input(user_input)

        # Generate a response
        response = chatbot(conversation)

        # Get the latest AI reply
        reply = response.generated_responses[-1].strip()

        # Fallback if reply is empty
        if not reply:
            reply = "Hmm, I’m not sure about that. Can you ask differently?"

        return reply

    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}"
