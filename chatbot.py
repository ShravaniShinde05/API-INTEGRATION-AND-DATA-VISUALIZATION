import nltk
from nltk.chat.util import Chat, reflections

# Define chatbot responses
chat_rules = [
    (r'hi|hello|hey|ok', ['Hello!', 'Hi there!', 'Hey! How can I help you?']),
    (r'(.*)(your name|who are you)', ["I'm ChatBot, your AI assistant."]),
    (r'how are you(.*)', ["I'm doing great, thanks for asking!"]),
    (r'who (created|developed|built) you(.*)', ["I was built during the CodTech internship using Python NLP."]),
    (r'(.*)(your purpose|what can you do|how can you help)', ["I'm here to assist you with basic queries like greetings, identity, and purpose."]),
    (r'(bye|exit|quit)', ['Goodbye! Have a great day.']),
    (r'(.*)', ["Sorry, I didn't catch that. Could you rephrase?"])  # fallback
]

# Build chatbot
def start_chatbot():
    print("🤖 CodTech NLP Chatbot (type 'bye' to exit)\n")
    chatbot = Chat(chat_rules, reflections)
    chatbot.converse()

# Entry point
if __name__ == "__main__":
    nltk.download('punkt')  # Only required the first time
    start_chatbot()
