import os
import json
import time
import random
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")

# Ensure the API key is set
if not api_key:
    print("Error: API key not found. Make sure it's set in the .env file.")
    exit()

# Configure Gemini API
genai.configure(api_key=api_key)

# Select a Gemini model
model_name = "gemini-1.5-pro-latest"

# Initialize the model
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    print(f"Error initializing Gemini model: {str(e)}")
    exit()

# Chat history files
CHAT_HISTORY_FILE = "chat_history.json"
CHAT_MEMORY_FILE = "chat_memory.json"  # Stores previous responses to avoid redundant API calls

# Load previous chat history
def load_chat_data(file_path):
    """Load chat history or memory from a JSON file."""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {} if file_path == CHAT_MEMORY_FILE else []
    return {} if file_path == CHAT_MEMORY_FILE else []

# Save chat history
def save_chat_data(file_path, data):
    """Save chat history or memory to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Load existing data
chat_history = load_chat_data(CHAT_HISTORY_FILE)
chat_memory = load_chat_data(CHAT_MEMORY_FILE)  # Stores previous user questions and responses

def chatbot_response(user_input):
    """Generate a response while reducing API calls and handling API limits."""
    global chat_history, chat_memory

    # Check if this question was asked before
    if user_input in chat_memory:
        return chat_memory[user_input]  # Return stored response (saves API quota)

    # Add user input to chat history
    chat_history.append({"role": "user", "parts": [user_input]})

    # Limit chat history to last 20 messages
    if len(chat_history) > 20:
        chat_history.pop(0)

    # Exponential backoff parameters
    wait_time = 60  # Start with 1 min
    max_wait_time = 600  # Max 10 mins

    while True:
        try:
            # Generate response using chat history
            response = model.generate_content(chat_history)

            if response and hasattr(response, "text"):
                bot_reply = response.text.strip()
            else:
                bot_reply = "Sorry, I couldn't generate a response."

            # Add bot response to chat history
            chat_history.append({"role": "model", "parts": [bot_reply]})

            # Save updated chat history
            save_chat_data(CHAT_HISTORY_FILE, chat_history)

            # Store this response in memory to avoid redundant API calls
            chat_memory[user_input] = bot_reply
            save_chat_data(CHAT_MEMORY_FILE, chat_memory)

            return bot_reply

        except Exception as e:
            error_message = str(e)
            
            # If API quota is exhausted, apply exponential backoff
            if "Resource has been exhausted" in error_message:
                print(f"⚠️ API limit reached. Waiting {wait_time // 60} min before retrying...")
                time.sleep(wait_time)  # Wait before retrying
                wait_time = min(wait_time * 2, max_wait_time)  # Double the wait time (max 10 min)
            else:
                return f"Error: {error_message}"

def main():
    """Main chatbot loop."""
    print("Chatbot: Hello! Ask me anything about general knowledge or type 'bye' to exit.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "bye":
            print("Chatbot: Goodbye!")
            break

        response = chatbot_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
