from transformers import pipeline

class ChatAgent:
    def __init__(self):
        self.chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

    def get_response(self, user_input):
        conversation = self.chatbot(user_input)
        return conversation.generated_responses[-1]

# Example usage
if __name__ == "__main__":
    agent = ChatAgent()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.get_response(user_input)
        print(f"ChatAgent: {response}")
